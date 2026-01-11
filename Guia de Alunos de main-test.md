# 🎓 GUIA DE USUÁRIOS DE TESTE

## 📋 Lista de Usuários Pré-cadastrados

### 1️⃣ **Maria Silva Santos** - Matrícula: `2024001`
**Perfil:** Aluna excelente 
**Ano:** 2º  
**Situação:** Aprovou TODAS as 16 disciplinas do 1º ano com notas altas

**Resultado esperado:**
- ✅ 16 disciplinas do 2º ano elegíveis
- 🎯 POO, BD, IHC, PI1 sugeridas como prioridade
- 📊 100% de conclusão do 1º ano
- ⭐ Média geral: ~9.0

**Use para demonstrar:** Sistema para aluno excelente progredindo normalmente

---

### 2️⃣ **João Pedro Oliveira** - Matrícula: `2024002`
**Perfil:** Aluno com dificuldades  
**Ano:** 1º  
**Situação:** 13 aprovações + 3 reprovações (FIS1, QUI1, LOGICA)

**Resultado esperado:**
- ❌ 3 reprovações
- 🔒 Disciplinas bloqueadas: POO, BD, ANALISE, IHC, PI1
- ⚠️ LOGICA é pré-requisito crítico
- 💡 Sugestão: Refazer LOGICA prioritariamente

**Use para demonstrar:** Sistema identificando bloqueios por pré-requisitos

---

### 3️⃣ **Ana Carolina Mendes** - Matrícula: `2023001`
**Perfil:** Veterana do 2º ano  
**Ano:** 2º  
**Situação:** 1º ano completo + POO, BD, IHC, ANALISE aprovadas

**Resultado esperado:**
- ✅ Pode cursar MOBILE e WEB (3º ano)
- 🎯 Sistema sugere disciplinas do próximo ano
- 📚 Disciplinas técnicas avançadas disponíveis

**Use para demonstrar:** Aluno adiantado podendo cursar ano seguinte

---

### 4️⃣ **Carlos Eduardo Costa** - Matrícula: `2024003`
**Perfil:** Aluno em situação crítica  
**Ano:** 1º  
**Situação:** 10 aprovações + 6 reprovações (MAT1, FIS1, QUI1, LOGICA, REDES, SO)

**Resultado esperado:**
- ⚠️ ALERTA: Risco de reprovação de ano (>3 reprovações)
- 🔴 Mensagem crítica do sistema
- 🔒 Muitas disciplinas bloqueadas
- 📉 Progresso: ~62%

**Use para demonstrar:** Sistema alertando sobre situação crítica

---

### 5️⃣ **Lucas Fernandes Lima** - Matrícula: `2024004`
**Perfil:** Forte em Exatas, fraco em Humanas  
**Ano:** 1º  
**Situação:** Notas 9-10 em Exatas, 6-7 em Humanas

**Resultado esperado:**
- ⭐ Heurística: "Área forte em Exatas"
- 🎯 Sistema prioriza disciplinas técnicas
- 📊 Média Exatas: ~9.5 | Média Humanas: ~6.5

**Use para demonstrar:** Sistema identificando área forte e priorizando

---

### 6️⃣ **Beatriz Almeida Rocha** - Matrícula: `2022001`
**Perfil:** Veterana avançada  
**Ano:** 3º  
**Situação:** 1º e 2º anos completos + algumas do 3º

**Resultado esperado:**
- 🎓 Faltam poucas disciplinas para concluir
- ✅ Pode cursar disciplinas finais (EDF3, FIS3, etc.)
- 📈 Progresso: ~80%
- 🏆 Perto da formatura

**Use para demonstrar:** Aluna experiente finalizando curso

---

## 🚀 Como Usar na Apresentação

### Método 1: Busca Rápida (com funcionalidade adicional)
1. Digite apenas a matrícula (ex: `2024001`)
2. Pressione Enter ou clique em "🔍 Buscar"
3. Sistema preenche automaticamente nome, ano e histórico
4. Clique em "Gerar Recomendação"

### Método 2: Preenchimento Manual (atual)
1. Digite a matrícula
2. Digite o nome manualmente
3. Selecione "Veterano" e o ano
4. Continue → Preencha histórico manualmente
5. Gerar Recomendação

---

## 📊 Casos de Uso para Demonstração

### Demonstração 1: Fluxo Normal (5 min)
**Aluno:** Maria Silva Santos (2024001)
**Objetivo:** Mostrar funcionamento padrão
- Sistema sugere 16 disciplinas do 2º ano
- Prioriza POO e BD (desbloqueiam outras)
- Ranking inteligente funcionando

### Demonstração 2: Bloqueios (3 min)
**Aluno:** João Pedro Oliveira (2024002)
**Objetivo:** Mostrar sistema de bloqueio
- LOGICA reprovada bloqueia 5+ disciplinas
- Sistema explica motivos do bloqueio
- Botão "Ver Bloqueadas" funciona

### Demonstração 3: Situação Crítica (2 min)
**Aluno:** Carlos Eduardo Costa (2024003)
**Objetivo:** Mostrar alertas do sistema
- Sistema alerta reprovação de ano
- 6 reprovações = crítico
- Interface mostra status vermelho

### Demonstração 4: Heurísticas (3 min)
**Aluno:** Lucas Fernandes Lima (2024004)
**Objetivo:** Mostrar inteligência do sistema
- Identifica área forte (Exatas)
- Prioriza disciplinas técnicas
- Explica raciocínio nas sugestões

### Demonstração 5: Progresso Avançado (2 min)
**Aluno:** Beatriz Almeida Rocha (2022001)
**Objetivo:** Mostrar aluno experiente
- 80% do curso concluído
- Poucas disciplinas restantes
- Próximo da formatura

---

## 🎯 Roteiro de Apresentação Sugerido

**[3 min] Introdução**
- Problema: Matrícula manual é complexa
- Solução: Sistema especialista com IA

**[5 min] Demonstração Técnica**
- Mostrar Maria (fluxo normal)
- Explicar: curriculum.json → regras SWRL → motor de inferência

**[3 min] Casos Especiais**
- Mostrar João (bloqueios)
- Mostrar Carlos (situação crítica)

**[2 min] Inteligência do Sistema**
- Mostrar Lucas (heurísticas)
- Explicar ranking e priorização

**[2 min] Conclusão**
- Beatriz (veterana)
- Benefícios: automação, redução de erros, orientação inteligente

---

## 💻 Comandos para Setup

```bash
# 1. Popular usuários de teste
python popular_usuarios_teste.py

# 2. Verificar se criou corretamente
python -c "from database import AlunoRepository; print(f'Alunos cadastrados: {len(AlunoRepository.listar_todos())}')"

# 3. Iniciar servidor
python main.py
```

---

## 🎓 Perguntas que a Banca Pode Fazer

**P: "Como o sistema lida com pré-requisitos?"**
R: Use João (2024002) - LOGICA reprovada bloqueia 5 disciplinas

**P: "E se o aluno reprovar muito?"**
R: Use Carlos (2024003) - Sistema alerta com 6 reprovações

**P: "O sistema considera perfil do aluno?"**
R: Use Lucas (2024004) - Heurística de área forte em Exatas

**P: "Funciona para veteranos também?"**
R: Use Ana (2023001) ou Beatriz (2022001)