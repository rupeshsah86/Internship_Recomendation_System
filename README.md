🎯 AI-Powered Internship Recommender
A Machine Learning-powered web application that provides personalized internship recommendations to students based on their skills, interests, and preferences.
📋 Project Overview
This project leverages Natural Language Processing (NLP) and Machine Learning (ML) to match students with the most relevant internship opportunities.
It uses TF-IDF vectorization and Cosine Similarity to compute how closely student profiles align with internship descriptions.
✨ Features
🔍 Smart Recommendations
AI-Powered Matching: Uses TF-IDF and Cosine Similarity algorithms
Personalized Results: Tailored to each student's profile
Multi-Criteria Filtering: Skills, interests, location, duration, stipend
Similarity Scoring: Displays Excellent, Good, or Fair matches
📊 Data Insights
Interactive Visualizations: Internship trends and distributions
Statistics Dashboard: Overview of internships and metrics
Exploratory Data Analysis: Understand stipend and duration patterns
🎨 User-Friendly Interface
Built with Streamlit: Responsive and intuitive design
Real-Time Recommendations: Instant output generation
Profile Setup Form: Easy-to-fill student profile
Custom Filters: Control the number and type of recommendations
🛠️ Technical Architecture
Machine Learning Pipeline
Data Preprocessing
Text cleaning, normalization, and lemmatization
Stopword removal
Stipend extraction and numeric conversion
Location and duration normalization
Feature Engineering
Combine multiple internship attributes
TF-IDF vectorization
Cosine similarity computation
Recommendation Engine
Profile-based similarity matching
Multi-level filtering: location, stipend, duration
Ranked recommendation results
🧩 Core Components
Component	Description
DataPreprocessor	Handles text cleaning and feature extraction
StudentProfile	Stores user preferences and profile data
InternshipRecommender	Core recommendation algorithm
Streamlit Interface	Frontend for user interaction
📁 Project Structure
internship_recommender/
├── app.py
├── utils.py
├── requirements.txt
├── internship.csv
├── internship_recommender_complete_20251025_072624.pkl
├── internship_recommender_components_20251025_072624.pkl
├── internship_recommender_data_20251025_072624.pkl
├── internship_recommender_metadata_20251025_072624.pkl
└── internship_recommender_info_20251025_072624.txt
🚀 Quick Start
Prerequisites
Python 3.8+
pip package manager
Installation
# Clone the repository
git clone <repository-url>
cd internship_recommender

# Create a virtual environment (recommended)
python -m venv internship_env
source internship_env/bin/activate    # Windows: internship_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
Open your browser and visit:
👉 http://localhost:8501
💻 Usage Guide
1. Student Profile Setup
Skills: Enter technical and soft skills (comma-separated)
Interests: Specify areas of interest or career goals
Location: Preferred locations or “Work From Home”
Duration: Maximum internship duration
Stipend: Minimum expected stipend
2. Getting Recommendations
Fill in profile details in the sidebar
Adjust the number of results (5–20)
Click Get Recommendations
3. Result Interpretation
Score Range	Indicator	Meaning
> 0.7	🟢 Excellent	Highly relevant
0.4 – 0.7	🟠 Good	Moderately relevant
< 0.4	🔵 Fair	Less relevant
⚙️ Configuration
TF-IDF Features: Max 1000
Stopwords: English stopwords removed
Text Processing: Lemmatization & normalization
Similarity Metric: Cosine similarity
Customization Options:
Number of recommendations (5–20)
Minimum stipend filter
Maximum duration filter
Location preference
📊 Dataset Requirements
CSV Format
internship_title	company_name	location	start_date	duration	stipend
Java Development	SunbaseData	Work From Home	Immediately	6 Months	₹ 30,000 /month
Digital Marketing	Tech Corp	Bangalore	Immediately	3 Months	₹ 15,000 /month
Data Processing:
Cleans and normalizes text
Converts stipend to numeric
Categorizes locations (Remote/On-site)
Converts duration to months
🤖 Algorithm Details
TF-IDF + Cosine Similarity: Converts text to vectors and measures similarity
Multi-Stage Filtering: Text similarity, stipend, duration, location
📈 Performance Highlights
Personalized Relevance: Individualized recommendations
Scalable: Handles large datasets efficiently
Real-Time Results: Instant output
Transparent Scoring: Clear similarity indicators
🔮 Future Enhancements
Planned Features:
User authentication & profile saving
Company-based filtering
Recommendation history tracking
Job portal integration
Sentiment analysis on company reviews
Skill gap detection & learning suggestions
Technical Improvements:
Database integration for persistence
REST API endpoints
Advanced NLP models (BERT, Transformers)
A/B testing for recommendation quality
Mobile app version
🧰 Troubleshooting
Issue	Solution
Module Not Found	Run: pip install --upgrade -r requirements.txt
Pickle File Error	Ensure .pkl files exist in the project folder
Memory Issues	Reduce TF-IDF max_features or use smaller dataset
Invalid CSV	Ensure all required columns are present
📄 License
This project is for educational and personal use.
Please credit the original authors when modifying or sharing.
👥 Contributing
Contributions are welcome:
Fix bugs
Add new features
Improve documentation
Optimize performance
📞 Support
Check the Troubleshooting section
Review console error messages
Verify CSV format
Open an Issue on GitHub
🧡 Built With
Streamlit, Scikit-learn, Python
