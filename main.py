from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import schemas

app = FastAPI()

host_name = "database-parcial.c6fxrh1itneq.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin"
password_db = "parcial777"
database_name = "api_usuarios"

# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get all usuarios
@app.get("/usuarios")
def get_usuarios():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM usuarios")
    result = cursor.fetchall()
    mydb.close()
    return {"usuarios": result}

# Get an usuario by ID
@app.get("/usuarios/{id}")
def get_usuario(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM usuarios WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    return {"usuario": result}


@app.post("/usuarios/login")
def login_usuario(item: schemas.Item):
    nombre = item.nombre
    contraseña = item.contraseña

    mydb = mysql.connector.connect(
        host=host_name,
        port=port_number,
        user=user_name,
        password=password_db,
        database=database_name
    )

    cursor = mydb.cursor()

    cursor.execute(f"SELECT * FROM usuarios WHERE nombre = '{nombre}' AND contraseña = '{contraseña}'")

    result = cursor.fetchone()

    mydb.close()

    if result is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"usuario": result}


# Add a new usuario
@app.post("/usuarios")
def add_usuarios(item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    nombre = item.nombre
    contraseña = item.contraseña
    perfil = item.perfil
    isesion = item.isesion
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    sql = "INSERT INTO usuarios (nombre, contraseña, perfil, isesion) VALUES (%s, %s, %s, %s)"
    val = (nombre, contraseña, perfil, isesion)
    cursor.execute(sql, val)
    mydb.commit()
    new_user_id = cursor.lastrowid
    mydb.close()
    return  {"message": "Usuario creado exitosamente", "user_id": new_user_id}

# Modify an usuario
@app.put("/usuarios/{id}")
def update_usuarios(id: int, item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    nombre = item.nombre
    contraseña = item.contraseña
    perfil = item.perfil
    isesion = item.isesion
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND id != %s", (nombre, id))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    sql = "UPDATE usuarios SET nombre=%s, contraseña=%s, perfil=%s, isesion=%s WHERE id=%s"
    val = (nombre, contraseña, perfil, isesion, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Usuario modificado exitosamente"}

# Delete an usuario by ID
@app.delete("/usuarios/{id}")
def delete_usuarios(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM usuarios WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Usuario eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
