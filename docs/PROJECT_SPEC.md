# PROJECT_SPEC.md

## 1. Problem

YÖKDİL'e hazırlanan bir öğrenci, akademik bir makale okurken hangi kelime ve
ifadelerin öğrenmeye gerçekten değeceğini bilmiyor. "Zor kelime" ile "faydalı
kelime" aynı şey değildir — nadir bir C2 teknik terim, sık geçen bir B2
akademik ifadeden daha az işe yarayabilir.

Bu proje, bir akademik PDF'i girdi olarak alıp, öğrenmeye değer kelime ve
ifadeleri **ölçülebilir kriterlerle** önceliklendiren hibrit bir NLP + LLM
sistemi geliştirir.

## 2. Kapsam ve Amaç

- Bu bir **kişisel öğrenme ve portfolyo projesidir**, ticari ürün değildir.
- Birincil kullanıcı: proje sahibi (kendi YÖKDİL hazırlığı için).
- İkincil kullanıcı: küçük bir arkadaş grubu.
- Ölçek hedefi yok: çoklu kullanıcı, auth, production altyapısı MVP'de
  gerekmiyor.
- Teknoloji seçimi kuralı: gerçek bir problemi çözmüyorsa eklenmez
  (RAG, vector DB, mikroservis, Kubernetes şu an için hayır).

## 3. Hedef Alan

YÖKDİL **Fen Bilimleri** alanı seçildi. Bu, kelime kaynağını ve test
makalelerini fizik/kimya/matematik ağırlıklı tutmamız gerektiği anlamına
gelir (biyoloji değil).

## 4. Girdi / Çıktı

**Girdi:** Açık erişimli akademik PDF (arXiv, fizik/kimya/matematik).

**v0.1 (MVP) çıktısı — Stage 6 sınırı:**

```
lemma | POS | raw_frequency | normalized_frequency | document_frequency | is_candidate
```

CEFR, YÖKDİL skoru, LLM analizi, flashcard, quiz **v0.1 kapsamı dışında**.
Bunlar ayrı, ölçümü tamamlanmış aşamalar olarak sırayla eklenecek.

## 5. "Öğrenmeye Değer Kelime" Tanımı — Taslak

Kesin tanım, elle etiketleme sürecinde (bkz. Bölüm 8) netleştirilecek.
Başlangıç kriterleri:

- Kullanıcının muhtemelen bilmediği (bilinen kelime tabanı: TBD — örn. ilk
  3000 frekans bandı dışı)
- Akademik yazıda tekrar eden bir işlev görüyor (salt alan terimi değil)
- Bağlamdan bağımsız olarak başka akademik metinlerde de karşılaşılabilir

Sınır vakalar annotation guideline'da ayrıca ele alınacak: alan terimleri
(`photosynthesis` tarzı), çok bilinen ama akademik kalıp taşıyan kelimeler
(`however`), çok kelimeli birimler (`in vitro`, `data suggest that`).

## 6. YÖKDİL Verisi — Kısıt ve Karar

**Doğrulanmış kısıt:** ÖSYM, YÖKDİL sorularının yalnızca kamuya açık bir
bölümünü yayımlıyor; tam kitapçık adaylara sınırlı süreyle açılıyor ve
telif hakları ÖSYM'ye ait — çoğaltılamaz, dağıtılamaz. Bu nedenle çok yıllı,
dağıtılabilir bir "YÖKDİL frekans korpusu" kurulamaz.

**Karar:** Formüldeki `YÖKDİL_frequency` terimi yeniden adlandırılacak:
`academic_relevance` — açık akademik korpuslardan (AWL/AVL) ve genel
frekans kaynaklarından türetilecek. Bu, YÖKDİL'in ölçtüğü şeyin (alan
temelli akademik İngilizce) savunulabilir bir proxy'sidir. Gerçek YÖKDİL
sınav verisiyle doğrulama, yalnızca yerel/dağıtılamayan bir validation set
olarak (Bölüm 8) yapılabilir.

## 7. CEFR Verisi — Kaynak ve Sınırlamalar

