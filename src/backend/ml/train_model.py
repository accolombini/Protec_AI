"""
train_model.py

Este script treina um modelo de regressão para prever a duração de testes técnicos
a partir de uma base de dados realista de coordenogramas. O modelo treinado é salvo
em formato .pkl para uso posterior na API.

"""

# src/backend/ml/train_model.py

import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error


class ModelTrainer:
    """Classe responsável por treinar e avaliar um modelo de regressão."""

    def __init__(self, data_path: str, model_output: str = "src/backend/ml/model.pkl"):
        """
        Inicializa a classe ModelTrainer.

        Args:
            data_path (str): Caminho para o arquivo CSV de entrada.
            model_output (str): Caminho onde o modelo treinado será salvo.
        """
        self.data_path = data_path
        self.model_output = Path(model_output)
        self.model = None
        self.mae = None
        self.X_train = self.X_test = self.y_train = self.y_test = None

        self.cat_features = [
            "Ativo", "Tipo_Ativo", "Ação", "Resultado",
            "Ambiente", "Executor", "Tipo_Falha", "Sprint", "Simulado"
        ]
        self.num_features = [
            "Tensão_kV", "Carga_kVA", "Corrente_A", "Temperatura_C",
            "Delta_Temp", "Tentativas"
        ]

    def load_data(self) -> pd.DataFrame:
        """Carrega os dados a partir do CSV informado."""
        return pd.read_csv(self.data_path)

    def prepare_pipeline(self) -> Pipeline:
        """Cria o pipeline de pré-processamento e modelo."""
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), self.cat_features)
            ],
            remainder="passthrough"
        )
        return Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(random_state=42))
        ])

    def train(self) -> None:
        """Executa o treinamento do modelo e armazena métricas internas."""
        df = self.load_data()

        X = df[self.cat_features + self.num_features]
        y = df["Criticidade"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        pipeline = self.prepare_pipeline()
        pipeline.fit(self.X_train, self.y_train)

        self.model = pipeline
        y_pred = pipeline.predict(self.X_test)
        self.mae = mean_absolute_error(self.y_test, y_pred)

    def save_model(self) -> None:
        """Salva o modelo treinado no caminho especificado."""
        if self.model:
            joblib.dump(self.model, self.model_output)
        else:
            raise RuntimeError(
                "Modelo não treinado. Execute train() antes de salvar.")

    def report(self) -> None:
        """Exibe resumo da execução."""
        print("Resumo do Treinamento:")
        print(f"modelo_salvo_em: {self.model_output}")
        print(f"MAE: {self.mae:.2f}")
        print(f"registros_treino: {len(self.X_train)}")
        print(f"registros_teste: {len(self.X_test)}")
        print(f"features_categoricas: {self.cat_features}")
        print(f"features_numericas: {self.num_features}")


if __name__ == "__main__":
    trainer = ModelTrainer("src/backend/ml/dataset.csv")
    trainer.train()
    trainer.save_model()
    trainer.report()
