from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel

app = FastAPI()

# Reemplaza esto con tu "External Database URL" de Render
DB_URL = "postgresql://api_bdd_bancomini_user:tu_password@dpg-d6u4vp7kijhs...oregon-postgres.render.com/api_bdd_bancomini"

# Modelo de datos para recibir desde Android
class Nino(BaseModel):
    nombre: str
    edad: int
    correo: str
    password: str

@app.post("/registrar_nino")
def registrar_nino(nino: Nino):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Insertar en la tabla 'nino' que ya creaste
        query = "INSERT INTO nino (nombre, edad, correo, password) VALUES (%s, %s, %s, %s) RETURNING id_nino;"
        cur.execute(query, (nino.nombre, nino.edad, nino.correo, nino.password))
        
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        
        cur.close()
        conn.close()
        return {"mensaje": "Niño registrado con éxito", "id": nuevo_id}
    except Exception as e:
        return {"error": str(e)}