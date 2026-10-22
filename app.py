import streamlit as st
import pandas as pd
from recommender import OutfitCompletionEngine, demo_catalog

st.set_page_config(page_title="StyleComplete | Outfit Recommender", page_icon="👗", layout="wide")
st.title("StyleComplete")
st.subheader("Outfit Completion Engine")
st.write("Choose an item and discover complementary pieces. This public demo uses a small illustrative catalogue; it does not contain the full H&M dataset.")

@st.cache_data
def load_catalog():
    try:
        df = pd.read_csv("data/demo_articles.csv")
        if len(df) > 0:
            return df
    except Exception:
        pass
    return demo_catalog()

catalog = load_catalog()
engine = OutfitCompletionEngine(catalog)
col1, col2 = st.columns([1, 2])
with col1:
    category = st.selectbox("Filter by category", ["All"] + sorted(catalog["category"].unique().tolist()))
    choices = catalog if category == "All" else catalog[catalog["category"] == category]
    chosen_id = st.selectbox("Choose an item", choices["article_id"].tolist(),
        format_func=lambda x: f"{choices.loc[choices.article_id == x, 'name'].iloc[0]} · {choices.loc[choices.article_id == x, 'category'].iloc[0]}")
    top_k = st.slider("Recommendations", 3, 8, 5)
    go = st.button("Complete this outfit", type="primary", use_container_width=True)
with col2:
    selected = catalog[catalog.article_id == chosen_id].iloc[0]
    st.markdown(f"### {selected['name']}")
    st.write(f"**Category:** {selected['category']}  ·  **Colour:** {selected['colour']}  ·  **Style:** {selected['style']}")
    st.info("Demo mode: recommendations are ranked from category complementarity, colour, style and material metadata.")

if go:
    recs = engine.recommend(chosen_id, top_k=top_k)
    st.markdown("## Your complementary pieces")
    cols = st.columns(min(4, len(recs)))
    for i, (_, row) in enumerate(recs.iterrows()):
        with cols[i % len(cols)]:
            st.markdown(f"**{row['name']}**")
            st.caption(f"{row['category']} · {row['colour']}")
            st.write(row["description"])
            st.metric("Match score", f"{row['score']:.0%}")
st.divider()
st.caption("Portfolio prototype. Demo catalogue is illustrative; evaluate on an authorised dataset before claiming measured recommendation performance.")
