"""
Base de Fatos - Gerencia o estado atual do problema (CORRIGIDO)

A Base de Fatos representa o estado atual do aluno e é alimentada
dinamicamente a partir da interação com o usuário e do banco de dados.

CORREÇÕES REALIZADAS:
1. Integração com banco de dados SQLite
2. Mapeamento correto dos fatos para as regras
3. Método preparar_fatos_disciplina corrigido
4. Cálculo correto de pré-requisitos faltantes
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json
from pathlib import Path
import sys

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import HistoricoRepository, AlunoRepository


@dataclass
class BaseFatos:
    """
    Gerencia os fatos do sistema.
    Os fatos são atualizados dinamicamente durante a interação e inferência.
    """
    fatos: Dict[str, Any] = field(default_factory=dict)
    historico_inferencia: List[Dict] = field(default_factory=list)
    
    def adicionar_fato(self, chave: str, valor: Any) -> None:
        """Adiciona ou atualiza um fato"""
        self.fatos[chave] = valor
    
    def remover_fato(self, chave: str) -> None:
        """Remove um fato"""
        if chave in self.fatos:
            del self.fatos[chave]
    
    def get_fato(self, chave: str, default: Any = None) -> Any:
        """Obtém um fato pelo nome"""
        return self.fatos.get(chave, default)
    
    def tem_fato(self, chave: str) -> bool:
        """Verifica se um fato existe"""
        return chave in self.fatos
    
    def limpar(self) -> None:
        """Limpa todos os fatos"""
        self.fatos.clear()
        self.historico_inferencia.clear()
    
    def get_todos_fatos(self) -> Dict[str, Any]:
        """Retorna cópia de todos os fatos"""
        return self.fatos.copy()
    
    def registrar_inferencia(self, regra_id: str, resultado: Dict) -> None:
        """Registra uma inferência realizada para explicação"""
        self.historico_inferencia.append({
            "regra": regra_id,
            "fatos_utilizados": {k: v for k, v in self.fatos.items() 
                               if not k.startswith('_')},  # Excluir internos
            "resultado": resultado
        })
    
    def get_explicacao(self) -> List[Dict]:
        """Retorna o histórico de inferências para explicação"""
        return self.historico_inferencia


class GerenciadorFatosAluno:
    """
    Gerenciador especializado para fatos relacionados ao aluno.
    
    CORREÇÃO: Agora integra com o banco de dados e mapeia corretamente
    os fatos para as condições das regras.
    """
    
    def __init__(self, base_fatos: BaseFatos):
        self.base_fatos = base_fatos
        self._carregar_curriculo()
    
    def _carregar_curriculo(self) -> None:
        """Carrega o currículo do arquivo JSON"""
        caminho = Path(__file__).parent.parent / "knowledge_base" / "curriculum.json"
        with open(caminho, "r", encoding="utf-8") as f:
            self.curriculo = json.load(f)
        
        # Indexar por ID para acesso rápido
        self.disciplinas_por_id = {d["id"]: d for d in self.curriculo}
        
        # Indexar por ano
        self.disciplinas_por_ano = {}
        for d in self.curriculo:
            ano = d["ano"]
            if ano not in self.disciplinas_por_ano:
                self.disciplinas_por_ano[ano] = []
            self.disciplinas_por_ano[ano].append(d)
    
    def inicializar_aluno(self, aluno_id: str, nome: str, ano: int, novo: bool = False) -> None:
        """Inicializa os fatos básicos do aluno"""
        self.base_fatos.adicionar_fato("aluno_id", aluno_id)
        self.base_fatos.adicionar_fato("aluno_nome", nome)
        self.base_fatos.adicionar_fato("aluno_ano", ano)
        self.base_fatos.adicionar_fato("aluno_novo", novo)
        self.base_fatos.adicionar_fato("disciplinas_aprovadas", [])
        self.base_fatos.adicionar_fato("disciplinas_reprovadas", [])
        self.base_fatos.adicionar_fato("disciplinas_cursando", [])
        self.base_fatos.adicionar_fato("notas", {})
    
    def inicializar_aluno_do_banco(self, aluno_id: str) -> bool:
        """Carrega dados do aluno do banco de dados"""
        aluno = AlunoRepository.buscar_por_id(aluno_id)
        if not aluno:
            return False
        
        # Carregar dados básicos
        self.base_fatos.adicionar_fato("aluno_id", aluno["id"])
        self.base_fatos.adicionar_fato("aluno_nome", aluno["nome"])
        self.base_fatos.adicionar_fato("aluno_ano", aluno["ano_atual"])
        self.base_fatos.adicionar_fato("aluno_novo", aluno["tipo"] == "novo")
        
        # Carregar histórico do banco
        historico = HistoricoRepository.buscar_historico_aluno(aluno_id)
        
        aprovadas_ids = [d["id"] for d in historico["aprovadas"]]
        reprovadas_ids = [d["id"] for d in historico["reprovadas"]]
        
        self.base_fatos.adicionar_fato("disciplinas_aprovadas", aprovadas_ids)
        self.base_fatos.adicionar_fato("disciplinas_reprovadas", reprovadas_ids)
        self.base_fatos.adicionar_fato("disciplinas_cursando", 
                                       [d["id"] for d in historico["cursando"]])
        
        # Carregar notas
        notas = HistoricoRepository.obter_notas(aluno_id)
        self.base_fatos.adicionar_fato("notas", notas)
        
        return True
    
    def registrar_aprovacao(self, disciplina_id: str, nota: float) -> None:
        """Registra aprovação em uma disciplina"""
        aprovadas = self.base_fatos.get_fato("disciplinas_aprovadas", [])
        if disciplina_id not in aprovadas:
            aprovadas.append(disciplina_id)
        self.base_fatos.adicionar_fato("disciplinas_aprovadas", aprovadas)
        
        notas = self.base_fatos.get_fato("notas", {})
        notas[disciplina_id] = nota
        self.base_fatos.adicionar_fato("notas", notas)
    
    def registrar_reprovacao(self, disciplina_id: str, nota: float) -> None:
        """Registra reprovação em uma disciplina"""
        reprovadas = self.base_fatos.get_fato("disciplinas_reprovadas", [])
        if disciplina_id not in reprovadas:
            reprovadas.append(disciplina_id)
        self.base_fatos.adicionar_fato("disciplinas_reprovadas", reprovadas)
        
        notas = self.base_fatos.get_fato("notas", {})
        notas[disciplina_id] = nota
        self.base_fatos.adicionar_fato("notas", notas)

    def calcular_fatos_derivados(self) -> None:
        """
        Calcula fatos derivados para suportar as regras R1-R11
        
        CORREÇÃO: Cálculo corrigido de todos os fatos necessários
        """
        ano_atual = self.base_fatos.get_fato("aluno_ano", 1)
        aprovadas = self.base_fatos.get_fato("disciplinas_aprovadas", [])
        reprovadas = self.base_fatos.get_fato("disciplinas_reprovadas", [])
        notas = self.base_fatos.get_fato("notas", {})

        # --- R5: Contagem de reprovações no ano atual ---
        reprovacoes_ano = sum(
            1 for d_id in reprovadas
            if self.disciplinas_por_id.get(d_id, {}).get("ano") == ano_atual
        )
        self.base_fatos.adicionar_fato("reprovacoes_ano", reprovacoes_ano)
        self.base_fatos.adicionar_fato("critico_reprovacoes", reprovacoes_ano > 3)

        # --- R2: Verificar se passou em todas do ano atual ---
        disciplinas_ano = self.disciplinas_por_ano.get(ano_atual, [])
        ids_ano = [d["id"] for d in disciplinas_ano]
        passou_todas = all(d_id in aprovadas for d_id in ids_ano) if ids_ano else False
        self.base_fatos.adicionar_fato("passou_todas_ano_atual", passou_todas)
        
        # --- Estatísticas do ano atual ---
        total_ano = len(ids_ano)
        aprovadas_ano = sum(1 for d_id in ids_ano if d_id in aprovadas)
        self.base_fatos.adicionar_fato("total_disciplinas_ano", total_ano)
        self.base_fatos.adicionar_fato("aprovadas_no_ano", aprovadas_ano)
        
        # --- R8: Médias por área ---
        medias_area = self._calcular_medias_por_area(aprovadas, notas)
        self.base_fatos.adicionar_fato("medias_por_area", medias_area)

        # Criar fatos de área forte (média >= 8.0)
        for area, media in medias_area.items():
            if media >= 8.0:
                self.base_fatos.adicionar_fato(f"area_forte_{area}", True)

        # --- R9: Lista de dependências ---
        # Dependências são disciplinas de anos anteriores não aprovadas
        lista_dep = []
        for ano in range(1, ano_atual):
            for d in self.disciplinas_por_ano.get(ano, []):
                if d["id"] not in aprovadas:
                    lista_dep.append(d["id"])

        self.base_fatos.adicionar_fato("lista_dependencias", lista_dep)
        self.base_fatos.adicionar_fato("tem_dependencia", len(lista_dep) > 0)
        self.base_fatos.adicionar_fato("quantidade_dependencias", len(lista_dep))

    def _calcular_medias_por_area(self, aprovadas: List[str], notas: Dict[str, float]) -> Dict[str, float]:
        """Calcula a média de notas por área de conhecimento"""
        areas_soma = {}
        areas_cont = {}
        
        for d_id in aprovadas:
            if d_id in notas and d_id in self.disciplinas_por_id:
                area = self.disciplinas_por_id[d_id].get("area", "Outros")
                areas_soma[area] = areas_soma.get(area, 0) + notas[d_id]
                areas_cont[area] = areas_cont.get(area, 0) + 1
        
        return {
            area: round(areas_soma[area] / areas_cont[area], 2) 
            for area in areas_soma
        }

    def preparar_fatos_disciplina(self, disciplina_id: str) -> Dict[str, Any]:
        """
        Prepara o contexto para o Motor avaliar uma disciplina específica.
        
        CORREÇÃO: Agora retorna TODOS os fatos necessários para as regras R4-R11
        """
        disciplina = self.disciplinas_por_id.get(disciplina_id, {})
        aprovadas = self.base_fatos.get_fato("disciplinas_aprovadas", [])
        ano_aluno = self.base_fatos.get_fato("aluno_ano", 1)
        lista_dep = self.base_fatos.get_fato("lista_dependencias", [])

        pre_requisitos = disciplina.get("pre_requisitos", [])
        
        # Calcular pré-requisitos faltantes
        pre_requisitos_faltantes = [pr for pr in pre_requisitos if pr not in aprovadas]
        prereqs_cumpridos = len(pre_requisitos_faltantes) == 0

        # Verificar se a área é forte
        area = disciplina.get("area", "Outros")
        area_forte = self.base_fatos.tem_fato(f"area_forte_{area}")

        return {
            # Identificação
            "id": disciplina_id,
            "nome": disciplina.get("nome", ""),
            "area": area,
            "carga_horaria": disciplina.get("carga_horaria", 60),
            
            # Contexto de ano
            "ano_disciplina": disciplina.get("ano", 1),
            "aluno_ano": ano_aluno,
            "mesmo_ano_aluno": disciplina.get("ano") == ano_aluno,
            
            # Pré-requisitos (CORRIGIDO)
            "tem_pre_requisito": len(pre_requisitos) > 0,
            "pre_requisitos": pre_requisitos,
            "pre_requisitos_cumpridos": prereqs_cumpridos,
            "pre_requisitos_faltantes": pre_requisitos_faltantes,
            
            # Status
            "ja_aprovada": disciplina_id in aprovadas,
            "eh_dependencia": disciplina_id in lista_dep,
            
            # Heurísticas
            "area_forte": area_forte
        }

    def get_curriculo(self) -> List[Dict]:
        """Retorna o currículo completo"""
        return self.curriculo
    
    def get_disciplina(self, disciplina_id: str) -> Optional[Dict]:
        """Retorna dados de uma disciplina específica"""
        return self.disciplinas_por_id.get(disciplina_id)
    
    def get_disciplinas_ano(self, ano: int) -> List[Dict]:
        """Retorna disciplinas de um ano específico"""
        return self.disciplinas_por_ano.get(ano, [])
    
    def get_estatisticas_aluno(self) -> Dict[str, Any]:
        """Retorna estatísticas do progresso do aluno"""
        aprovadas = self.base_fatos.get_fato("disciplinas_aprovadas", [])
        reprovadas = self.base_fatos.get_fato("disciplinas_reprovadas", [])
        notas = self.base_fatos.get_fato("notas", {})
        
        total_curriculo = len(self.curriculo)
        total_aprovadas = len(aprovadas)
        
        # Calcular média geral
        if notas:
            media_geral = sum(notas.values()) / len(notas)
        else:
            media_geral = 0
        
        # Calcular carga horária cursada
        ch_aprovada = sum(
            self.disciplinas_por_id.get(d_id, {}).get("carga_horaria", 0)
            for d_id in aprovadas
        )
        
        ch_total = sum(d.get("carga_horaria", 0) for d in self.curriculo)
        
        return {
            "total_disciplinas": total_curriculo,
            "aprovadas": total_aprovadas,
            "reprovadas": len(reprovadas),
            "pendentes": total_curriculo - total_aprovadas,
            "percentual_conclusao": round((total_aprovadas / total_curriculo) * 100, 1),
            "media_geral": round(media_geral, 2),
            "carga_horaria_aprovada": ch_aprovada,
            "carga_horaria_total": ch_total,
            "percentual_ch": round((ch_aprovada / ch_total) * 100, 1) if ch_total > 0 else 0
        }
