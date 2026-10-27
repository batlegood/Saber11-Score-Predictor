import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score


df = pd.read_csv("dataset/saber11_100k.csv")

print(df.dtypes)

df = df.dropna()


encoders = {}


for columna in df.select_dtypes(include=["object"]).columns:

    le = LabelEncoder()

    df[columna] = le.fit_transform(
        df[columna].astype(str)
    )

    encoders[columna] = le


y = df["PUNT_GLOBAL"]


X = df.drop(columns=["PUNT_GLOBAL"])


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


modelo = RandomForestRegressor(
    n_estimators=25,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("Entrenando modelo...")

modelo.fit(X_train, y_train)

pred = modelo.predict(X_test)

r2 = r2_score(y_test, pred)

print(f"R2: {r2:.4f}")


os.makedirs("modelo", exist_ok=True)

joblib.dump(
    modelo,
    "modelo/modelo.pkl"
)

joblib.dump(
    encoders,
    "modelo/encoders.pkl"
)

print("Modelo guardado correctamente")