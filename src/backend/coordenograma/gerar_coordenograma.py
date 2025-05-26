"""
Geração de Coordenograma Dinâmico PETRO_ProtecAI

Este módulo lê uma base técnica de ativos e eventos elétricos,
e gera uma visualização interativa do coordenograma técnico
em formato SVG usando Plotly.

Autor: PETRO_ProtecAI Team
"""

from common.utils import carregar_base_coordenograma
import plotly.express as px
import plotly.express as px
from pathlib import Path


def gerar_coordenograma(caminho_csv: str, caminho_saida: str) -> None:
    """
    Gera coordenograma SVG a partir de uma base CSV.

    Args:
        caminho_csv (str): Caminho do arquivo .csv com os dados de entrada
        caminho_saida (str): Caminho do arquivo de saída .svg
    """
    df = carregar_base_coordenograma(caminho_csv)
    df["Início Previsto"] = pd.to_datetime(df["Início Previsto"], format="%H:%M")
    df["Término"] = df["Início Previsto"] + pd.to_timedelta(df["Duração"] + ":00")

    fig = px.timeline(
        df,
        x_start="Início Previsto",
        x_end="Término",
        y="Ativo",
        color="Ação",
        hover_data=["Dependência / Intertravamento", "Observações"],
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(title="Coordenograma Dinâmico – PETRO_ProtecAI")

    fig.write_image(caminho_saida)