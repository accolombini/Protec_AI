'''
Testes para o pipeline de coordenograma.
Este módulo contém testes para garantir que o pipeline de coordenograma funcione corretamente.
'''

from backend.common.utils import carregar_base_coordenograma, validar_colunas_essenciais
import pandas as pd
from pathlib import Path
import sys
src_path = Path(__file__).resolve().parents[2] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_base_exists():
    path = Path("data/coordenograma/coordenograma_base.csv")
    assert path.exists(), "Base CSV não encontrada."


def test_base_columns():
    df = pd.read_csv("data/coordenograma/coordenograma_base.csv")
    expected_columns = [
        "Ativo", "Ação", "Início Previsto", "Duração",
        "Dependência / Intertravamento", "Observações"
    ]
    assert all(
        col in df.columns for col in expected_columns), "Colunas obrigatórias ausentes."


def test_carregar_base_coordenograma():
    df = carregar_base_coordenograma(
        "data/coordenograma/coordenograma_base.csv")
    assert "Término" in df.columns, "Coluna 'Término' não foi gerada corretamente."
    assert pd.api.types.is_datetime64_any_dtype(
        df["Início Previsto"]), "Coluna 'Início Previsto' não está em datetime."


def test_validar_colunas_essenciais():
    df = pd.read_csv("data/coordenograma/coordenograma_base.csv")
    colunas = ["Ativo", "Ação", "Início Previsto", "Duração"]
    assert validar_colunas_essenciais(
        df, colunas), "Validação de colunas essenciais falhou."
