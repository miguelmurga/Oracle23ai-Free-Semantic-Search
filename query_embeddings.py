import oracledb
from sentence_transformers import SentenceTransformer
import numpy as np

# Configuración de conexión
ORACLE_USER = "miguel"
ORACLE_PASSWORD = "NuevaClave123"
ORACLE_DSN = "localhost:1521/FREEPDB1"

# Conectar a la base de datos
conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
cursor = conn.cursor()

# Inicializar modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Solicitar consulta al usuario
query = input("🔍 Ingrese su consulta en lenguaje natural: ")
query_embedding = model.encode(query).astype(np.float32)

# Recuperar embeddings de la base de datos
cursor.execute("SELECT filename, fragment_number, content, embedding FROM documents WHERE DBMS_LOB.GETLENGTH(embedding) > 0")
documents = cursor.fetchall()

# Convertir los embeddings almacenados en BLOB a numpy arrays
document_vectors = []
document_data = []

for filename, fragment_number, content, embedding_blob in documents:
    if embedding_blob is None:
        continue  # Ignorar registros sin embedding

    # Convertir LOB a bytes
    embedding_bytes = embedding_blob.read() if hasattr(embedding_blob, 'read') else embedding_blob
    embedding_array = np.frombuffer(embedding_bytes, dtype=np.float32)

    if embedding_array.shape[0] == 0:
        continue  # Ignorar embeddings corruptos

    # Convertir CLOB a string si es necesario
    if isinstance(content, oracledb.LOB):
        content = content.read()  # Convierte el CLOB a string

    document_vectors.append(embedding_array)
    document_data.append((filename, fragment_number, content))

# Si no hay embeddings válidos, mostrar mensaje
if len(document_vectors) == 0:
    print("⚠️ No hay embeddings válidos en la base de datos.")
    cursor.close()
    conn.close()
    exit()

# Convertir a matriz de NumPy para cálculos de similitud
document_vectors = np.array(document_vectors)

# Calcular similitud de coseno
from numpy.linalg import norm

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

similarities = [cosine_similarity(query_embedding, doc_vec) for doc_vec in document_vectors]

# Ordenar fragmentos por similitud (de mayor a menor)
sorted_docs = sorted(zip(similarities, document_data), reverse=True, key=lambda x: x[0])

# Mostrar los 5 fragmentos más relevantes
print("\n📌 Resultados más relevantes:")
for similarity, (filename, fragment_number, content) in sorted_docs[:5]:
    print(f"📄 {filename} (Fragmento {fragment_number}, Similitud: {similarity:.4f}):\n{content[:500]}...\n")

cursor.close()
conn.close()

