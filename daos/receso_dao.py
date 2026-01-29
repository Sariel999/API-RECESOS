from config import get_connection
from psycopg2.extras import RealDictCursor
from datetime import time

class RecesoDAO:
    TABLA = '"break"'

    def _time_to_str(self, value):
        if isinstance(value, time):
            return value.strftime("%H:%M:%S")
        return value

    def _map_row(self, r):
        return {
            "id": r["id_b"],
            "id_t": r["id_t"],
            "hora_inicio": self._time_to_str(r["hora_inicio_b"]),
            "hora_fin": self._time_to_str(r["tiempo_receso_b"]),
            "hora_total": self._time_to_str(r["total_b"]),
            "nombre": (r["nombre_b"] or "").strip(),
            "descripcion": (r["descripcion_b"] or "").strip(),
            "tipo": (r["tipo_b"] or "").strip(),
        }

    def recuperar_todos(self):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
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
            return [self._map_row(r) for r in rows]
        finally:
            cur.close()
            conn.close()

    def recuperar_por_nombre(self, nombre):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
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
                WHERE nombre_b ILIKE %s
                ORDER BY id_b
            """, (f"%{nombre}%",))
            rows = cur.fetchall()
            return [self._map_row(r) for r in rows]
        finally:
            cur.close()
            conn.close()

    def recuperar_por_id(self, receso_id):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
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
                WHERE id_b = %s
            """, (receso_id,))
            row = cur.fetchone()
            return self._map_row(row) if row else None
        finally:
            cur.close()
            conn.close()

    def crear(self, receso):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(f"""
                INSERT INTO {self.TABLA}
                    (id_t, hora_inicio_b, tiempo_receso_b, total_b, nombre_b, descripcion_b, tipo_b)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id_b, id_t, hora_inicio_b, tiempo_receso_b, total_b, nombre_b, descripcion_b, tipo_b
            """, (
                receso.id_t,
                receso.hora_inicio,
                receso.hora_fin,
                receso.hora_total,
                receso.nombre,
                receso.descripcion,
                receso.tipo,
            ))
            row = cur.fetchone()
            conn.commit()
            return self._map_row(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    def actualizar(self, receso_id, receso):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(f"""
                UPDATE {self.TABLA}
                SET
                    id_t = %s,
                    hora_inicio_b = %s,
                    tiempo_receso_b = %s,
                    total_b = %s,
                    nombre_b = %s,
                    descripcion_b = %s,
                    tipo_b = %s
                WHERE id_b = %s
                RETURNING
                    id_b, id_t, hora_inicio_b, tiempo_receso_b, total_b, nombre_b, descripcion_b, tipo_b
            """, (
                receso.id_t,
                receso.hora_inicio,
                receso.hora_fin,
                receso.hora_total,
                receso.nombre,
                receso.descripcion,
                receso.tipo,
                receso_id
            ))
            row = cur.fetchone()
            if not row:
                conn.rollback()
                return None
            conn.commit()
            return self._map_row(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
def turno_existe(self, id_t: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT 1 FROM turno WHERE id_t = %s', (id_t,))
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()