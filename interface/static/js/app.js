// ===== ESTADO DA APLICAÇÃO =====
const state = {
    aluno: { nome: '', matricula: '', tipo: 'veterano', ano: 2 },
    curriculo: [],
    historico: { aprovadas: [], reprovadas: [] },
    resultado: null
};

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', async () => {
    await carregarCurriculo();
    inicializarEventos();
    adicionarEstilos();
    adicionarBotaoBuscar();
});

// ===== CARREGAR CURRÍCULO =====
async function carregarCurriculo() {
    try {
        const response = await fetch('/api/curriculo');
        const data = await response.json();
        state.curriculo = data.curriculo;
        state.curriculoPorAno = data.por_ano;
    } catch (error) {
        console.error('Erro ao carregar currículo:', error);
        alert('Erro ao carregar currículo. Recarregue a página.');
    }
}

// ===== EVENTOS =====
function inicializarEventos() {
    // Tipo de aluno
    document.getElementById('tipoNovo').addEventListener('change', () => {
        document.getElementById('veteranoOptions').classList.add('hidden');
    });

    document.getElementById('tipoVeterano').addEventListener('change', () => {
        document.getElementById('veteranoOptions').classList.remove('hidden');
    });

    // Form aluno
    document.getElementById('formAluno').addEventListener('submit', (e) => {
        e.preventDefault();
        avancarParaHistorico();
    });

    // Buscar aluno ao pressionar Enter na matrícula
    document.getElementById('matricula').addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            await buscarAlunoCadastrado();
        }
    });

    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const ano = tab.dataset.ano;
            mostrarDisciplinasAno(ano);
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        });
    });

    // Botões de navegação
    document.getElementById('btnVoltar1').addEventListener('click', () => mostrarEtapa(1));
    document.getElementById('btnVoltar2').addEventListener('click', () => mostrarEtapa(1));
    document.getElementById('btnConsultar').addEventListener('click', executarConsulta);
    document.getElementById('btnConfirmar').addEventListener('click', confirmarMatricula);
}

// ===== BUSCAR ALUNO PRÉ-CADASTRADO =====
async function buscarAlunoCadastrado() {
    const matricula = document.getElementById('matricula').value.trim();

    if (!matricula) {
        return;
    }

    console.log(`🔍 Buscando aluno: ${matricula}`);

    try {
        const response = await fetch(`/api/aluno/${matricula}`);

        if (!response.ok) {
            console.log('Aluno não encontrado no banco');
            return;
        }

        const data = await response.json();
        console.log('✓ Aluno encontrado:', data);

        // Preencher dados do aluno
        document.getElementById('nome').value = data.aluno.nome;
        document.getElementById('anoAtual').value = data.aluno.ano_atual;

        // Marcar como veterano
        document.getElementById('tipoVeterano').checked = true;
        document.getElementById('veteranoOptions').classList.remove('hidden');

        // Armazenar histórico NO STATE
        state.historico = {
            aprovadas: data.historico?.aprovadas || [],
            reprovadas: data.historico?.reprovadas || []
        };

        console.log('State atualizado:', state.historico);

        // Mostrar notificação
        mostrarNotificacao(`✅ ${data.aluno.nome} encontrado!`, 'success');

        // Aguardar e avançar
        setTimeout(() => {
            avancarParaHistorico();
            // Preencher histórico após avançar
            setTimeout(() => {
                preencherHistoricoCarregado();
            }, 500);
        }, 800);

    } catch (error) {
        console.error('❌ Erro ao buscar aluno:', error);
        mostrarNotificacao('Erro ao buscar aluno. Tente novamente.', 'error');
    }
}


