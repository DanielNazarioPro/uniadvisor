"""
Motor de Inferência - Encadeamento para Frente (Forward Chaining) CORRIGIDO

O Motor de Inferência aplica a Base de Conhecimento sobre a Base de Fatos
para derivar novas conclusões e determinar as recomendações para o aluno.

CORREÇÕES REALIZADAS:
1. Avaliação correta de TODAS as disciplinas do currículo
2. Consulta direta de pré-requisitos do curriculum.json
3. Avaliação de disciplinas do ano atual E do próximo ano
4. Sistema de recomendação completo com ranking
5. Explicações detalhadas para cada decisão
"""
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from knowledge_base.rules import Regra, TipoRegra, get_todas_regras, get_regras_por_tipo
from facts_base.student_facts import BaseFatos, GerenciadorFatosAluno


class StatusInferencia(Enum):
    """Status possíveis do resultado da inferência"""
    MATRICULA_AUTOMATICA = "matricula_automatica"
    SELECAO_MANUAL = "selecao_manual"
    REPROVADO_ANO = "reprovado_ano"
    AGUARDANDO = "aguardando"
    CURSO_CONCLUIDO = "curso_concluido"


@dataclass
class ResultadoInferencia:
    """Resultado do processo de inferência"""
    status: StatusInferencia
    mensagem: str
    disciplinas_matriculadas: List[str] = field(default_factory=list)
    disciplinas_elegiveis: List[Dict] = field(default_factory=list)
    disciplinas_bloqueadas: List[Dict] = field(default_factory=list)
    disciplinas_sugeridas: List[Dict] = field(default_factory=list)
    disciplinas_aprovadas: List[Dict] = field(default_factory=list)
    explicacao: List[Dict] = field(default_factory=list)
    novo_ano: int = 0
    estatisticas: Dict = field(default_factory=dict)


