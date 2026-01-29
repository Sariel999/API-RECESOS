from pydantic import ValidationError
from daos.receso_dao import RecesoDAO
from schemas.receso_schema import RecesoSchema

class RecesoService:
    def __init__(self):
        self.dao = RecesoDAO()

    def listar(self):
        return self.dao.recuperar_todos()

    def buscar_por_nombre(self, nombre: str):
        return self.dao.recuperar_por_nombre(nombre)

    def crear(self, data: dict):
        receso = RecesoSchema(**data)
        return self.dao.crear(receso)

    def actualizar(self, receso_id: int, data: dict):
        receso = RecesoSchema(**data)
        return self.dao.actualizar(receso_id, receso)
