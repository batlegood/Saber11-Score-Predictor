import pandas as pd
import joblib

df = pd.read_csv("dataset/saber11_100k.csv")


def promedio_por_estrato():

    datos = (
        df.groupby("FAMI_ESTRATOVIVIENDA")["PUNT_GLOBAL"]
        .mean()
        .round(2)
    )

    return {
        "labels": [str(x) for x in datos.index],
        "values": [float(x) for x in datos.values]
    }


def promedio_por_naturaleza():

    datos = (
        df.groupby("COLE_NATURALEZA")["PUNT_GLOBAL"]
        .mean()
        .round(2)
    )

    return {
        "labels": [str(x) for x in datos.index],
        "values": [float(x) for x in datos.values]
    }


def promedio_por_area():

    datos = (
        df.groupby("COLE_AREA_UBICACION")["PUNT_GLOBAL"]
        .mean()
        .round(2)
    )

    return {
        "labels": [str(x) for x in datos.index],
        "values": [float(x) for x in datos.values]
    }


def obtener_metricas():

    return joblib.load(
        "modelo/metricas.pkl"
    )

def mejor_icfes():

    return int(
        df["PUNT_GLOBAL"].max()
    )



    