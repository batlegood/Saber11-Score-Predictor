import pandas as pd
import joblib

modelo_rf = joblib.load("modelo/modelo_rf.pkl")
modelo_lr = joblib.load("modelo/modelo_lr.pkl")

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

                nuevo[columna] = (
                    encoders[columna]
                    .transform(nuevo[columna])
                )

            except:

                nuevo[columna] = 0

    score_rf = modelo_rf.predict(nuevo)[0]

    score_lr = modelo_lr.predict(nuevo)[0]

    level_rf = clasificar_nivel(score_rf)

    level_lr = clasificar_nivel(score_lr)

    diferencia = abs(
        round(score_rf) - round(score_lr)
    )

    return {

        "score_rf": round(score_rf),

        "level_rf": level_rf,

        "score_lr": round(score_lr),

        "level_lr": level_lr,

        "difference": diferencia

    }