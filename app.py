import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Course Recommender", layout="wide")
st.title("📚 AI Course Recommendation System (Optimized)")

# 1. Load Optimized Models
@st.cache_resource
def load_models():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, 'models')
    
    try:
        # Load the dictionary and the dataframe
        rec_dict = joblib.load(os.path.join(models_dir, 'recommendation_dict.pkl'))
        df = joblib.load(os.path.join(models_dir, 'content_df.pkl'))
        return rec_dict, df
    except FileNotFoundError:
        st.error("Model files not found. Please run 'optimize_model.py' first.")
        return None, None

recommendation_dict, content_df = load_models()

# 2. Recommendation Function (Lookup Strategy)
def get_recommendations(course_id):
    # Simply look up the ID in our pre-calculated dictionary
    if course_id in recommendation_dict:
        similar_ids = recommendation_dict[course_id]
        # Filter the dataframe to show these courses
        return content_df[content_df['course_id'].isin(similar_ids)]
    else:
        return None

# 3. User Interface
if content_df is not None:
    # Sidebar
    st.sidebar.header("Select a Course")
    
    # Create dropdown list
    course_options = content_df['course_name'] + " (ID: " + content_df['course_id'].astype(str) + ")"
    selected_option = st.sidebar.selectbox("Choose a course you liked:", course_options)

    if st.sidebar.button("Recommend"):
        # Extract ID
        selected_id = int(selected_option.split("ID: ")[1].replace(")", ""))
        
        # Get results
        results = get_recommendations(selected_id)
        
        if results is not None:
            st.subheader(f"Top Recommendations for: {selected_option.split(' (ID')[0]}")
            
            # Display results
            for _, row in results.iterrows():
                with st.container():
                    st.markdown("---")
                    c1, c2, c3 = st.columns([2, 1, 1])
                    c1.markdown(f"**{row['course_name']}**")
                    c1.caption(f"Instructor: {row['instructor']}")
                    c2.write(f"Level: {row['difficulty_level']}")
                    c3.write(f"Price: ${row['course_price']}")
        else:
            st.warning("No recommendations found for this course.")