import oracledb
import random
from datetime import datetime, timedelta

# 🔹 Configuración de conexión a Oracle
ORACLE_USER = "miguel"
ORACLE_PASSWORD = "NuevaClave123"
ORACLE_DSN = "localhost:1521/FREEPDB1"

# 🔹 Conectar a la base de datos
conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
cursor = conn.cursor()

# 🔹 Lista de beneficiarios ficticios
beneficiarios = ["Juan Pérez", "María García", "Carlos López", "Ana Martínez", "Luis Ramírez", "Sofía Fernández", "Roberto Díaz", "Elena Torres"]

# 🔹 Lista de monedas
monedas = ["MXN", "USD", "EUR"]

# 🔹 Lista de estados de pago
estatus_opciones = ["Procesado", "Pendiente", "Rechazado"]

# 🔹 Fecha de inicio (año 2000)
fecha_inicio = datetime(2000, 1, 1)

# 🔹 Insertar 2000 pagos ficticios
for _ in range(2000):
    fecha_pago = fecha_inicio + timedelta(days=random.randint(0, 9000))  # Fechas aleatorias entre 2000 y hoy
    monto = round(random.uniform(100, 5000), 2)  # Montos entre 100 y 5000
    moneda = random.choice(monedas)
    estatus = random.choice(estatus_opciones)
    beneficiario = random.choice(beneficiarios)

    cursor.execute("""
        INSERT INTO pagos (fecha, monto, moneda, estatus, beneficiario) 
        VALUES (:1, :2, :3, :4, :5)
    """, (fecha_pago, monto, moneda, estatus, beneficiario))

conn.commit()
print("✅ 2000 pagos ficticios insertados en Oracle Database 23ai Free.")

cursor.close()
conn.close()
