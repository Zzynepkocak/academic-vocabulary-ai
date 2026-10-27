import sys
import pandas as pd


def prepare_for_labeling(candidates_csv, output_csv, top_n=100):
    """
    Bir candidates.csv dosyasından etiketleme için hazır bir dosya üretir:
    ilk top_n satırı alır, karıştırır, skoru gizler, boş bir 'etiket'
    sütunu ekler.
    """
    # 1. candidates_csv'yi pandas ile oku (pd.read_csv)
    prepared_csv = pd.read_csv(candidates_csv)
    # 2. df.head(top_n) ile ilk top_n satırı al, sadece 'lemma' ve 'pos'
    #    sütunlarını tut (df[["lemma", "pos"]] gibi bir seçim yap)
    prepared_csv = prepared_csv.head(top_n)
    prepared_csv = prepared_csv[["lemma", "pos"]]
    # 3. df.sample(frac=1) ile satırları karıştır
    #    (ipucu: bunu yeni bir değişkene ata, üzerine yazmayı unutma)
    mixed_csv = prepared_csv.sample(frac=1) 
    # 4. yeni bir 'etiket' sütunu ekle, hepsini boş string yap ("")
    mixed_csv["etiket"] =""
    # 5. output_csv'ye kaydet (to_csv, index=False)
    mixed_csv.to_csv(output_csv, index =False)
   


if __name__ == "__main__":
    prepare_for_labeling(sys.argv[1], sys.argv[2])