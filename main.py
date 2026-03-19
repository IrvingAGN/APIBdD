from fastapi import FastAPI
import psycopg2

app = FastAPI()

# Configuración de tu base de datos
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "rupOmDFlan4y8jLT",
    "host": "localhost", # O la IP de tu servidor
    "port": "5432"
}

@app.get("/")
def read_root():
    return {"status": "API funcionando"}

@app.get("/usuarios")
def get_usuarios():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM usuarios;")
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        # Transformamos los datos a un formato JSON que Android entienda
        return [{"id": u[0], "nombre": u[1]} for u in usuarios]
    except Exception as e:
        return {"error": str(e)}