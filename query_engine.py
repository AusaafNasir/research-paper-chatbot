import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Initialize SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Paths
METADATA_FILE = os.path.join("data", "metadata.txt")
CLEANED_FOLDER = os.path.join("data", "cleaned_text")
INDEX_PATH = os.path.join("data", "faiss_index", "papers_index.faiss")
FILENAMES_PATH = os.path.join("data", "faiss_index", "filenames.txt")

# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load filenames
with open(FILENAMES_PATH, "r") as f:
    filenames = f.read().splitlines()

def load_metadata():
    """Loads paper metadata."""
    metadata = {}
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            filename, title, link = line.strip().split("|")
            metadata[filename] = {"title": title, "link": link}
    return metadata

def load_sentences(file_path):
    """Loads sentences from a text file, where each line is a sentence."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def semantic_search(sentences, query, top_n=3):
    """Finds the most relevant sentences for a query."""
    query_embedding = model.encode([query], convert_to_tensor=True)
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, sentence_embeddings)[0]
    sorted_indices = similarities.argsort(descending=True)
    return [(sentences[i], similarities[i].item()) for i in sorted_indices[:top_n]]

def search_query(query, top_k=5):
    """Searches for the most relevant papers and snippets."""
    query_embedding = model.encode([query], convert_to_tensor=False).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    metadata = load_metadata()
    results = []

    for idx, distance in zip(indices[0], distances[0]):
        if idx == -1:
            continue

        filename = filenames[idx]
        file_path = os.path.join(CLEANED_FOLDER, filename)
        meta = metadata.get(filename, {"title": "Unknown", "link": "#"})

        sentences = load_sentences(file_path)
        snippets = semantic_search(sentences, query)

        results.append({
            "title": meta["title"],
            "link": meta["link"],
            "relevance": distance,
            "snippets": snippets
        })
    return results
