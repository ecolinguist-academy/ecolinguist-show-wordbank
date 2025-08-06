import glob
import pandas as pd
import streamlit as st

# ——— Robust loader that skips bad CSVs ———
@st.cache_data
def load_wordbank():
    tables = []
    for path in glob.glob("data/*.csv"):
        try:
            df = pd.read_csv(path)
        except Exception as e:
            st.warning(f"Could not read {path}: {e}")
            continue

        # If fewer than 2 columns, skip
        if len(df.columns) < 2:
            st.warning(f"Skipped {path}: needs ≥2 columns (found {len(df.columns)})")
            continue

        # Keep only first two columns and rename
        df = df.iloc[:, :2]
        df.columns = ["Language", "Word"]
        tables.append(df)

    if tables:
        return pd.concat(tables, ignore_index=True)
    return pd.DataFrame(columns=["Language", "Word"])

# Load the wordbank
df = load_wordbank()

# ——— Page config & header ———
st.set_page_config(page_title="Ecolinguist Show Wordbank", layout="wide")
st.title("📚 Ecolinguist Show Wordbank")
st.markdown("Search words used in past episodes and avoid repetition.")

# ——— Sidebar: language selection ———
languages = sorted(df["Language"].unique())
lang = st.sidebar.selectbox("🔤 Select language", languages)

# ——— Main: word lookup UI ———
st.subheader(f"Check a word in **{lang}** episodes")
query = st.text_input("Enter the word to check:")

if query:
    hits = df[
        (df["Language"] == lang) &
        (df["Word"].str.lower() == query.strip().lower())
    ]
    if not hits.empty:
        st.success(f"✅ **'{query}'** was used in **{lang}** episodes.")
        st.dataframe(hits)
    else:
        st.warning(f"❌ **'{query}'** has **not** been used yet.")

# ——— Expander: full list for the selected language ———
with st.expander(f"📖 All words in {lang}"):
    st.dataframe(
        df[df["Language"] == lang]
          .sort_values("Word")
          .reset_index(drop=True)
    )
