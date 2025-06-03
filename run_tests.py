#!/usr/bin/env python3
"""
run_tests.py

Executa todos os testes automatizados do projeto PETRO_ProtecAI utilizando o framework pytest.

Este script percorre o diretório `tests/` e executa os testes localizados em subpastas como:
- tests/coordenograma/
- tests/ml/

Requisitos:
- pytest instalado no ambiente virtual
- Estrutura de diretórios conforme especificado no projeto

Uso:
$ python run_tests.py
"""

import subprocess
import sys
from pathlib import Path


def run_all_tests():
    try:
        project_root = Path(__file__).resolve().parent
        tests_dir = project_root / "tests"

        if not tests_dir.exists():
            print("❌ Diretório 'tests/' não encontrado.")
            sys.exit(1)

        print("🚀 Executando testes com pytest...\n")
        result = subprocess.run(
            ["pytest", str(tests_dir)], capture_output=False)
        sys.exit(result.returncode)

    except Exception as e:
        print(f"❌ Erro durante execução dos testes: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
