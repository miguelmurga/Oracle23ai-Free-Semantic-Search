import os
import subprocess
import pdfplumber
import pytesseract
from PIL import Image
import pdf2image
import ftfy

# Archivos PDF en la carpeta actual
pdf_files = ["ETHPA.pdf", "IA_Generativa__Particularidades_de_los_Modelos_de_Lenguaje_Grandes.pdf"]

output_file = "extracted_text.txt"

def extract_text_pdftotext(pdf_file):
    """Extraer texto usando pdftotext si pdfplumber falla."""
    try:
        result = subprocess.run(["pdftotext", pdf_file, "-"], capture_output=True, text=True, encoding="utf-8")
        return result.stdout.strip()
    except Exception as e:
        print(f"⚠️ Error con pdftotext: {e}")
        return ""

def extract_text_ocr(pdf_file):
    """Extraer texto usando OCR si todo lo demás falla."""
    print(f"⚠️ Usando OCR para extraer texto de {pdf_file}...")
    pages = pdf2image.convert_from_path(pdf_file)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page, lang="spa") + "\n"
    return text

with open(output_file, "w", encoding="utf-8") as f_out:
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            print(f"⚠️ No se encontró el archivo {pdf_file}, omitiendo...")
            continue

        print(f"📄 Extrayendo texto de {pdf_file}...")

        # Intentar primero con pdftotext
        extracted_text = extract_text_pdftotext(pdf_file)

        # Si pdftotext no funcionó bien, probar con pdfplumber
        if len(extracted_text.strip()) < 100:
            print(f"⚠️ Extracción de texto insuficiente con pdftotext en {pdf_file}, probando con pdfplumber...")
            try:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            page_text = ftfy.fix_text(page_text)
                            extracted_text += page_text + "\n"
            except Exception as e:
                print(f"⚠️ Error al extraer con pdfplumber: {e}")

        # Si el texto sigue mal, usar OCR
        if len(extracted_text.strip()) < 100:
            print(f"⚠️ Último intento: OCR en {pdf_file}...")
            extracted_text = extract_text_ocr(pdf_file)

        f_out.write(f"### {pdf_file} ###\n{extracted_text.strip()}\n\n")

print("✅ Extracción completada: guardado en extracted_text.txt")

