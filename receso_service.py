from receso_dao import RecesoDAO

class RecesoService:
    def __init__(self):
        self.dao = RecesoDAO()

    def recuperar_todos(self):
        return self.dao.recuperar_todos()
