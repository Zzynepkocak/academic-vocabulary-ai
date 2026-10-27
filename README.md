# Academic Vocabulary AI

Akademik bir İngilizce makalenin (PDF) içinden, YÖKDİL'e hazırlanan biri için öğrenmeye değebilecek kelime adaylarını çıkaran ve bu adayların sıralama kalitesini ölçen bir Python projesi. Kişisel öğrenme ve portfolyo projesidir, ticari değildir.

Proje, "sık geçen kelime öğrenmeye değer kelimedir" varsayımını test etmek için kuruldu. Bu varsayımın her makale türünde doğru olmadığı ölçüldü (bkz. [Sonuçlar](#sonuçlar)).

## Şu an ne yapıyor

1. **PDF'ten metin çıkarır.** PyMuPDF ile okur, ligatürleri (`ﬂ` → `fl`) düzeltir, sayfa numarası gibi artıkları temizler.
2. **Metni işler.** spaCy ile cümlelere, token'lara, lemma'lara ve kelime türlerine ayırır.
3. **Aday kelime tablosu üretir.** Durak sözcükleri ve noktalama işaretlerini eler, yalnızca isim, fiil, sıfat ve zarfları tutar. Her `(lemma, pos)` çifti için ham ve normalize sıklığı hesaplar.
4. **Elle etiketleme için dosya hazırlar.** İlk 100 adayı karıştırır, skorları gizler, boş bir `etiket` sütunu ekler.
5. **Sıralamayı ölçer.** Etiketli dosyadan Precision@20 ve nDCG@20 hesaplar.
6. **Akademik kelime listesini okuyabilir.** Academic Vocabulary List'i (AVL) `lemma, pos, academic_frequency, academic_ratio` tablosuna çevirir. Bu tablo henüz ana pipeline'a bağlı değil.

## Kurulum

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Kullanım

Aday tablosu üretmek için (PDF'i `data/` klasörüne koy):

```
python -m src.pipeline data/makale.pdf
```

İlk 20 aday ekrana yazılır, tablonun tamamı `makale_candidates.csv` olarak kaydedilir. Sütunlar:

```
lemma | pos | raw_frequency | normalized_frequency | is_candidate
```

Etiketleme dosyası hazırlamak:

```
python -m src.vocabulary.prepare_annotation makale_candidates.csv makale_to_label.csv
```

`etiket` sütununu elle doldur (`1` = öğrenmeye değer, `0` = değmez), sonra `makale_labeled.csv` olarak kaydet. Kurallar için [`docs/annotation_guideline.md`](docs/annotation_guideline.md).

Skoru hesaplamak:

```
python -m src.vocabulary.score_annotation makale_candidates.csv makale_labeled.csv
```

## Sonuçlar

Üç arXiv makalesinde, her birinin ilk 100 adayı elle etiketlendi. Aday listesi ham frekansa göre sıralandı. Ayrıntılar ve yöntem: [`docs/baseline_results.md`](docs/baseline_results.md).

| Makale | Konu | Ham frekans P@20 | Ham frekans nDCG@20 | Rastgele beklenen P@20 |
|---|---|---|---|---|
| airplane_wings | Popüler bilim | 0,20 | 0,16 | 0,28 |
| coherent_states | Kuantum optik | 0,55 | 0,54 | 0,47 |
| ecg_encryption | EKG + şifreleme | 0,45 | 0,43 | 0,36 |

Ham frekans, yoğun akademik metinlerde rastgele seçimden iyi, popüler bilim metninde rastgele seçimden kötü çıktı. Yani sıklık tek başına güvenilir bir ölçüt değil, metnin türüne bağlı.

## Veri kaynakları

- **Academic Vocabulary List (AVL)**, Gardner & Davies (2014), "A New Academic Vocabulary List", *Applied Linguistics* 35(3). Liste [academicwords.info](https://www.academicwords.info) adresinden indirilir ("Academic core" dosyası). Sitenin koşulu gereği liste **bu repoda yer almaz**. Kullanmak için dosyayı kendin indirip `data/` klasörüne koy (`data/acadCore.xlsx`). Liste yalnızca akademik, ticari olmayan kullanım içindir.
- **arXiv makaleleri** test için yerelde kullanıldı, repoya dahil değil.

`data/` klasörü `.gitignore`'dadır.

## Klasör yapısı

```
src/
  pdf/          PDF'ten metin çıkarma ve temizleme
  nlp/          spaCy ile metin işleme
  vocabulary/   aday çıkarma, AVL okuma, etiketleme ve skor araçları
  pipeline.py   PDF'ten aday tablosuna uçtan uca akış
docs/
  PROJECT_SPEC.md          proje tanımı ve kararlar
  annotation_guideline.md  etiketleme kuralları
  baseline_results.md      değerlendirme sonuçları
```

## Bilinen sınırlamalar

- Değerlendirme küçük: 3 makale, makale başına 100 aday, tek etiketleyici.
- Yalnızca İngilizce, metin katmanı olan PDF'lerle denendi. Taranmış (görüntü) PDF'ler desteklenmiyor.
- Başlık satırları bazen sonraki paragrafla aynı cümle olarak bölünüyor.
- Çok kelimeli ifadeler (collocation) henüz ele alınmıyor, yalnızca tek kelimeler.

## Daha fazlası

Proje tanımı, kapsam kararları ve açık sorular için [`docs/PROJECT_SPEC.md`](docs/PROJECT_SPEC.md).
