"""
Testes para o pipeline de coordenograma.

Este módulo valida o funcionamento correto da função gerar_coordenograma.

Cobertura:
- Execução sem erro com dados válidos.

   ||> Importante:
            Os linters e formatadores (como o Black) não reordenam sys.path.insert(...) se ele estiver abaixo dos imports padrão (pytest, pandas, sys, pathlib).
            Ao evitar o uso de # fmt: off, você garante compatibilidade com o formatador do VSCode mesmo que ele esteja ativado automaticamente.
            A importação de gerar_coordenograma funciona corretamente porque ROOT está inserido em tempo de execução antes do import.
"""

"""
Testes para o pipeline de coordenograma.

Cobertura dos testes:
- Execução correta com dados válidos.
- Erros inesperados são tratados.
"""

import pandas as pd
import pytest
from pathlib import Path
from src.backend.coordenograma.gerar_coordenograma import gerar_coordenograma


@pytest.fixture
def dados_simulados(tmp_path: Path) -> Path:
    """
    Cria um CSV simulado com todas as colunas esperadas e formatos compatíveis com o carregamento.
    """
    df = pd.DataFrame({
        "ID": [1],
        "Ativo": ["Transformador"],
        "Tipo_Ativo": ["Elétrico"],
        "Ação": ["Inspeção"],
        "Tensão_kV": [13.8],
        "Carga_kVA": [500],
        "Corrente_A": [20],
        "Temperatura_C": [35],
        "Delta_Temp": [5],
        "Tentativas": [1],
        "Duracao_Min": [60],
        "Resultado": ["Ok"],
        "Ambiente": ["Subterrâneo"],
        "Executor": ["Equipe A"],
        "Tipo_Falha": ["Nenhuma"],
        "Sprint": ["Sprint 1"],
        "Simulado": ["Simulado 1"],
        "Início Previsto": ["08:00"],        # <-- Formato correto: "%H:%M"
        "Término Previsto": ["09:00"],       # <-- Formato correto: "%H:%M"
        "Duração": ["1:00"],
        "Término": ["09:00"],
        "Dependência / Intertravamento": ["-"],
        "Observações": ["Teste completo"]
    })

    caminho_csv = tmp_path / "simulado.csv"
    df.to_csv(caminho_csv, index=False)
    return caminho_csv

def test_gerar_coordenograma_com_dados_validos(dados_simulados: Path) -> None:
    """
    Testa se a função gerar_coordenograma executa corretamente com dados válidos.
    """
    # caminho_saida = Path("outputs/coordenograma/test_output.html")
    caminho_saida = Path("outputs/coordenograma/test_output.png")
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    try:
        gerar_coordenograma(dados_simulados, caminho_saida)
    except Exception as e:
        pytest.fail(f"Erro inesperado ao gerar coordenograma: {e}")
