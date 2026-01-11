"""
Script Simplificado para Criar Banco de Dados
"""
import sqlite3
from pathlib import Path

print("=" * 80)
print("CRIANDO BANCO DE DADOS")
print("=" * 80)
print()

# Caminho do banco
db_path = Path(__file__).parent / "uniadvisor.db"
print(f"Caminho: {db_path}")

# Deletar se existir
if db_path.exists():
    print("⚠️ Banco existente encontrado, deletando...")
    db_path.unlink()

# Criar banco
print("Criando novo banco...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabela alunos
cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    ano_atual INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✓ Tabela 'alunos' criada")

# Tabela historico_disciplinas
cursor.execute('''
CREATE TABLE IF NOT EXISTS historico_disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id TEXT NOT NULL,
    disciplina_id TEXT NOT NULL,
    status TEXT NOT NULL,
    nota REAL,
    ano_cursado INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
)
''')
print("✓ Tabela 'historico_disciplinas' criada")

# Tabela matriculas
cursor.execute('''
CREATE TABLE IF NOT EXISTS matriculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id TEXT NOT NULL,
    disciplina_id TEXT NOT NULL,
    ano_letivo INTEGER NOT NULL,
    status TEXT DEFAULT 'cursando',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
)
''')
print("✓ Tabela 'matriculas' criada")

# Tabela log_inferencias
cursor.execute('''
CREATE TABLE IF NOT EXISTS log_inferencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id TEXT NOT NULL,
    regras_disparadas TEXT,
    resultado TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
)
''')
print("✓ Tabela 'log_inferencias' criada")

conn.commit()
conn.close()

# Verificar
if db_path.exists():
    size = db_path.stat().st_size
    print()
    print("=" * 80)
    print("✅ BANCO CRIADO COM SUCESSO!")
    print("=" * 80)
    print(f"Local: {db_path}")
    print(f"Tamanho: {size} bytes")
    print()
    print("Próximo passo:")
    print("  python popular_usuarios_teste.py")
else:
    print()
    print("✗ ERRO: Banco não foi criado!")