import glob
import pandas as pd
import streamlit as st

@st.cache_data
def load_wordbank():
    files = glob.glob("data/*.csv")
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        # Ensure consistent column names:
        df = df.rename(columns={df.columns[0]: "Language", df.columns[1]: "Word"})
        dfs.append(df[["Language", "Word"]])
    return pd.concat(dfs, ignore_index=True)

df = load_wordbank()

st.set_page_config(page_title="Ecolinguist Wordbank", layout="wide")
st.title("📚 Ecolinguist Show Wordbank")

# Sidebar for language selection
languages = sorted(df["Language"].unique())
lang = st.sidebar.selectbox("🔤 Select language", languages)

# Word lookup
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

# Show full list
with st.expander(f"📖 All words in {lang}"):
    st.dataframe(df[df["Language"] == lang].sort_values("Word").reset_index(drop=True))
