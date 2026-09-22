import pandas as pd
from collections import Counter

def extract_candidates(doc):
 
    sayac = Counter()
    for token in doc:
        if token.is_alpha and not token.is_stop and token.pos_ in {"NOUN","VERB","ADJ", "ADV"}:
            sayac[(token.lemma_, token.pos_)] += 1

    satirlar = [(lemma, pos, adet) for (lemma, pos), adet in sayac.items()]
    df = pd.DataFrame(satirlar, columns=['lemma', 'pos', 'raw_frequency'])

    df['normalized_frequency'] = df['raw_frequency'] / len(doc)
    df['is_candidate'] = True
    df = df.sort_values("raw_frequency", ascending=False)

    return df
    