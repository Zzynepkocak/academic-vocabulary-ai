# annotation_guideline.md

Bu doküman, aday kelime tablosunu (`candidates.csv`) elle etiketlerken
kullanılacak sabit kuralları tanımlar. Amaç: etiketleme sırasında kriterin
kaymaması, farklı makalelerde tutarlı karar verilmesi.

## Etiket

Her lemma için: `1` (öğrenmeye değer) veya `0` (değmez).

## Karar Sırası

Bir kelimeye şu sırayla bak, ilk uyan kuralda karar ver:

### Adım 1 — CEFR eşiği (biliniyor mu?)

- CEFR-J listesinde **A1 veya A2** ise → `0` (biliniyor sayılır, dur).
- Listede yoksa veya **B1 ve üzeri** ise → Adım 2'ye geç.

> Not: v0.1 pipeline'ında CEFR entegrasyonu henüz yok (Stage 8'de
> gelecek). Bu adımı şimdilik CEFR-J wordlist'ine elle bakarak uygula.

### Adım 2 — Çapraz-alan testi (alan terimi mi, genel bilim kelimesi mi?)

- Kelime **en az iki farklı bilim dalında** (fizik / kimya / matematik)
  genel bir kavramı ifade ediyorsa → genel bilim kelimesi → `1`.
- Kelime **tek bir alt dala özgü, dar teknik bir terimse** → `0`.

| Örnek | Karar | Gerekçe |
|---|---|---|
| `equilibrium` | 1 | fizik + kimyada da genel kavram |
| `coefficient` | 1 | matematik + fizikte genel kavram |
| `velocity` | 1 | fizikte genel, günlük dile de yakın ama akademik kullanımı farklı |
| `photosynthesis` | 0 | tek alt dala (biyokimya) özgü, Fen YÖKDİL'inde biyoloji ağırlığı düşük |
| `chloroplast` | 0 | dar teknik terim |

### Adım 3 — Akademik kayıt / sıklık kalıpları

Akademik bağlaç ve geçiş ifadeleri: CEFR eşiğinin altında kalanlar zaten
Adım 1'de elenir (`however`, `also` → A2 → `0`). Adım 2'ye kadar gelen
**nadir akademik eşdeğerler** için:

- Yaygın bir kelimenin daha resmi/akademik eşanlamlısıysa → `1`.

| Örnek | Karar | Gerekçe |
|---|---|---|
| `however` | 0 | Adım 1'de elenir (A2) |
| `notwithstanding` | 1 | `however`'ın nadir/akademik eşdeğeri, B2+ |
| `moreover` | 1 (sınırda) | B1/B2 sınırında, CEFR-J'de kontrol et |

### Adım 4 — Çok kelimeli ifadeler (ileriye dönük politika)

- **İngilizce kökenli** çok kelimeli akademik ifadeler (`play a crucial
  role`, `be associated with`) → kapsam **içinde** sayılır.
- **Latince/yabancı kökenli** ifadeler (`in vitro`, `a priori`) → kapsam
  **dışında**.

> ⚠️ Bu adım şu an **uygulanamıyor**: Stage 6 pipeline'ı yalnızca tek
> kelime (lemma) üretiyor, n-gram/collocation çıkarımı Stage 11'de
> gelecek. Bu kural, o aşamaya geldiğimizde geçerli olacak — şimdiden
> karar altına alınıyor ki unutulmasın.

## Etiketleme Prosedürü (Anchoring Bias'tan Kaçınma)

1. `candidates.csv`'yi aç.
2. Satırları karıştır (`df.sample(frac=1)`), skor sütununu **gizle**.
3. Her lemma'ya yukarıdaki 4 adımı sırayla uygulayıp etiket koy.
4. Bitince skoru geri göster, `Precision@20` / `nDCG@20` hesapla.

## Kapsam

Bu guideline v0.1 için **tek kelime (lemma)** etiketlemesini kapsar.
Adım 4'teki çok-kelimeli ifade politikası, Stage 11 pipeline'ı hazır
olduğunda tekrar gözden geçirilecek.
