'''
    ||> Testes para o modelo treinado
         "features_numericas": numerical
         "MAE": round(mae, 2)
         "registros_treino": len(X_train),
         "registros_teste": len(X_test)
         "modelo_salvo_em": salvar_em
         "features_categoricas": categorical  

    ||> Objetivo
        Garantir que o train_model.py esteja:
        Totalmente testado em nível de unidade
        Modular, reutilizável e confiável
        Com cobertura mínima sobre:
        Carga de dados
        Treinamento
        Persistência do modelo
        Métricas
'''

# tests/test_train_model.py

import os
import joblib
import pytest
import pandas as pd
from pathlib import Path
from src.backend.ml.train_model import ModelTrainer

# Caminho de teste isolado
TEST_DATA_PATH = "tests/test_data.csv"
MODEL_OUTPUT_PATH = "tests/model_test.pkl"


@pytest.fixture(scope="module")
def dummy_dataset():
    """Cria um dataset pequeno e fictício para testes."""
    df = pd.DataFrame({
        "Ativo": ["T1", "T2"],
        "Tipo_Ativo": ["Transformador", "Chave"],
        "Ação": ["Inspeção", "Reparo"],
        "Resultado": ["OK", "Falha"],
        "Ambiente": ["Subterrâneo", "Aéreo"],
        "Executor": ["Técnico A", "Técnico B"],
        "Tipo_Falha": ["Elétrica", "Mecânica"],
        "Sprint": ["S1", "S2"],
        "Simulado": ["Sim", "Não"],
        "Tensão_kV": [13.8, 11.4],
        "Carga_kVA": [200, 150],
        "Corrente_A": [100, 85],
        "Temperatura_C": [45, 42],
        "Delta_Temp": [5, 3],
        "Tentativas": [1, 2],
        "Criticidade": [7.2, 4.9],
    })
    df.to_csv(TEST_DATA_PATH, index=False)
    yield df
    os.remove(TEST_DATA_PATH)
    if Path(MODEL_OUTPUT_PATH).exists():
        os.remove(MODEL_OUTPUT_PATH)


def test_model_training_pipeline(dummy_dataset):
    """Testa o pipeline completo de treinamento e salvamento do modelo."""
    trainer = ModelTrainer(data_path=TEST_DATA_PATH,
                           model_output=MODEL_OUTPUT_PATH)

    trainer.train()

    # Verificações
    assert trainer.model is not None
    assert trainer.mae >= 0
    assert len(trainer.X_train) > 0
    assert len(trainer.X_test) > 0

    trainer.save_model()
    assert Path(MODEL_OUTPUT_PATH).exists()

    # Testa carregamento do modelo salvo
    loaded_model = joblib.load(MODEL_OUTPUT_PATH)
    preds = loaded_model.predict(trainer.X_test)
    assert len(preds) == len(trainer.X_test)
