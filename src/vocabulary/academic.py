import pandas as pd


def load_academic_list(file_path):
    df = pd.read_excel(file_path, sheet_name="list")

    eslesme = {"n": "NOUN", "v": "VERB", "j":"ADJ","r": "ADV"}
    df["PoS"] = df["PoS"].map(eslesme)
    df = df.rename(columns={"word": "lemma", "COCA-Acad": "academic_frequency", "ratio": "academic_ratio", "PoS": "pos"})

    return df[["lemma", "pos", "academic_frequency", "academic_ratio"]]

test_df = load_academic_list("data/acadCore.xlsx")
print(test_df["pos"].isna().sum())