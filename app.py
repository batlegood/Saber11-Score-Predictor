from flask import Flask, render_template, request

from modelo.predictor import predecir
from modelo.catalogos import obtener_catalogos

from modelo.analisis import (
    promedio_por_estrato,
    promedio_por_naturaleza,
    promedio_por_area
)




app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/conceptos")
def conceptos():
    return render_template("conceptos.html")

@app.route("/prediccion", methods=["GET", "POST"])
def prediccion():

    catalogos = obtener_catalogos()

    resultado = None

    if request.method == "POST":

        datos = {

            "COLE_AREA_UBICACION":
            request.form["COLE_AREA_UBICACION"],

            "COLE_BILINGUE":
            request.form["COLE_BILINGUE"],

            "COLE_CALENDARIO":
            request.form["COLE_CALENDARIO"],

            "COLE_CARACTER":
            request.form["COLE_CARACTER"],

            "COLE_NATURALEZA":
            request.form["COLE_NATURALEZA"],

            "ESTU_DEPTO_RESIDE":
            request.form["ESTU_DEPTO_RESIDE"],

            "ESTU_GENERO":
            request.form["ESTU_GENERO"],

            "ESTU_MCPIO_RESIDE":
            request.form["ESTU_MCPIO_RESIDE"],

            "FAMI_EDUCACIONMADRE":
            request.form["FAMI_EDUCACIONMADRE"],

            "FAMI_EDUCACIONPADRE":
            request.form["FAMI_EDUCACIONPADRE"],

            "FAMI_ESTRATOVIVIENDA":
            request.form["FAMI_ESTRATOVIVIENDA"],

            "FAMI_PERSONASHOGAR":
            int(request.form["FAMI_PERSONASHOGAR"]),

            "FAMI_TIENEAUTOMOVIL":
            request.form["FAMI_TIENEAUTOMOVIL"],

            "FAMI_TIENECOMPUTADOR":
            request.form["FAMI_TIENECOMPUTADOR"],

            "FAMI_TIENEINTERNET":
            request.form["FAMI_TIENEINTERNET"]
        }

        resultado = predecir(datos)

    return render_template(
        "prediccion.html",
        resultado=resultado,
        catalogos=catalogos
    )

@app.route("/estadisticas")
def estadisticas():

    estrato = promedio_por_estrato()
    naturaleza = promedio_por_naturaleza()
    area = promedio_por_area()

    return render_template(
        "estadisticas.html",
        estrato=estrato,
        naturaleza=naturaleza,
        area=area
    )

if __name__ == "__main__":
    app.run(debug=True)