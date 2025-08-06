import glob
import pandas as pd
import streamlit as st

# ——— Robust loader to skip bad CSVs ———
@st.cache_data
def load_wordbank():
    tables = []
    for path in glob.glob("data/*.csv"):
        df = pd.read_csv(path)
        # Skip files with fewer than 2 columns
        if len(df.columns) < 2:
            st.warning(f"Skipped {path}: needs ≥2 columns, found {len(df.columns)}")
            continue
        # Keep only first two columns and standardize names
        df = df.iloc[:, :2]
        df.columns = ["Language", "Word"]
        tables.append(df)
    if tables:
        return pd.concat(tables, ignore_index=True)
    # Fallback to empty DataFrame
    return pd.DataFrame(columns=["Language", "Word"])

# Load data
df = load_wordbank()

# ——— Page config & title ———
st.set_page_config(page_title="Ecolinguist Show Wordbank", layout="wide")
st.title("📚 Ecolinguist Show Wordbank")
st.markdown("Search words used in past episodes and avoid repetition.")

# ——— Sidebar: select language ———
languages = sorted(df["Language"].unique())
lang = st.sidebar.selectbox("🔤 Select language", languages)

# ——— Main: word lookup ———
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

# ——— Expander: show full list for that language ———
with st.expander(f"📖 All words in {lang}"):
    st.dataframe(
        df[df["Language"] == lang]
          .sort_values("Word")
          .reset_index(drop=True)
    )
