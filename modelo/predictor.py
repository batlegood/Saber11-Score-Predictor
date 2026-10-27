import pandas as pd
import joblib

modelo = joblib.load("modelo/modelo.pkl")
encoders = joblib.load("modelo/encoders.pkl")


def clasificar_nivel(score):

    if score < 200:
        return "Very Low"

    elif score < 300:
        return "Low"

    elif score < 350:
        return "Medium"

    elif score < 400:
        return "High"

    return "Excellent"


def predecir(datos):

    nuevo = pd.DataFrame([datos])

    for columna in nuevo.columns:

        if columna in encoders:

            try:
                nuevo[columna] = encoders[columna].transform(
                    nuevo[columna]
                )

            except:
                nuevo[columna] = 0

    score = modelo.predict(nuevo)[0]

    return {
        "score": round(score),
        "level": clasificar_nivel(score)
    }