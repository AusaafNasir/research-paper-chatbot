import os
import faiss
from sentence_transformers import SentenceTransformer

CLEANED_TEXT_FOLDER = "data/cleaned_text"
FAISS_INDEX_FOLDER = "data/faiss_index"

os.makedirs(FAISS_INDEX_FOLDER, exist_ok=True)

# Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load and embed text
def load_and_embed_text(input_folder):
    texts = []
    filenames = []
    
    for txt_file in os.listdir(input_folder):
        if txt_file.endswith(".txt"):
            file_path = os.path.join(input_folder, txt_file)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                texts.append(text)
                filenames.append(txt_file)
    
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings, filenames

# Build and save FAISS index
def build_faiss_index(embeddings, output_folder, filenames):
    d = embeddings.shape[1]  
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    faiss.write_index(index, os.path.join(output_folder, "papers_index.faiss"))

    # Save filenames for reference
    with open(os.path.join(output_folder, "filenames.txt"), "w") as f:
        for filename in filenames:
            f.write(f"{filename}\n")

if __name__ == "__main__":
    print("Building FAISS index...")
    embeddings, filenames = load_and_embed_text(CLEANED_TEXT_FOLDER)
    build_faiss_index(embeddings, FAISS_INDEX_FOLDER, filenames)
    print("FAISS index built and saved successfully!")
