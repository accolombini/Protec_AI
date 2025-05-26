"""
Funções utilitárias para o projeto PETRO_ProtecAI.
"""

import pandas as pd
from datetime import timedelta


def carregar_base_coordenograma(caminho_csv: str) -> pd.DataFrame:
    """
    Lê a base de coordenograma e converte colunas de tempo.

    Args:
        caminho_csv (str): Caminho do arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame com colunas convertidas.
    """
    df = pd.read_csv(caminho_csv)
    df["Início Previsto"] = pd.to_datetime(
        df["Início Previsto"], format="%H:%M")
    df["Término"] = df["Início Previsto"] + \
        pd.to_timedelta(df["Duração"] + ":00")
    return df


def validar_colunas_essenciais(df: pd.DataFrame, colunas: list) -> bool:
    """
    Verifica se todas as colunas essenciais estão presentes no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        colunas (list): Lista de colunas obrigatórias.

    Returns:
        bool: True se todas as colunas existem, False caso contrário.
    """
    return all(col in df.columns for col in colunas)
