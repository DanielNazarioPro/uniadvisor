#!/usr/bin/env python3
"""
UniAdvisor - Sistema Baseado em Conhecimento para Orientação Acadêmica
IFAM - Instituto Federal do Amazonas

Ponto de entrada principal da aplicação.
"""
import sys
from pathlib import Path

# Garantir que os módulos estão no path
sys.path.insert(0, str(Path(__file__).parent))

from interface.app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🎓 UniAdvisor - Sistema Especialista de Matrícula")
    print("   Sistema Baseado em Conhecimento com Forward Chaining")
    print("=" * 60)
    print("\n✅ Iniciando servidor...")
    print("📍 Acesse: http://localhost:5000")
    print("\nPressione Ctrl+C para encerrar\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
