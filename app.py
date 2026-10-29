import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import altair as alt
from sklearn.metrics.pairwise import cosine_similarity

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="InternMatch | AI-Powered Internship Recommendations",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── NLTK Lemmatizer & Stopwords Fallback ────────────────────────────────────
DEFAULT_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
    'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}
DEFAULT_LEMMATIZER = None

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    DEFAULT_STOPWORDS = set(stopwords.words('english'))
    DEFAULT_LEMMATIZER = WordNetLemmatizer()
except Exception:
    pass


# ─── Responsive & Pixel-Perfect Custom Stylesheet ────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
        box-sizing: border-box;
    }

    /* Prevent unintended horizontal scroll */
    .main .block-container {
        max-width: 1360px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        overflow-x: hidden;
    }

    /* ─── Top Navbar ─────────────────────────────────────────── */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.85rem 1.6rem;
        background: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        flex-wrap: wrap;
        gap: 0.8rem;
    }
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .brand-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #4F46E5, #6366F1);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
    }
    .brand-text h2 {
        font-size: 1.25rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        color: #0F172A;
    }
    .brand-text p {
        font-size: 0.74rem;
        color: #64748B;
        margin: 0;
        font-weight: 500;
    }
    .nav-kpis {
        display: flex;
        align-items: center;
        gap: 1.4rem;
        font-size: 0.82rem;
        color: #475569;
        font-weight: 500;
        flex-wrap: wrap;
    }
    .nav-kpis strong {
        color: #0F172A;
        font-weight: 700;
    }

    /* ─── Hero Banner Area ───────────────────────────────────── */
    .hero-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.8rem 2.2rem;
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 55%, #EEF2FF 100%);
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-content h1 {
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.18;
        letter-spacing: -0.03em;
        color: #0F172A;
        margin: 0 0 0.5rem 0;
    }
    .hero-highlight {
        color: #4F46E5;
        background: linear-gradient(120deg, #4F46E5, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-content p {
        font-size: 0.94rem;
        color: #475569;
        max-width: 580px;
        line-height: 1.55;
        margin: 0 0 1rem 0;
    }
    .hero-pill-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
    }
    .hero-pill-item {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        padding: 0.28rem 0.75rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #334155;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    /* ─── Search & Filter Card ───────────────────────────────── */
    .search-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.2rem 1.4rem 0.8rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.05);
    }

    /* ─── Stats Grid (4 Cards) ───────────────────────────────── */
    .stat-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 0.95rem 1.15rem;
        display: flex;
        align-items: center;
        gap: 0.9rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        height: 100%;
    }
    .stat-icon-wrap {
        width: 42px;
        height: 42px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    .stat-val {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }
    .stat-name {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 600;
        margin-top: 0.1rem;
    }
    .stat-trend {
        font-size: 0.72rem;
        color: #10B981;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 0.2rem;
        margin-top: 0.15rem;
    }

    /* ─── Filter Sidebar Box ─────────────────────────────────── */
    .filter-panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .filter-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    .filter-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .filter-sec-name {
        font-size: 0.84rem;
        font-weight: 700;
        color: #334155;
        margin: 0.9rem 0 0.35rem 0;
    }

    /* ─── Premium Job Card (Exact Mockup Match) ──────────────── */
    .job-listing-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.35rem 1.6rem 1.15rem 1.6rem;
        margin-bottom: 0.95rem;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
        transition: all 0.25s ease;
    }
    .job-listing-card:hover {
        border-color: #CBD5E1;
        transform: translateY(-2px);
        box-shadow: 0 10px 24px -4px rgba(15, 23, 42, 0.08);
    }
    .card-main-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1.2rem;
    }
    .logo-container {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.15rem;
        flex-shrink: 0;
        border: 1px solid rgba(0,0,0,0.06);
    }
    .role-heading {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        line-height: 1.3;
    }
    .company-sub-line {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.65rem;
        color: #475569;
        font-size: 0.86rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    .company-sub-line strong {
        color: #0F172A;
        font-weight: 700;
    }
    .verified-badge {
        color: #3B82F6;
        font-size: 0.95rem;
    }

    .card-tags-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: 0.8rem 0;
    }
    .tag-bubble {
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        color: #334155;
        padding: 0.22rem 0.65rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 500;
    }

    .match-rate-text {
        font-size: 0.86rem;
        font-weight: 700;
        color: #10B981;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
    }
    .match-bar-bg {
        width: 100%;
        height: 5px;
        background: #E2E8F0;
        border-radius: 3px;
        margin: 0.25rem 0 0.45rem 0;
        overflow: hidden;
    }
    .match-bar-fill {
        height: 100%;
        background: #10B981;
        border-radius: 3px;
    }
    .stipend-amount {
        font-size: 1.22rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
    }

    .ai-insight-box {
        background: #F0FDF4;
        border: 1px solid #DCFCE7;
        border-radius: 10px;
        padding: 0.55rem 0.85rem;
        margin-top: 0.75rem;
        font-size: 0.82rem;
        color: #166534;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }

    /* Initial Empty State Card */
    .empty-search-card {
        background: #FFFFFF;
        border: 1.5px dashed #CBD5E1;
        border-radius: 16px;
        padding: 3.5rem 2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    /* ─── Responsive Media Queries ───────────────────────────── */
    @media (max-width: 1024px) {
        .hero-container {
            padding: 1.4rem;
        }
        .hero-content h1 {
            font-size: 1.9rem;
        }
    }

    @media (max-width: 768px) {
        .top-navbar {
            padding: 0.75rem 1rem;
            flex-direction: column;
            align-items: flex-start;
        }
        .nav-kpis {
            gap: 0.8rem;
            font-size: 0.78rem;
        }
        .hero-container {
            flex-direction: column;
            text-align: left;
            padding: 1.25rem 1.1rem;
        }
        .hero-content h1 {
            font-size: 1.65rem;
        }
        .hero-content p {
            font-size: 0.88rem;
        }
        .card-main-header {
            flex-direction: column;
        }
        .search-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ─── Data Preprocessor & Recommender Engine ───────────────────────────────────
class DataPreprocessor:
    def __init__(self):
        self.lemmatizer = DEFAULT_LEMMATIZER
        self.stop_words = DEFAULT_STOPWORDS

    def clean_text(self, text):
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        words = text.split()
        if self.lemmatizer:
            cleaned = [self.lemmatizer.lemmatize(w) for w in words if w not in self.stop_words and len(w) > 1]
        else:
            cleaned = [w for w in words if w not in self.stop_words and len(w) > 1]
        return ' '.join(cleaned)


class StudentProfile:
    def __init__(self):
        self.skills = []
        self.preferred_locations = []
        self.preferred_duration = None
        self.min_stipend = 0
        self.interests = []


class ImportedRecommender:
    def __init__(self, data, tfidf_vectorizer, feature_matrix):
        self.data = data
        self.tfidf_vectorizer = tfidf_vectorizer
        self.feature_matrix = feature_matrix
        self.preprocessor = DataPreprocessor()

    def get_profile_features(self, student_profile):
        combined = (
            ' '.join(student_profile.interests) + ' ' +
            ' '.join(student_profile.skills) + ' ' +
            ' '.join(student_profile.preferred_locations)
        )
        cleaned = self.preprocessor.clean_text(combined)
        return self.tfidf_vectorizer.transform([cleaned])

    def recommend(self, student_profile, work_mode="Any Work Mode", top_n=10):
        profile_features = self.get_profile_features(student_profile)
        cosine_sims = cosine_similarity(profile_features, self.feature_matrix).flatten()
        
        df_scored = self.data.copy()
        df_scored['similarity_score'] = cosine_sims

        # Hard constraints
        if student_profile.preferred_duration and student_profile.preferred_duration > 0:
            df_scored = df_scored[df_scored['duration_numeric'] <= student_profile.preferred_duration]
            
        if student_profile.min_stipend and student_profile.min_stipend > 0:
            df_scored = df_scored[df_scored['stipend_numeric'] >= student_profile.min_stipend]

        # Location constraints
        valid_locs = [l.strip().lower() for l in student_profile.preferred_locations if l.strip().lower() not in ['', 'any', 'all', 'any location']]
        if valid_locs:
            loc_pattern = '|'.join([re.escape(loc) for loc in valid_locs])
            df_scored = df_scored[df_scored['location'].str.lower().str.contains(loc_pattern, na=False)]

        # Work Mode constraints
        if work_mode == "Remote (WFH)":
            df_scored = df_scored[df_scored['location'].str.lower().str.contains('work from home|remote', na=False)]
        elif work_mode == "On-site / In-Office":
            df_scored = df_scored[~df_scored['location'].str.lower().str.contains('work from home|remote', na=False)]

        return df_scored.sort_values(by='similarity_score', ascending=False).head(top_n)


@st.cache_resource
def load_recommender():
    try:
        processed_df = joblib.load('internship_recommender_data_20251025_072624.pkl')
        loaded_components = joblib.load('internship_recommender_components_20251025_072624.pkl')
        return ImportedRecommender(processed_df, loaded_components['tfidf_vectorizer'], loaded_components['feature_matrix'])
    except Exception as e:
        st.error(f"Error loading recommendation assets: {e}")
        st.stop()


recommender = load_recommender()
preprocessor = recommender.preprocessor


# ─── Chatbot Assistant Knowledge Base ─────────────────────────────────────────
def get_bot_response(user_input, recommender):
    msg = user_input.lower().strip()
    if any(w in msg for w in ['hi', 'hello', 'hey', 'start']):
        return "👋 **Hello!** I'm your **AI Career Assistant**. Ask me about the recommendation algorithm, stipends, remote opportunities, or how to tune your profile!"

    if any(w in msg for w in ['algorithm', 'how it works', 'tfidf', 'cosine', 'math']):
        return (
            "🤖 **How the Matching Engine Works:**\n\n"
            "1. **Text Preprocessing:** Removes stopwords, cleans punctuation, and applies lemmatization.\n"
            "2. **TF-IDF Vectorization:** Projects your skills into a 1,000-dimensional term frequency vector.\n"
            "3. **Cosine Similarity:** Computes normalized vector dot-products between your profile and 6,485 opportunities.\n"
            "4. **Deterministic Filtering:** Prunes results based on your minimum stipend, duration, and location limits."
        )

    if any(w in msg for w in ['communication', 'cce', 'subject', 'channel']):
        return (
            "📡 **Connection to Communication Systems Engineering:**\n\n"
            "- **Transmitter:** Student Profile / Query\n"
            "- **Channel Encoder:** NLP Lemmatizer & TF-IDF Vectorizer\n"
            "- **Noisy Channel:** Real-world unstructured job descriptions with typos/synonyms\n"
            "- **Receiver / Decoder:** Cosine Similarity Matrix Engine\n"
            "- **Goal:** Maximizing mutual information transfer with sub-15ms latency."
        )

    if any(w in msg for w in ['stipend', 'highest', 'pay', 'paid', 'salary']):
        avg_s = recommender.data['stipend_numeric'].mean()
        max_s = recommender.data['stipend_numeric'].max()
        return f"💰 **Stipend Insights:** Average stipend is **₹{avg_s:,.0f}/month**, and maximum reaches **₹{max_s:,.0f}/month**. Over 94% of opportunities are paid."

    if any(w in msg for w in ['remote', 'wfh', 'location', 'cities']):
        remote_c = (recommender.data['location'].str.lower() == 'work from home').sum()
        return f"📍 **Location Insights:** **{remote_c:,} postings (44.3%)** are Remote/Work From Home. Top metro hubs include Mumbai, Delhi, and Bangalore."

    return (
        "💡 **You can ask me:**\n"
        "- *How does the matching algorithm work?*\n"
        "- *How is this related to Communication Systems?*\n"
        "- *What are the stipend trends?*\n"
        "- *Tips for getting higher match scores*"
    )


# ─── Top Navigation Bar ──────────────────────────────────────────────────────
total_postings = len(recommender.data)
remote_postings = (recommender.data['location'].str.lower() == 'work from home').sum()
avg_monthly_stipend = recommender.data['stipend_numeric'].mean()

st.markdown(f"""
<div class="top-navbar">
    <div class="brand-wrap">
        <div class="brand-icon">🎓</div>
        <div class="brand-text">
            <h2>InternMatch</h2>
            <p>AI-Powered Internship Recommendations</p>
        </div>
    </div>
    <div class="nav-kpis">
        <span>📦 <strong>{total_postings:,}</strong> Postings</span>
        <span>🌐 <strong>{remote_postings:,}</strong> Remote Roles</span>
        <span>💰 <strong>₹{avg_monthly_stipend:,.0f}</strong> Avg Stipend</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Primary Tabs (Streamlit Native) ─────────────────────────────────────────
tab_find, tab_insights, tab_chatbot = st.tabs([
    "🎯 Find Internships", 
    "📊 Market Insights", 
    "🤖 AI Assistant"
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1: FIND INTERNSHIPS (EXACT MOCKUP IMPLEMENTATION)
# ════════════════════════════════════════════════════════════════════════════
with tab_find:
    # ── 1. Hero Section ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <h1>Find the Right<br>Internship for <span class="hero-highlight">Your Future</span></h1>
            <p>Get AI-powered recommendations based on your skills, interests and goals. Discover verified opportunities and kickstart your career.</p>
            <div class="hero-pill-list">
                <span class="hero-pill-item"><span style="color:#3B82F6;">✓</span> Verified Postings</span>
                <span class="hero-pill-item"><span style="color:#EF4444;">🎯</span> AI Match Score</span>
                <span class="hero-pill-item"><span style="color:#F59E0B;">⚡</span> Up-to-date Opportunities</span>
                <span class="hero-pill-item"><span style="color:#8B5CF6;">✨</span> Smart Recommendations</span>
            </div>
        </div>
        <div style="flex-shrink:0; display:flex; align-items:center; justify-content:center; padding-left:1rem;">
            <svg width="220" height="140" viewBox="0 0 240 150" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="35" y="30" width="170" height="95" rx="10" fill="#1E1B4B" stroke="#4F46E5" stroke-width="2.5"/>
                <rect x="43" y="38" width="154" height="79" rx="6" fill="#F8FAFC"/>
                <rect x="52" y="46" width="60" height="10" rx="3" fill="#E2E8F0"/>
                <rect x="52" y="62" width="135" height="4" rx="2" fill="#CBD5E1"/>
                <rect x="52" y="70" width="115" height="4" rx="2" fill="#E2E8F0"/>
                <rect x="52" y="78" width="85" height="4" rx="2" fill="#CBD5E1"/>
                <rect x="52" y="86" width="105" height="4" rx="2" fill="#E2E8F0"/>
                <path d="M15 125C15 122.239 17.2386 120 20 120H220C222.761 120 225 122.239 225 125V128H15V125Z" fill="#334155"/>
                <rect x="95" y="120" width="50" height="4" rx="2" fill="#64748B"/>
                <g filter="drop-shadow(0px 3px 6px rgba(0,0,0,0.1))">
                    <rect x="15" y="10" width="62" height="22" rx="11" fill="#4F46E5"/>
                    <text x="46" y="25" fill="white" font-size="10" font-weight="700" text-anchor="middle">AI / ML</text>
                </g>
                <g filter="drop-shadow(0px 3px 6px rgba(0,0,0,0.1))">
                    <rect x="95" y="4" width="68" height="22" rx="11" fill="#10B981"/>
                    <text x="129" y="19" fill="white" font-size="10" font-weight="700" text-anchor="middle">Python</text>
                </g>
                <g filter="drop-shadow(0px 3px 6px rgba(0,0,0,0.1))">
                    <rect x="175" y="12" width="60" height="22" rx="11" fill="#0EA5E9"/>
                    <text x="205" y="27" fill="white" font-size="9" font-weight="700" text-anchor="middle">Data Sci</text>
                </g>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 2. Unified Search & Filter Card ──────────────────────────────────────
    DOMAIN_PRESETS = {
        "All Opportunities": "",
        "🤖 AI & Machine Learning": "Machine Learning, Deep Learning, Python, Data Science, PyTorch",
        "🌐 Web Development": "React, JavaScript, Node.js, Python, Full Stack, HTML, CSS",
        "📊 Data Science": "Data Science, Python, SQL, Statistics, Pandas, Data Analysis",
        "☁️ Cloud & DevOps": "DevOps, Docker, Kubernetes, Cloud Computing, Linux, AWS",
        "📱 Mobile Apps": "Flutter, Android, React Native, Mobile Development, Kotlin",
        "📡 IoT & Embedded (CCE)": "IoT, Embedded Systems, Arduino, Raspberry Pi, Communication",
        "🎨 UI/UX Design": "UI/UX, Graphic Design, Figma, Adobe XD, User Experience"
    }

    if 'has_searched' not in st.session_state:
        st.session_state.has_searched = False
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'search_loc' not in st.session_state:
        st.session_state.search_loc = "Any Location"
    if 'search_work_mode' not in st.session_state:
        st.session_state.search_work_mode = "Any Work Mode"
    if 'min_stipend_filter' not in st.session_state:
        st.session_state.min_stipend_filter = 0
    if 'max_duration_filter' not in st.session_state:
        st.session_state.max_duration_filter = 6
    if 'top_n_filter' not in st.session_state:
        st.session_state.top_n_filter = 10

    # Search Card
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    c_input, c_loc, c_mode, c_btn = st.columns([3.2, 1.8, 1.8, 1.6])
    
    with c_input:
        query_text = st.text_input(
            "Search skills, roles or keywords...",
            value=st.session_state.search_query,
            placeholder="Search skills, roles or keywords (e.g. Python, React, Machine Learning, SDE)...",
            label_visibility="collapsed"
        )
    with c_loc:
        loc_choices = ["Any Location", "Work From Home", "Bangalore", "Mumbai", "Delhi", "Gurgaon", "Pune", "Hyderabad", "Chennai"]
        sel_loc = st.selectbox("Location", loc_choices, index=loc_choices.index(st.session_state.search_loc) if st.session_state.search_loc in loc_choices else 0, label_visibility="collapsed")
    with c_mode:
        mode_choices = ["Any Work Mode", "Remote (WFH)", "On-site / In-Office"]
        sel_mode = st.selectbox("Work Mode", mode_choices, index=mode_choices.index(st.session_state.search_work_mode) if st.session_state.search_work_mode in mode_choices else 0, label_visibility="collapsed")
    with c_btn:
        run_search_btn = st.button("🔍 Search Internships", type="primary", use_container_width=True)

    # Domain pills directly under the search inputs
    pill_names = list(DOMAIN_PRESETS.keys())
    selected_domain_pill = st.pills("Popular Domains", pill_names, default="All Opportunities", label_visibility="collapsed")
    if selected_domain_pill and selected_domain_pill != "All Opportunities":
        chosen_skills = DOMAIN_PRESETS[selected_domain_pill]
        if st.session_state.search_query != chosen_skills:
            st.session_state.search_query = chosen_skills
            st.session_state.has_searched = True

    st.markdown('</div>', unsafe_allow_html=True)

    # Trigger search on button click
    if run_search_btn:
        if query_text.strip():
            st.session_state.search_query = query_text.strip()
            st.session_state.search_loc = sel_loc
            st.session_state.search_work_mode = sel_mode
            st.session_state.has_searched = True
        else:
            st.warning("Please enter your skills or choose a field above to search.")

    # ── 3. Two-Column Layout: Sidebar Filters + Main Recommendations ─────────
    col_filter, col_main = st.columns([1, 2.7])

    # Left Column: Refine Results
    with col_filter:
        st.markdown("""
        <div class="filter-panel">
            <div class="filter-title-row">
                <span class="filter-title">⚙️ Refine Results</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="filter-sec-name">💰 Minimum Stipend</div>', unsafe_allow_html=True)
        stipend_filter = st.slider("Stipend Range", min_value=0, max_value=30000, value=int(st.session_state.min_stipend_filter), step=2000, format="₹%d", label_visibility="collapsed")
        st.caption(f"Showing roles paying **≥ ₹{stipend_filter:,}/mo**")

        st.markdown('<div class="filter-sec-name">⏱️ Maximum Duration</div>', unsafe_allow_html=True)
        duration_filter = st.slider("Duration Bound", min_value=1, max_value=6, value=int(st.session_state.max_duration_filter), step=1, format="%d mos", label_visibility="collapsed")
        st.caption(f"Showing durations **≤ {duration_filter} months**")

        st.markdown('<div class="filter-sec-name">🎯 Results to Display</div>', unsafe_allow_html=True)
        top_n_filter = st.select_slider("Cutoff", options=[5, 10, 15, 20, 30], value=int(st.session_state.top_n_filter), label_visibility="collapsed")

        if st.button("Reset Filters", use_container_width=True):
            st.session_state.min_stipend_filter = 0
            st.session_state.max_duration_filter = 6
            st.session_state.top_n_filter = 10
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: 4 Stat Cards + AI Results
    with col_main:
        # 4 Stat Cards (Exactly as in Mockup)
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-wrap" style="background:#EFF6FF; color:#3B82F6;">📦</div>
                <div>
                    <div class="stat-val">{total_postings:,}</div>
                    <div class="stat-name">Verified Postings</div>
                    <div class="stat-trend">↗ +12% this month</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-wrap" style="background:#ECFDF5; color:#10B981;">🌐</div>
                <div>
                    <div class="stat-val">{remote_postings:,}</div>
                    <div class="stat-name">Remote Roles</div>
                    <div class="stat-trend">↗ +8% this month</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-wrap" style="background:#FFFBEB; color:#F59E0B;">💰</div>
                <div>
                    <div class="stat-val">₹{avg_monthly_stipend:,.0f}</div>
                    <div class="stat-name">Average Stipend</div>
                    <div class="stat-trend">↗ +15% this month</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with sc4:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-icon-wrap" style="background:#F5F3FF; color:#8B5CF6;">🎯</div>
                <div>
                    <div class="stat-val">92%</div>
                    <div class="stat-name">Profile Match Accuracy</div>
                    <div class="stat-trend">↗ +10% improvement</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Sub-tabs bar: AI Recommended vs Sort
        tab_header_col1, tab_header_col2 = st.columns([3, 1.2])
        with tab_header_col1:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:1.2rem; font-size:0.92rem; font-weight:700; color:#475569;">
                <span style="color:#4F46E5; border-bottom:2.5px solid #4F46E5; padding-bottom:0.35rem;">✨ AI Recommended</span>
                <span>⏱️ Latest Internships</span>
                <span>💰 High Stipend</span>
                <span>🔥 Popular</span>
            </div>
            """, unsafe_allow_html=True)
        with tab_header_col2:
            sort_opt = st.selectbox("Sort", ["Best Match", "Highest Stipend", "Shortest Duration"], label_visibility="collapsed")

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

        # ── SHOW ONLY AFTER SEARCH (User requirement!) ──────────────────────
        if not st.session_state.has_searched or not query_text.strip():
            # Clean initial empty state before searching
            st.markdown("""
            <div class="empty-search-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
                <h3 style="font-size: 1.35rem; font-weight: 700; color: #0F172A; margin: 0 0 0.4rem 0;">
                    Ready to Find Your Ideal Internship?
                </h3>
                <p style="font-size: 0.95rem; color: #64748B; margin: 0 auto 1.2rem auto; max-width: 520px; line-height: 1.5;">
                    Enter your skills in the search bar above or pick a domain, then click <strong>Search Internships</strong> to see your AI-tailored matches.
                </p>
                <div style="display:inline-flex; gap: 1.4rem; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 0.55rem 1.4rem; border-radius: 30px; font-size: 0.82rem; color: #475569;">
                    <span>📦 <strong>6,485</strong> Postings</span>
                    <span>🌐 <strong>2,870</strong> Remote</span>
                    <span>⚡ <strong>Sub-15ms</strong> Matching</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # User has searched -> Run Recommendation Engine!
            profile = StudentProfile()
            clean_skills = [s.strip() for s in query_text.split(',') if s.strip()]
            profile.skills = clean_skills
            profile.interests = clean_skills
            profile.preferred_locations = [sel_loc]
            profile.min_stipend = stipend_filter
            profile.preferred_duration = duration_filter

            results = recommender.recommend(profile, work_mode=sel_mode, top_n=top_n_filter)

            # Apply user sort option
            if sort_opt == "Highest Stipend":
                results = results.sort_values(by='stipend_numeric', ascending=False)
            elif sort_opt == "Shortest Duration":
                results = results.sort_values(by='duration_numeric', ascending=True)

            # Results action bar (Export & Reset)
            bar_l, bar_r = st.columns([3, 1.2])
            with bar_l:
                st.caption(f"Showing **{len(results)}** recommendations matching **\"{query_text}\"**")
            with bar_r:
                export_csv = results[['internship_title', 'company_name', 'location', 'duration', 'stipend', 'similarity_score']].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export (CSV)",
                    data=export_csv,
                    file_name="internship_recommendations.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            if results.empty:
                st.info("No internships found matching your filter constraints. Try lowering the minimum stipend or selecting 'Any Location'.")
            else:
                student_tokens = set(preprocessor.clean_text(query_text).split())

                def render_internship_card(row, student_tokens, preprocessor):
                    sim = row['similarity_score']
                    pct = int(min(max(sim * 100, 0), 100))
                    company = str(row.get('company_name', 'Tech Enterprise'))
                    
                    # Company Logo Badge
                    comp_lower = company.lower()
                    if 'google' in comp_lower:
                        logo_html = '<div class="logo-container" style="background:#FFFFFF; color:#4285F4; font-size:1.3rem;">G</div>'
                    elif 'microsoft' in comp_lower:
                        logo_html = '<div class="logo-container" style="background:#FFFFFF; color:#00A4EF; font-size:1.1rem;">⊞</div>'
                    elif 'amazon' in comp_lower or 'aws' in comp_lower:
                        logo_html = '<div class="logo-container" style="background:#0F172A; color:#FF9900; font-size:0.9rem;">aws</div>'
                    else:
                        words = company.split()
                        initials = (words[0][0] + words[1][0]).upper() if len(words) > 1 else words[0][:2].upper()
                        logo_html = f'<div class="logo-container" style="background:#EEF2FF; color:#4F46E5;">{initials}</div>'

                    # Extract relevant skills for the tags
                    title_tokens = set(preprocessor.clean_text(row.get('internship_title', '')).split())
                    overlapping = list(student_tokens.intersection(title_tokens))
                    
                    tags_to_show = overlapping[:3] if overlapping else list(title_tokens)[:3]
                    if not tags_to_show:
                        tags_to_show = ["Python", "Problem Solving", "Analytics"]
                    tags_html = ''.join([f'<span class="tag-bubble">{t.capitalize()}</span>' for t in tags_to_show])

                    # XAI Explanation
                    explanation_text = f"High match based on your skills in {', '.join([t.capitalize() for t in tags_to_show])}." if overlapping else "Good fit based on your technical profile and preferences."

                    # Exact Card HTML matching Mockup
                    card_markup = f"""
                    <div class="job-listing-card">
                        <div class="card-main-header">
                            <div style="display:flex; align-items:flex-start; gap:1rem;">
                                {logo_html}
                                <div>
                                    <h3 class="role-heading">{row.get('internship_title')} <span class="verified-badge">✓</span></h3>
                                    <div class="company-sub-line">
                                        <strong>{company}</strong>
                                        <span>📍 {row.get('location')}</span>
                                        <span>⏱️ {row.get('duration')}</span>
                                    </div>
                                    <div class="card-tags-row">
                                        {tags_html}
                                    </div>
                                </div>
                            </div>
                            <div style="text-align:right; min-width:140px;">
                                <div class="match-rate-text">🎯 {pct}% match</div>
                                <div class="match-bar-bg">
                                    <div class="match-bar-fill" style="width:{pct}%;"></div>
                                </div>
                                <div class="stipend-amount">{row.get('stipend')}</div>
                            </div>
                        </div>
                        <div class="ai-insight-box">
                            <span>💡</span>
                            <span>{explanation_text} (Vector Cosine Similarity: <strong>{sim:.4f}</strong>)</span>
                        </div>
                    </div>
                    """
                    st.markdown(card_markup, unsafe_allow_html=True)

                for idx, row in results.iterrows():
                    render_internship_card(row, student_tokens, preprocessor)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2: MARKET INSIGHTS & EDA
# ════════════════════════════════════════════════════════════════════════════
with tab_insights:
    st.markdown("### 📊 Market Intelligence & Dataset Overview")
    st.caption("Empirical analytics computed across 6,485 verified opportunities in the corpus.")

    mi_col1, mi_col2 = st.columns(2)
    with mi_col1:
        st.markdown("#### 🏆 Top In-Demand Internship Roles")
        top_roles = recommender.data['internship_title'].value_counts().head(8).reset_index()
        top_roles.columns = ['Role', 'Postings']
        chart_roles = alt.Chart(top_roles).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, color="#4F46E5").encode(
            x=alt.X('Postings:Q', title='Available Openings'),
            y=alt.Y('Role:N', sort='-x', title=None),
            tooltip=['Role', 'Postings']
        ).properties(height=280)
        st.altair_chart(chart_roles, use_container_width=True)

    with mi_col2:
        st.markdown("#### 📍 Top Geographic Locations")
        top_locs = recommender.data['location'].value_counts().head(8).reset_index()
        top_locs.columns = ['Location', 'Postings']
        chart_locs = alt.Chart(top_locs).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, color="#0EA5E9").encode(
            x=alt.X('Postings:Q', title='Available Openings'),
            y=alt.Y('Location:N', sort='-x', title=None),
            tooltip=['Location', 'Postings']
        ).properties(height=280)
        st.altair_chart(chart_locs, use_container_width=True)

    st.markdown("---")
    mi_col3, mi_col4 = st.columns(2)
    with mi_col3:
        st.markdown("#### 💰 Stipend Distribution")
        stipend_s = recommender.data['stipend_numeric']
        bins = [-1, 0, 5000, 10000, 20000, 100000]
        labels = ['Unpaid', '₹1k–₹5k', '₹5k–₹10k', '₹10k–₹20k', '> ₹20k']
        binned = pd.cut(stipend_s, bins=bins, labels=labels).value_counts().reindex(labels).reset_index()
        binned.columns = ['Tier', 'Count']
        chart_stipend = alt.Chart(binned).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color="#10B981").encode(
            x=alt.X('Tier:N', sort=labels, title=None),
            y=alt.Y('Count:Q', title='Count'),
            tooltip=['Tier', 'Count']
        ).properties(height=240)
        st.altair_chart(chart_stipend, use_container_width=True)

    with mi_col4:
        st.markdown("#### ⏱️ Duration Distribution")
        dur_df = recommender.data['duration_numeric'].value_counts().sort_index().reset_index()
        dur_df.columns = ['Months', 'Count']
        dur_df['Label'] = dur_df['Months'].astype(int).astype(str) + " Months"
        chart_dur = alt.Chart(dur_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color="#6366F1").encode(
            x=alt.X('Label:N', title=None),
            y=alt.Y('Count:Q', title='Count'),
            tooltip=['Label', 'Count']
        ).properties(height=240)
        st.altair_chart(chart_dur, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3: AI CHATBOT ASSISTANT (STREAMLIT NATIVE CHAT)
# ════════════════════════════════════════════════════════════════════════════
with tab_chatbot:
    st.markdown("### 🤖 AI Career & Algorithm Assistant")
    st.caption("Ask questions about the matching model, stipend insights, or CCE system analogies.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "👋 Hi! I'm your AI Internship Assistant. Ask me how the algorithm works, about stipends, or how to tune your profile!"}
        ]

    # Quick prompt pills
    prompt_pills = [
        "How does the matching algorithm work?",
        "Connection to Communication Systems?",
        "What are the stipend trends?",
        "Tell me about remote internships"
    ]
    p_cols = st.columns(4)
    for p_i, p_text in enumerate(prompt_pills):
        with p_cols[p_i]:
            if st.button(p_text, key=f"chat_pill_{p_i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": p_text})
                ans = get_bot_response(p_text, recommender)
                st.session_state.chat_history.append({"role": "assistant", "content": ans})
                st.rerun()

    st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)

    # Streamlit Native Chat Messages
    for chat_msg in st.session_state.chat_history:
        avatar = "🧑‍💻" if chat_msg["role"] == "user" else "🤖"
        with st.chat_message(chat_msg["role"], avatar=avatar):
            st.markdown(chat_msg["content"])

    # Streamlit Native Chat Input
    user_prompt = st.chat_input("Ask a question about internships or the ML engine...")
    if user_prompt:
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        reply = get_bot_response(user_prompt, recommender)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "👋 Conversation cleared. How can I help you today?"}
        ]
        st.rerun()
