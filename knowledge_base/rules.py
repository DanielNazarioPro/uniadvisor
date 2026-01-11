"""
Base de Conhecimento - Regras do Sistema UniAdvisor (CORRIGIDO)

Este módulo contém TODAS as regras de negócio do sistema,
implementando corretamente o encadeamento para frente (Forward Chaining).

CORREÇÕES REALIZADAS:
1. Mapeamento correto entre fatos do GerenciadorFatosAluno e condições das regras
2. Nomes de fatos padronizados
3. Regras de elegibilidade funcionando para TODAS as disciplinas
"""
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from enum import Enum


class TipoRegra(Enum):
    """Tipos de regras do sistema"""
    MATRICULA_AUTOMATICA = "matricula_automatica"
    BLOQUEIO = "bloqueio"
    ELEGIBILIDADE = "elegibilidade"
    HEURISTICA = "heuristica"
    REPROVACAO_ANO = "reprovacao_ano"


@dataclass
class Regra:
    """Representa uma regra SE-ENTÃO do sistema"""
    id: str
    nome: str
    tipo: TipoRegra
    descricao: str
    condicao: Callable[[Dict], bool]
    acao: Callable[[Dict], Any]
    prioridade: int = 0
    
    def avaliar(self, fatos: Dict) -> bool:
        """Avalia se a condição da regra é satisfeita"""
        try:
            return self.condicao(fatos)
        except Exception as e:
            print(f"Erro ao avaliar regra {self.id}: {e}")
            return False
    
    def executar(self, fatos: Dict) -> Any:
        """Executa a ação da regra"""
        return self.acao(fatos)


