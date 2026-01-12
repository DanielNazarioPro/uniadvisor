"""
Interface Web - Aplicação Flask para o UniAdvisor (CORRIGIDO)

Interface completamente reestruturada com:
1. Integração com banco de dados SQLite
2. Seleção visual de disciplinas (checkboxes)
3. Endpoints corrigidos para todas as operações
4. Persistência do histórico do aluno
5. Busca rápida de alunos pré-cadastrados
"""
from flask import Flask, render_template, request, jsonify, session
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from facts_base.student_facts import BaseFatos, GerenciadorFatosAluno
from inference_engine.engine import MotorInferencia, StatusInferencia
from database import AlunoRepository, HistoricoRepository, MatriculaRepository, LogRepository, inicializar_banco

app = Flask(__name__)
app.secret_key = 'uniadvisor-secret-key-2026-ifam'

inicializar_banco()


def criar_motor_inferencia(base_fatos: BaseFatos) -> tuple:
    """Factory para criar o motor de inferência"""
    gerenciador = GerenciadorFatosAluno(base_fatos)
    motor = MotorInferencia(base_fatos, gerenciador)
    return motor, gerenciador


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/curriculo', methods=['GET'])
def get_curriculo():
    """Retorna o currículo completo organizado por ano"""
    base_fatos = BaseFatos()
    gerenciador = GerenciadorFatosAluno(base_fatos)
    curriculo = gerenciador.get_curriculo()

    por_ano = {}
    for d in curriculo:
        ano = d['ano']
        if ano not in por_ano:
            por_ano[ano] = []
        por_ano[ano].append(d)

    return jsonify({
        'curriculo': curriculo,
        'por_ano': por_ano,
        'total_disciplinas': len(curriculo),
        'total_carga_horaria': sum(d.get('carga_horaria', 60) for d in curriculo)
    })


@app.route('/api/aluno/<aluno_id>', methods=['GET'])
def buscar_aluno(aluno_id):
    """Busca dados completos de um aluno pelo ID/matrícula"""
    # Buscar aluno
    aluno = AlunoRepository.buscar_por_id(aluno_id)
    if not aluno:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

    # Buscar histórico
    historico = HistoricoRepository.buscar_historico_aluno(aluno_id)

    return jsonify({
        'aluno': aluno,
        'historico': historico,
        'sucesso': True
    })


@app.route('/api/alunos', methods=['GET'])
def listar_alunos():
    """Lista todos os alunos cadastrados"""
    alunos = AlunoRepository.listar_todos()
    return jsonify({
        'alunos': alunos,
        'total': len(alunos)
    })


@app.route('/api/consultar', methods=['POST'])
def consultar():
    """Endpoint principal de consulta - retorna recomendação de matrícula"""
    dados = request.json

    base_fatos = BaseFatos()
    motor, gerenciador = criar_motor_inferencia(base_fatos)

    tipo_aluno = dados.get('tipo', 'veterano')
    eh_novo = tipo_aluno == 'novo'
    ano_atual = dados.get('ano_atual', 1)

    if eh_novo:
        ano_atual = 1

    aluno_id = dados.get('aluno_id', dados.get('matricula', 'aluno_temp'))

    # ===== PERSISTÊNCIA NO BANCO =====
    # 1. Criar/Atualizar aluno no banco
    AlunoRepository.criar_ou_atualizar(
        aluno_id=aluno_id,
        nome=dados.get('nome', 'Aluno'),
        ano=ano_atual,
        tipo=tipo_aluno
    )

    # 2. Limpar histórico anterior (se for uma nova consulta)
   # HistoricoRepository.limpar_historico(aluno_id)

    # 3. Salvar histórico no banco
    if not eh_novo:
        ano_cursado = datetime.now().year

        # Salvar aprovações
        for aprovacao in dados.get('aprovadas', []):
            disc_id = aprovacao.get('id') or aprovacao.get('disciplina_id')
            nota = aprovacao.get('nota', 7.0)
            if disc_id:
                HistoricoRepository.registrar_disciplina(
                    aluno_id=aluno_id,
                    disciplina_id=disc_id,
                    status='aprovado',
                    nota=nota,
                    ano_cursado=ano_cursado
                )

        # Salvar reprovações
        for reprovacao in dados.get('reprovadas', []):
            disc_id = reprovacao.get('id') or reprovacao.get('disciplina_id')
            nota = reprovacao.get('nota', 4.0)
            if disc_id:
                HistoricoRepository.registrar_disciplina(
                    aluno_id=aluno_id,
                    disciplina_id=disc_id,
                    status='reprovado',
                    nota=nota,
                    ano_cursado=ano_cursado
                )

    # ===== PROCESSAMENTO (como antes) =====
    gerenciador.inicializar_aluno(
        aluno_id=aluno_id,
        nome=dados.get('nome', 'Aluno'),
        ano=ano_atual,
        novo=eh_novo
    )

    if not eh_novo:
        for aprovacao in dados.get('aprovadas', []):
            disc_id = aprovacao.get('id') or aprovacao.get('disciplina_id')
            if disc_id:
                gerenciador.registrar_aprovacao(disc_id, aprovacao.get('nota', 7.0))

        for reprovacao in dados.get('reprovadas', []):
            disc_id = reprovacao.get('id') or reprovacao.get('disciplina_id')
            if disc_id:
                gerenciador.registrar_reprovacao(disc_id, reprovacao.get('nota', 4.0))

    resultado = motor.inferir()
    explicacao_completa = motor.get_explicacao_completa()

    # 4. Registrar log da inferência
    LogRepository.registrar_consulta(
        aluno_id=aluno_id,
        regras=explicacao_completa['regras_disparadas'],
        resultado={'status': resultado.status.value, 'mensagem': resultado.mensagem}
    )

    resposta = {
        'status': resultado.status.value,
        'mensagem': resultado.mensagem,
        'novo_ano': resultado.novo_ano,
        'disciplinas_matriculadas': resultado.disciplinas_matriculadas,
        'disciplinas_elegiveis': resultado.disciplinas_elegiveis,
        'disciplinas_bloqueadas': resultado.disciplinas_bloqueadas,
        'disciplinas_sugeridas': resultado.disciplinas_sugeridas,
        'disciplinas_aprovadas': resultado.disciplinas_aprovadas,
        'explicacao': resultado.explicacao,
        'estatisticas': resultado.estatisticas,
        'aluno_salvo': True,  # Indicador de que foi salvo
        'debug': {
            'regras_disparadas': explicacao_completa['regras_disparadas'],
            'total_regras': explicacao_completa['total_regras_sistema']
        }
    }

    return jsonify(resposta)


@app.route('/api/matricular', methods=['POST'])
def matricular():
    """Confirma matrícula nas disciplinas selecionadas"""
    dados = request.json
    disciplinas = dados.get('disciplinas', [])
    aluno_id = dados.get('aluno_id', 'aluno_temp')

    count = MatriculaRepository.registrar_multiplas(aluno_id, disciplinas)

    return jsonify({
        'sucesso': True,
        'mensagem': f'Matrícula confirmada em {count} disciplina(s)',
        'disciplinas': disciplinas
    })


@app.route('/api/regras', methods=['GET'])
def get_regras():
    """Retorna lista de regras do sistema"""
    base_fatos = BaseFatos()
    motor, _ = criar_motor_inferencia(base_fatos)
    return jsonify({'regras': motor.get_resumo_regras()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
