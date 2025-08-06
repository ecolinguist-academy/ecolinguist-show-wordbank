import glob
import pandas as pd
import streamlit as st

# ——— Load all CSVs from data/ ———
@st.cache_data
def load_wordbank():
    # Adjust the glob pattern if your files live elsewhere
    files = glob.glob("data/*.csv")
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        # Ensure consistent column names
        df = df.rename(columns={
            df.columns[0]: "Language",
            df.columns[1]: "Word"
        }).loc[:, ["Language", "Word"]]
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

df = load_wordbank()

# ——— UI ———
st.set_page_config(page_title="Ecolinguist Wordbank", layout="wide")
st.title("📚 Ecolinguist Show Wordbank")

# Language selector
languages = sorted(df["Language"].unique())
lang = st.sidebar.selectbox("🔤 Select language", languages)

# Word lookup
st.subheader(f"Check a word in **{lang}** episodes")
query = st.text_input("Enter the word to check:")

if query:
    # Filter by language + case-insensitive match
    hits = df[
        (df["Language"] == lang) &
        df["Word"].str.lower().eq(query.strip().lower())
    ]
    if not hits.empty:
        st.success(f"✅ **'{query}'** was used in **{lang}** episodes.")
        st.dataframe(hits)
    else:
        st.warning(f"❌ **'{query}'** has **not** been used (or spelled differently).")

# Optionally show full list for the selected language
with st.expander(f"📖 All words used in {lang}"):
    st.dataframe(df[df["Language"] == lang].sort_values("Word").reset_index(drop=True))
