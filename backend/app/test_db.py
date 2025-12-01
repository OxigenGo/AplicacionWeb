import os
from db import get_connection

print("HOST:", os.environ.get("DB_HOST"))
print("PORT:", os.environ.get("DB_PORT"))
print("USER:", os.environ.get("DB_USER"))
print("PASSWORD:", os.environ.get("DB_PASSWORD"))
print("DB:", os.environ.get("DB_NAME"))

try:
    conn = get_connection()
    print("✔ Conexión OK")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tablas:", tables)
except Exception as e:
    print("❌ ERROR DE CONEXIÓN:")
    print(e)
finally:
    if conn:
        conn.close()
