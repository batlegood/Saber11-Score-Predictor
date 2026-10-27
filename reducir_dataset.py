import pandas as pd

archivo = "Resultados_únicos_Saber_11_20261025.csv"

columnas = [
    "PUNT_GLOBAL",
    "ESTU_GENERO",
    "ESTU_DEPTO_RESIDE",
    "ESTU_MCPIO_RESIDE",
    "FAMI_ESTRATOVIVIENDA",
    "FAMI_PERSONASHOGAR",
    "FAMI_TIENEINTERNET",
    "FAMI_TIENECOMPUTADOR",
    "FAMI_TIENEAUTOMOVIL",
    "FAMI_EDUCACIONMADRE",
    "FAMI_EDUCACIONPADRE",
    "COLE_NATURALEZA",
    "COLE_AREA_UBICACION",
    "COLE_CARACTER",
    "COLE_BILINGUE",
    "COLE_CALENDARIO"
]


print("Leyendo dataset...")

df = pd.read_csv(
    archivo,
    usecols=columnas,
    low_memory=False
)

print("Registros encontrados:", len(df))

muestra = df.sample(
    n=100000,
    random_state=42
)

muestra.to_csv(
    "dataset/saber11_100k.csv",
    index=False
)

print("Archivo generado correctamente")