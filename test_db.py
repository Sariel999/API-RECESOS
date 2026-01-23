from config import get_connection

try:
    conn = get_connection()
    print("Conexion exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print("Error:", e)
