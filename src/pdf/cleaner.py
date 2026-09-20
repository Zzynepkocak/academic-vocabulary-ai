import re
import unicodedata

def clean_text(text):
    
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'\n\d{1,3}\n', ' ', text)

    return text
    