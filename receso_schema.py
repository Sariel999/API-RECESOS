from pydantic import BaseModel

class RecesoSchema(BaseModel):
    id_t: int
    hora_inicio: str
    hora_fin: str
    hora_total: str
    nombre: str
    descripcion: str
    tipo: str
