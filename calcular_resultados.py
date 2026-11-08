from assessment_questions import QUESTIONS


def calcular_puntajes(respuestas):

    resultados = {}

    total_correctas = 0
    total_preguntas = 0

    for materia, preguntas in QUESTIONS.items():

        correctas = 0

        for pregunta in preguntas:

            respuesta_usuario = respuestas.get(
                pregunta["id"]
            )

            if respuesta_usuario == pregunta["correct"]:
                correctas += 1

        porcentaje = round(
            (correctas / len(preguntas)) * 100
        )

        resultados[materia] = {
            "correct": correctas,
            "total": len(preguntas),
            "percentage": porcentaje
        }

        total_correctas += correctas
        total_preguntas += len(preguntas)

    porcentaje_global = round(
        (total_correctas / total_preguntas) * 100
    )

    puntaje_estimado = round(
        (porcentaje_global / 100) * 500
    )

    if puntaje_estimado >= 400:
        nivel = "Excellent"

    elif puntaje_estimado >= 300:
        nivel = "High"

    elif puntaje_estimado >= 200:
        nivel = "Medium"

    else:
        nivel = "Low"

    materias_academicas = {
        k: v
        for k, v in resultados.items()
        if k != "Socioeconomic Profile"
    }

    mejor_materia = max(
        materias_academicas,
        key=lambda x:
        materias_academicas[x]["percentage"]
    )

    peor_materia = min(
        materias_academicas,
        key=lambda x:
        materias_academicas[x]["percentage"]
    )

    recomendaciones = []

    for materia, datos in materias_academicas.items():

        porcentaje = datos["percentage"]

        if materia == "Critical Reading":

            if porcentaje < 40:

                recomendaciones.append(
                    "Improve reading comprehension through text analysis and inference exercises."
                )

            elif porcentaje < 70:

                recomendaciones.append(
                    "Continue strengthening critical reading and information interpretation skills."
                )

        elif materia == "Mathematics":

            if porcentaje < 40:

                recomendaciones.append(
                    "Practice algebra, geometry and mathematical problem-solving exercises."
                )

            elif porcentaje < 70:

                recomendaciones.append(
                    "Continue improving mathematical reasoning and analytical thinking."
                )

        elif materia == "English":

            if porcentaje < 40:

                recomendaciones.append(
                    "Increase English vocabulary and reading comprehension practice."
                )

            elif porcentaje < 70:

                recomendaciones.append(
                    "Continue improving grammar and English communication skills."
                )

        elif materia == "Natural Sciences":

            if porcentaje < 40:

                recomendaciones.append(
                    "Review biology, chemistry and scientific reasoning concepts."
                )

            elif porcentaje < 70:

                recomendaciones.append(
                    "Continue strengthening scientific interpretation and analysis."
                )

        elif materia == "Social Studies":

            if porcentaje < 40:

                recomendaciones.append(
                    "Study citizenship, democracy and historical-social processes."
                )

            elif porcentaje < 70:

                recomendaciones.append(
                    "Improve understanding of civic and social issues."
                )

    if len(recomendaciones) == 0:

        recomendaciones.append(
            "Excellent performance. Maintain your study habits and continue strengthening all academic areas."
        )

    return {
        "materias": resultados,
        "total_correctas": total_correctas,
        "total_preguntas": total_preguntas,
        "porcentaje_global": porcentaje_global,
        "puntaje_estimado": puntaje_estimado,
        "nivel": nivel,
        "mejor_materia": mejor_materia,
        "peor_materia": peor_materia,
        "recomendaciones": recomendaciones
    }