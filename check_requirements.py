"""
Script para verificar integridade de ambiente virtual Python.

- Verifica se o ambiente virtual está ativo.
- Lê o arquivo requirements.txt.
- Confirma se os pacotes estão instalados corretamente.
- Testa conflitos de dependências via pip check.
"""

import os
import sys
import importlib.util
import subprocess

REQUIREMENTS_FILE = 'requirements.txt'


def check_virtualenv():
    """
    Verifica se o ambiente virtual está ativo.
    Encerra o programa caso não esteja.
    """
    print("📍 Verificando ambiente virtual...")
    if 'VIRTUAL_ENV' not in os.environ:
        print("❌ Ambiente virtual NÃO está ativo.")
        sys.exit(1)
    print(f"✅ Ambiente virtual ativo: {os.environ['VIRTUAL_ENV']}")


def parse_requirements(file_path):
    """
    Lê os pacotes listados no arquivo requirements.txt.

    Args:
        file_path (str): Caminho para o arquivo requirements.txt.

    Returns:
        list: Lista de nomes de pacotes.
    """
    print(f"\n📄 Lendo '{file_path}'...")
    if not os.path.exists(file_path):
        print(f"❌ Arquivo '{file_path}' não encontrado.")
        sys.exit(1)

    packages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                packages.append(pkg)

    return packages


def check_packages(packages):
    """
    Verifica se os pacotes especificados estão instalados corretamente.

    Args:
        packages (list): Lista de pacotes extraídos do requirements.txt.

    Returns:
        list: Lista de pacotes que estão ausentes ou com falha de importação.
    """
    print("\n🔍 Verificando pacotes instalados...")

    # Dicionário de correção de nomes: pip → módulo importável
    pip_to_module = {
        "python-dateutil": "dateutil",
        "scikit-learn": "sklearn",
        # Adicione mais mapeamentos se necessário
    }

    missing = []
    for pkg in packages:
        module_name = pip_to_module.get(pkg, pkg)
        if importlib.util.find_spec(module_name) is None:
            print(
                f"❌ {pkg} não está instalado ou falha ao localizar o módulo '{module_name}'.")
            missing.append(pkg)
        else:
            print(f"✅ {pkg} instalado corretamente.")
    return missing


def check_dependency_conflicts():
    """
    Executa o comando 'pip check' para detectar conflitos de dependência entre pacotes.
    """
    print("\n🔍 Verificando conflitos de dependência com 'pip check'...")
    try:
        result = subprocess.run(
            ["pip", "check"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Nenhum conflito de dependência encontrado.")
        else:
            print("❌ Conflitos de dependência encontrados:")
            print(result.stdout.strip())
    except Exception as e:
        print(f"⚠️ Erro ao executar 'pip check': {e}")


def main():
    """
    Função principal do script.
    Orquestra a verificação do ambiente, pacotes e conflitos.
    """
    print("🔧 Teste de integridade do ambiente virtual iniciado.\n")
    check_virtualenv()
    packages = parse_requirements(REQUIREMENTS_FILE)
    missing = check_packages(packages)
    check_dependency_conflicts()

    if missing:
        print("\n⚠️ Pacotes ausentes ou com erro:")
        for pkg in missing:
            print(f"- {pkg}")
        print("\n💡 Solução sugerida:")
        print(f"pip install -r {REQUIREMENTS_FILE}")
    else:
        print("\n✅ Todos os pacotes do requirements.txt estão instalados e funcionando!\n")


if __name__ == "__main__":
    main()
