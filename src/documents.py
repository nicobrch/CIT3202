import os
import string
import re
import nltk
import config
nltk.download('punkt')
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords

def tokenize_text(text):
    return word_tokenize(text)

def to_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]', '', text)

def remove_stopwords(words):
    stop_words = set(stopwords.words('spanish'))
    return [word for word in words if word not in stop_words]

def tokenize(text):
    text = to_lowercase(text)
    text = remove_special_characters(text)
    words = tokenize_text(text)
    words = remove_stopwords(words)
    return words

def tokenize_files():
    docs_folder = f"{config.path}docs/"
    for file_name in os.listdir(docs_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(docs_folder, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        words = tokenize(text)

    with open(f"{config.path}data/{file_name}", 'w', encoding='utf-8') as file:
        file.write(' '.join(words))