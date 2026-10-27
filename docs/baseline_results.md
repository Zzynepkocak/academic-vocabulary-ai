# Baseline Değerlendirme Sonuçları — Ham Frekans

**Tarih:** 2026-09-25
**Yöntem:** `annotation_guideline.md`'deki 4 adımlı kurala göre, 3 makalenin
her birinden ilk 100 aday kelime (frekansa göre) elle etiketlendi (`0`/`1`),
skor gizlenip satırlar karıştırılarak (anchoring bias önlemi). Precision@20
ve nDCG@20, `src/vocabulary/score_annotation.py` ile hesaplandı. nDCG@20,
Precision@20'nin göremediği bir şeyi ölçüyor: ilk 20'deki doğru kelimelerin
sadece *var olup olmadığını* değil, *ne kadar üst sıralarda* olduğunu da
ödüllendiriyor (IDCG, aynı 100'lük havuzun etikete göre mümkün en iyi
dizilişinden hesaplanıyor).

## Sonuçlar

| Makale | Konu | Etiketli havuzda "1" oranı (n=100) | Ham frekans P@20 | Ham frekans nDCG@20 | Rastgele beklenen P@20 | Fark (P@20) |
|---|---|---|---|---|---|---|
| airplane_wings | Uçak kanadı / popüler bilim | %28 | 0.20 | 0.16 | 0.28 | **−0.08** |
| coherent_states | Kuantum optik (akademik) | %47 | 0.55 | 0.54 | 0.47 | +0.08 |
| ecg_encryption | EKG + kaotik şifreleme | %36 | 0.45 | 0.43 | 0.36 | +0.09 |

## Yorum

Ham frekansa göre sıralamanın değeri, **metnin akademik kaydına göre değişiyor:**

- Yoğun akademik/teknik metinlerde (`coherent_states`, `ecg_encryption`),
  sık geçen kelimeler gerçekten öğrenmeye değer kelimelerle örtüşme
  eğiliminde — ham frekans rastgele seçimden daha iyi.
- Gündelik dile yakın, popüler bilim yazısında (`airplane_wings`), sık
  geçen kelimeler çoğunlukla konuya özgü ama zaten bilinen isimler
  (`wing`, `flight`, `airfoil`) — ham frekans burada **rastgele seçimden
  daha kötü** sonuç veriyor.

nDCG@20, bu tabloya ikinci bir boyut ekliyor: `coherent_states` ve
`ecg_encryption`'da nDCG, Precision'a çok yakın (fark ≤0.02) — yani
yakalanan doğru kelimeler ilk 20 içinde de makul sıralarda duruyor.
`airplane_wings`'te ise fark daha büyük (0.04, oransal olarak ~%20'lik bir
düşüş) — az sayıdaki doğru kelime, aynı zamanda ilk 20'nin **geç
sıralarına** düşmüş durumda. Yani ham frekans popüler bilim metninde hem
daha az doğru kelime yakalıyor hem de yakaladıklarını daha kötü konumluyor.

Bu, projenin en başından beri kabul ettiği "hard word ≠ important word"
prensibinin ölçülmüş bir kanıtı: tek başına frekans, güvenilir bir
öğrenmeye-değerlik göstergesi değil, metnin türüne bağlı — hem miktar
(Precision) hem de sıralama kalitesi (nDCG) açısından.

## Sınırlamalar

- Örneklem küçük (makale başına 100 aday, ilk 20'ye bakılıyor) — P@20 ve
  nDCG@20 değerleri birkaç satırlık etiket farkıyla belirgin oynayabilir.
- Tek etiketleyici (proje sahibi) — inter-rater reliability yok.
- 3 makale, tek bir alan (YÖKDİL Fen) içinde ama üç farklı akademik
  kayıt seviyesini temsil ediyor; genel bir iddia için yetersiz, ama
  yön göstermek için yeterli.
- nDCG@20 için rastgele-seçim beklenen değeri hesaplanmadı (Precision@20'de
  yapılan random baseline simülasyonu nDCG'ye henüz uygulanmadı) — bu
  yüzden nDCG sütununda sadece ham frekans değerleri var, bir karşılaştırma
  ölçütü yok. İleride gerekirse eklenebilir.

## Bu sonucun kullanımı

Stage 10'da kurulacak gerçek öncelik skoru (CEFR + akademik frekans +
diğer sinyaller), bu üç makalede yukarıdaki ham-frekans P@20 ve nDCG@20
değerlerini **geçmelidir**. Geçmiyorsa, eklenen karmaşıklık
gerekçesizdir (bkz. `PROJECT_SPEC.md` Bölüm 8).
