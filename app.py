import streamlit as st
from recommender import get_recommendations, movies, cosine_sim, all_titles

st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎬", layout="centered")

st.title("🎬 Movie Recommender")
st.markdown("Pick a movie you love and we'll find similar ones for you!")
st.divider()

# ── Input Section ─────────────────────────────────────────────────────────────
# Searchable dropdown with all movie titles
selected_movie = st.selectbox(
    "🔍 Search or select a movie:",
    options=all_titles,
    index=0,
    help="Start typing to search for a movie"
)

# Slider to control number of recommendations
num_recommendations = st.slider("How many recommendations do you want?", min_value=2,max_value=10,value =5)

# ── Recommendation Button ─────────────────────────────────────────────────────
if st.button("🎯 Get Recommendations", type="primary"):
    results = get_recommendations(selected_movie, movies, cosine_sim, top_n=num_recommendations)
    
    if len(results) == 0:
        st.error("Sorry, movie not found. Please try another title.")
    else:
        st.success(f"Because you liked **{selected_movie}**, you might also enjoy:")
        st.divider()
        
        # Display results as a styled table
        for i, (_, row) in enumerate(results.iterrows(), 1):
            col1, col2, col3 = st.columns([0.5, 3, 2])
            with col1:
                st.write(f"**{i}.**")
            with col2:
                st.write(f"**{row['title']}**")
            with col3:
                # Show genres as tags
                genres = row["genres"].split(" ")
                st.write(" • ".join(genres))
        
        st.divider()
        
        # Show raw dataframe for transparency
        with st.expander("📊 See similarity scores"):
            st.dataframe(
                results[["title", "similarity_score"]].reset_index(drop=True),
                use_container_width=True
            )