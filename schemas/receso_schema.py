from pydantic import BaseModel, Field

class RecesoSchema(BaseModel):
    id_t: int = Field(..., ge=1)
    hora_inicio: str
    hora_fin: str
    hora_total: str
    nombre: str
    descripcion: str
    tipo: str
