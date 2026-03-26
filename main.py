from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel

#arriba el pachuca :D
app = FastAPI()

# External URL de DB
DB_URL = "postgresql://api_bdd_bancomini_user:xyDekXdHvLwtnnz5ya1Qtkw8YonktGBh@dpg-d6u4vp7kijhs73fgumug-a.oregon-postgres.render.com/api_bdd_bancomini"

# Modelo de datos para recibir desde Android
class Nino(BaseModel):
    nombre: str
    edad: int
    correo: str
    password: str

class Tutor(BaseModel):
    nombre: str
    telefono: str
    correo: str
    password: str

# Rutas para las consultas

@app.post("/registrar_nino")
def registrar_nino(nino: Nino):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        query = "INSERT INTO nino (nombre, edad, correo, password) VALUES (%s, %s, %s, %s) RETURNING id_nino;"
        cur.execute(query, (nino.nombre, nino.edad, nino.correo, nino.password))
        
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        
        cur.close()
        conn.close()
        return {"mensaje": "Niño registrado con éxito", "id": nuevo_id}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/registrar_tutor")
def registrar_tutor(tutor: Tutor):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        query = "INSERT INTO tutor (nombre, telefono, correo, password) VALUES (%s, %s, %s, %s) RETURNING id_tutor;"
        cur.execute(query, (tutor.nombre, tutor.telefono, tutor.correo, tutor.password))
        
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        
        cur.close()
        conn.close()
        return {"mensaje": "Tutor registrado con éxito", "id": nuevo_id}
    except Exception as e:
        return {"error": str(e)}