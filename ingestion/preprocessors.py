import re
import spacy
import indic

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()

    # Process the text with spaCy
    doc = nlp(text)

    # Filter tokens: Remove stopwords, punctuation, and non-alphanumeric tokens, and lemmatize
    words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

    return ' '.join(words)