**Kaynak adayı:** CEFR-J Wordlist (Yukio Tono, TUFS) + Octanove Vocabulary
Profile (C1/C2) — CC BY-SA 4.0 ile kullanılabilir. English Vocabulary
Profile'ın kendisi toplu indirilebilir bir veri seti olarak değil, arama
arayüzü olarak sunuluyor; bu yüzden birincil kaynak olarak kullanılamaz.

**Bilinen sınırlamalar (spec'e açıkça yazılıyor, gizlenmiyor):**

- CEFR seviyesi *anlama* aittir, kelimeye değil (`issue`: A2 "konu" vs. B2
  "yayımlamak"). Sistem lemma bazlı eşleşme yapacak — bu kabul edilen bir
  hata payı.
- Kapsam sınırlı: akademik makalede geçen birçok kelime (`mitigate`,
  `heterogeneity`) hiçbir CEFR listesinde bulunmayabilir. OOV
  (liste dışı) davranışı Stage 8'de ayrıca karara bağlanacak.

## 8. Değerlendirme Yöntemi (Success Criteria)

Sıralama algoritmasının gerçekten işe yarayıp yaramadığını ölçmeden ilerlemek
"arbitrary weights" problemine düşer. Bu yüzden:

- En az **3 makale** üzerinde, pipeline'ın ürettiği aday listesi elle
  etiketlenecek (`öğrenmeye değer / değmez`), skorlar gizlenerek
  (anchoring bias'tan kaçınmak için sıra karıştırılacak).
- Metrikler: Precision@20, nDCG@20.
- Baseline karşılaştırması zorunlu: ham frekans sıralaması ve rastgele
  sıralama. Geliştirilen skor bu baseline'ları yenmiyorsa, eklenen
  karmaşıklık gerekçesizdir.
- Etiketleme öncesi yazılı bir `docs/annotation_guideline.md` hazırlanacak
  (kriterin süreç içinde kaymaması için).

## 9. Veri ve Lisans Yönetimi

| Kaynak | Repoya girer mi? | Not |
|---|---|---|
| ÖSYM sınav metinleri | Hayır | Telif ÖSYM'de; sadece yerel, `.gitignore` |
| CEFR-J / Octanove wordlist | Evet (türetilmiş haliyle) | CC BY-SA 4.0 — ShareAlike, aynı lisansla paylaşılmalı |
| arXiv test makaleleri | Hayır (PDF olarak) | Lisans makaleye göre değişir; yalnızca yerel işlenir |
| Kullanıcı yüklediği özel PDF'ler | Hayır | `.gitignore`, asla commit edilmez |

Repo `LICENSE` (kod, MIT vb.) ve `data/LICENSES.md` (veri kaynakları ve
lisansları) olarak ikiye ayrılacak.

## 10. NLP vs LLM Sorumluluk Ayrımı

Orijinal proje dokümanındaki ayrım aynen geçerli: frekans, CEFR, akademik
sözlük eşleştirme, öncelik skoru gibi *ölçülebilir* işler deterministik
NLP ile yapılır. Bağlamsal anlam, örnek cümle, açıklama üretimi gibi
*üretici* işler LLM'e bırakılır. LLM, CEFR/YÖKDİL/frekans için ground truth
değildir.

## 11. v0.1 Teknoloji Seti (Kasıtlı Olarak Minimal)

`pymupdf`, `spacy`, `pandas`, `pytest`. Veritabanı, web arayüzü, LLM API,
RAG — hiçbiri v0.1'de yok. Her biri, kendi aşamasında, gerekçesiyle
birlikte eklenecek.

## 12. Geliştirici Profili Notu

Python'a yeni başlandı (tutorial seviyesi, henüz bağımsız proje
yazılmadı); terminal kullanımı rahat. Bu, ilerleme temposunu doğrudan
etkiler: her yeni kütüphane ilk kullanıldığında ayrıca açıklanacak, kod
küçük ve izole adımlarla yazılacak. Bu not, ileride spec'i okuyan biri
(ileride kendisi dahil) neden bazı aşamaların uzun sürdüğünü anlasın diye
buraya yazıldı.

## 13. Açık Kalan Kararlar

- Bilinen kelime tabanı eşiği (ör. ilk N frekans bandı) — annotation
  guideline yazılırken netleşecek.
- 3. test makalesi (çok sütunlu layout örneği) henüz seçilmedi.
- CEFR kaynağının kesin entegrasyon şekli — Stage 8'de.
