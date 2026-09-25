import spacy


def process_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return doc