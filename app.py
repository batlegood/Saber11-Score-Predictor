from flask import Flask, render_template, request, session, redirect, url_for

from modelo.predictor import predecir
from modelo.catalogos import obtener_catalogos
from modelo.conexion import obtener_conexion
from calcular_resultados import calcular_puntajes
from assessment_questions import QUESTIONS

from modelo.analisis import (
    mejor_icfes,
    obtener_metricas,
    promedio_por_estrato,
    promedio_por_naturaleza,
    promedio_por_area
)


import joblib

def validar_login(usuario, password):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM Usuarios
        WHERE Usuario = ?
        AND Password = ?
        """,
        usuario,
        password
    )

    usuario_db = cursor.fetchone()

    conexion.close()

    return usuario_db


def existe_usuario(usuario):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM Usuarios
        WHERE Usuario = ?
        """,
        usuario
    )

    resultado = cursor.fetchone()

    conexion.close()

    return resultado


def crear_usuario(
    nombre,
    usuario,
    correo,
    password
):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO Usuarios
        (
            Nombre,
            Usuario,
            Correo,
            Password
        )
        VALUES
        (
            ?, ?, ?, ?
        )
        """,
        nombre,
        usuario,
        correo,
        password
    )

    conexion.commit()

    conexion.close()

app = Flask(__name__)

app.secret_key = "saber11"


def validar_login(usuario, password):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM Usuarios
        WHERE Usuario = %s
        AND Password = %s
        """,
        (usuario, password)
    )

    usuario_db = cursor.fetchone()

    conexion.close()

    return usuario_db


def existe_usuario(usuario):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM Usuarios
        WHERE Usuario = %s
        """,
        (usuario,)
    )

    resultado = cursor.fetchone()

    conexion.close()

    return resultado


def crear_usuario(nombre, usuario, correo, password):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO Usuarios
        (
            Nombre,
            Usuario,
            Correo,
            Password
        )
        VALUES
        (
            %s,%s,%s,%s
        )
        """,
        (
            nombre,
            usuario,
            correo,
            password
        )
    )

    conexion.commit()

    conexion.close()

@app.route("/")
def inicio():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        usuario = request.form["usuario"]
        clave = request.form["clave"]

        usuario_db = validar_login(
            usuario,
            clave
        )

        if usuario_db:

            session["usuario"] = usuario

            session["nombre"] = usuario_db[1]

            return redirect("/learning")

        else:

            error = "Invalid username or password"

    return render_template(
        "login.html",
        error=error
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    error = None
    mensaje = None

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        usuario = request.form["usuario"].strip()
        correo = request.form["correo"].strip()
        password = request.form["password"]
        confirmar = request.form["confirmar"]

        if password != confirmar:

            error = "Passwords do not match"

        elif existe_usuario(usuario):

            error = "Username already exists"

        else:

            crear_usuario(
                nombre,
                usuario,
                correo,
                password
            )

            mensaje = "User created successfully"

    return render_template(
        "register.html",
        error=error,
        mensaje=mensaje
    ) 
    
@app.route("/development")
def development():

    return render_template(
        "project_development.html"
    )

@app.route("/about")
def about():

    return render_template(
        "about_project.html"
    )

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if "usuario" not in session:
        return redirect("/login")

    resultado_materias = None

    if request.method == "POST":

        respuestas = request.form.to_dict()

        resultado_materias = calcular_puntajes(
            respuestas
        )

        print("\n==========================")
        print("RESULTADO_MATERIAS")
        print(resultado_materias)
        print("==========================\n")

        session["resultado_materias"] = resultado_materias
        session["mejor_materia"] = resultado_materias["mejor_materia"]
        session["peor_materia"] = resultado_materias["peor_materia"]

        print("\n==========================")
        print("RESULTADO_MATERIAS")
        print(resultado_materias)
        print(type(resultado_materias))
        print("==========================")

        

    return render_template(
        "academic_assessment.html",
        questions=QUESTIONS,
        resultado_materias=resultado_materias
    )

@app.route("/learning")
def learning():

    if "usuario" not in session:

        return redirect("/login")

    return render_template(
        "learning_models.html"
    )

@app.route("/home")
def home():

    if "usuario" not in session:

        return redirect("/")

    return render_template("index.html")




@app.route("/conceptos")
def conceptos():

    if "usuario" not in session:

        return redirect("/")

    return render_template("conceptos.html")




@app.route("/prediccion", methods=["GET", "POST"])
def prediccion():

    if "usuario" not in session:

        return redirect("/")

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

    metricas = obtener_metricas()

    estrato = promedio_por_estrato()

    naturaleza = promedio_por_naturaleza()

    area = promedio_por_area()

    resultado_materias = session.get(
        "resultado_materias"
    )

    mejor_materia = session.get(
        "mejor_materia"
    )

    peor_materia = session.get(
"peor_materia"
    )

    mejor_icfes_score = mejor_icfes()

    return render_template(
        "estadisticas.html",
        metricas=metricas,
        estrato=estrato,
        naturaleza=naturaleza,
        area=promedio_por_area(),
        resultado_materias=resultado_materias,
        mejor_materia=mejor_materia,
        peor_materia=peor_materia,
        mejor_icfes_score = mejor_icfes_score
    )




@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)