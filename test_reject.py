import sys; sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from main import app
from app.database import get_connection
from app.auth import hash_password

client = TestClient(app)

conn = get_connection()
c = conn.cursor()
c.execute("DELETE FROM notificaciones")
c.execute("DELETE FROM reportes")
c.execute("DELETE FROM solicitudes")
c.execute("DELETE FROM usuarios")

c.execute("INSERT INTO usuarios (correo, clave_hash, nombre, rol) VALUES (%s, %s, %s, %s)",
          ("dir@test.com", hash_password("123"), "Dir", "directora"))
c.execute("INSERT INTO usuarios (correo, clave_hash, nombre, rol) VALUES (%s, %s, %s, %s)",
          ("doc@test.com", hash_password("123"), "Doc", "docente"))
doc_id = c.lastrowid
c.execute("INSERT INTO solicitudes (directora_id, titulo, descripcion, fecha_limite) VALUES (1, 'Test', 'Desc', '2026-07-01')")
c.execute("INSERT INTO reportes (docente_id, solicitud_id, titulo, descripcion, archivo_ruta, estado) VALUES (%s, 1, 'R', 'D', 'test.pdf', 'pendiente')", (doc_id,))
conn.commit()
c.close()
conn.close()
print("DB ready")

# Login directora
r = client.post("/login/", json={"correo": "dir@test.com", "clave": "123"})
tok = r.json()["token"]
print(f"Login: {r.status_code}")

# Reject
r2 = client.put("/directora/reportes/1/rechazar",
    json={"comentarios": "Test error"},
    headers={"Authorization": f"Bearer {tok}"})
print(f"Reject status: {r2.status_code}")
print(f"Reject body: {r2.text}")
