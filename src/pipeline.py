import sys
import spacy
from pathlib import Path
from src.pdf.extractor import extract_text_from_pdf
from src.vocabulary.candidates import extract_candidates
from src.nlp.preprocessing import process_text

def run_pipeline(pdf_path, output_csv=None):
   
    pdf_data = extract_text_from_pdf(pdf_path)
    doc = process_text(pdf_data["text"])
    candidates = extract_candidates(doc)

    if output_csv is not None:
           candidates.to_csv(output_csv, index=False)

    return candidates
    
   
if __name__ == "__main__":
    pdf_path = sys.argv[1]
    output_name = Path(pdf_path).stem + "_candidates.csv"
    tablo = run_pipeline(pdf_path, output_csv=output_name)
    print(tablo.head(20))
    print("Toplam aday sayısı:", len(tablo))