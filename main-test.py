"""
Script para Popular Banco de Dados com Usuários de Teste
Útil para demonstrações e testes do sistema
"""
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from database import AlunoRepository, HistoricoRepository, inicializar_banco
    print("✓ Módulos importados com sucesso")
except ImportError as e:
    print(f"✗ ERRO ao importar módulos: {e}")
    print("\nVerifique se você está no diretório correto:")
    print("  cd uniadvisor_corrigido")
    print("\nOu se o arquivo database.py existe:")
    print("  ls database/")
    sys.exit(1)


def criar_usuarios_teste():
    """Cria usuários de teste com diferentes perfis"""

    print("=" * 80)
    print("CRIANDO USUÁRIOS DE TESTE")
    print("=" * 80)
    print()

    # Verificar se banco existe
    db_path = Path(__file__).parent / "uniadvisor.db"
    print(f"Caminho do banco: {db_path}")

    if db_path.exists():
        print(f"✓ Banco existente encontrado (tamanho: {db_path.stat().st_size} bytes)")
        resposta = input("Deseja recriar o banco? (s/N): ").lower()
        if resposta == 's':
            db_path.unlink()
            print("✓ Banco anterior removido")
    else:
        print("• Banco não existe, será criado")

    # Garantir que o banco existe
    print("\nInicializando banco de dados...")
    try:
        inicializar_banco()
        print("✓ Banco inicializado com sucesso")
    except Exception as e:
        print(f"✗ ERRO ao inicializar banco: {e}")
        sys.exit(1)

    # Verificar se foi criado
    if db_path.exists():
        print(f"✓ Banco criado: {db_path} ({db_path.stat().st_size} bytes)")
    else:
        print("✗ ERRO: Banco não foi criado!")
        sys.exit(1)

    print()

    usuarios = [
        # ALUNO 1: Excelente
        {
            "id": "2024001",
            "nome": "Maria Silva Santos",
            "ano": 2,
            "tipo": "veterano",
            "historico": {
                "aprovadas": [
                    {"id": "PORT1", "nota": 9.5, "ano": 2024},
                    {"id": "ART1", "nota": 9.0, "ano": 2024},
                    {"id": "EDF1", "nota": 8.5, "ano": 2024},
                    {"id": "MAT1", "nota": 9.8, "ano": 2024},
                    {"id": "FIS1", "nota": 9.2, "ano": 2024},
                    {"id": "QUI1", "nota": 8.8, "ano": 2024},
                    {"id": "BIO1", "nota": 9.0, "ano": 2024},
                    {"id": "HIST1", "nota": 8.7, "ano": 2024},
                    {"id": "GEO1", "nota": 8.5, "ano": 2024},
                    {"id": "FIL1", "nota": 9.3, "ano": 2024},
                    {"id": "SOC1", "nota": 9.1, "ano": 2024},
                    {"id": "DOC_TEC", "nota": 9.5, "ano": 2024},
                    {"id": "LOGICA", "nota": 10.0, "ano": 2024},
                    {"id": "HARDWARE", "nota": 9.0, "ano": 2024},
                    {"id": "REDES", "nota": 9.2, "ano": 2024},
                    {"id": "SO", "nota": 9.4, "ano": 2024},
                ],
                "reprovadas": []
            }
        },
        # ALUNO 2: 3 reprovações
        {
            "id": "2024002",
            "nome": "João Pedro Oliveira",
            "ano": 1,
            "tipo": "veterano",
            "historico": {
                "aprovadas": [
                    {"id": "PORT1", "nota": 8.0, "ano": 2024},
                    {"id": "ART1", "nota": 7.5, "ano": 2024},
                    {"id": "EDF1", "nota": 8.5, "ano": 2024},
                    {"id": "MAT1", "nota": 7.0, "ano": 2024},
                    {"id": "BIO1", "nota": 8.0, "ano": 2024},
                    {"id": "HIST1", "nota": 7.5, "ano": 2024},
                    {"id": "GEO1", "nota": 8.0, "ano": 2024},
                    {"id": "FIL1", "nota": 7.8, "ano": 2024},
                    {"id": "SOC1", "nota": 8.2, "ano": 2024},
                    {"id": "DOC_TEC", "nota": 7.5, "ano": 2024},
                    {"id": "HARDWARE", "nota": 8.5, "ano": 2024},
                    {"id": "REDES", "nota": 7.8, "ano": 2024},
                    {"id": "SO", "nota": 8.0, "ano": 2024},
                ],
                "reprovadas": [
                    {"id": "FIS1", "nota": 4.5, "ano": 2024},
                    {"id": "QUI1", "nota": 5.0, "ano": 2024},
                    {"id": "LOGICA", "nota": 4.0, "ano": 2024},
                ]
            }
        },
        # ALUNO 3: Veterana 2º ano
        {
            "id": "2023001",
            "nome": "Ana Carolina Mendes",
            "ano": 2,
            "tipo": "veterano",
            "historico": {
                "aprovadas": [
                    # 1º Ano completo
                    {"id": "PORT1", "nota": 8.5, "ano": 2023},
                    {"id": "ART1", "nota": 9.0, "ano": 2023},
                    {"id": "EDF1", "nota": 8.0, "ano": 2023},
                    {"id": "MAT1", "nota": 7.5, "ano": 2023},
                    {"id": "FIS1", "nota": 7.8, "ano": 2023},
                    {"id": "QUI1", "nota": 8.2, "ano": 2023},
                    {"id": "BIO1", "nota": 8.5, "ano": 2023},
                    {"id": "HIST1", "nota": 9.0, "ano": 2023},
                    {"id": "GEO1", "nota": 8.3, "ano": 2023},
                    {"id": "FIL1", "nota": 8.8, "ano": 2023},
                    {"id": "SOC1", "nota": 9.2, "ano": 2023},
                    {"id": "DOC_TEC", "nota": 8.0, "ano": 2023},
                    {"id": "LOGICA", "nota": 9.5, "ano": 2023},
                    {"id": "HARDWARE", "nota": 8.5, "ano": 2023},
                    {"id": "REDES", "nota": 8.8, "ano": 2023},
                    {"id": "SO", "nota": 9.0, "ano": 2023},
                    # 2º Ano parcial
                    {"id": "PORT2", "nota": 8.0, "ano": 2024},
                    {"id": "ING2", "nota": 7.5, "ano": 2024},
                    {"id": "MAT2", "nota": 7.8, "ano": 2024},
                    {"id": "POO", "nota": 9.0, "ano": 2024},
                    {"id": "BD", "nota": 8.5, "ano": 2024},
                    {"id": "ANALISE", "nota": 8.0, "ano": 2024},
                    {"id": "IHC", "nota": 8.5, "ano": 2024},
                ],
                "reprovadas": []
            }
        },
        # ALUNO 4: Crítico (6 reprovações)
        {
            "id": "2024003",
            "nome": "Carlos Eduardo Costa",
            "ano": 1,
            "tipo": "veterano",
            "historico": {
                "aprovadas": [
                    {"id": "PORT1", "nota": 7.0, "ano": 2024},
                    {"id": "ART1", "nota": 7.5, "ano": 2024},
                    {"id": "EDF1", "nota": 8.0, "ano": 2024},
                    {"id": "BIO1", "nota": 6.5, "ano": 2024},
                    {"id": "HIST1", "nota": 7.0, "ano": 2024},
                    {"id": "GEO1", "nota": 6.8, "ano": 2024},
                    {"id": "FIL1", "nota": 7.2, "ano": 2024},
                    {"id": "SOC1", "nota": 7.5, "ano": 2024},
                    {"id": "DOC_TEC", "nota": 6.5, "ano": 2024},
                    {"id": "HARDWARE", "nota": 7.0, "ano": 2024},
                ],
                "reprovadas": [
                    {"id": "MAT1", "nota": 3.5, "ano": 2024},
                    {"id": "FIS1", "nota": 4.0, "ano": 2024},
                    {"id": "QUI1", "nota": 3.8, "ano": 2024},
                    {"id": "LOGICA", "nota": 4.5, "ano": 2024},
                    {"id": "REDES", "nota": 4.2, "ano": 2024},
                    {"id": "SO", "nota": 3.9, "ano": 2024},
                ]
            }
        },
        # ALUNO 5: Forte em Exatas
        {
            "id": "2024004",
            "nome": "Lucas Fernandes Lima",
            "ano": 1,
            "tipo": "veterano",
            "historico": {
                "aprovadas": [
                    {"id": "MAT1", "nota": 10.0, "ano": 2024},
                    {"id": "FIS1", "nota": 9.5, "ano": 2024},
                    {"id": "QUI1", "nota": 9.0, "ano": 2024},
                    {"id": "LOGICA", "nota": 10.0, "ano": 2024},
                    {"id": "HARDWARE", "nota": 9.5, "ano": 2024},
                    {"id": "REDES", "nota": 9.8, "ano": 2024},
                    {"id": "SO", "nota": 9.2, "ano": 2024},
                    {"id": "PORT1", "nota": 6.5, "ano": 2024},
                    {"id": "HIST1", "nota": 6.0, "ano": 2024},
                    {"id": "GEO1", "nota": 6.5, "ano": 2024},
                    {"id": "FIL1", "nota": 6.8, "ano": 2024},
                    {"id": "SOC1", "nota": 6.2, "ano": 2024},
                    {"id": "ART1", "nota": 7.0, "ano": 2024},
                    {"id": "EDF1", "nota": 8.0, "ano": 2024},
                    {"id": "BIO1", "nota": 7.5, "ano": 2024},
                    {"id": "DOC_TEC", "nota": 8.5, "ano": 2024},
                ],
                "reprovadas": []
            }
        },
        # ALUNO 6: Veterana 3º ano
        {
            "id": "2022001",
            "nome": "Beatriz Almeida Rocha",
            "ano": 3,
            "tipo": "veterano",
            "historico": {
                "aprovadas": [
                    # 1º Ano
                    {"id": "PORT1", "nota": 8.5, "ano": 2022},
                    {"id": "ART1", "nota": 8.0, "ano": 2022},
                    {"id": "EDF1", "nota": 8.5, "ano": 2022},
                    {"id": "MAT1", "nota": 8.8, "ano": 2022},
                    {"id": "FIS1", "nota": 8.2, "ano": 2022},
                    {"id": "QUI1", "nota": 8.0, "ano": 2022},
                    {"id": "BIO1", "nota": 8.5, "ano": 2022},
                    {"id": "HIST1", "nota": 9.0, "ano": 2022},
                    {"id": "GEO1", "nota": 8.7, "ano": 2022},
                    {"id": "FIL1", "nota": 9.2, "ano": 2022},
                    {"id": "SOC1", "nota": 9.0, "ano": 2022},
                    {"id": "DOC_TEC", "nota": 8.5, "ano": 2022},
                    {"id": "LOGICA", "nota": 9.0, "ano": 2022},
                    {"id": "HARDWARE", "nota": 8.5, "ano": 2022},
                    {"id": "REDES", "nota": 8.8, "ano": 2022},
                    {"id": "SO", "nota": 8.7, "ano": 2022},
                    # 2º Ano
                    {"id": "PORT2", "nota": 8.5, "ano": 2023},
                    {"id": "ING2", "nota": 8.0, "ano": 2023},
                    {"id": "EDF2", "nota": 8.5, "ano": 2023},
                    {"id": "MAT2", "nota": 8.8, "ano": 2023},
                    {"id": "FIS2", "nota": 8.5, "ano": 2023},
                    {"id": "QUI2", "nota": 8.2, "ano": 2023},
                    {"id": "BIO2", "nota": 8.7, "ano": 2023},
                    {"id": "HIST2", "nota": 9.0, "ano": 2023},
                    {"id": "GEO2", "nota": 8.8, "ano": 2023},
                    {"id": "FIL2", "nota": 9.0, "ano": 2023},
                    {"id": "SOC2", "nota": 8.9, "ano": 2023},
                    {"id": "PI1", "nota": 9.5, "ano": 2023},
                    {"id": "BD", "nota": 9.0, "ano": 2023},
                    {"id": "ANALISE", "nota": 8.5, "ano": 2023},
                    {"id": "POO", "nota": 9.5, "ano": 2023},
                    {"id": "IHC", "nota": 8.8, "ano": 2023},
                    # 3º Ano
                    {"id": "PORT3", "nota": 8.5, "ano": 2024},
                    {"id": "MAT3", "nota": 8.0, "ano": 2024},
                    {"id": "MEIO_AMB", "nota": 9.0, "ano": 2024},
                    {"id": "EMPREEND", "nota": 9.5, "ano": 2024},
                ],
                "reprovadas": []
            }
        }
    ]

    # Criar cada usuário
    contador = 0
    for usuario in usuarios:
        try:
            print(f"[{contador+1}/6] Criando: {usuario['nome']} ({usuario['id']})")

            # Criar aluno
            AlunoRepository.criar_ou_atualizar(
                aluno_id=usuario['id'],
                nome=usuario['nome'],
                ano=usuario['ano'],
                tipo=usuario['tipo']
            )

            # Limpar histórico anterior
            HistoricoRepository.limpar_historico(usuario['id'])

            # Registrar aprovações
            for disc in usuario['historico']['aprovadas']:
                HistoricoRepository.registrar_disciplina(
                    aluno_id=usuario['id'],
                    disciplina_id=disc['id'],
                    status='aprovado',
                    nota=disc['nota'],
                    ano_cursado=disc['ano']
                )

            # Registrar reprovações
            for disc in usuario['historico']['reprovadas']:
                HistoricoRepository.registrar_disciplina(
                    aluno_id=usuario['id'],
                    disciplina_id=disc['id'],
                    status='reprovado',
                    nota=disc['nota'],
                    ano_cursado=disc['ano']
                )

            print(f"  ✓ {len(usuario['historico']['aprovadas'])} aprovações")
            print(f"  ✓ {len(usuario['historico']['reprovadas'])} reprovações")
            contador += 1

        except Exception as e:
            print(f"  ✗ ERRO: {e}")
            continue

    print()
    print("=" * 80)
    print(f"✓ {contador}/6 USUÁRIOS CRIADOS COM SUCESSO!")
    print("=" * 80)
    print()

    # Verificar se foram salvos
    print("Verificando no banco...")
    try:
        alunos = AlunoRepository.listar_todos()
        print(f"✓ Total de alunos no banco: {len(alunos)}")
        for aluno in alunos:
            print(f"  • {aluno['id']}: {aluno['nome']}")
    except Exception as e:
        print(f"✗ ERRO ao verificar: {e}")

    print()
    print("TABELA DE USUÁRIOS:")
    print("┌─────────┬──────────────────────────┬──────┬─────────────────────────┐")
    print("│ MATRÍC. │ NOME                     │ ANO  │ PERFIL                  │")
    print("├─────────┼──────────────────────────┼──────┼─────────────────────────┤")
    print("│ 2024001 │ Maria Silva Santos       │ 2º   │ Excelente (tudo 1º ano) │")
    print("│ 2024002 │ João Pedro Oliveira      │ 1º   │ 3 reprovações (LOGICA)  │")
    print("│ 2023001 │ Ana Carolina Mendes      │ 2º   │ POO/BD aprovadas        │")
    print("│ 2024003 │ Carlos Eduardo Costa     │ 1º   │ Crítico (6 reprovações) │")
    print("│ 2024004 │ Lucas Fernandes Lima     │ 1º   │ Forte em Exatas         │")
    print("│ 2022001 │ Beatriz Almeida Rocha    │ 3º   │ Veterana avançada       │")
    print("└─────────┴──────────────────────────┴──────┴─────────────────────────┘")
    print()
    print("COMO TESTAR:")
    print("  1. python main.py")
    print("  2. Abra: http://localhost:5000")
    print("  3. Digite matrícula: 2024001")
    print("  4. Pressione Enter")
    print("  5. Sistema preenche automaticamente!")
    print()


if __name__ == "__main__":
    criar_usuarios_teste()