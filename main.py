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

class Cuenta(BaseModel):
    id_nino: int
    mini_coins: int
    saldo: float
    
# Rutas para las consultas

@app.post("/registrar_nino")
def registrar_nino(nino: Nino):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        query = "INSERT INTO nino (nombre, edad,  id_tutor) VALUES (%s, %s, %s) RETURNING id_nino;"
        cur.execute(query, (nino.nombre, nino.edad, nino.id_tutor))
        
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
    
@app.post("/registrar_cuenta")
def registrar_cuenta(cuenta: Cuenta):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        query = "INSERT INTO cuenta (id_nino, mini_coins, saldo) VALUES (%s, %s, %s) RETURNING id_cuenta;"
        cur.execute(query, (cuenta.id_nino, cuenta.mini_coins, cuenta.saldo))
        
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        
        cur.close()
        conn.close()
        return {"mensaje": "Cuenta registrada con éxito", "id": nuevo_id}
    except Exception as e:
        return {"error": str(e)}
    

#QUERYS DE LA PANTALLA PRINCIPAL
@app.get("/obtener_cuenta/{id_cuenta}")
def seleccionar_saldo(id_cuenta: int):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        query = "SELECT id_nino, mini_coins, saldo FROM cuenta WHERE id_cuenta = %s;"
        cur.execute(query, (id_cuenta))
        resultado = cur.fetchone()
            
        cur.close()
        conn.close()

        if resultado:
            # resultado[0] es id_nino, resultado[1] es mini_coins, resultado[2] es saldo
            return {
                "id_nino": resultado[0],
                "mini_coins": resultado[1],
                "saldo": float(resultado[2])
            }
        else:
            return {"error": "No se encontró la cuenta"}
            
    except Exception as e:
        return {"error": str(e)}

