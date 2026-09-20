import pymupdf as fitz
import unicodedata
import re
from src.pdf.cleaner import clean_text

def extract_text_from_pdf(pdf_path):
   
    doc = fitz.open(pdf_path)

    all_text = ""

    for i in range(doc.page_count):
          page = doc[i]
          text = page.get_text()
          all_text += text + "\n"

    all_text = clean_text(all_text)   # <- tek, doğru yerde, doğru kalıpla
    
    page_count = doc.page_count
    word_count = len(all_text.split())
    char_count = len(all_text)
    
    return {
    "text": all_text,
    "page_count": page_count,
    "char_count": char_count,
    "word_count": word_count
}

if __name__ == "__main__":
    result = extract_text_from_pdf("data/coherent_states.pdf")
    kalan = re.findall(r'\n\d{1,3}\n', result["text"])
    print("Sayfa sayısı:", result["page_count"])
    print("Kalan yalnız sayı sayısı:", len(kalan))
    uzun_kelimeler = [w for w in result["text"].split() if len(w) > 15]
    print("15+ harfli kelime sayısı:", len(uzun_kelimeler))
    print("Örnekler:", uzun_kelimeler[:15])