import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy

nltk.download("stopwords")
nltk.download("punkt")

nlp = spacy.load("en_core_web_sm")

# Paths
EXTRACTED_TEXT_FOLDER = "data/extracted_text"
CLEANED_TEXT_FOLDER = "data/cleaned_text"

os.makedirs(CLEANED_TEXT_FOLDER, exist_ok=True)

def clean_and_preprocess_text(text):
    """
    Cleans and tokenizes text into meaningful sentences.
    Each sentence is cleaned, lemmatized, and stopwords are removed.
    """
    # Split text into sentences
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words("english"))
    cleaned_sentences = []

    for sentence in sentences:
        # Tokenize, remove stopwords, and lemmatize
        words = word_tokenize(sentence)
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
        cleaned_sentence = " ".join(filtered_words)
        lemmatized_sentence = " ".join([token.lemma_ for token in nlp(cleaned_sentence) if not token.is_stop])
        
        if len(lemmatized_sentence) > 1:  # Ignore very short sentences
            cleaned_sentences.append(lemmatized_sentence)

    return cleaned_sentences

def preprocess_text_files(input_folder, output_folder):
    """
    Processes all text files in input_folder and saves cleaned sentences in output_folder.
    Each sentence is written on a new line.
    """
    for i, txt_file in enumerate(os.listdir(input_folder)):
        if txt_file.endswith(".txt"):
            input_path = os.path.join(input_folder, txt_file)
            output_path = os.path.join(output_folder, txt_file)

            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
                cleaned_sentences = clean_and_preprocess_text(raw_text)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned_sentences))

            print(f"Processed: {txt_file} ({i+1})")

if __name__ == "__main__":
    print("Starting text preprocessing...")
    preprocess_text_files(EXTRACTED_TEXT_FOLDER, CLEANED_TEXT_FOLDER)
    print("Text preprocessing completed successfully!")