class MotorInferencia:
    """
    Motor de Inferência usando Encadeamento para Frente (Forward Chaining).

    O encadeamento para frente parte dos fatos conhecidos e aplica as regras
    para derivar novos fatos até que não haja mais regras aplicáveis.
    """

    def __init__(self, base_fatos: BaseFatos, gerenciador: GerenciadorFatosAluno):
        self.base_fatos = base_fatos
        self.gerenciador = gerenciador
        self.regras = get_todas_regras()
        self.regras_disparadas: List[str] = []
        self.explicacoes: List[Dict] = []

    def inferir(self) -> ResultadoInferencia:
        """
        Executa o processo de inferência completo.

        Fluxo:
        1. Calcula fatos derivados do histórico do aluno
        2. Verifica situação geral (reprovação de ano, progressão)
        3. Avalia cada disciplina (bloqueio, elegibilidade)
        4. Aplica heurísticas para sugestões
        5. Retorna resultado com explicação
        """
        # Passo 1: Calcular fatos derivados
        self.gerenciador.calcular_fatos_derivados()

        ano_aluno = self.base_fatos.get_fato("aluno_ano", 1)
        aprovadas = self.base_fatos.get_fato("disciplinas_aprovadas", [])

        resultado = ResultadoInferencia(
            status=StatusInferencia.AGUARDANDO,
            mensagem="Processando...",
            novo_ano=ano_aluno
        )

        # Verificar se já concluiu o curso
        total_disciplinas = len(self.gerenciador.curriculo)
        if len(aprovadas) >= total_disciplinas:
            resultado.status = StatusInferencia.CURSO_CONCLUIDO
            resultado.mensagem = "🎓 Parabéns! Você completou todas as disciplinas do curso!"
            resultado.estatisticas = self.gerenciador.get_estatisticas_aluno()
            return resultado

        # Passo 2: Verificar situação geral do aluno
        situacao = self._avaliar_situacao_geral()

        if situacao["reprovado_ano"]:
            resultado.status = StatusInferencia.REPROVADO_ANO
            resultado.mensagem = situacao["mensagem"]
            resultado.explicacao = self.explicacoes
            resultado.estatisticas = self.gerenciador.get_estatisticas_aluno()
            # Mesmo reprovado, mostrar disciplinas elegíveis
            disciplinas_avaliadas = self._avaliar_disciplinas()
            resultado.disciplinas_elegiveis = disciplinas_avaliadas["elegiveis"]
            resultado.disciplinas_bloqueadas = disciplinas_avaliadas["bloqueadas"]
            resultado.disciplinas_aprovadas = disciplinas_avaliadas["aprovadas"]
            return resultado

        if situacao["matricula_automatica"]:
            resultado.status = StatusInferencia.MATRICULA_AUTOMATICA
            resultado.mensagem = situacao["mensagem"]
            resultado.novo_ano = situacao.get("novo_ano", resultado.novo_ano)
            resultado.disciplinas_matriculadas = self._obter_disciplinas_ano(resultado.novo_ano)
            resultado.explicacao = self.explicacoes
            resultado.estatisticas = self.gerenciador.get_estatisticas_aluno()
            return resultado

        # Passo 3: Avaliar cada disciplina do currículo
        disciplinas_avaliadas = self._avaliar_disciplinas()
        resultado.disciplinas_elegiveis = disciplinas_avaliadas["elegiveis"]
        resultado.disciplinas_bloqueadas = disciplinas_avaliadas["bloqueadas"]
        resultado.disciplinas_aprovadas = disciplinas_avaliadas["aprovadas"]

        # Passo 4: Aplicar heurísticas para sugestões
        resultado.disciplinas_sugeridas = self._gerar_sugestoes(
            disciplinas_avaliadas["elegiveis"]
        )

        # Passo 5: Determinar status final
        if resultado.disciplinas_elegiveis:
            resultado.status = StatusInferencia.SELECAO_MANUAL
            qtd = len(resultado.disciplinas_elegiveis)
            resultado.mensagem = f"📋 {qtd} disciplina(s) disponível(is) para matrícula. Veja as sugestões ordenadas por prioridade."
        else:
            resultado.status = StatusInferencia.AGUARDANDO
            resultado.mensagem = "⏳ Nenhuma disciplina elegível no momento. Verifique os pré-requisitos das disciplinas bloqueadas."

        resultado.explicacao = self.explicacoes
        resultado.estatisticas = self.gerenciador.get_estatisticas_aluno()

        return resultado

    def _avaliar_situacao_geral(self) -> Dict[str, Any]:
        """Avalia a situação geral do aluno aplicando regras de progressão"""
        fatos = self.base_fatos.get_todos_fatos()
        resultado = {
            "reprovado_ano": False,
            "matricula_automatica": False,
            "mensagem": "",
            "novo_ano": fatos.get("aluno_ano", 1)
        }

        # Aplicar regras de reprovação de ano (maior prioridade)
        for regra in get_regras_por_tipo(TipoRegra.REPROVACAO_ANO):
            if regra.avaliar(fatos):
                acao = regra.executar(fatos)
                resultado["reprovado_ano"] = True
                resultado["mensagem"] = acao["mensagem"]
                self._registrar_disparo(regra, fatos, acao)
                return resultado

        # Aplicar regras de matrícula automática (em ordem de prioridade)
        for regra in get_regras_por_tipo(TipoRegra.MATRICULA_AUTOMATICA):
            if regra.avaliar(fatos):
                acao = regra.executar(fatos)
                resultado["matricula_automatica"] = True
                resultado["mensagem"] = acao["mensagem"]
                resultado["novo_ano"] = acao.get("novo_ano", resultado["novo_ano"])
                self._registrar_disparo(regra, fatos, acao)
                return resultado

        return resultado

    def _avaliar_disciplinas(self) -> Dict[str, List[Dict]]:
        """
        Avalia cada disciplina do currículo quanto a bloqueio e elegibilidade.

        *** CORREÇÃO PRINCIPAL ***
        1. Avalia disciplinas do ano atual E do próximo ano (ano+1)
        2. Consulta pré-requisitos DIRETAMENTE do curriculum.json
        3. Não depende de regras SWRL para bloqueio básico
        """
        resultado = {
            "elegiveis": [],
            "bloqueadas": [],
            "aprovadas": []
        }

        curriculo = self.gerenciador.get_curriculo()
        ano_aluno = self.base_fatos.get_fato("aluno_ano", 1)
        aprovadas = self.base_fatos.get_fato("disciplinas_aprovadas", [])

        for disciplina in curriculo:
            disc_id = disciplina["id"]

            # Disciplinas já aprovadas
            if disc_id in aprovadas:
                resultado["aprovadas"].append({
                    "id": disc_id,
                    "nome": disciplina["nome"],
                    "ano": disciplina["ano"],
                    "area": disciplina["area"],
                    "carga_horaria": disciplina.get("carga_horaria", 60),
                    "nota": self.base_fatos.get_fato("notas", {}).get(disc_id)
                })
                continue

            # *** CORREÇÃO: Avaliar até ano+1 para sugerir disciplinas do próximo ano ***
            if disciplina["ano"] > ano_aluno + 1:
                continue

            # *** CORREÇÃO CRÍTICA: Consultar pré-requisitos diretamente do curriculum.json ***
            pre_requisitos = disciplina.get("pre_requisitos", [])
            pre_requisitos_faltantes = [pr for pr in pre_requisitos if pr not in aprovadas]
            tem_pre_requisito = len(pre_requisitos) > 0
            pre_requisitos_cumpridos = len(pre_requisitos_faltantes) == 0

            # *** LÓGICA CORRIGIDA: Se tem pré-requisitos não cumpridos = BLOQUEADA ***
            if tem_pre_requisito and not pre_requisitos_cumpridos:
                # Buscar nomes legíveis dos pré-requisitos faltantes
                nomes_faltantes = []
                for pr_id in pre_requisitos_faltantes:
                    disc_pr = next((d for d in curriculo if d["id"] == pr_id), None)
                    if disc_pr:
                        nomes_faltantes.append(disc_pr["nome"])

                resultado["bloqueadas"].append({
                    "id": disc_id,
                    "nome": disciplina["nome"],
                    "ano": disciplina["ano"],
                    "area": disciplina["area"],
                    "carga_horaria": disciplina.get("carga_horaria", 60),
                    "motivo": f"Faltam pré-requisitos: {', '.join(nomes_faltantes)}",
                    "prerequisitos_faltantes": pre_requisitos_faltantes,
                    "prerequisitos_faltantes_nomes": nomes_faltantes
                })
                continue

            # *** Se não está bloqueada, é ELEGÍVEL ***
            motivo_elegibilidade = "Sem pré-requisitos"
            if tem_pre_requisito:
                motivo_elegibilidade = "Pré-requisitos cumpridos"

            # Adicionar flags para priorização
            eh_ano_seguinte = disciplina["ano"] == ano_aluno + 1
            eh_ano_atual = disciplina["ano"] == ano_aluno

            resultado["elegiveis"].append({
                "id": disc_id,
                "nome": disciplina["nome"],
                "ano": disciplina["ano"],
                "area": disciplina["area"],
                "carga_horaria": disciplina.get("carga_horaria", 60),
                "motivo_elegibilidade": motivo_elegibilidade,
                "prioridade": 0,  # Será calculada nas heurísticas
                "motivos_sugestao": [],
                "eh_ano_seguinte": eh_ano_seguinte,
                "eh_ano_atual": eh_ano_atual
            })

        return resultado

    def _gerar_sugestoes(self, elegiveis: List[Dict]) -> List[Dict]:
        """
        Aplica heurísticas para ordenar e sugerir disciplinas.

        PRIORIDADES:
        1. Disciplinas do ano atual (+10 pontos)
        2. Disciplinas que são pré-requisitos de outras (+5 pontos)
        3. Disciplinas da área forte do aluno (+3 pontos)
        4. Disciplinas do próximo ano (+2 pontos)
        """
        if not elegiveis:
            return []

        curriculo = self.gerenciador.get_curriculo()
        aprovadas = self.base_fatos.get_fato("disciplinas_aprovadas", [])

        sugestoes = []

        for disc in elegiveis:
            prioridade = 0
            motivos = []

            # PRIORIDADE 1: Disciplinas do ano atual
            if disc.get("eh_ano_atual", False):
                prioridade += 10
                motivos.append("📚 Disciplina do seu ano atual")

            # PRIORIDADE 2: É pré-requisito de outras disciplinas?
            disciplinas_desbloqueadas = []
            for outras_disc in curriculo:
                if outras_disc["id"] not in aprovadas:
                    pre_reqs = outras_disc.get("pre_requisitos", [])
                    if disc["id"] in pre_reqs:
                        # Verificar se só falta esse pré-requisito
                        faltantes = [pr for pr in pre_reqs if pr not in aprovadas and pr != disc["id"]]
                        if len(faltantes) == 0:
                            disciplinas_desbloqueadas.append(outras_disc["nome"])

            if disciplinas_desbloqueadas:
                prioridade += 5
                if len(disciplinas_desbloqueadas) <= 2:
                    motivos.append(f"🔓 Desbloqueia: {', '.join(disciplinas_desbloqueadas)}")
                else:
                    motivos.append(f"🔓 Desbloqueia {len(disciplinas_desbloqueadas)} disciplinas")

            # PRIORIDADE 3: Aplicar heurísticas das regras SWRL (se existirem)
            fatos_disc = self.gerenciador.preparar_fatos_disciplina(disc["id"])
            fatos_completos = {**self.base_fatos.get_todos_fatos(), **fatos_disc}

            for regra in get_regras_por_tipo(TipoRegra.HEURISTICA):
                if regra.avaliar(fatos_completos):
                    acao = regra.executar(fatos_completos)
                    bonus = acao.get("bonus_prioridade", 0)
                    prioridade += bonus
                    motivos.append(acao["mensagem"])
                    self._registrar_disparo(regra, fatos_completos, acao)

            # PRIORIDADE 4: Disciplinas do próximo ano
            if disc.get("eh_ano_seguinte", False):
                prioridade += 2
                motivos.append("⏭️ Adiante-se no próximo ano")

            sugestoes.append({
                **disc,
                "prioridade": prioridade,
                "motivos_sugestao": motivos,
                "ranking": 0  # Será atualizado após ordenação
            })

        # Ordenar por prioridade (maior primeiro)
        sugestoes.sort(key=lambda x: x["prioridade"], reverse=True)

        # Atribuir ranking
        for i, sugestao in enumerate(sugestoes, 1):
            sugestao["ranking"] = i

        return sugestoes

    def _obter_disciplinas_ano(self, ano: int) -> List[str]:
        """Retorna IDs das disciplinas de um ano específico"""
        return [d["id"] for d in self.gerenciador.get_disciplinas_ano(ano)]

    def _registrar_disparo(self, regra: Regra, fatos: Dict, resultado: Dict) -> None:
        """Registra o disparo de uma regra para explicação"""
        if regra.id not in self.regras_disparadas:
            self.regras_disparadas.append(regra.id)

        # Filtrar fatos relevantes para a explicação
        fatos_relevantes = {
            k: v for k, v in fatos.items()
            if not k.startswith('_') and k in [
                'id', 'nome', 'aluno_ano', 'tem_pre_requisito',
                'pre_requisitos_cumpridos', 'eh_dependencia',
                'area_forte', 'mesmo_ano_aluno', 'area'
            ]
        }

        self.explicacoes.append({
            "regra_id": regra.id,
            "regra_nome": regra.nome,
            "tipo": regra.tipo.value,
            "descricao": regra.descricao,
            "resultado": resultado["mensagem"],
            "contexto": fatos_relevantes
        })

        self.base_fatos.registrar_inferencia(regra.id, resultado)

    def get_explicacao_completa(self) -> Dict[str, Any]:
        """Retorna explicação completa do processo de inferência"""
        return {
            "regras_disparadas": self.regras_disparadas,
            "total_regras_sistema": len(self.regras),
            "total_regras_disparadas": len(self.regras_disparadas),
            "explicacoes": self.explicacoes,
            "fatos_finais": {
                k: v for k, v in self.base_fatos.get_todos_fatos().items()
                if not k.startswith('_')
            }
        }

    def get_resumo_regras(self) -> List[Dict]:
        """Retorna resumo das regras do sistema"""
        return [
            {
                "id": r.id,
                "nome": r.nome,
                "tipo": r.tipo.value,
                "descricao": r.descricao,
                "prioridade": r.prioridade
            }
            for r in self.regras
        ]