# 🎓 UniAdvisor - Sistema Especialista para Recomendação de Matrícula

Sistema Baseado em Conhecimento desenvolvido para automatizar e otimizar o processo de recomendação de matrícula acadêmica no IFAM (Instituto Federal do Amazonas).

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
  - [Opção 1: Execução Local](#opção-1-execução-local-windowslinuxmac)
  - [Opção 2: Execução com Docker](#opção-2-execução-com-docker)
- [Uso do Sistema](#uso-do-sistema)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Testes](#testes)
- [Troubleshooting](#troubleshooting)
- [Contribuindo](#contribuindo)
- [Licença](#licença)
- [Autores](#autores)

---

## 🎯 Sobre o Projeto

O **UniAdvisor** é um sistema especialista que utiliza técnicas de Inteligência Artificial Simbólica para auxiliar alunos do IFAM na escolha de disciplinas para matrícula. O sistema analisa o histórico acadêmico do aluno e, através de um motor de inferência baseado em regras SWRL (Semantic Web Rule Language), recomenda as melhores disciplinas a serem cursadas.

### Características Principais:

- 🧠 **Motor de Inferência Forward Chaining**
- 📊 **Base de Conhecimento com 45 disciplinas**
- 🎯 **11 Regras de Inferência** (matrícula, bloqueio, elegibilidade, heurísticas)
- 💾 **Persistência em SQLite**
- 🌐 **Interface Web Responsiva**
- 🐳 **Containerização com Docker**
- 📝 **Logs de Auditoria**

---

## ✨ Funcionalidades

### Para Alunos:
- ✅ Consulta de disciplinas disponíveis para matrícula
- ✅ Verificação automática de pré-requisitos
- ✅ Recomendação inteligente baseada no histórico
- ✅ Identificação de disciplinas bloqueadas
- ✅ Priorização com base em heurísticas (área forte, desbloqueio)
- ✅ Busca rápida de histórico salvo

### Para Coordenadores:
- ✅ Visão geral de alunos cadastrados
- ✅ Logs de inferências realizadas
- ✅ API REST para integração

---

## 🛠️ Tecnologias

### Backend
- **Python 3.11+** - Linguagem principal
- **Flask 3.0.0** - Framework web
- **SQLite 3** - Banco de dados

### Frontend
- **HTML5 / CSS3** - Estrutura e estilo
- **JavaScript (Vanilla)** - Interatividade

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração

---

## 📦 Pré-requisitos

### Para Execução Local:

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

### Para Execução com Docker:

- Docker Desktop instalado
- Docker Compose (geralmente incluído no Docker Desktop)

---

## 🚀 Instalação e Execução

## Opção 1: Execução Local (Windows/Linux/Mac)

### 1️⃣ Clonar/Baixar o Projeto

```bash
# Se usar Git
git clone https://github.com/DanielNazarioPro/uniadvisor.git
cd uniadvisor

# OU extrair o ZIP baixado
cd uniadvisor_corrigido
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

**OU instalar manualmente:**
```bash
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
pip install python-dateutil==2.8.2
```

### 3️⃣ Criar o Banco de Dados

```bash
python criar_banco.py
```

**Saída esperada:**
```
================================================================================
CRIANDO BANCO DE DADOS
================================================================================
✓ Tabela 'alunos' criada
✓ Tabela 'historico_disciplinas' criada
✓ Tabela 'matriculas' criada
✓ Tabela 'log_inferencias' criada

✅ BANCO CRIADO COM SUCESSO!
Local: C:\...\uniadvisor.db
Tamanho: 16384 bytes
```

### 4️⃣ Popular com Dados de Teste

```bash
python main-test.py
```

**Saída esperada:**
```
✓ Total de alunos: 6
✓ Total de históricos: 114

• 2024001: Maria Silva Santos
  Ano: 2º | Aprovadas: 16 | Reprovadas: 0
• 2024002: João Pedro Oliveira
  Ano: 1º | Aprovadas: 13 | Reprovadas: 3
...
✅ BANCO POPULADO COM SUCESSO!
```

### 5️⃣ Iniciar o Servidor

```bash
python main.py
```

**Saída esperada:**
```
✅ Banco de dados inicializado com sucesso!
 * Serving Flask app 'interface.app'
 * Running on http://127.0.0.1:5000
```

### 6️⃣ Acessar a Aplicação

Abra seu navegador em:
```
http://localhost:5000
```

### 7️⃣ Testar o Sistema

1. Digite uma matrícula de teste: `2024001`
2. Pressione **Enter** (busca automática)
3. O sistema preenche nome, ano e histórico
4. Clique em **"Continuar"**
5. Clique em **"🔍 Gerar Recomendação"**
6. Veja as disciplinas sugeridas!

### 8️⃣ Parar o Servidor

No terminal onde o servidor está rodando:
```
Ctrl + C
```

---

## Opção 2: Execução com Docker

### 1️⃣ Clonar/Baixar o Projeto

```bash
cd uniadvisor_corrigido
```

### 2️⃣ Construir a Imagem Docker

```bash
docker-compose build
```

**Tempo estimado:** 2-3 minutos

### 3️⃣ Iniciar os Containers

```bash
# Iniciar em background (recomendado)
docker-compose up -d

# OU iniciar com logs visíveis
docker-compose up
```

### 4️⃣ Verificar Status

```bash
docker-compose ps
```

**Saída esperada:**
```
NAME                    STATUS              PORTS
uniadvisor_app          Up 10 seconds       0.0.0.0:5000->5000/tcp
```

### 5️⃣ Popular Banco de Dados

```bash
docker exec -it uniadvisor_app python main-test.py
```

### 6️⃣ Acessar a Aplicação

Abra seu navegador em:
```
http://localhost:5000
```

### 7️⃣ Ver Logs (Opcional)

```bash
# Logs em tempo real
docker-compose logs -f

# Últimas 50 linhas
docker-compose logs --tail=50

# Logs de um serviço específico
docker-compose logs uniadvisor_app
```

### 8️⃣ Parar os Containers

```bash
# Parar (mantém dados)
docker-compose stop

# Parar e remover (mantém dados no volume)
docker-compose down

# Parar e remover TUDO (⚠️ APAGA BANCO!)
docker-compose down -v
```

### 9️⃣ Reiniciar

```bash
docker-compose restart
```

### 🔟 Entrar no Container (Shell)

```bash
docker exec -it uniadvisor_app bash

# Dentro do container você pode:
ls                          # Listar arquivos
python main-test.py  # Rodar scripts
cat curriculum.json         # Ver arquivos
exit                        # Sair
```

---

## 📖 Uso do Sistema

### 👤 Usuários de Teste Pré-cadastrados

Após popular o banco, estes usuários estarão disponíveis:

| Matrícula | Nome | Ano | Perfil | Uso Recomendado |
|-----------|------|-----|--------|-----------------|
| **2024001** | Maria Silva Santos | 2º | ⭐ Excelente (16/16 aprovadas) | Demonstrar fluxo ideal |
| **2024002** | João Pedro Oliveira | 1º | ⚠️ 3 reprovações | Demonstrar bloqueios |
| **2023001** | Ana Carolina Mendes | 2º | 🎯 Veterana (POO+BD) | Demonstrar progressão |
| **2024003** | Carlos Eduardo Costa | 1º | 🔴 Crítico (6 reprov.) | Demonstrar alertas |
| **2024004** | Lucas Fernandes Lima | 1º | 🧮 Forte em Exatas | Demonstrar heurísticas |
| **2022001** | Beatriz Almeida Rocha | 3º | 🏆 Quase formada | Demonstrar final |

### 🎬 Fluxo de Uso

#### 1. **Tela Inicial - Identificação**
```
1. Digite a matrícula (ex: 2024001)
2. Pressione Enter (busca automática) OU preencha manualmente
3. Nome e ano são preenchidos automaticamente
4. Clique em "Continuar →"
```

#### 2. **Tela de Histórico** (apenas para veteranos)
```
1. Marque disciplinas como Aprovado/Reprovado
2. Preencha as notas
3. Clique em "🔍 Gerar Recomendação"
```

#### 3. **Tela de Resultado**
```
✅ Disciplinas Sugeridas (ordenadas por prioridade)
🔴 Disciplinas Bloqueadas (com motivo)
📊 Estatísticas do aluno
💡 Explicações das regras aplicadas
```

### 🔍 Busca Rápida

Para alunos já cadastrados:
1. Digite apenas a matrícula
2. Pressione **Enter**
3. Sistema busca e preenche **TUDO automaticamente**:
   - Nome
   - Ano
   - Histórico completo (aprovadas/reprovadas)
   - Notas

---

## 📁 Estrutura do Projeto

```
uniadvisor_corrigido/
│
├── database/                      # Camada de Dados
│   ├── __init__.py
│   └── db.py                      # Repositories (Aluno, Histórico, etc)
│
├── facts_base/                    # Base de Fatos
│   ├── __init__.py
│   └── student_facts.py           # BaseFatos e GerenciadorFatos
│
├── inference_engine/              # Motor de Inferência
│   ├── __init__.py
│   └── engine.py                  # Forward Chaining Engine
│
├── knowledge_base/                # Base de Conhecimento
│   ├── __init__.py
│   ├── curriculum.json            # 45 disciplinas do IFAM
│   └── rules.py                   # 11 Regras SWRL
│
├── interface/                     # Interface Web
│   ├── __init__.py
│   ├── app.py                     # Backend Flask (API REST)
│   ├── templates/
│   │   └── index.html             # Frontend HTML
│   └── static/
│       ├── css/
│       │   └── style.css          # Estilos
│       └── js/
│           └── app.js             # Lógica JavaScript
│
├── Dockerfile                     # Container do app
├── docker-compose.yml             # Orquestração
├── requirements.txt               # Dependências Python
├── main.py                        # Entry point
│
├── criarbanco.py                 # Script: Criar banco
├── main-test.py                  # Script: Popular dados de teste
│
├── README.md                      # Este arquivo
└── uniadvisor.db                  # Banco SQLite (gerado)
```

---

## 🔌 API Endpoints

### 📚 Currículo

```http
GET /api/curriculo
```

**Resposta:**
```json
{
  "curriculo": [...],
  "por_ano": {
    "1": [...],
    "2": [...],
    "3": [...]
  },
  "total_disciplinas": 45
}
```

### 👤 Buscar Aluno

```http
GET /api/aluno/<matricula>
```

**Exemplo:**
```bash
curl http://localhost:5000/api/aluno/2024001
```

**Resposta:**
```json
{
  "aluno": {
    "id": "2024001",
    "nome": "Maria Silva Santos",
    "ano_atual": 2,
    "tipo": "veterano"
  },
  "historico": {
    "aprovadas": [
      {"id": "PORT1", "nota": 9.5, "ano_cursado": 2024},
      {"id": "MAT1", "nota": 9.8, "ano_cursado": 2024}
    ],
    "reprovadas": []
  },
  "sucesso": true
}
```

### 📝 Listar Alunos

```http
GET /api/alunos
```

**Resposta:**
```json
{
  "alunos": [
    {"id": "2024001", "nome": "Maria Silva Santos", "ano_atual": 2},
    {"id": "2024002", "nome": "João Pedro Oliveira", "ano_atual": 1}
  ],
  "total": 2
}
```

### 🎯 Consultar Recomendação

```http
POST /api/consultar
Content-Type: application/json
```

**Body:**
```json
{
  "nome": "Teste",
  "matricula": "TEST001",
  "tipo": "veterano",
  "ano_atual": 2,
  "aprovadas": [
    {"id": "PORT1", "nota": 9.0},
    {"id": "MAT1", "nota": 8.5}
  ],
  "reprovadas": []
}
```

**Resposta:**
```json
{
  "status": "selecao_manual",
  "mensagem": "Selecione as disciplinas desejadas",
  "disciplinas_sugeridas": [
    {
      "id": "PORT2",
      "nome": "Português II",
      "prioridade": 95,
      "ranking": 1,
      "motivo": "Área forte e desbloqueia outras"
    }
  ],
  "disciplinas_bloqueadas": [
    {
      "id": "POO",
      "nome": "Programação Orientada a Objetos",
      "motivo": "Faltam pré-requisitos: LOGICA"
    }
  ],
  "estatisticas": {
    "total_aprovadas": 2,
    "total_reprovadas": 0,
    "media_geral": 8.75
  }
}
```

---

## 🧪 Testes

### Teste Rápido do Sistema

```bash
# 1. Testar API do currículo
curl http://localhost:5000/api/curriculo | head -20

# 2. Testar busca de aluno
curl http://localhost:5000/api/aluno/2024001

# 3. Testar consulta via POST
curl -X POST http://localhost:5000/api/consultar \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste API",
    "matricula": "API001",
    "tipo": "veterano",
    "ano_atual": 1,
    "aprovadas": [{"id": "LOGICA", "nota": 9.0}],
    "reprovadas": []
  }'
```

### Diagnóstico do Banco

```bash
python main-test.py
```

### Verificar Estrutura

```bash
# Contar alunos
python -c "from database import AlunoRepository; print(f'Alunos: {len(AlunoRepository.listar_todos())}')"

# Ver histórico
python -c "from database import HistoricoRepository; h = HistoricoRepository.buscar_historico_aluno('2024001'); print(f'Aprovadas: {len(h[\"aprovadas\"])}')"
```

---

## 🐛 Troubleshooting

### ❌ Problema: Porta 5000 já em uso

**Windows:**
```bash
# Encontrar processo
netstat -ano | findstr :5000

# Matar processo (substitua <PID>)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Encontrar processo
lsof -i :5000

# Matar processo
kill -9 <PID>
```

**OU mudar a porta no `main.py`:**
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

---

### ❌ Problema: Erro ao importar módulos

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# OU com Docker
docker-compose build --no-cache
```

---

### ❌ Problema: Banco de dados vazio

```bash
# Verificar se banco existe
dir uniadvisor.db      # Windows
ls -lh uniadvisor.db   # Linux/Mac

# Verificar conteúdo
python diagnostico_historico.py

# Se vazio, popular
python executar_sql.py
```

---

### ❌ Problema: Histórico não aparece no frontend

**Diagnóstico:**
```bash
# 1. Verificar banco
python diagnostico_historico.py

# 2. Verificar API
curl http://localhost:5000/api/aluno/2024001

# 3. Verificar JavaScript (F12 → Console)
# Deve aparecer: "🔍 Buscando aluno..."
```

**Solução:**
1. Limpar cache do navegador (`Ctrl + Shift + Delete`)
2. Hard reload (`Ctrl + F5`)
3. Ver guia: `SOLUCAO_DEFINITIVA_HISTORICO.md`

---

### ❌ Problema: Docker não inicia

```bash
# Ver logs detalhados
docker-compose logs

# Recriar container
docker-compose down
docker-compose up -d --build

# Verificar se porta está livre
docker ps -a
```

---

### ❌ Problema: Permissão negada (Linux/Mac)

```bash
# Dar permissão aos scripts
chmod +x *.py

# OU rodar com sudo (Docker)
sudo docker-compose up -d
```

---

## 📊 Comandos Úteis

### Python Local

```bash
# Criar banco do zero
python criarbanco.py

# Popular com dados
python main-test.py

# Iniciar servidor
python main.py

# Backup do banco
cp uniadvisor.db backup_$(date +%Y%m%d).db
```

### Docker

```bash
# Build e iniciar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar
docker-compose stop

# Remover tudo
docker-compose down -v

# Entrar no container
docker exec -it uniadvisor_app bash

# Rodar comando no container
docker exec -it uniadvisor_app python diagnostico_historico.py
```

### Banco de Dados (SQLite)

```bash
# Abrir banco
sqlite3 uniadvisor.db

# Dentro do SQLite:
.tables                                    # Listar tabelas
SELECT COUNT(*) FROM alunos;               # Contar alunos
SELECT * FROM alunos;                      # Ver todos alunos
SELECT * FROM historico_disciplinas WHERE aluno_id='2024001';
.quit                                      # Sair
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes:

- Mantenha o código limpo e comentado
- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autores

**Daniel**
- 🎓 Universidade do Estado do Amazonas (UEA)
- 📚 Sistemas de Informação - 6º Semestre
- 📅 Janeiro 2025
- 🔗 [GitHub]([https://github.com/DanielNazarioPro](https://github.com/DanielNazarioPro/uniadvisor))

---

## 🙏 Agradecimentos

- Instituto Federal do Amazonas (IFAM) - Currículo base
- Universidade do Estado do Amazonas (UEA) - Orientação acadêmica
- Professores e colegas do curso de Sistemas de Informação
- Comunidade Python e Flask

---

## 📚 Referências

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
2. Giarratano, J., & Riley, G. (2004). *Expert Systems: Principles and Programming*
3. Flask Documentation: https://flask.palletsprojects.com/
4. Docker Documentation: https://docs.docker.com/

---
