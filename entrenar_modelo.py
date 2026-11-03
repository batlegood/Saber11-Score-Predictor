import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

df = pd.read_csv("dataset/saber11_100k.csv")

print("Loading dataset...")
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

print("\n==============================")
print("TRAINING RANDOM FOREST")
print("==============================")

modelo_rf = RandomForestRegressor(
    n_estimators=25,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

modelo_rf.fit(X_train, y_train)

pred_rf = modelo_rf.predict(X_test)

r2_rf = r2_score(y_test, pred_rf)

mae_rf = mean_absolute_error(
    y_test,
    pred_rf
)

rmse_rf = mean_squared_error(
    y_test,
    pred_rf
) ** 0.5

print(f"R²   : {r2_rf:.4f}")
print(f"MAE  : {mae_rf:.2f}")
print(f"RMSE : {rmse_rf:.2f}")

print("\n==============================")
print("TRAINING LINEAR REGRESSION")
print("==============================")

modelo_lr = LinearRegression()

modelo_lr.fit(X_train, y_train)

pred_lr = modelo_lr.predict(X_test)

r2_lr = r2_score(y_test, pred_lr)

mae_lr = mean_absolute_error(
    y_test,
    pred_lr
)

rmse_lr = mean_squared_error(
    y_test,
    pred_lr
) ** 0.5

print(f"R²   : {r2_lr:.4f}")
print(f"MAE  : {mae_lr:.2f}")
print(f"RMSE : {rmse_lr:.2f}")

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

print("\nRandom Forest")

print(f"R²   : {r2_rf:.4f}")
print(f"MAE  : {mae_rf:.2f}")
print(f"RMSE : {rmse_rf:.2f}")

print("\nLinear Regression")

print(f"R²   : {r2_lr:.4f}")
print(f"MAE  : {mae_lr:.2f}")
print(f"RMSE : {rmse_lr:.2f}")

os.makedirs("modelo", exist_ok=True)

joblib.dump(
    modelo_rf,
    "modelo/modelo_rf.pkl"
)

joblib.dump(
    modelo_lr,
    "modelo/modelo_lr.pkl"
)

joblib.dump(
    encoders,
    "modelo/encoders.pkl"
)

metricas = {
    "random_forest": {
        "r2": float(r2_rf),
        "mae": float(mae_rf),
        "rmse": float(rmse_rf)
    },
    "linear_regression": {
        "r2": float(r2_lr),
        "mae": float(mae_lr),
        "rmse": float(rmse_lr)
    }
}

joblib.dump(
    metricas,
    "modelo/metricas.pkl"
)

print("\nModels saved successfully!")

print("modelo_rf.pkl")
print("modelo_lr.pkl")
print("encoders.pkl")
print("metricas.pkl")