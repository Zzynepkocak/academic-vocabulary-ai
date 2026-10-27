import sys
import pandas as pd
import math

def dcg(relevance_list):
    toplam = 0
    for i, rel in enumerate(relevance_list, start=1):
        toplam += rel / math.log2(i + 1)
    return toplam


def compute_precision_at_20(candidates_csv, labeled_csv):
    """
    Bir makalenin orijinal aday tablosunu (frekans sıralı) ve elle
    etiketlenmiş halini birleştirip Precision@20 hesaplar.
    """
    # 1. candidates_csv'yi oku (frekans bilgisi burada)
    candidates = pd.read_csv(candidates_csv)
    # 2. labeled_csv'yi oku (etiket bilgisi burada)
    labeled = pd.read_csv(labeled_csv)
    # 3. İkisini lemma VE pos üzerinden birleştir
    #    ipucu: pd.merge(df1, df2, on=["lemma", "pos"])
    merged =  pd.merge(candidates,labeled, on = ["lemma", "pos"])
    # 4. Birleşmiş tabloyu raw_frequency'ye göre azalan sırada sırala
    merged = merged.sort_values("raw_frequency", ascending=False)
    # 5. İlk 20 satırı al (head(20))
    top_20 = merged.head(20)
    # 6. Precision@20 = (etiket == 1 olan satır sayısı) / 20
    #    ipucu: (df["etiket"] == 1).sum() / 20
    precision= (top_20["etiket"] == 1).sum() / 20
    
    return precision
    
def compute_ndcg_at_20(candidates_csv, labeled_csv):
   
    candidates = pd.read_csv(candidates_csv)
    labeled = pd.read_csv(labeled_csv)
    merged = pd.merge(candidates, labeled, on =["lemma", "pos"])
    
    merged = merged.sort_values("raw_frequency", ascending= False)
   
    top_20 = merged.head(20)
    relevance_list= top_20["etiket"].tolist()
    dcg_gercek = dcg(relevance_list)
    
    ideal_siralama = merged.sort_values("etiket", ascending=False)
    ideal_top_20 = ideal_siralama.head(20)
    relevance_list_ideal = ideal_top_20["etiket"].tolist()
    idcg = dcg(relevance_list_ideal)

    if idcg == 0:
       return None   # havuzda hiç "1" etiketli kelime yoksa nDCG tanımsız
    nDCG = dcg_gercek / idcg
    return nDCG
  

if __name__ == "__main__":
    p = compute_precision_at_20(sys.argv[1], sys.argv[2])
    n = compute_ndcg_at_20(sys.argv[1], sys.argv[2])
    print(f"Precision@20: {p}")
    print(f"ncdg@20: {n}")