def criar_regras() -> List[Regra]:
    """
    Cria e retorna todas as regras do sistema.
    
    FATOS ESPERADOS (produzidos por GerenciadorFatosAluno):
    - aluno_ano: int - ano atual do aluno
    - aluno_novo: bool - se é aluno novo
    - disciplinas_aprovadas: List[str] - IDs das disciplinas aprovadas
    - disciplinas_reprovadas: List[str] - IDs das disciplinas reprovadas
    - notas: Dict[str, float] - notas por disciplina
    - reprovacoes_ano: int - quantidade de reprovações no ano atual
    - passou_todas_ano_atual: bool - se passou em todas do ano
    - tem_dependencia: bool - se tem dependências
    - lista_dependencias: List[str] - IDs das dependências
    - medias_por_area: Dict[str, float] - média por área
    
    FATOS DE DISCIPLINA (produzidos por preparar_fatos_disciplina):
    - id: str - ID da disciplina
    - ano_disciplina: int - ano da disciplina
    - mesmo_ano_aluno: bool - se é do ano do aluno
    - tem_pre_requisito: bool - se tem pré-requisitos
    - pre_requisitos_cumpridos: bool - se todos pré-requisitos estão aprovados
    - ja_aprovada: bool - se já foi aprovada
    - eh_dependencia: bool - se está na lista de dependências
    - area_forte: bool - se a área é forte (média > 8)
    - area: str - área da disciplina
    - pre_requisitos_faltantes: List[str] - pré-requisitos não cumpridos
    """
    regras = []
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R1: Matrícula automática no primeiro ano (aluno novo)
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R1",
        nome="Matrícula Primeiro Ano",
        tipo=TipoRegra.MATRICULA_AUTOMATICA,
        descricao="Aluno novo no 1º ano → matrícula automática em todas as disciplinas do ano 1",
        condicao=lambda f: (
            f.get("aluno_ano") == 1 and 
            f.get("aluno_novo", False) == True
        ),
        acao=lambda f: {
            "acao": "matricular_todas",
            "ano": 1,
            "mensagem": "✅ Aluno novo matriculado automaticamente em todas as disciplinas do 1º ano"
        },
        prioridade=100
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R2: Progressão de ano (aprovou em tudo)
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R2",
        nome="Progressão de Ano - Aprovação Total",
        tipo=TipoRegra.MATRICULA_AUTOMATICA,
        descricao="Aluno aprovou em todas → avança de ano com matrícula automática",
        condicao=lambda f: (
            f.get("passou_todas_ano_atual", False) == True and
            f.get("aluno_ano", 1) < 3 and
            not f.get("aluno_novo", False)
        ),
        acao=lambda f: {
            "acao": "avancar_ano_completo",
            "novo_ano": f.get("aluno_ano", 1) + 1,
            "mensagem": f"🎉 Parabéns! Aprovado em todas. Avançando para o {f.get('aluno_ano', 1) + 1}º ano com matrícula automática"
        },
        prioridade=90
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R3: Progressão com dependência
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R3",
        nome="Progressão com Dependência",
        tipo=TipoRegra.MATRICULA_AUTOMATICA,
        descricao="Aluno com até 3 dependências → avança mantendo dependências",
        condicao=lambda f: (
            f.get("tem_dependencia", False) == True and
            f.get("reprovacoes_ano", 0) <= 3 and
            f.get("aluno_ano", 1) < 3 and
            not f.get("aluno_novo", False) and
            not f.get("passou_todas_ano_atual", False)
        ),
        acao=lambda f: {
            "acao": "avancar_com_dependencia",
            "novo_ano": f.get("aluno_ano", 1) + 1,
            "dependencias": f.get("lista_dependencias", []),
            "mensagem": f"📚 Aluno avança para o {f.get('aluno_ano', 1) + 1}º ano, mas deve cursar {len(f.get('lista_dependencias', []))} dependência(s)"
        },
        prioridade=80
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R4: Bloqueio por pré-requisito não cumprido
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R4",
        nome="Bloqueio por Pré-requisito",
        tipo=TipoRegra.BLOQUEIO,
        descricao="Disciplina com pré-requisito não aprovado → BLOQUEADA",
        condicao=lambda f: (
            f.get("tem_pre_requisito", False) == True and
            f.get("pre_requisitos_cumpridos", True) == False
        ),
        acao=lambda f: {
            "acao": "bloquear_disciplina",
            "disciplina_id": f.get("id"),
            "prerequisito": f.get("pre_requisitos_faltantes", []),
            "mensagem": f"🚫 Bloqueada: falta aprovar {', '.join(f.get('pre_requisitos_faltantes', ['pré-requisito']))}"
        },
        prioridade=100
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R5: Reprovação de ano (mais de 3 reprovações)
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R5",
        nome="Reprovação de Ano",
        tipo=TipoRegra.REPROVACAO_ANO,
        descricao="Mais de 3 reprovações no ano → repete o ano",
        condicao=lambda f: f.get("reprovacoes_ano", 0) > 3,
        acao=lambda f: {
            "acao": "repetir_ano",
            "ano": f.get("aluno_ano"),
            "total_reprovacoes": f.get("reprovacoes_ano"),
            "mensagem": f"⚠️ Aluno reprovado de ano! {f.get('reprovacoes_ano')} reprovações (máximo permitido: 3)"
        },
        prioridade=100
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R6: Elegibilidade COM pré-requisito cumprido
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R6",
        nome="Elegibilidade por Pré-requisito Cumprido",
        tipo=TipoRegra.ELEGIBILIDADE,
        descricao="Pré-requisitos aprovados → disciplina ELEGÍVEL",
        condicao=lambda f: (
            f.get("tem_pre_requisito", False) == True and
            f.get("pre_requisitos_cumpridos", False) == True and
            f.get("ja_aprovada", True) == False
        ),
        acao=lambda f: {
            "acao": "tornar_elegivel",
            "disciplina_id": f.get("id"),
            "mensagem": f"✓ Elegível: pré-requisitos cumpridos"
        },
        prioridade=50
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R7: Elegibilidade SEM pré-requisito
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R7",
        nome="Elegibilidade sem Pré-requisito",
        tipo=TipoRegra.ELEGIBILIDADE,
        descricao="Disciplina sem pré-requisito do ano atual ou anterior → ELEGÍVEL",
        condicao=lambda f: (
            f.get("tem_pre_requisito", True) == False and
            f.get("ano_disciplina", 99) <= f.get("aluno_ano", 1) and
            f.get("ja_aprovada", True) == False
        ),
        acao=lambda f: {
            "acao": "tornar_elegivel",
            "disciplina_id": f.get("id"),
            "mensagem": f"✓ Elegível: sem pré-requisito"
        },
        prioridade=50
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R8: Heurística - Priorizar área forte (média > 8.0)
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R8",
        nome="Heurística - Área Forte",
        tipo=TipoRegra.HEURISTICA,
        descricao="Média > 8.0 na área → priorizar disciplinas desta área",
        condicao=lambda f: f.get("area_forte", False) == True,
        acao=lambda f: {
            "acao": "priorizar_area",
            "area": f.get("area"),
            "bonus_prioridade": 3,
            "mensagem": f"⭐ Priorizada: você tem bom desempenho em {f.get('area', 'esta área')}"
        },
        prioridade=30
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R9: Heurística - Priorizar dependências
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R9",
        nome="Heurística - Priorizar Dependências",
        tipo=TipoRegra.HEURISTICA,
        descricao="Disciplina em dependência → alta prioridade",
        condicao=lambda f: f.get("eh_dependencia", False) == True,
        acao=lambda f: {
            "acao": "priorizar_dependencia",
            "disciplina_id": f.get("id"),
            "bonus_prioridade": 5,
            "mensagem": f"🔴 Alta prioridade: dependência de ano anterior"
        },
        prioridade=40
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R10: Heurística - Disciplinas do ano atual têm prioridade
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R10",
        nome="Heurística - Disciplina do Ano Atual",
        tipo=TipoRegra.HEURISTICA,
        descricao="Disciplina do ano atual → prioridade moderada",
        condicao=lambda f: (
            f.get("mesmo_ano_aluno", False) == True and
            f.get("eh_dependencia", True) == False
        ),
        acao=lambda f: {
            "acao": "priorizar_ano_atual",
            "disciplina_id": f.get("id"),
            "bonus_prioridade": 2,
            "mensagem": f"📌 Disciplina do seu ano atual"
        },
        prioridade=20
    ))
    
    # ═══════════════════════════════════════════════════════════════
    # REGRA R11: Heurística - Disciplinas técnicas para curso técnico
    # ═══════════════════════════════════════════════════════════════
    regras.append(Regra(
        id="R11",
        nome="Heurística - Disciplina Técnica",
        tipo=TipoRegra.HEURISTICA,
        descricao="Disciplina da área técnica → prioridade extra para formação profissional",
        condicao=lambda f: f.get("area") in ["Tecnica", "Técnica"],
        acao=lambda f: {
            "acao": "priorizar_tecnica",
            "disciplina_id": f.get("id"),
            "bonus_prioridade": 1,
            "mensagem": f"💼 Importante para formação técnica"
        },
        prioridade=10
    ))
    
    return regras


def get_regras_por_tipo(tipo: TipoRegra) -> List[Regra]:
    """Retorna regras filtradas por tipo, ordenadas por prioridade"""
    return sorted(
        [r for r in criar_regras() if r.tipo == tipo],
        key=lambda r: r.prioridade,
        reverse=True
    )


def get_todas_regras() -> List[Regra]:
    """Retorna todas as regras ordenadas por prioridade"""
    return sorted(criar_regras(), key=lambda r: r.prioridade, reverse=True)


# Exportar para uso no motor de inferência
__all__ = ['Regra', 'TipoRegra', 'criar_regras', 'get_regras_por_tipo', 'get_todas_regras']
