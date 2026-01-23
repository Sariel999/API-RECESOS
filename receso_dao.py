from config import get_connection
from psycopg2.extras import RealDictCursor
from datetime import time

class RecesoDAO:
    TABLA = '"break"'

    def _time_to_str(self, value):
        if isinstance(value, time):
            return value.strftime("%H:%M:%S")
        return value

    def recuperar_todos(self):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(f"""
            SELECT
                id_b,
                id_t,
                hora_inicio_b,
                tiempo_receso_b,
                total_b,
                nombre_b,
                descripcion_b,
                tipo_b
            FROM {self.TABLA}
            ORDER BY id_b
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "id": r["id_b"],
                "id_t": r["id_t"],
                "hora_inicio": self._time_to_str(r["hora_inicio_b"]),
                "hora_fin": self._time_to_str(r["tiempo_receso_b"]),
                "hora_total": self._time_to_str(r["total_b"]),
                "nombre": (r["nombre_b"] or "").strip(),
                "descripcion": (r["descripcion_b"] or "").strip(),
                "tipo": (r["tipo_b"] or "").strip()
            }
            for r in rows
        ]