function preencherHistoricoCarregado() {
    console.log('📋 Preenchendo histórico carregado...');
    console.log('Aprovadas:', state.historico.aprovadas?.length || 0);
    console.log('Reprovadas:', state.historico.reprovadas?.length || 0);

    // Função para tentar preencher
    const tentarPreencher = (tentativa = 1) => {
        console.log(`Tentativa ${tentativa} de preencher histórico`);

        let preenchidas = 0;

        // Marcar aprovadas
        state.historico.aprovadas?.forEach(disc => {
            const select = document.querySelector(`.status-select[data-id="${disc.id}"]`);
            const input = document.querySelector(`.nota-input[data-id="${disc.id}"]`);

            if (select && input) {
                select.value = 'aprovado';
                input.disabled = false;
                input.value = disc.nota || '';

                // Disparar evento change para atualizar visual
                const changeEvent = new Event('change', { bubbles: true });
                select.dispatchEvent(changeEvent);

                preenchidas++;
            } else {
                console.warn(`Disciplina ${disc.id} não encontrada no DOM`);
            }
        });

        // Marcar reprovadas
        state.historico.reprovadas?.forEach(disc => {
            const select = document.querySelector(`.status-select[data-id="${disc.id}"]`);
            const input = document.querySelector(`.nota-input[data-id="${disc.id}"]`);

            if (select && input) {
                select.value = 'reprovado';
                input.disabled = false;
                input.value = disc.nota || '';

                // Disparar evento change para atualizar visual
                const changeEvent = new Event('change', { bubbles: true });
                select.dispatchEvent(changeEvent);

                preenchidas++;
            } else {
                console.warn(`Disciplina ${disc.id} não encontrada no DOM`);
            }
        });

        console.log(`✓ ${preenchidas} disciplinas preenchidas`);

        // Se não preencheu nada e ainda tem tentativas, tentar novamente
        const total = (state.historico.aprovadas?.length || 0) + (state.historico.reprovadas?.length || 0);
        if (preenchidas === 0 && total > 0 && tentativa < 5) {
            console.log('⚠️ Nenhuma disciplina preenchida, tentando novamente...');
            setTimeout(() => tentarPreencher(tentativa + 1), 300);
        } else if (preenchidas > 0) {
            mostrarNotificacao(`📊 ${preenchidas} disciplinas carregadas do histórico!`, 'success');
        }
    };

    // Aguardar renderização inicial e tentar preencher
    setTimeout(() => tentarPreencher(), 300);
}

