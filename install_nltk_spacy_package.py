import nltk
import spacy
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_lg')