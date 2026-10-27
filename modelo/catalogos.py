import pandas as pd

df = pd.read_csv("dataset/saber11_100k.csv")


def obtener_catalogos():

    municipios_por_departamento = {}

    for depto in sorted(
        df["ESTU_DEPTO_RESIDE"].dropna().unique()
    ):

        municipios = sorted(

            df[
                df["ESTU_DEPTO_RESIDE"] == depto
            ]["ESTU_MCPIO_RESIDE"]
            .dropna()
            .unique()

        )

        municipios_por_departamento[depto] = municipios

    return {

        "departamentos":
        sorted(df["ESTU_DEPTO_RESIDE"].dropna().unique()),

        "municipios_por_departamento":
        municipios_por_departamento,

        "educacion_madre":
        sorted(df["FAMI_EDUCACIONMADRE"].dropna().unique()),

        "educacion_padre":
        sorted(df["FAMI_EDUCACIONPADRE"].dropna().unique()),

        "naturaleza":
        sorted(df["COLE_NATURALEZA"].dropna().unique()),

        "caracter":
        sorted(df["COLE_CARACTER"].dropna().unique()),

        "area":
        sorted(df["COLE_AREA_UBICACION"].dropna().unique()),

        "bilingue":
        sorted(df["COLE_BILINGUE"].dropna().unique()),

        "calendario":
        sorted(df["COLE_CALENDARIO"].dropna().unique())

    }