function mostrarNotificacao(mensagem, tipo = 'info') {
    const notif = document.createElement('div');
    notif.className = `notificacao notif-${tipo}`;
    notif.textContent = mensagem;
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${tipo === 'success' ? '#4CAF50' : '#2196F3'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notif);

    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// ===== NAVEGAÇÃO =====
function mostrarEtapa(numero) {
    document.querySelectorAll('.card').forEach(card => card.classList.add('hidden'));
    document.getElementById(`step-${numero}`).classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== ETAPA 1 -> ETAPA 2 =====
function avancarParaHistorico() {
    state.aluno = {
        nome: document.getElementById('nome').value,
        matricula: document.getElementById('matricula').value,
        tipo: document.querySelector('input[name="tipoAluno"]:checked').value,
        ano: parseInt(document.getElementById('anoAtual').value)
    };

    // Se aluno novo, pular histórico
    if (state.aluno.tipo === 'novo') {
        executarConsulta();
        return;
    }

    renderizarDisciplinas();
    mostrarEtapa(2);
    mostrarDisciplinasAno(1);
}

// ===== RENDERIZAR DISCIPLINAS =====
function renderizarDisciplinas() {
    const container = document.getElementById('disciplinasContainer');
    container.innerHTML = '';

    for (let ano = 1; ano <= 3; ano++) {
        const disciplinas = state.curriculoPorAno[ano] || [];

        const divAno = document.createElement('div');
        divAno.className = `disciplinas-ano ${ano === 1 ? 'active' : ''}`;
        divAno.id = `disciplinas-ano-${ano}`;

        divAno.innerHTML = disciplinas.map(d => `
            <div class="disciplina-item" data-id="${d.id}">
                <div class="disciplina-info">
                    <div class="disciplina-nome">${d.id} - ${d.nome}</div>
                    <div class="disciplina-meta">
                        ${d.area} | ${d.carga_horaria}h
                        ${d.pre_requisitos.length > 0 ? `| Pré-req: ${d.pre_requisitos.join(', ')}` : ''}
                    </div>
                </div>
                <div class="disciplina-status">
                    <select class="status-select" data-id="${d.id}">
                        <option value="nao_cursou">Não cursou</option>
                        <option value="aprovado">Aprovado</option>
                        <option value="reprovado">Reprovado</option>
                    </select>
                    <input type="number" class="nota-input" data-id="${d.id}" 
                           placeholder="Nota" min="0" max="10" step="0.5" disabled>
                </div>
            </div>
        `).join('');

        container.appendChild(divAno);
    }

    // Eventos dos selects
    document.querySelectorAll('.status-select').forEach(select => {
        select.addEventListener('change', (e) => {
            const id = e.target.dataset.id;
            const nota = document.querySelector(`.nota-input[data-id="${id}"]`);
            const item = e.target.closest('.disciplina-item');

            item.classList.remove('aprovada', 'reprovada');

            if (e.target.value === 'nao_cursou') {
                nota.disabled = true;
                nota.value = '';
            } else {
                nota.disabled = false;
                item.classList.add(e.target.value === 'aprovado' ? 'aprovada' : 'reprovada');
            }
        });
    });
}

function mostrarDisciplinasAno(ano) {
    document.querySelectorAll('.disciplinas-ano').forEach(div => div.classList.remove('active'));
    document.getElementById(`disciplinas-ano-${ano}`).classList.add('active');
}

// ===== COLETAR HISTÓRICO =====
function coletarHistorico() {
    const aprovadas = [];
    const reprovadas = [];

    document.querySelectorAll('.status-select').forEach(select => {
        const id = select.dataset.id;
        const status = select.value;
        const nota = parseFloat(document.querySelector(`.nota-input[data-id="${id}"]`).value) || 7;

        if (status === 'aprovado') {
            aprovadas.push({ id, nota });
        } else if (status === 'reprovado') {
            reprovadas.push({ id, nota });
        }
    });

    state.historico = { aprovadas, reprovadas };
}

// ===== EXECUTAR CONSULTA =====
async function executarConsulta() {
    if (state.aluno.tipo === 'veterano') {
        coletarHistorico();
    }

    const payload = {
        nome: state.aluno.nome,
        matricula: state.aluno.matricula,
        aluno_id: state.aluno.matricula,
        tipo: state.aluno.tipo,
        ano_atual: state.aluno.ano,
        aprovadas: state.historico.aprovadas,
        reprovadas: state.historico.reprovadas
    };

    try {
        const response = await fetch('/api/consultar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        state.resultado = await response.json();
        renderizarResultado();
        mostrarEtapa(3);
    } catch (error) {
        console.error('Erro na consulta:', error);
        alert('Erro ao processar consulta. Tente novamente.');
    }
}

// ===== RENDERIZAR RESULTADO =====
function renderizarResultado() {
    const r = state.resultado;

    // Mensagem principal
    document.getElementById('mensagemResultado').innerHTML = r.mensagem;

    // Estatísticas
    const stats = r.estatisticas || {};
    document.getElementById('statAprovadas').textContent = stats.aprovadas || 0;
    document.getElementById('statElegiveis').textContent = r.disciplinas_elegiveis?.length || 0;
    document.getElementById('statBloqueadas').textContent = r.disciplinas_bloqueadas?.length || 0;
    document.getElementById('statProgresso').textContent = `${stats.percentual_conclusao || 0}%`;

    // Disciplinas Sugeridas
    const listaSugeridas = document.getElementById('listaSugeridas');
    const sugeridas = r.disciplinas_sugeridas || r.disciplinas_elegiveis || [];

    if (sugeridas.length > 0) {
        listaSugeridas.innerHTML = sugeridas.map((d, i) => `
            <div class="item sugerida">
                <div class="item-info">
                    <h4>${d.id} - ${d.nome}</h4>
                    <div class="motivo">
                        ${d.area} | ${d.carga_horaria}h
                        ${d.motivos_sugestao?.length > 0 ? '<br>' + d.motivos_sugestao.join(' | ') : ''}
                    </div>
                </div>
                <div>
                    <span class="badge ranking">#${d.ranking || i + 1}</span>
                    ${d.prioridade > 3 ? '<span class="badge prioridade-alta">Alta Prioridade</span>' : ''}
                </div>
            </div>
        `).join('');
        document.getElementById('secaoSugeridas').classList.remove('hidden');
    } else {
        document.getElementById('secaoSugeridas').classList.add('hidden');
    }

    // Disciplinas Bloqueadas
    const listaBloqueadas = document.getElementById('listaBloqueadas');
    const bloqueadas = r.disciplinas_bloqueadas || [];

    if (bloqueadas.length > 0) {
        listaBloqueadas.innerHTML = bloqueadas.map(d => `
            <div class="item bloqueada">
                <div class="item-info">
                    <h4>${d.id} - ${d.nome}</h4>
                    <div class="motivo">
                        ${d.motivo}
                        ${d.prerequisitos_faltantes?.length > 0 ? 
                            `<br>Falta: ${d.prerequisitos_faltantes.join(', ')}` : ''}
                    </div>
                </div>
            </div>
        `).join('');
        document.getElementById('secaoBloqueadas').classList.remove('hidden');
    } else {
        document.getElementById('secaoBloqueadas').classList.add('hidden');
    }

    // Explicações
    const listaExplicacao = document.getElementById('listaExplicacao');
    const explicacoes = r.explicacao || [];

    listaExplicacao.innerHTML = explicacoes.slice(0, 20).map(e => `
        <div class="explanation-item">
            <span class="regra">[${e.regra_id}]</span> 
            ${e.resultado}
        </div>
    `).join('');
}

// ===== CONFIRMAR MATRÍCULA =====
async function confirmarMatricula() {
    const disciplinas = (state.resultado.disciplinas_sugeridas || state.resultado.disciplinas_elegiveis || [])
        .map(d => d.id);

    if (disciplinas.length === 0) {
        alert('Nenhuma disciplina para matricular.');
        return;
    }

    try {
        const response = await fetch('/api/matricular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                aluno_id: state.aluno.matricula,
                disciplinas
            })
        });

        const result = await response.json();

        if (result.sucesso) {
            alert(`✅ ${result.mensagem}\n\nDisciplinas: ${disciplinas.join(', ')}`);
            location.reload();
        }
    } catch (error) {
        console.error('Erro ao confirmar matrícula:', error);
        alert('Erro ao confirmar matrícula.');
    }
}

// ===== ESTILOS =====
function adicionarEstilos() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

function adicionarBotaoBuscar() {
    const matriculaInput = document.getElementById('matricula');

    // Criar botão
    const btnBuscar = document.createElement('button');
    btnBuscar.type = 'button';
    btnBuscar.id = 'btnBuscarAluno';
    btnBuscar.className = 'btn-buscar';
    btnBuscar.innerHTML = '🔍 Buscar Aluno';
    btnBuscar.style.cssText = `
        margin-left: 10px;
        padding: 10px 20px;
        background: #2196F3;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        transition: background 0.3s;
    `;

    btnBuscar.addEventListener('mouseover', () => {
        btnBuscar.style.background = '#1976D2';
    });

    btnBuscar.addEventListener('mouseout', () => {
        btnBuscar.style.background = '#2196F3';
    });

    btnBuscar.addEventListener('click', buscarAlunoCadastrado);

    // Inserir botão ao lado do campo matrícula
    const matriculaContainer = matriculaInput.parentElement;
    matriculaContainer.style.display = 'flex';
    matriculaContainer.style.alignItems = 'center';
    matriculaContainer.appendChild(btnBuscar);
}