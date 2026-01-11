"""
Módulo de Banco de Dados - Persistência com SQLite

Gerencia o armazenamento persistente do histórico dos alunos,
disciplinas cursadas, notas e status de matrícula.
"""
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from datetime import datetime


DATABASE_PATH = Path(__file__).parent.parent / "uniadvisor.db"


@contextmanager
def get_connection():
    """Context manager para conexão com o banco"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def inicializar_banco():
    """Cria as tabelas do banco de dados se não existirem"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Tabela de Alunos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                ano_atual INTEGER NOT NULL DEFAULT 1,
                tipo TEXT NOT NULL DEFAULT 'novo',
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de Histórico de Disciplinas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id TEXT NOT NULL,
                disciplina_id TEXT NOT NULL,
                status TEXT NOT NULL,
                nota REAL,
                ano_cursado INTEGER,
                semestre INTEGER,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (aluno_id) REFERENCES alunos(id),
                UNIQUE(aluno_id, disciplina_id, ano_cursado)
            )
        """)
        
        # Tabela de Matrículas Ativas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id TEXT NOT NULL,
                disciplina_id TEXT NOT NULL,
                ano_letivo INTEGER NOT NULL,
                data_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'ativa',
                FOREIGN KEY (aluno_id) REFERENCES alunos(id),
                UNIQUE(aluno_id, disciplina_id, ano_letivo)
            )
        """)
        
        # Tabela de Log de Inferências (para auditoria)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_inferencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id TEXT NOT NULL,
                regras_disparadas TEXT,
                resultado TEXT,
                data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (aluno_id) REFERENCES alunos(id)
            )
        """)
        
        print("✅ Banco de dados inicializado com sucesso!")


class AlunoRepository:
    """Repositório para operações com alunos"""
    
    @staticmethod
    def criar_ou_atualizar(aluno_id: str, nome: str, ano: int, tipo: str = 'veterano') -> Dict:
        """Cria ou atualiza um aluno no banco"""
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO alunos (id, nome, ano_atual, tipo, data_atualizacao)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    nome = excluded.nome,
                    ano_atual = excluded.ano_atual,
                    tipo = excluded.tipo,
                    data_atualizacao = excluded.data_atualizacao
            """, (aluno_id, nome, ano, tipo, datetime.now()))
            
            return AlunoRepository.buscar_por_id(aluno_id)
    
    @staticmethod
    def buscar_por_id(aluno_id: str) -> Optional[Dict]:
        """Busca um aluno pelo ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def listar_todos() -> List[Dict]:
        """Lista todos os alunos"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alunos ORDER BY nome")
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def deletar(aluno_id: str) -> bool:
        """Remove um aluno e seu histórico"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historico_disciplinas WHERE aluno_id = ?", (aluno_id,))
            cursor.execute("DELETE FROM matriculas WHERE aluno_id = ?", (aluno_id,))
            cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
            return cursor.rowcount > 0


class HistoricoRepository:
    """Repositório para operações com histórico de disciplinas"""
    
    @staticmethod
    def registrar_disciplina(aluno_id: str, disciplina_id: str, status: str, 
                            nota: float = None, ano_cursado: int = None) -> Dict:
        """Registra uma disciplina no histórico do aluno"""
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO historico_disciplinas (aluno_id, disciplina_id, status, nota, ano_cursado)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(aluno_id, disciplina_id, ano_cursado) DO UPDATE SET
                    status = excluded.status,
                    nota = excluded.nota,
                    data_registro = CURRENT_TIMESTAMP
            """, (aluno_id, disciplina_id, status, nota, ano_cursado or datetime.now().year))
            
            return {
                "aluno_id": aluno_id,
                "disciplina_id": disciplina_id,
                "status": status,
                "nota": nota
            }
    
    @staticmethod
    def registrar_multiplas(aluno_id: str, disciplinas: List[Dict]) -> int:
        """Registra múltiplas disciplinas de uma vez"""
        count = 0
        for disc in disciplinas:
            HistoricoRepository.registrar_disciplina(
                aluno_id=aluno_id,
                disciplina_id=disc['id'],
                status=disc.get('status', 'aprovado'),
                nota=disc.get('nota'),
                ano_cursado=disc.get('ano_cursado')
            )
            count += 1
        return count
    
    @staticmethod
    def buscar_historico_aluno(aluno_id: str) -> Dict[str, List]:
        """Retorna o histórico completo de um aluno organizado por status"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT disciplina_id, status, nota, ano_cursado
                FROM historico_disciplinas
                WHERE aluno_id = ?
                ORDER BY ano_cursado, disciplina_id
            """, (aluno_id,))
            
            historico = {
                "aprovadas": [],
                "reprovadas": [],
                "cursando": []
            }
            
            for row in cursor.fetchall():
                item = {
                    "id": row["disciplina_id"],
                    "nota": row["nota"],
                    "ano_cursado": row["ano_cursado"]
                }
                
                if row["status"] == "aprovado":
                    historico["aprovadas"].append(item)
                elif row["status"] == "reprovado":
                    historico["reprovadas"].append(item)
                elif row["status"] == "cursando":
                    historico["cursando"].append(item)
            
            return historico
    
    @staticmethod
    def obter_disciplinas_aprovadas(aluno_id: str) -> List[str]:
        """Retorna lista de IDs das disciplinas aprovadas"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT disciplina_id FROM historico_disciplinas
                WHERE aluno_id = ? AND status = 'aprovado'
            """, (aluno_id,))
            return [row["disciplina_id"] for row in cursor.fetchall()]
    
    @staticmethod
    def obter_notas(aluno_id: str) -> Dict[str, float]:
        """Retorna dicionário de notas por disciplina"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT disciplina_id, nota FROM historico_disciplinas
                WHERE aluno_id = ? AND nota IS NOT NULL
            """, (aluno_id,))
            return {row["disciplina_id"]: row["nota"] for row in cursor.fetchall()}
    
    @staticmethod
    def limpar_historico(aluno_id: str) -> int:
        """Remove todo o histórico de um aluno"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historico_disciplinas WHERE aluno_id = ?", (aluno_id,))
            return cursor.rowcount


class MatriculaRepository:
    """Repositório para operações com matrículas"""
    
    @staticmethod
    def registrar_matricula(aluno_id: str, disciplina_id: str, ano_letivo: int = None) -> Dict:
        """Registra uma matrícula ativa"""
        ano = ano_letivo or datetime.now().year
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO matriculas (aluno_id, disciplina_id, ano_letivo)
                VALUES (?, ?, ?)
                ON CONFLICT(aluno_id, disciplina_id, ano_letivo) DO UPDATE SET
                    status = 'ativa',
                    data_matricula = CURRENT_TIMESTAMP
            """, (aluno_id, disciplina_id, ano))
            
            return {
                "aluno_id": aluno_id,
                "disciplina_id": disciplina_id,
                "ano_letivo": ano
            }
    
    @staticmethod
    def registrar_multiplas(aluno_id: str, disciplinas: List[str], ano_letivo: int = None) -> int:
        """Registra múltiplas matrículas"""
        count = 0
        for disc_id in disciplinas:
            MatriculaRepository.registrar_matricula(aluno_id, disc_id, ano_letivo)
            count += 1
        return count
    
    @staticmethod
    def obter_matriculas_ativas(aluno_id: str) -> List[str]:
        """Retorna disciplinas com matrícula ativa"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT disciplina_id FROM matriculas
                WHERE aluno_id = ? AND status = 'ativa'
            """, (aluno_id,))
            return [row["disciplina_id"] for row in cursor.fetchall()]


class LogRepository:
    """Repositório para log de inferências"""
    
    @staticmethod
    def registrar_consulta(aluno_id: str, regras: List[str], resultado: Dict) -> int:
        """Registra uma consulta de inferência"""
        import json
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO log_inferencias (aluno_id, regras_disparadas, resultado)
                VALUES (?, ?, ?)
            """, (aluno_id, json.dumps(regras), json.dumps(resultado)))
            return cursor.lastrowid


# Inicializar banco ao importar o módulo
inicializar_banco()
