
# Oracle Database 23ai Free + Semantic Search (Embeddings) 🚀

This project demonstrates how to deploy **Oracle Database 23ai Free** in a Podman container, load it with sample data, generate semantic embeddings using **SentenceTransformers**, and perform semantic searches.

It also shows how to integrate the solution with a pre-configured Docker container and automate the entire workflow.

---

## 🛠️ Technologies Used:

- **Oracle Database 23ai Free** (Podman Container)
- **Python 3**
- **SentenceTransformers**
- **OracleDB (Python Driver)**
- **Fedora 40 (Host OS)**
- **Bash (Automation scripts)**

---

## 📦 Pre-configured Docker Container:

You can pull the pre-configured Oracle 23ai Free container loaded with sample data and embeddings:

```bash
podman pull docker.io/miguelmurga/oracle23ai-free:embeddings-v1
```

This container includes:

- Oracle Database 23ai Free installed
- Payments data
- Pre-generated embeddings from PDFs

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `ETHPA.pdf` | Sample PDF document used to generate embeddings. |
| `IA_Generativa__Particularidades_de_los_Modelos_de_Lenguaje_Grandes.pdf` | Second PDF for embeddings. |
| `extracted_text.txt` | Extracted text from PDFs. |
| `extract_pdfs.py` | Script to extract text from PDF files. |
| `insertar_pagos_ficticios.py` | Inserts 2000 fake payment records into Oracle DB. |
| `insert_embeddings.py` | Generates sentence embeddings using Python and stores them in Oracle DB. |
| `query_embeddings.py` | Allows natural language search over embeddings stored in Oracle. |
| `test_connection.py` | Tests connection to Oracle DB. |
| `run_project.sh` | Automates execution of all scripts. |

---

## 🏃‍♂️ How to Run:

### 1️⃣ Clone this repository:

```bash
git clone https://github.com/your_github_username/oracle23ai-free-semantic-search.git
cd oracle23ai-free-semantic-search
```

### 2️⃣ (Option A) Pull pre-configured container:

```bash
podman pull docker.io/miguelmurga/oracle23ai-free:embeddings-v1
podman run -d --name oracle-db -p 1521:1521 docker.io/miguelmurga/oracle23ai-free:embeddings-v1
```

### 2️⃣ (Option B) Start Oracle Database 23ai Free fresh:

```bash
podman run -d --name oracle-db -p 1521:1521 container-registry.oracle.com/database/free:latest
```

Then configure the user:

```bash
podman exec -it oracle-db sqlplus / as sysdba
```

Inside SQL:

```sql
ALTER SESSION SET CONTAINER=FREEPDB1;
CREATE USER miguel IDENTIFIED BY NuevaClave123;
GRANT CONNECT, RESOURCE TO miguel;
ALTER USER miguel QUOTA UNLIMITED ON USERS;
```

---

### 3️⃣ Install Python Dependencies:

```bash
pip install oracledb sentence-transformers PyPDF2
```

---

### 4️⃣ Run the full pipeline:

```bash
chmod +x run_project.sh
./run_project.sh
```

---

## 🔍 Key Functionalities:

- Extracts text from PDFs
- Inserts 2000 fake payments with random years, currencies, beneficiaries, and statuses
- Generates sentence embeddings using `SentenceTransformers`
- Stores embeddings in Oracle DB as BLOB
- Enables semantic search querying using cosine similarity over stored embeddings
- All deployed locally, no external services required!

---

## ⚠️ AI_VECTOR_EMBEDDING Notice:

The **Oracle Database 23ai Free** version **does not include native `AI_VECTOR_EMBEDDING` functionality**.

Embeddings are generated externally with Python and inserted manually into the database.

---

## 📌 Example Semantic Search:

Run:

```bash
python query_embeddings.py
```

It will ask:

```
🔍 Enter your query in natural language:
```

Type:

```
Pending payments in dollars
```

And it will return the top relevant payment records based on vector similarity.

---

## ✅ Conclusion:

This project showcases:

- Effective hybrid usage of **Oracle Database 23ai Free + semantic search**
- How to combine structured SQL data with unstructured semantic search
- Fully local deployment (Oracle DB + Podman + Python)

---

## 🔗 Contact:

Feel free to reach out for questions or improvements:

**Miguel Murga Guevara**  
[Docker Hub Profile](https://hub.docker.com/u/miguelmurga)  
[GitHub Profile](https://github.com/your_github_username)
