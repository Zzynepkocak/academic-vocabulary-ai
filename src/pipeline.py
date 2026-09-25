import sys
import spacy

from src.pdf.extractor import extract_text_from_pdf
from src.vocabulary.candidates import extract_candidates


def run_pipeline(pdf_path, output_csv=None):
    """
    PDF -> temiz metin -> spaCy analizi -> aday kelime tablosu.

    Girdi:
        pdf_path: işlenecek PDF dosyasının yolu
        output_csv: (opsiyonel) sonucun kaydedileceği CSV dosyasının yolu.
                     None ise, dosyaya kaydetmeden sadece DataFrame döndürür.

    Çıktı:
        pandas.DataFrame: raw_frequency'ye göre azalan sırada aday tablo
    """
    # 1. extract_text_from_pdf(pdf_path) çağır
    pdf_data = extract_text_from_pdf(pdf_path)
   
    # 2. spacy.load("en_core_web_sm") ile modeli yükle, nlp(text) çalıştır
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(pdf_data["text"])
    # 3. extract_candidates(doc) çağır
    candidates = extract_candidates(doc)
    # 5. eğer output_csv verilmişse (None değilse), df.to_csv(output_csv, index=False)
    if output_csv is not None:
           candidates.to_csv(output_csv, index=False)

    return candidates
    
   
if __name__ == "__main__":
    pdf_path = sys.argv[1]
    tablo = run_pipeline(pdf_path, output_csv="output.csv")
    print(tablo.head(20))
    print("Toplam aday sayısı:", len(tablo))