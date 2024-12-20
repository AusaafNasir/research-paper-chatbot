import os
import fitz  # PyMuPDF
import re

# Paths
PDF_FOLDER = "data/papers"
TEXT_FOLDER = "data/extracted_text"
METADATA_FILE = "data/metadata.txt"


os.makedirs(TEXT_FOLDER, exist_ok=True)

# Function to extract title from the first page of PDF
def extract_title(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            first_page_text = doc[0].get_text()
            
            for line in first_page_text.split("\n"):
                if len(line.split()) > 3:
                    return line.strip()
    except Exception as e:
        print(f"Error extracting title from {pdf_path}: {e}")
    return "Title not found"

# Extract text and metadata from PDFs
def extract_text_from_pdfs():
    metadata = []
    for i, pdf_file in enumerate(os.listdir(PDF_FOLDER)):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, pdf_file)
            text_file = os.path.join(TEXT_FOLDER, pdf_file.replace(".pdf", ".txt"))

            try:
                with fitz.open(pdf_path) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                
                
                with open(text_file, "w", encoding="utf-8") as f:
                    f.write(text)
                
                # Extract paper title and generate link
                title = extract_title(pdf_path)
                link = f"http://arxiv.org/pdf/{pdf_file.replace('.pdf', '')}"
                metadata.append(f"{pdf_file.replace('.pdf', '.txt')}|{title}|{link}")
                print(f"Extracted: {pdf_file}")
            
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")

    # Save metadata
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        for line in metadata:
            f.write(line + "\n")

if __name__ == "__main__":
    extract_text_from_pdfs()
    print("PDF Extraction Completed.")
