# AI Research Paper Chatbot 📚

This application allows you to search and query research papers using semantic search. The app provides:
1. **Top relevant papers** based on your query.
2. **Paper titles and links** for easy access.
3. **Concise snippets** extracted from the papers that closely match your query.

---

## Features
- **Semantic Search**: Uses advanced Sentence Transformers for understanding query intent.
- **Clean Results**: Provides paper title, link, and top 5 matching sentences.
- **Scalable**: Handles hundreds of papers efficiently using FAISS.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Streamlit
- Required libraries in `requirements.txt`

---

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/research-ai-chatbot.git
   cd research-ai-chatbot

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py


## Generating Data Folder

To recreate the `data` folder, follow these steps:

1. Download PDFs using `download_papers.py`.
2. Extract text using `pdf_extractor.py`.
3. Clean and preprocess the text using `text_preprocessor.py`.
4. Build the FAISS index using `index_builder.py`.

Once done, the `data` folder will contain the necessary files for running the app.



   
