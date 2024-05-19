from pydantic import BaseModel
class Item(BaseModel):
    nombre: str
    contraseña: str
    perfil: str = None
    isesion: str = None
