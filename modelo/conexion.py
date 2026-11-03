import psycopg2

def obtener_conexion():

    return psycopg2.connect(
        "postgresql://predictoruser:P5ScCO4wkQrEcNb1CwGR9gFxvQrb88UN@dpg-dbkmvk6gekts73ekfjp0-a.oregon-postgres.render.com/predictoricfes"
    )