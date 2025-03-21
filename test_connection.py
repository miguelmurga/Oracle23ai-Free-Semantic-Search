import oracledb

# Configuración de conexión
ORACLE_USER = "miguel"
ORACLE_PASSWORD = "MiContraseña"  # Usa la misma contraseña que funcionó en SQL*Plus
ORACLE_DSN = "localhost:1521/FREEPDB1"  # O usa la IP del contenedor si es necesario

try:
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
    print("✅ ¡Conexión exitosa a Oracle Database desde Python!")
    conn.close()
except oracledb.DatabaseError as e:
    print(f"❌ Error en la conexión: {e}")
