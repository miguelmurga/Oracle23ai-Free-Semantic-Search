#!/bin/bash

echo "🚀 Ejecutando pipeline completo de embeddings y búsqueda semántica"

echo "📌 Extrayendo texto de PDFs..."
python extract_pdfs.py

echo "📌 Insertando embeddings en Oracle Database..."
python insert_embeddings.py

echo "📌 Ejecutando consulta semántica..."
python query_embeddings.py

