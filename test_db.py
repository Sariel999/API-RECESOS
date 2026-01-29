from config import get_connection

if __name__ == "__main__":
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        print("Connection OK:", cur.fetchone())
        cur.close()
        conn.close()
    except Exception as e:
        print("Connection ERROR:", e)
