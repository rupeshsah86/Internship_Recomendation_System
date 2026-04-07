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

# Download required NLTK data
for resource in ['stopwords', 'wordnet', 'punkt']:
    nltk.download(resource, quiet=True)

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Internship Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { font-size: 2.2rem; margin: 0; }
    .main-header p  { font-size: 1rem; margin: 0.4rem 0 0; opacity: 0.9; }

    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .metric-card h3 { font-size: 1.8rem; color: #667eea; margin: 0; }
    .metric-card p  { color: #64748b; margin: 0.2rem 0 0; font-size: 0.85rem; }

    .match-excellent { color: #16a34a; font-weight: 600; }
    .match-good      { color: #d97706; font-weight: 600; }
    .match-fair      { color: #2563eb; font-weight: 600; }

    .chat-bubble-user {
        background: #667eea;
        color: white;
        padding: 0.7rem 1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.4rem 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.92rem;
    }
    .chat-bubble-bot {
        background: #f1f5f9;
        color: #1e293b;
        padding: 0.7rem 1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.4rem 0;
        max-width: 80%;
        font-size: 0.92rem;
        border-left: 3px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover { opacity: 0.9; }
</style>
""", unsafe_allow_html=True)


# ─── Class Definitions ───────────────────────────────────────────────────────
class DataPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        words = [self.lemmatizer.lemmatize(w) for w in text.split() if w not in self.stop_words]
        return ' '.join(words)


class StudentProfile:
    def __init__(self):
        self.skills = []
        self.preferred_locations = []
        self.preferred_duration = None
        self.min_stipend = 0
        self.interests = []

    def set_skills(self, skills):           self.skills = skills
    def set_preferred_locations(self, l):   self.preferred_locations = l
    def set_preferred_duration(self, d):    self.preferred_duration = d
    def set_min_stipend(self, s):           self.min_stipend = s
    def set_interests(self, i):             self.interests = i


class ImportedRecommender:
    def __init__(self, data, tfidf_vectorizer, feature_matrix):
        self.data = data
        self.tfidf_vectorizer = tfidf_vectorizer
        self.feature_matrix = feature_matrix
        self.preprocessor = DataPreprocessor()

    def get_profile_features(self, student_profile):
        combined_text = (
            ' '.join(student_profile.interests) + ' ' +
            ' '.join(student_profile.skills) + ' ' +
            ' '.join(student_profile.preferred_locations)
        )
        cleaned_text = self.preprocessor.clean_text(combined_text)
        return self.tfidf_vectorizer.transform([cleaned_text])

    def recommend(self, student_profile, top_n=10):
        profile_features = self.get_profile_features(student_profile)
        cosine_similarities = cosine_similarity(profile_features, self.feature_matrix).flatten()
        similar_indices = cosine_similarities.argsort()[:-top_n-1:-1]
        recommendations = self.data.iloc[similar_indices].copy()
        recommendations['similarity_score'] = cosine_similarities[similar_indices]
        if student_profile.preferred_duration:
            recommendations = recommendations[
                recommendations['duration_numeric'] <= student_profile.preferred_duration
            ]
        if student_profile.min_stipend > 0:
            recommendations = recommendations[
                recommendations['stipend_numeric'] >= student_profile.min_stipend
            ]
        return recommendations.head(top_n)


# ─── Model Loading ───────────────────────────────────────────────────────────
@st.cache_resource
def load_recommender():
    try:
        processed_df = joblib.load('internship_recommender_data_20251025_072624.pkl')
        loaded_components = joblib.load('internship_recommender_components_20251025_072624.pkl')
        tfidf_vectorizer = loaded_components['tfidf_vectorizer']
        feature_matrix = loaded_components['feature_matrix']
        return ImportedRecommender(processed_df, tfidf_vectorizer, feature_matrix)
    except FileNotFoundError:
        st.error("Model files not found. Ensure .pkl files are in the project folder.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred during model loading: {e}")
        st.stop()


# ─── Chatbot Logic ───────────────────────────────────────────────────────────
def get_bot_response(user_input, recommender):
    msg = user_input.lower().strip()

    # ── Greetings
    if any(w in msg for w in ['hi', 'hello', 'hey', 'good morning', 'good evening']):
        return "👋 Hello! I'm your AI Internship Assistant. Ask me anything about this app, how it works, or internship opportunities!"

    # ── What is this app
    if any(w in msg for w in ['what is this', 'about this app', 'what does this do', 'purpose', 'this project']):
        return (
            "🎯 **AI-Powered Internship Recommender**\n\n"
            "This app uses Machine Learning to match students with the most relevant internship opportunities "
            "based on their skills, interests, location, stipend, and duration preferences.\n\n"
            "It uses **TF-IDF Vectorization** + **Cosine Similarity** to rank internships by relevance to your profile."
        )

    # ── How it works / algorithm
    if any(w in msg for w in ['how does it work', 'algorithm', 'how it works', 'tfidf', 'cosine', 'ml', 'machine learning', 'model']):
        return (
            "🤖 **How the Recommendation Engine Works:**\n\n"
            "1. Your skills & interests are cleaned using NLP (lemmatization, stopword removal)\n"
            "2. Text is converted to a numeric vector using **TF-IDF** (up to 1000 features)\n"
            "3. **Cosine Similarity** measures how close your profile is to each internship\n"
            "4. Results are filtered by stipend, duration, and location\n"
            "5. Top matches are ranked and displayed with a similarity score"
        )

    # ── How to use
    if any(w in msg for w in ['how to use', 'how do i', 'steps', 'guide', 'get started', 'use this']):
        return (
            "📋 **How to Use the App:**\n\n"
            "1. Go to the **🔍 Recommendations** tab\n"
            "2. Fill in your **Skills & Interests** in the sidebar\n"
            "3. Set your **preferred location**, **minimum stipend**, and **max duration**\n"
            "4. Choose how many results you want (5–20)\n"
            "5. Click **Find Internships** and get your personalized matches!"
        )

    # ── Similarity score / match quality
    if any(w in msg for w in ['score', 'similarity', 'excellent', 'good match', 'fair', 'match']):
        return (
            "📊 **Understanding Match Scores:**\n\n"
            "| Score | Label | Meaning |\n"
            "|-------|-------|---------|\n"
            "| > 0.7 | 🟢 Excellent | Highly relevant to your profile |\n"
            "| 0.4–0.7 | 🟠 Good | Moderately relevant |\n"
            "| < 0.4 | 🔵 Fair | Less relevant but still a match |"
        )

    # ── Dataset / internships info
    if any(w in msg for w in ['dataset', 'data', 'how many internship', 'total internship', 'internships available']):
        total = len(recommender.data)
        locations = recommender.data['location'].nunique() if 'location' in recommender.data.columns else 'N/A'
        return (
            f"📦 **Dataset Info:**\n\n"
            f"- Total internships: **{total}**\n"
            f"- Unique locations: **{locations}**\n"
            f"- Columns: internship title, company, location, duration, stipend\n"
            f"- Data is preprocessed with NLP before matching"
        )

    # ── Stipend related
    if any(w in msg for w in ['stipend', 'salary', 'pay', 'money', 'paid']):
        if 'stipend_numeric' in recommender.data.columns:
            avg = recommender.data['stipend_numeric'].mean()
            max_s = recommender.data['stipend_numeric'].max()
            return (
                f"💰 **Stipend Insights:**\n\n"
                f"- Average stipend: **₹{avg:,.0f}/month**\n"
                f"- Highest stipend: **₹{max_s:,.0f}/month**\n"
                f"- You can filter by minimum stipend using the sidebar slider"
            )
        return "💰 Stipend data is available. Use the sidebar slider to filter by minimum expected stipend."

    # ── Location related
    if any(w in msg for w in ['location', 'remote', 'work from home', 'wfh', 'city', 'bangalore', 'delhi', 'mumbai']):
        if 'location' in recommender.data.columns:
            top_locs = recommender.data['location'].value_counts().head(5).index.tolist()
            return (
                f"📍 **Location Info:**\n\n"
                f"Top locations in the dataset: **{', '.join(top_locs)}**\n\n"
                f"You can enter your preferred location in the sidebar (e.g., 'Work From Home', 'Bangalore')."
            )

    # ── Duration related
    if any(w in msg for w in ['duration', 'months', 'how long', 'period']):
        return (
            "⏱️ **Duration Info:**\n\n"
            "Internship durations typically range from **1 to 12 months**.\n"
            "Use the **Maximum Duration** slider in the sidebar to filter results."
        )

    # ── Technologies / skills
    if any(w in msg for w in ['python', 'java', 'skills', 'technology', 'tech', 'programming', 'web', 'data science', 'marketing']):
        return (
            "💻 **Skills & Technologies:**\n\n"
            "You can enter any skills in the sidebar such as:\n"
            "- Programming: Python, Java, JavaScript, C++\n"
            "- Data: Machine Learning, Data Science, SQL\n"
            "- Others: Digital Marketing, Graphic Design, Finance\n\n"
            "The more specific your skills, the better your matches!"
        )

    # ── Help
    if any(w in msg for w in ['help', 'support', 'issue', 'problem', 'error', 'not working']):
        return (
            "🛠️ **Troubleshooting Help:**\n\n"
            "- **No results?** Try lowering the stipend or increasing the duration\n"
            "- **Module error?** Run `pip install -r requirements.txt`\n"
            "- **Pickle error?** Ensure all `.pkl` files are in the project folder\n"
            "- **Memory issues?** Reduce TF-IDF max_features in the model"
        )

    # ── Thanks
    if any(w in msg for w in ['thank', 'thanks', 'great', 'awesome', 'nice', 'good']):
        return "😊 You're welcome! Feel free to ask anything else about the app or internships."

    # ── Bye
    if any(w in msg for w in ['bye', 'goodbye', 'exit', 'quit']):
        return "👋 Goodbye! Best of luck with your internship search! 🚀"

    # ── Default fallback
    return (
        "🤔 I'm not sure about that. Here are some things you can ask me:\n\n"
        "- *What is this app?*\n"
        "- *How does the algorithm work?*\n"
        "- *How do I use this app?*\n"
        "- *How many internships are available?*\n"
        "- *What do the match scores mean?*\n"
        "- *Tell me about stipends / locations / duration*"
    )


# ─── Load Model ──────────────────────────────────────────────────────────────
recommender = load_recommender()

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🎓 AI-Powered Internship Recommender</h1>
    <p>Find your perfect internship using Machine Learning & NLP</p>
</div>
""", unsafe_allow_html=True)

# ─── Metrics Row ─────────────────────────────────────────────────────────────
total_internships = len(recommender.data)
unique_companies = recommender.data['company_name'].nunique() if 'company_name' in recommender.data.columns else 'N/A'
unique_locations = recommender.data['location'].nunique() if 'location' in recommender.data.columns else 'N/A'

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><h3>{total_internships}</h3><p>Total Internships</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h3>{unique_companies}</h3><p>Companies</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><h3>{unique_locations}</h3><p>Locations</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><h3>TF-IDF</h3><p>AI Algorithm</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🔍 Recommendations", "🤖 AI Assistant"])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    # Sidebar
    st.sidebar.markdown("## ⚙️ Your Preferences")
    st.sidebar.markdown("---")

    interests = st.sidebar.text_area(
        "🧠 Skills & Interests",
        "Python, Machine Learning, Web Development",
        help="Enter keywords relevant to the internship you are looking for."
    )
    location = st.sidebar.text_input(
        "📍 Preferred Location",
        "Work From Home",
        help="Enter preferred locations separated by commas."
    )
    min_stipend = st.sidebar.slider(
        "💰 Minimum Stipend (₹/month)",
        min_value=0, max_value=50000, value=5000, step=1000
    )
    max_duration = st.sidebar.slider(
        "⏱️ Maximum Duration (Months)",
        min_value=1, max_value=12, value=6, step=1
    )
    top_n = st.sidebar.slider(
        "📊 Number of Results",
        min_value=5, max_value=20, value=10, step=1
    )

    st.sidebar.markdown("---")
    find_btn = st.sidebar.button("🚀 Find Internships", type="primary", use_container_width=True)

    if find_btn:
        profile = StudentProfile()
        profile.set_interests([i.strip() for i in interests.split(',') if i.strip()])
        profile.set_preferred_locations([l.strip() for l in location.split(',') if l.strip()])
        profile.set_min_stipend(min_stipend)
        profile.set_preferred_duration(max_duration)

        with st.spinner('🔍 Finding the best internships for you...'):
            recommendations = recommender.recommend(profile, top_n=top_n)

        if recommendations.empty:
            st.warning("⚠️ No internships found matching your preferences. Try adjusting your filters.")
        else:
            st.success(f"✅ Found **{len(recommendations)}** matching internships for your profile!")
            st.markdown("---")

            for idx, row in recommendations.iterrows():
                score = row['similarity_score']
                if score > 0.7:
                    badge = "🟢 Excellent Match"
                    badge_class = "match-excellent"
                elif score >= 0.4:
                    badge = "🟠 Good Match"
                    badge_class = "match-good"
                else:
                    badge = "🔵 Fair Match"
                    badge_class = "match-fair"

                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"### {row.get('internship_title', 'N/A')}")
                        st.markdown(f"🏢 **{row.get('company_name', 'N/A')}** &nbsp;|&nbsp; 📍 {row.get('location', 'N/A')} &nbsp;|&nbsp; ⏱️ {row.get('duration', 'N/A')} &nbsp;|&nbsp; 💰 {row.get('stipend', 'N/A')}")
                    with c2:
                        st.markdown(f'<p class="{badge_class}" style="text-align:right; margin-top:1rem;">{badge}<br><small>Score: {score:.4f}</small></p>', unsafe_allow_html=True)
                    st.markdown("---")

            st.balloons()
    else:
        st.info("👈 Set your preferences in the sidebar and click **Find Internships** to get started.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHATBOT
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🤖 AI Internship Assistant")
    st.markdown("Ask me anything about this app, how it works, or internship data!")
    st.markdown("---")

    # Init chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "text": "👋 Hi! I'm your AI Internship Assistant. Ask me anything about this app or internships!"}
        ]

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">🧑 {msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">🤖 {msg["text"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Suggested questions
    st.markdown("**💡 Quick Questions:**")
    q_cols = st.columns(3)
    quick_questions = [
        "What is this app?",
        "How does the algorithm work?",
        "How do I use this app?",
        "How many internships are available?",
        "What do match scores mean?",
        "Tell me about stipends",
    ]
    for i, q in enumerate(quick_questions):
        with q_cols[i % 3]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "text": q})
                response = get_bot_response(q, recommender)
                st.session_state.chat_history.append({"role": "bot", "text": response})
                st.rerun()

    st.markdown("---")

    # User input
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            user_input = st.text_input("Type your message...", label_visibility="collapsed", placeholder="Ask me anything...")
        with col_send:
            send = st.form_submit_button("Send 📨", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})
        response = get_bot_response(user_input.strip(), recommender)
        st.session_state.chat_history.append({"role": "bot", "text": response})
        st.rerun()

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=False):
        st.session_state.chat_history = [
            {"role": "bot", "text": "👋 Hi! I'm your AI Internship Assistant. Ask me anything about this app or internships!"}
        ]
        st.rerun()
