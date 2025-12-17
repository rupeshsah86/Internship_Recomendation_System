import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# --- 1. Class Definitions (From your internship_recommender.ipynb) ---

# Note: The DataPreprocessor is necessary to clean the *user's input*
class DataPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        """Clean and preprocess text data for user input"""
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        words = text.split()
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        return ' '.join(words)

# Used to structure user input
class StudentProfile:
    def __init__(self):
        self.skills = []
        self.preferred_locations = []
        self.preferred_duration = None
        self.min_stipend = 0
        self.interests = []

    def set_skills(self, skills):
        self.skills = skills

    def set_preferred_locations(self, locations):
        self.preferred_locations = locations

    def set_preferred_duration(self, duration):
        self.preferred_duration = duration

    def set_min_stipend(self, stipend):
        self.min_stipend = stipend

    def set_interests(self, interests):
        self.interests = interests


# The core recommender class for deployment (based on Cell 13 logic)
class ImportedRecommender:
    def __init__(self, data, tfidf_vectorizer, feature_matrix):
        self.data = data
        self.tfidf_vectorizer = tfidf_vectorizer
        self.feature_matrix = feature_matrix
        self.preprocessor = DataPreprocessor() # Use for cleaning user input

    def get_profile_features(self, student_profile):
        """Converts a StudentProfile object into a feature vector."""
        combined_text = (
            ' '.join(student_profile.interests) + ' ' +
            ' '.join(student_profile.skills) + ' ' +
            ' '.join(student_profile.preferred_locations)
        )
        cleaned_text = self.preprocessor.clean_text(combined_text)
        profile_vector = self.tfidf_vectorizer.transform([cleaned_text])
        return profile_vector

    def recommend(self, student_profile, top_n=10):
        """Generates recommendations based on the student profile."""
        profile_features = self.get_profile_features(student_profile)
        cosine_similarities = cosine_similarity(profile_features, self.feature_matrix).flatten()

        # Get indices of the top N most similar internships
        similar_indices = cosine_similarities.argsort()[:-top_n-1:-1]

        # Get the recommended internships and their similarity scores
        recommendations = self.data.iloc[similar_indices].copy()
        recommendations['similarity_score'] = cosine_similarities[similar_indices]

        # Apply Hard Filters (Duration and Stipend)
        if student_profile.preferred_duration:
            recommendations = recommendations[
                recommendations['duration_numeric'] <= student_profile.preferred_duration
            ]
        if student_profile.min_stipend > 0:
            recommendations = recommendations[
                recommendations['stipend_numeric'] >= student_profile.min_stipend
            ]

        # Return the top N after filtering
        return recommendations.head(top_n)


# --- 2. Model Loading and Caching ---

@st.cache_resource
def load_recommender():
    """Load the pre-trained model components using joblib and initialize the recommender class."""
    try:
        # File names are taken from your upload:
        data_file = 'internship_recommender_data_20251025_072624.pkl'
        components_file = 'internship_recommender_components_20251025_072624.pkl'

        # 1. Load the processed data (DataFrame)
        processed_df = joblib.load(data_file)
        
        # 2. Load the TF-IDF components (Vectorizer and Feature Matrix)
        loaded_components = joblib.load(components_file)
        tfidf_vectorizer = loaded_components['tfidf_vectorizer']
        feature_matrix = loaded_components['feature_matrix'] # This should be the actual sparse matrix

        # 3. Initialize the deployment class
        recommender = ImportedRecommender(processed_df, tfidf_vectorizer, feature_matrix)

        return recommender

    except FileNotFoundError:
        st.error(f"One or more model files were not found. Please ensure the following files are in the same directory as 'streamlit_app.py': \n- {data_file} \n- {components_file}")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred during model loading: {e}")
        st.stop()


# --- 3. Streamlit Application Layout ---

# Load the recommender system
recommender = load_recommender()

st.title("Internship Recommender System 🎓")
st.markdown("Enter your preferences below to get the top matching internships.")
st.markdown("---")


# --- User Input Sidebar ---
st.sidebar.header("Your Preferences")

# Skills/Interests Input
interests = st.sidebar.text_area(
    "Skills & Interests (e.g., Python, Data Science, Digital Marketing)",
    "Python, Machine Learning, Web Development",
    help="Enter keywords relevant to the internship profile you are looking for."
)

# Preferred Location
location = st.sidebar.text_input(
    "Preferred Location (e.g., Bangalore, Work From Home)",
    "Work From Home",
    help="Enter one or more preferred locations separated by commas. Use 'Work From Home' for remote jobs."
)

# Minimum Stipend Filter
min_stipend = st.sidebar.slider(
    "Minimum Expected Stipend (per month)",
    min_value=0, max_value=50000, value=5000, step=1000,
    help="Only show internships with a stipend greater than or equal to this amount (0 for Unpaid)."
)

# Maximum Duration Filter
max_duration = st.sidebar.slider(
    "Maximum Duration (Months)",
    min_value=1, max_value=12, value=6, step=1,
    help="Only show internships with a duration less than or equal to this many months."
)

# Number of recommendations
top_n = st.sidebar.slider(
    "Number of Recommendations to Show",
    min_value=5, max_value=20, value=10, step=1
)

# Button to trigger recommendation
if st.sidebar.button("Find Internships", type="primary"):
    # Create the StudentProfile object from user input
    profile = StudentProfile()
    profile.set_interests([i.strip() for i in interests.split(',') if i.strip()])
    profile.set_preferred_locations([l.strip() for l in location.split(',') if l.strip()])
    profile.set_min_stipend(min_stipend)
    profile.set_preferred_duration(max_duration) # Use max_duration as the filter for recommend()

    st.header(f"Top {top_n} Internship Recommendations")

    # Generate recommendations
    with st.spinner('Searching for the best internships...'):
        recommendations = recommender.recommend(profile, top_n=top_n)

    if recommendations.empty:
        st.warning("No internships found matching your preferences. Try adjusting your filters.")
    else:
        st.success(f"Found **{len(recommendations)}** matching internships based on your profile and filters.")

        # Prepare DataFrame for display
        display_cols = [
            'internship_title',
            'company_name',
            'location',
            'duration',
        'stipend',
            'similarity_score'
        ]
        display_df = recommendations[display_cols].rename(columns={
            'internship_title': 'Internship Title',
            'company_name': 'Company',
            'location': 'Location',
            'duration': 'Duration',
            'stipend': 'Stipend',
            'similarity_score': 'Similarity Score (0.0 - 1.0)'
        })

        # Format Similarity Score for better reading
        display_df['Similarity Score (0.0 - 1.0)'] = display_df['Similarity Score (0.0 - 1.0)'].map('{:.4f}'.format)

        st.dataframe(display_df, use_container_width=True)
        st.balloons()

else:
    st.info("Please set your preferences in the sidebar and click **Find Internships** to get started.")