import html
import re
import random
import json
from pathlib import Path
from datetime import date
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# Urjaa AI Hub - Streamlit app
# =========================================================

st.set_page_config(
    page_title="Urjaa AI Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- CSS ----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: #050817;
        --panel: #0c1531;
        --purple: #8b45ff;
        --blue: #247bff;
        --text: #f5f7ff;
        --muted: #b8c9ec;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 78% 8%, rgba(67, 31, 130, .28), transparent 38%),
            linear-gradient(135deg, #040817 0%, #080d24 62%, #100821 100%);
        color: var(--text);
        font-family: 'Poppins', sans-serif;
    }

    [data-testid="stHeader"] { background: rgba(4, 8, 23, .92); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070d21, #0d0925);
        border-right: 1px solid #293b79;
    }
    [data-testid="stSidebar"] * { color: var(--text); }
    .block-container { max-width: 1450px; padding-top: 1.6rem; padding-bottom: 2rem; }

    .sidebar-brand { text-align: center; padding: 8px 0 20px; }
    .sidebar-bot {
        font-size: 54px;
        filter: drop-shadow(0 0 13px rgba(121, 96, 255, .8));
    }
    .sidebar-brand h2 { font-size: 21px; margin: 6px 0; }
    .sidebar-sub { color: #91b8ee; font-size: 12px; }
    .sidebar-quote {
        padding: 17px 12px; margin-top: 28px; text-align: center;
        border: 1px solid #43349c; border-radius: 16px;
        background: linear-gradient(145deg, #111b43, #100b2c);
        color: #c8ddff; line-height: 1.8; font-size: 13px;
    }

    .hero {
        position: relative; overflow: hidden; min-height: 340px;
        padding: 30px; border: 1px solid #303e91; border-radius: 23px;
        background:
            radial-gradient(ellipse at 90% 25%, rgba(73, 35, 145, .42), transparent 48%),
            linear-gradient(120deg, #09142f, #090d26 68%, #140c34);
        box-shadow: 0 0 32px rgba(76, 79, 255, .10);
        box-sizing: border-box;
    }
    .hero-label { color: #65dcff; font-size: 13px; font-weight: 600; }
    .hero-title { font-size: clamp(30px, 3.1vw, 46px); font-weight: 800; line-height: 1.17; margin: 20px 0; color: #fff; }
    .gradient-text {
        background: linear-gradient(90deg, #db5aff, #51baff);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle { color: #d4e1ff; font-size: 19px; font-weight: 600; margin: 0 0 14px; }
    .hero-description { color: #c4d8ff; line-height: 1.8; font-size: 13px; }
    .badge {
        display: inline-block; padding: 9px 14px; margin-top: 16px;
        border: 1px solid #7858ff; border-radius: 30px;
        color: #e3d5ff; background: rgba(35, 22, 81, .7); font-size: 11px;
    }

    .robot-stage {
        min-height: 340px; height: 100%; padding: 10px;
        display: flex; align-items: center; justify-content: center;
    }
    .robot-glow {
        position: absolute; width: 245px; height: 245px; border-radius: 50%;
        background: radial-gradient(circle, rgba(76,75,255,.58) 0%, rgba(112,41,255,.18) 48%, transparent 72%);
        filter: blur(12px);
    }
    .robot {
        position: relative; z-index: 1; display: block; width: min(100%, 285px); height: auto;
        animation: floatRobot 4s ease-in-out infinite;
        filter: drop-shadow(0 0 18px rgba(72,110,255,.38));
    }
    @keyframes floatRobot {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-9px); }
    }
    .floating-chip {
        position: absolute; z-index: 2; padding: 8px 11px;
        border: 1px solid #4055cc; border-radius: 11px;
        background: #0b1740; color: #b8e6ff; font-size: 11px;
        box-shadow: 0 0 18px rgba(65,91,255,.18);
    }
    .chip-one { top: 27px; right: 10px; }
    .chip-two { bottom: 25px; left: 8px; }

    .section-title { color: #fff; font-size: 25px; font-weight: 700; margin-top: 27px; }
    .section-subtitle { color: #9bb8e9; margin: 2px 0 17px; font-size: 12px; }
    .tool-card {
        min-height: 170px; padding: 18px; border: 1px solid #293c7d;
        border-radius: 17px; background: linear-gradient(145deg, #0c1734, #080e23);
        margin-bottom: 9px; box-sizing: border-box;
    }
    .tool-icon {
        width: 47px; height: 47px; display: flex; align-items: center; justify-content: center;
        border-radius: 50%; font-size: 23px;
        background: linear-gradient(145deg, #34208b, #111f5b);
        box-shadow: 0 0 17px rgba(108,66,255,.18);
    }
    .tool-card h3 { color: #fff; font-size: 16px; margin: 13px 0 7px; }
    .tool-card p { color: #b5c9ec; font-size: 11px; line-height: 1.7; margin-bottom: 0; }
    .stButton > button {
        background: linear-gradient(100deg, #832eff, #155fff);
        color: white; border: 1px solid transparent; border-radius: 10px;
        font-weight: 600; transition: .2s ease;
    }
    .stButton > button:hover {
        color: white; border-color: #bb9aff;
        box-shadow: 0 0 15px rgba(108,77,255,.35);
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: #0a1430; color: white; border: 1px solid #344982; border-radius: 9px;
    }
    div[data-baseweb="select"] > div { background: #0a1430; color: white; border-color: #344982; }
    [data-testid="stMetric"] { background: #0b1532; padding: 13px; border: 1px solid #293d79; border-radius: 12px; }
    .footer {
        text-align: center; color: #8ca4d1; font-size: 11px; margin-top: 30px;
        padding: 18px; border-top: 1px solid #202f59;
    }
    @media (max-width: 750px) {
        .hero { padding: 20px; min-height: auto; }
        .robot-stage { min-height: 270px; }
        .hero-title { font-size: 31px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------- SVG robot ----------------------
# The SVG is inserted into a single HTML fragment and rendered with unsafe_allow_html=True.
ROBOT_SVG = """
<svg class="robot" viewBox="0 0 320 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Friendly futuristic AI robot">
  <defs>
    <linearGradient id="robotBody" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#b5c8ff"/>
      <stop offset="100%" stop-color="#647eff"/>
    </linearGradient>
    <linearGradient id="robotScreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#102d76"/>
      <stop offset="100%" stop-color="#02091e"/>
    </linearGradient>
    <linearGradient id="laptopColor" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5ce7ff"/>
      <stop offset="100%" stop-color="#783cff"/>
    </linearGradient>
    <filter id="robotGlow">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <circle cx="160" cy="174" r="125" fill="#252064" opacity=".38"/>
  <path d="M160 54 L160 29" stroke="#8ccaff" stroke-width="5" stroke-linecap="round"/>
  <circle cx="160" cy="21" r="10" fill="#65e8ff" filter="url(#robotGlow)"/>
  <rect x="70" y="48" width="180" height="150" rx="55" fill="url(#robotBody)" stroke="#b4cfff" stroke-width="3"/>
  <rect x="52" y="94" width="25" height="63" rx="12" fill="#778dff" stroke="#b6d9ff" stroke-width="3"/>
  <rect x="243" y="94" width="25" height="63" rx="12" fill="#778dff" stroke="#b6d9ff" stroke-width="3"/>
  <rect x="88" y="72" width="144" height="104" rx="36" fill="url(#robotScreen)" stroke="#648eff" stroke-width="3"/>
  <path d="M112 120 Q123 99 134 120" fill="none" stroke="#5cecff" stroke-width="8" stroke-linecap="round" filter="url(#robotGlow)"/>
  <path d="M186 120 Q197 99 208 120" fill="none" stroke="#5cecff" stroke-width="8" stroke-linecap="round" filter="url(#robotGlow)"/>
  <path d="M139 145 Q160 162 181 145" fill="none" stroke="#a17aff" stroke-width="5" stroke-linecap="round"/>
  <path d="M92 211 Q92 190 119 190 L201 190 Q228 190 228 220 L228 285 L92 285 Z" fill="url(#robotBody)" stroke="#9bbdff" stroke-width="3"/>
  <circle cx="160" cy="224" r="16" fill="#364cc4"/>
  <circle cx="160" cy="224" r="9" fill="#5cecff" filter="url(#robotGlow)"/>
  <path d="M99 213 Q68 218 73 249" fill="none" stroke="#9cb9ff" stroke-width="20" stroke-linecap="round"/>
  <path d="M221 213 Q252 220 247 249" fill="none" stroke="#9cb9ff" stroke-width="20" stroke-linecap="round"/>
  <path d="M42 229 L163 218 L174 293 L55 303 Z" fill="url(#laptopColor)" stroke="#a6cfff" stroke-width="3"/>
  <path d="M55 238 L153 230 L161 282 L64 291 Z" fill="#11184b"/>
  <path d="M109 258 C96 244 82 260 109 279 C136 260 122 244 109 258 Z" fill="#e9b4ff" filter="url(#robotGlow)"/>
  <path d="M48 304 L174 293 L187 305 Q187 310 177 311 L55 318 Q44 317 48 304 Z" fill="#738fff" stroke="#9cdcff" stroke-width="2"/>
  <ellipse cx="132" cy="292" rx="27" ry="9" fill="#839bff"/>
  <ellipse cx="201" cy="292" rx="25" ry="9" fill="#839bff"/>
</svg>
"""

TOOLS = {
    "Resume Helper": ("📝", "Improve your resume with useful writing suggestions."),
    "Python Helper": ("🐍", "Learn Python concepts with beginner-friendly examples."),
    "Career Advisor": ("🎯", "Explore career paths based on your interests and skills."),
    "Study Planner": ("📅", "Build a simple personalized study schedule."),
    "Text Summarizer": ("📄", "Create a shorter version of long text."),
    "Interview Prep": ("🎤", "Practice common interview questions."),
    "Free Voice Interview": ("🎙️", "Practice interview questions using browser voice features."),
}

# ------------------------- Session-only data -------------------------
# No login, database, or file-based user-data storage is used.


def improve_interview_answer(question, answer):
    """Free deterministic English cleanup plus question-specific guidance.

    This is deliberately rule-based (not generative AI), so it only corrects
    common patterns and must not be presented as a complete grammar checker.
    """
    text = re.sub(r"\s+", " ", str(answer or "")).strip()
    if not text:
        return "Please write or speak an answer first.", "Write at least one sentence in your own words."

    replacements = [
        (r"\bi am agree\b", "I agree"),
        (r"\bi am not agree\b", "I do not agree"),
        (r"\bi is\b", "I am"), (r"\bi are\b", "I am"),
        (r"\bi has\b", "I have"), (r"\bi have a knowledge of\b", "I have knowledge of"),
        (r"\bmyself\s+([A-Z][a-z]+)\b", r"My name is \1"),
        (r"\bi want to learn more and more\b", "I want to keep learning and improving"),
        (r"\bvery much interested\b", "very interested"),
        (r"\bdo hard work\b", "work hard"),
        (r"\baccording to me\b", "In my opinion"),
        (r"\bi am having\b", "I have"),
        (r"\bi am good in\b", "I am good at"),
        (r"\bi have completed my graduation\b", "I have completed my degree"),
        (r"\bi belongs to\b", "I belong to"),
        (r"\bi was completed\b", "I completed"),
        (r"\bi can able to\b", "I can"),
        (r"\bi am passionate for\b", "I am passionate about"),
        (r"\bi am interested for\b", "I am interested in"),
        (r"\bi have knowledge about\b", "I have knowledge of"),
        (r"\bmyself is\b", "My name is"),
        (r"\bthanks for giving me this opportunity\b", "Thank you for giving me this opportunity"),
        (r"\bi didn't knew\b", "I did not know"),
        (r"\bi don't knows\b", "I do not know"),
        (r"\bhe don't\b", "he does not"), (r"\bshe don't\b", "she does not"),
        (r"\bit don't\b", "it does not"),
        (r"\bdiscuss about\b", "discuss"),
        (r"\bmore better\b", "better"), (r"\bvery unique\b", "unique"),
        (r"\bone of my strength is\b", "one of my strengths is"),
        (r"\bmy aim is to become\b", "my goal is to become"),
        (r"\bbasically\b[, ]*", ""), (r"\bumm+\b[, ]*", ""), (r"\buh+\b[, ]*", ""),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r"\bi\b", "I", text)
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    text = re.sub(r"([,.!?])(?=[A-Za-z])", r"\1 ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    text = text[:1].upper() + text[1:]
    if text[-1] not in ".!?":
        text += "."

    q = str(question or "").lower()

    # For common technical-definition questions, expand a short or copied
    # definition into a fuller, question-specific model answer. This avoids
    # showing the user's unchanged sentence under the "improved" heading.
    technical_topics = [
        "clustering", "classification", "regression", "supervised learning",
        "unsupervised learning", "k-means", "kmeans", "decision tree",
        "random forest", "neural network", "overfitting", "underfitting",
        "inheritance", "polymorphism", "encapsulation", "abstraction",
        "python", "sql", "machine learning", "deep learning", "data preprocessing",
        "feature scaling", "confusion matrix", "accuracy", "precision", "recall",
        "streamlit", "pandas", "numpy"
    ]
    is_definition_question = any(phrase in q for phrase in ["what is", "define", "explain", "meaning of", "describe"])
    if is_definition_question and any(topic in q for topic in technical_topics):
        try:
            model_version = sample_professional_answer(question)
        except NameError:
            model_version = ""
        normalized_user = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
        normalized_model = re.sub(r"[^a-z0-9]+", " ", model_version.lower()).strip()
        # Expand if the user supplied only a brief definition or essentially
        # pasted the same sentence; otherwise preserve their own answer and
        # apply the normal rule-based cleanup below.
        if model_version and (len(normalized_user.split()) < 24 or normalized_user == normalized_model or normalized_model.startswith(normalized_user)):
            text = model_version

    if any(k in q for k in ["tell me about yourself", "introduce yourself"]):
        tip = "Use this order: your education, 2–3 relevant skills, one real project, and your current career goal."
    elif "strength" in q:
        tip = "Name one or two real strengths, then support one with a short example from college or a project."
    elif "weakness" in q or "area are you improving" in q:
        tip = "Choose a genuine skill you are improving and explain the practical steps you take. Avoid saying you have no weaknesses."
    elif "project" in q:
        tip = "Explain the problem, your role, tools used, what you did, the result, and one thing you learned. Only include details that are true."
    elif any(k in q for k in ["why should", "select you", "hire you"]):
        tip = "Connect your current skills, willingness to learn, and reliability to the internship or role. Avoid claiming experience you do not have."
    elif "why" in q or "motivat" in q or "goal" in q:
        tip = "Answer the question directly first, then give one personal reason and a relevant example or next step."
    else:
        tip = "Start with your main point, explain it in simple sentences, and add one relevant example when possible. This free tool corrects selected common patterns, not every grammar error."
    return text, tip


def sample_professional_answer(question):
    """Return a short, editable example for common interview question types."""
    q = str(question or "").lower()
    if any(k in q for k in ["tell me about yourself", "introduce yourself"]):
        return ("I am a third-year B.E. student in Artificial Intelligence and Data Science. "
                "I am building my skills in Python, SQL, and machine learning. I have worked on academic projects where I practised data preprocessing and model evaluation. "
                "I am looking for an opportunity to learn from real tasks, contribute to a team, and improve my technical skills.")
    if "strength" in q:
        return ("One of my strengths is that I am willing to learn and work consistently. "
                "When I face a new topic, I break it into smaller parts, practise, and ask for feedback. "
                "This helps me improve step by step.")
    if "weakness" in q or "area are you improving" in q:
        return ("One area I am improving is my confidence when explaining technical ideas. "
                "I practise by explaining concepts in simple words and preparing small examples. "
                "I am gradually becoming clearer and more confident.")
    if any(k in q for k in ["why should", "select you", "hire you"]):
        return ("I am eager to learn, responsible with assigned work, and ready to accept feedback. "
                "My current skills give me a foundation, and I am willing to practise and improve wherever needed. "
                "I would try to contribute consistently while learning from the team.")
    if "why" in q and any(k in q for k in ["ai", "data science", "internship", "role", "career"]):
        return ("I chose this field because I enjoy understanding how data and technology can help solve problems. "
                "I am especially interested in Python and machine learning, and I want to strengthen these skills through practical work.")
    if "project" in q:
        return ("In my project, I first identified the problem and prepared the data for analysis. "
                "I used the tools required for the task, tested the result, and reviewed the model's performance. "
                "The project helped me understand the importance of clean data, evaluation, and explaining results clearly.")
    if any(k in q for k in ["team", "teammate", "conflict", "feedback"]):
        return ("I try to listen carefully, communicate respectfully, and focus on the shared goal. "
                "If there is a problem, I discuss it calmly and agree on the next steps. "
                "I also treat feedback as a chance to improve.")
    if "pressure" in q or "time" in q or "manage" in q:
        return ("I list the tasks, identify the most urgent ones, and break larger work into smaller steps. "
                "I try to track my progress and ask for clarification early if I am stuck. "
                "This helps me stay organised and manage my time better.")

    # Machine-learning and data-science concepts commonly asked in interviews.
    if "clustering" in q:
        return ("Clustering is an unsupervised machine learning technique that groups similar data points "
                "together based on their features, without using predefined labels. For example, a business "
                "can group customers by their purchasing behaviour. K-Means is a commonly used clustering "
                "algorithm. Clustering helps discover hidden patterns and segments in data.")
    if "classification" in q and any(k in q for k in ["what is", "define", "explain", "meaning"]):
        return ("Classification is a supervised machine learning task that predicts a category or class label "
                "from input features. For example, an email model can classify a message as spam or not spam. "
                "Common algorithms include decision trees, logistic regression, and support vector machines.")
    if "regression" in q and any(k in q for k in ["what is", "define", "explain", "meaning"]):
        return ("Regression is a supervised machine learning task used to predict a numerical value. For "
                "example, a model can estimate crop yield or house prices from relevant features. Linear "
                "regression and random forest regression are two common methods.")
    if "supervised learning" in q:
        return ("Supervised learning trains a model using labelled examples, where each training input has a "
                "known target. It is commonly used for classification and regression. For example, a model can "
                "learn from past labelled loan applications to predict approval outcomes.")
    if "unsupervised learning" in q:
        return ("Unsupervised learning finds patterns in data without predefined target labels. Clustering and "
                "dimensionality reduction are common examples. For instance, K-Means can group customers with "
                "similar purchasing behaviour.")
    if "k-means" in q or "kmeans" in q:
        return ("K-Means is an unsupervised clustering algorithm that divides data into K groups. It assigns "
                "points to the nearest cluster centroid and updates the centroids repeatedly until assignments "
                "stabilise or a stopping condition is reached. The value of K must be chosen in advance.")
    if "decision tree" in q:
        return ("A decision tree is a machine learning model that makes predictions by splitting data through "
                "a sequence of feature-based decisions. Its tree structure is relatively easy to interpret. "
                "It can be used for both classification and regression, though a deep tree may overfit.")
    if "random forest" in q:
        return ("Random Forest is an ensemble learning algorithm that combines predictions from many decision "
                "trees. It uses random samples and feature subsets to help reduce overfitting compared with a "
                "single tree. It can be used for classification and regression.")
    if "neural network" in q:
        return ("A neural network is a machine learning model made of connected units arranged in layers. It "
                "learns patterns by adjusting weights during training. Neural networks are useful for complex "
                "tasks such as image recognition, language processing, and forecasting.")
    if "data preprocessing" in q or "preprocessing" in q:
        return ("Data preprocessing prepares raw data before analysis or model training. It can include handling "
                "missing values, removing duplicates, encoding categorical variables, and scaling numerical "
                "features. Good preprocessing can improve data quality and help a model learn reliably.")
    if "overfitting" in q:
        return ("Overfitting happens when a model learns the training data too closely, including noise, and "
                "then performs poorly on new data. It can be reduced with validation, regularisation, simpler "
                "models, or more representative training data.")
    if "underfitting" in q:
        return ("Underfitting happens when a model is too simple to learn important patterns in the data. It "
                "often performs poorly on both training and test data. A more suitable model, better features, "
                "or improved training may help.")
    if "train" in q and "test" in q and any(k in q for k in ["difference", "split", "data"]):
        return ("Training data is used to fit a model, while test data is held aside to evaluate how well the "
                "model performs on unseen examples. Keeping them separate gives a more realistic estimate of "
                "generalisation and helps reveal overfitting.")
    if "confusion matrix" in q:
        return ("A confusion matrix compares a classifier's predicted labels with the actual labels. In binary "
                "classification, it summarises true positives, true negatives, false positives, and false negatives. "
                "It helps us understand which types of errors the model makes.")
    if "accuracy" in q and any(k in q for k in ["what is", "define", "explain", "metric"]):
        return ("Accuracy is the proportion of predictions that a model gets correct out of all predictions. "
                "It is easy to understand, but it can be misleading when classes are imbalanced, so metrics such "
                "as precision, recall, and F1-score may also be needed.")
    if "precision" in q and "recall" in q:
        return ("Precision measures how many predicted positive cases are actually positive, while recall "
                "measures how many actual positive cases the model identifies. Precision matters when false "
                "alarms are costly, while recall matters when missing a positive case is costly.")
    if "feature scaling" in q or "standardization" in q or "normalization" in q:
        return ("Feature scaling puts numerical features on comparable scales. Normalization often rescales "
                "values to a chosen range, while standardization transforms values using the mean and standard "
                "deviation. Scaling is especially important for distance-based and gradient-based algorithms.")
    if "pandas" in q:
        return ("Pandas is a Python library used to work with structured data. Its main data structures are "
                "Series and DataFrame. It supports tasks such as loading CSV files, cleaning missing values, "
                "filtering rows, grouping data, and calculating summary statistics.")
    if "numpy" in q:
        return ("NumPy is a Python library for efficient numerical computing. It provides multidimensional "
                "arrays and functions for mathematical operations. It is widely used in data analysis and "
                "machine learning as a foundation for many other libraries.")
    if "streamlit" in q:
        return ("Streamlit is a Python framework for building interactive data apps and machine learning demos "
                "with relatively little web-development code. For example, a user can enter input values in a "
                "Streamlit form and view a model prediction on the same page.")
    if "api" in q and any(k in q for k in ["what is", "define", "explain"]):
        return ("An API, or Application Programming Interface, lets software components communicate through a "
                "defined set of rules. For example, an application can call a weather API to request current "
                "weather data and display the response.")

    # Common technical / academic questions: provide a relevant example rather than
    # repeating one generic answer for every question.
    if "inheritance" in q:
        return ("Inheritance is an object-oriented programming concept in which a child class "
                "can reuse attributes and methods from a parent class. For example, a Dog class "
                "can inherit a sound() method from an Animal class. It improves code reuse and "
                "reduces duplication.")
    if "polymorphism" in q:
        return ("Polymorphism means that the same interface or method name can behave differently "
                "for different objects. For example, different animal classes can implement their "
                "own sound() method. It makes code more flexible and easier to extend.")
    if "encapsulation" in q:
        return ("Encapsulation means bundling data and the methods that operate on it inside a class, "
                "while controlling how the data is accessed. It helps protect an object's internal "
                "state and keeps code organised.")
    if "abstraction" in q:
        return ("Abstraction means showing the essential features of something while hiding unnecessary "
                "implementation details. For example, a user can drive a car without needing to know "
                "how its engine works internally. It reduces complexity.")
    if "machine learning" in q and any(k in q for k in ["what is", "define", "explain", "meaning"]):
        return ("Machine learning is a branch of artificial intelligence in which computers learn patterns "
                "from data to make predictions or decisions. For example, a model can learn from past data "
                "to estimate crop yield. The model's performance should be evaluated on data it has not seen.")
    if "overfitting" in q:
        return ("Overfitting happens when a model learns the training data too closely, including noise, "
                "and then performs poorly on new data. It can be reduced with validation, simpler models, "
                "regularisation, or more representative training data.")
    if "underfitting" in q:
        return ("Underfitting happens when a model is too simple to learn the important patterns in the data. "
                "It performs poorly on both training and test data. A more suitable model or better features "
                "may help.")
    if "sql" in q and any(k in q for k in ["what is", "define", "explain", "meaning"]):
        return ("SQL stands for Structured Query Language. It is used to create, read, update, and delete data "
                "in relational databases. For example, a SELECT query retrieves records from a table.")
    if "python" in q and any(k in q for k in ["why", "useful", "what is"]):
        return ("Python is a high-level programming language known for readable syntax and a large library "
                "ecosystem. It is used in automation, data analysis, web development, and machine learning. "
                "For example, pandas can help analyse tabular data.")
    if "difference between" in q or "differentiate" in q:
        topic = str(question or "the two concepts").strip().rstrip("? .")
        return (f"To explain {topic.lower()}, I would define both terms first, compare their main purpose and "
                "features, and then give a short example. The key difference should be stated clearly at the end.")
    if any(k in q for k in ["what is", "define", "explain", "meaning of"]):
        topic = str(question or "this concept").strip().rstrip("? .")
        return (f"{topic} can be explained by first defining the main concept, then describing how it works "
                "and why it is useful. A good answer should include one accurate example and a short takeaway. "
                "Check the definition against your course notes before using this as a technical answer.")
    # For unknown HR questions, give a prompt-specific answer framework, not a repeated first-person script.
    topic = str(question or "this question").strip().rstrip("? .")
    return (f"For '{topic}', I would answer directly, give one truthful detail from my studies or experience, "
            "and explain what I learned or how it relates to the role. I would keep the answer concise and "
            "avoid claiming experience or results I do not have.")


def save_practice(tool, question, answer, score=None, feedback=None):
    """Keep practice only in the current Streamlit session."""
    st.session_state.setdefault("practice_history", [])
    st.session_state.practice_history.insert(0, {
        "tool": tool, "question": question, "answer": answer,
        "score": score, "feedback_json": json.dumps(feedback, ensure_ascii=False, default=str) if feedback is not None else None,
        "created_at": "This session",
    })

def load_practice_history(limit=100):
    return st.session_state.get("practice_history", [])[:limit]

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "Resume Helper"
if "interview_question" not in st.session_state:
    st.session_state.interview_question = ""
st.session_state.setdefault("practice_history", [])

# ------------------------- Page helpers --------------------
def show_hero():
    left, right = st.columns([1.05, 0.95], gap="medium")
    with left:
        st.markdown(
            """
            <div class="hero">
              <div class="hero-label">👋 Hello, welcome!</div>
              <div class="hero-title">
                Welcome to<br><span class="gradient-text">Urjaa AI Hub</span>
              </div>
              <div class="hero-subtitle">Your Personal AI Assistant</div>
              <div class="hero-description">
                Explore smart tools designed to help students with studies,
                coding, careers, and interviews.
              </div>
              <div class="badge">✨ Smarter Tools &nbsp; • &nbsp; Better You</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        # Build one complete HTML string. No f-string interpolation is used,
        # so SVG tags cannot accidentally be displayed as code.
        robot_html = (
            '<div class="hero robot-stage">'
            '<div class="robot-glow"></div>'
            '<div class="floating-chip chip-one">📚 Learn</div>'
            '<div class="floating-chip chip-two">💡 Create</div>'
            + ROBOT_SVG
            + "</div>"
        )
        st.markdown(robot_html, unsafe_allow_html=True)


# ---------------------- Study Planner session storage ----------------------
def load_study_plan():
    return st.session_state.get("study_plan", {})

def save_study_plan(data):
    """Keep the study plan only until this Streamlit session ends."""
    st.session_state["study_plan"] = data
    return True


def show_tool(tool_name):
    icon, description = TOOLS[tool_name]
    st.markdown(
        f'<div class="section-title">{icon} {html.escape(tool_name)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="section-subtitle">{html.escape(description)}</div>',
        unsafe_allow_html=True,
    )

    if tool_name == "Resume Helper":
        st.markdown("#### 📄 Upload your existing resume")
        uploaded_resume = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, and TXT.",
            key="resume_upload",
        )

        # Keep the editor text across Streamlit reruns. Only replace it when
        # the user selects a different file, so manual edits are not lost.
        st.session_state.setdefault("resume_text_input", "")
        st.session_state.setdefault("resume_loaded_file", None)
        extracted_resume = ""

        if uploaded_resume is not None:
            file_signature = f"{uploaded_resume.name}:{uploaded_resume.size}"
            file_name = uploaded_resume.name.lower()

            try:
                if file_name.endswith(".txt"):
                    extracted_resume = uploaded_resume.getvalue().decode(
                        "utf-8", errors="replace"
                    )
                elif file_name.endswith(".pdf"):
                    try:
                        import io
                        from pypdf import PdfReader
                        reader = PdfReader(io.BytesIO(uploaded_resume.getvalue()))
                        extracted_resume = "\n".join(
                            page.extract_text() or "" for page in reader.pages
                        )
                    except ImportError:
                        st.error(
                            "PDF reading requires pypdf. Install it with: "
                            "python -m pip install pypdf"
                        )
                elif file_name.endswith(".docx"):
                    try:
                        import io
                        from docx import Document
                        document = Document(io.BytesIO(uploaded_resume.getvalue()))
                        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
                        for table in document.tables:
                            for row in table.rows:
                                paragraphs.append(" | ".join(cell.text for cell in row.cells))
                        extracted_resume = "\n".join(paragraphs)
                    except ImportError:
                        st.error(
                            "DOCX reading requires python-docx. Install it with: "
                            "python -m pip install python-docx"
                        )

                if st.session_state["resume_loaded_file"] != file_signature:
                    if extracted_resume.strip():
                        st.session_state["resume_text_input"] = extracted_resume
                        st.session_state["resume_loaded_file"] = file_signature
                        st.success(f"Resume uploaded: {uploaded_resume.name}")
                    elif file_name.endswith((".pdf", ".docx")):
                        st.info(
                            "No selectable text was found. If this is a scanned PDF, "
                            "run OCR first or paste the resume text below."
                        )

                if extracted_resume.strip():
                    with st.expander("Preview extracted resume text"):
                        st.text(extracted_resume[:12000])

            except Exception as exc:
                st.error(f"Could not read this file: {exc}")

        resume = st.text_area(
            "Or paste/edit your resume text",
            height=220,
            placeholder="Upload a file above or paste your resume content here...",
            key="resume_text_input",
        )

        if st.button("Review Resume", key="review_resume"):
            if not resume.strip():
                st.warning("Please upload a readable resume file or enter your resume text first.")
            else:
                words = resume.split()
                c1, c2, c3 = st.columns(3)
                c1.metric("Word Count", len(words))
                c2.metric("Characters", len(resume))
                c3.metric("Lines", len([line for line in resume.splitlines() if line.strip()]))

                st.markdown("### 💡 Suggestions")
                suggestions = []
                if len(words) < 100:
                    suggestions.append(
                        "Add more detail about projects, skills, education, or experience."
                    )
                if not re.search(r"\b(project|experience|internship)\b", resume, re.I):
                    suggestions.append(
                        "Consider adding project, internship, or practical experience details."
                    )
                if not re.search(r"\b(python|sql|machine learning|skills)\b", resume, re.I):
                    suggestions.append("Include relevant technical skills for your target role.")
                if not re.search(r"\b(education|degree|college|university)\b", resume, re.I):
                    suggestions.append("Add an Education section with your degree and institution.")
                if not re.search(r"\b(email|phone|linkedin|github)\b", resume, re.I):
                    suggestions.append("Add appropriate contact details or professional profile links.")
                suggestions.append(
                    "Use clear section headings, concise bullet points, and consistent formatting."
                )
                for item in suggestions:
                    st.write("• " + item)
                st.caption(
                    "This review uses basic text checks. It does not send your resume to an AI model."
                )

    elif tool_name == "Python Helper":
        lessons = {
            "Variables": ("Variables store values.", "name = 'Urjaa'\\nage = 20\\nprint(name)"),
            "Conditions": ("Conditions let a program make decisions.", "marks = 75\\n\\nif marks >= 40:\\n    print('Pass')\\nelse:\\n    print('Try again')"),
            "Loops": ("Loops repeat instructions.", "for i in range(1, 6):\\n    print(i)"),
            "Functions": ("Functions are reusable blocks of code.", "def greet(name):\\n    return 'Hello ' + name\\n\\nprint(greet('Urjaa'))"),
            "Lists": ("Lists store multiple values.", "marks = [80, 75, 90]\\nprint(marks[0])"),
            "Dictionaries": ("Dictionaries store key-value pairs.", "student = {'name': 'Urjaa'}\\nprint(student['name'])"),
        }

        topic = st.selectbox("Choose a Python topic", list(lessons))
        explanation, code_sample = lessons[topic]

        st.info(explanation)

        st.markdown("### 💻 Python Code")
        st.code(code_sample, language="python")

        outputs = {
            "Variables": "Urjaa",
            "Conditions": "Pass",
            "Loops": "1\\n2\\n3\\n4\\n5",
            "Functions": "Hello Urjaa",
            "Lists": "80",
            "Dictionaries": "Urjaa",
        }

        st.markdown("### 🖥️ Expected Output")
        st.code(outputs[topic], language="text")

    elif tool_name == "Career Advisor":
        career_map = {
            "Python Programming": ["Python Developer", "Backend Developer"],
            "Data Analysis": ["Data Analyst", "Business Intelligence Analyst"],
            "Machine Learning": ["Machine Learning Engineer", "AI Engineer"],
            "Cloud Computing": ["Cloud Support Associate", "Cloud Engineer"],
            "Web Development": ["Web Developer", "Python Full-Stack Developer"],
            "Problem Solving": ["Software Developer", "QA Automation Engineer"],
        }
        interests = st.multiselect("Select your interests", list(career_map))
        if st.button("Explore Careers", key="career_button"):
            if not interests:
                st.warning("Please select at least one interest.")
            else:
                st.markdown("### 🎯 Career paths to explore")
                for interest in interests:
                    st.markdown(f"**{interest}**")
                    for career in career_map[interest]:
                        st.write("• " + career)

    elif tool_name == "Study Planner":
        saved_plan = load_study_plan()
        default_subjects = saved_plan.get("subjects_text", "")
        default_hours = int(saved_plan.get("hours", 3))
        default_hours = min(12, max(1, default_hours))
        try:
            saved_exam_date = date.fromisoformat(saved_plan.get("exam_date", date.today().isoformat()))
        except (TypeError, ValueError):
            saved_exam_date = date.today()
        if saved_exam_date < date.today():
            saved_exam_date = date.today()

        st.markdown("### 📝 Plan your studies")
        subjects_text = st.text_input(
            "Subjects (separate with commas)",
            value=default_subjects,
            placeholder="Python, SQL, Machine Learning",
            key="study_subjects_input",
        )
        exam_date = st.date_input(
            "Exam date",
            value=saved_exam_date,
            min_value=date.today(),
            key="study_exam_date_input",
        )
        hours = st.number_input(
            "Available study hours per day",
            min_value=1,
            max_value=12,
            value=default_hours,
            key="study_hours_input",
        )

        if st.button("💾 Save & Create My Study Plan", key="study_button"):
            subjects = [item.strip() for item in subjects_text.split(",") if item.strip()]
            # Remove duplicate subjects while keeping the original order.
            subjects = list(dict.fromkeys(subjects))
            if not subjects:
                st.warning("Please enter at least one subject.")
            elif exam_date < date.today():
                st.warning("Please choose today or a future exam date.")
            else:
                previous_completed = saved_plan.get("completed_tasks", [])
                task_names = [f"{subject} — {task}" for subject in subjects for task in ("Read notes", "Practice questions", "Revision")]
                plan_data = {
                    "subjects_text": ", ".join(subjects),
                    "subjects": subjects,
                    "exam_date": exam_date.isoformat(),
                    "hours": int(hours),
                    "completed_tasks": [task for task in previous_completed if task in task_names],
                }
                if save_study_plan(plan_data):
                    st.session_state["study_plan_saved_notice"] = True
                    st.rerun()
                else:
                    st.error("Could not save the planner file. Check that this folder is writable.")

        current_plan = load_study_plan()
        if current_plan.get("subjects"):
            subjects = current_plan.get("subjects", [])
            try:
                current_exam_date = date.fromisoformat(current_plan.get("exam_date", date.today().isoformat()))
            except (TypeError, ValueError):
                current_exam_date = date.today()
            days_left = max(0, (current_exam_date - date.today()).days)

            if st.session_state.pop("study_plan_saved_notice", False):
                st.success("Your Study Planner is available for this session only!")

            st.markdown("### 📅 Your Saved Study Plan")
            m1, m2, m3 = st.columns(3)
            m1.metric("Subjects", len(subjects))
            m2.metric("Days until exam", days_left)
            m3.metric("Study hours/day", current_plan.get("hours", 3))

            per_subject = current_plan.get("hours", 3) / len(subjects)
            st.markdown("#### ⏰ Daily timetable")
            for i, subject in enumerate(subjects, start=1):
                st.write(f"**{i}. {subject}** — {per_subject:.1f} hour(s)")
            st.caption("Tip: take short breaks between subjects and leave time for revision.")

            st.markdown("#### ✅ Study task checklist")
            completed_tasks = set(current_plan.get("completed_tasks", []))
            all_tasks = [f"{subject} — {task}" for subject in subjects for task in ("Read notes", "Practice questions", "Revision")]
            for task_index, task in enumerate(all_tasks):
                checkbox_key = f"study_task_{task_index}_{re.sub(r'[^a-zA-Z0-9]+', '_', task).strip('_')}"
                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = task in completed_tasks
                st.checkbox(task, key=checkbox_key)

            updated_completed = []
            for task_index, task in enumerate(all_tasks):
                checkbox_key = f"study_task_{task_index}_{re.sub(r'[^a-zA-Z0-9]+', '_', task).strip('_')}"
                if st.session_state.get(checkbox_key, False):
                    updated_completed.append(task)
            current_plan["completed_tasks"] = updated_completed
            if save_study_plan(current_plan):
                progress = len(updated_completed) / len(all_tasks) if all_tasks else 0
                st.progress(progress, text=f"Progress: {len(updated_completed)} of {len(all_tasks)} tasks completed")
            else:
                st.warning("Your checklist is visible, but changes could not be saved to the local file.")
            st.caption("Your study plan is kept temporarily in this session and is not saved to a file or database.")

    elif tool_name == "Text Summarizer":
        st.markdown("Paste notes, an article, or study material. The tool will select important sentences and make a shorter version.")
        source_text = st.text_area(
            "Your text",
            height=240,
            placeholder="Paste your paragraph or study notes here...",
            key="summarizer_source_text",
        )
        c1, c2 = st.columns(2)
        with c1:
            ratio = st.slider("Summary length (%)", min_value=20, max_value=80, value=40, step=10)
        with c2:
            summary_style = st.selectbox("Summary format", ["Paragraph", "Key Points"])

        if st.button("✨ Summarize Text", key="summarize_button"):
            if not source_text.strip():
                st.warning("Please paste some text first.")
            else:
                sentences = [
                    sentence.strip()
                    for sentence in re.split(r"(?<=[.!?])\s+|\n+", source_text.strip())
                    if sentence.strip()
                ]

                # Rank sentences using simple word frequency and choose the most relevant ones.
                stop_words = {
                    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
                    "be", "been", "being", "to", "of", "in", "on", "for", "with", "as",
                    "by", "at", "from", "it", "this", "that", "these", "those", "we", "you",
                    "they", "he", "she", "i", "our", "their", "its", "can", "could", "will",
                    "would", "should", "has", "have", "had", "do", "does", "did", "not", "than",
                    "then", "also", "such", "into", "about", "which", "who", "what", "when",
                }
                words = re.findall(r"[A-Za-z0-9']+", source_text.lower())
                frequencies = {}
                for word in words:
                    if word not in stop_words and len(word) > 2:
                        frequencies[word] = frequencies.get(word, 0) + 1

                def sentence_score(sentence):
                    sentence_words = re.findall(r"[A-Za-z0-9']+", sentence.lower())
                    useful_words = [w for w in sentence_words if w not in stop_words and len(w) > 2]
                    if not useful_words:
                        return 0
                    return sum(frequencies.get(w, 0) for w in useful_words) / len(useful_words)

                desired_count = max(1, min(len(sentences), round(len(sentences) * ratio / 100)))
                ranked_indices = sorted(range(len(sentences)), key=lambda i: sentence_score(sentences[i]), reverse=True)
                selected_indices = sorted(ranked_indices[:desired_count])
                selected_sentences = [sentences[i] for i in selected_indices]
                summary = " ".join(selected_sentences)

                st.session_state["summarizer_result"] = summary
                st.session_state["summarizer_original"] = source_text
                st.session_state["summarizer_style"] = summary_style

        if st.session_state.get("summarizer_result"):
            summary = st.session_state["summarizer_result"]
            original = st.session_state.get("summarizer_original", source_text)
            st.markdown("### 📄 Your Summary")
            if st.session_state.get("summarizer_style") == "Key Points":
                for sentence in re.split(r"(?<=[.!?])\s+", summary):
                    if sentence.strip():
                        st.markdown(f"- {sentence.strip()}")
            else:
                st.write(summary)

            original_words = len(original.split())
            summary_words = len(summary.split())
            reduction = max(0, round((1 - summary_words / original_words) * 100)) if original_words else 0
            m1, m2, m3 = st.columns(3)
            m1.metric("Original Words", original_words)
            m2.metric("Summary Words", summary_words)
            m3.metric("Shorter By", f"{reduction}%")
            st.download_button(
                "⬇️ Download Summary",
                data=summary,
                file_name="urjaa_summary.txt",
                mime="text/plain",
                key="download_summary",
            )
            st.caption("This version uses simple word-frequency sentence ranking. It works locally and does not call an external AI model.")

    elif tool_name == "Interview Prep":
        st.markdown("### 🎤 Interview Prep — Answer Analysis")
        st.write("Practice unlimited questions. Review checks now look at relevant concepts, keywords, grammar signals, clarity, examples, and professional answer structure—not only word count. This is a local rule-based coach, not a full AI evaluator.")

        question_bank = {
            "HR / Introduction": [
                "Tell me about yourself", "What are your strengths?", "What is one weakness you are working on?",
                "Why should we select you?", "Why did you choose AI and Data Science?", "What motivates you?",
                "What are your short-term and long-term goals?", "How do you manage your time?",
                "How do you handle pressure?", "How do you respond to feedback?", "What makes you a good teammate?",
                "Tell me about a challenge you overcame", "Tell me about a mistake and what you learned",
                "Why are you interested in this internship?", "What achievement are you proud of?",
                "Where do you see yourself in three years?"
            ],
            "Python / Programming": [
                "What is Python and where is it useful?", "Explain the difference between a list and a tuple",
                "What is a dictionary in Python?", "What is a function and why do we use it?",
                "Explain mutable and immutable data types", "What is exception handling?",
                "What is the difference between a for loop and a while loop?", "What is object-oriented programming?",
                "What is the purpose of a Python library?", "How would you debug a Python program?",
                "What is the difference between a syntax error and a logical error?", "What is list comprehension?",
                "What is a class and what is an object?", "What is inheritance?", "What is the difference between == and is?"
            ],
            "SQL / Data Analytics": [
                "What is SQL used for?", "What is a primary key?", "What is a foreign key?",
                "Explain the difference between WHERE and HAVING", "What is the difference between DELETE and DROP?",
                "What is a JOIN? Explain common types", "What is GROUP BY used for?",
                "What is the difference between COUNT(*) and COUNT(column)?", "What is NULL in SQL?",
                "How would you find duplicate rows?", "What is normalization?", "What is a subquery?",
                "What is the difference between INNER JOIN and LEFT JOIN?", "What is data cleaning?",
                "How would you handle missing values in a dataset?", "What is an outlier?",
                "What is the difference between Excel and Power BI?", "What is a dashboard?",
                "What is data visualization?"
            ],
            "AI / Machine Learning": [
                "What is Artificial Intelligence?", "What is Machine Learning?", "What is Deep Learning?",
                "Explain supervised and unsupervised learning", "What is the difference between classification and regression?",
                "What is overfitting?", "Why do we split data into training and testing sets?",
                "What is a feature in a dataset?", "What is data preprocessing?", "What is a confusion matrix?",
                "Explain accuracy, precision, recall and F1-score", "What is a Random Forest model?",
                "Why do we encode categorical data?", "What is cross-validation?", "What is data leakage?",
                "What is clustering?", "What is natural language processing?"
            ],
            "Projects": [
                "Explain a project you have developed", "What problem does your project solve?",
                "Why did you choose this project?", "Which technologies did you use and why?",
                "What was your role in the project?", "What was the biggest challenge in your project?",
                "How did you test your project?", "How did you evaluate your ML model?",
                "What would you improve if you had more time?", "How did you handle missing or inconsistent data?",
                "Why did you choose that algorithm?", "How would you explain your project to a beginner?",
                "What did you learn while building your project?", "What limitations does your project have?"
            ],
            "Situational / Behavioural": [
                "What would you do if you had two urgent deadlines?", "How would you respond to constructive criticism?",
                "What would you do if your code did not work before a deadline?",
                "How would you handle a disagreement with a teammate?", "How would you learn a tool you have never used?",
                "What would you do if you made a mistake in a report?", "How would you explain a complex topic simply?",
                "How would you respond if you did not understand a task?", "Describe a time you worked toward a goal",
                "What would you do if a team member missed a deadline?"
            ]
        }
        category = st.selectbox("Interview category", list(question_bank), key="prep_category")
        if "prep_question_history" not in st.session_state:
            st.session_state.prep_question_history = []
        if "prep_current_question" not in st.session_state:
            st.session_state.prep_current_question = ""
        if "prep_question_count" not in st.session_state:
            st.session_state.prep_question_count = 0

        followups = [
            "Explain with a practical example: {q}",
            "How would you explain this professionally in an interview? {q}",
            "What is your practical understanding of this? {q}",
            "Can you give a real-world example related to this? {q}",
            "Explain the key points and why they matter: {q}",
            "How would you explain this to a beginner? {q}",
        ]

        def make_prep_question(selected_category):
            base = random.choice(question_bank[selected_category])
            return base if random.random() < 0.65 else random.choice(followups).format(q=base)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎲 Ask Me a Question", key="prep_next_question"):
                new_q = make_prep_question(category)
                for _ in range(20):
                    if new_q not in st.session_state.prep_question_history[-30:]:
                        break
                    new_q = make_prep_question(category)
                st.session_state.prep_current_question = new_q
                st.session_state.prep_question_history.append(new_q)
                st.session_state.prep_question_count += 1
                st.session_state.pop("prep_answer", None)
                st.session_state.pop("prep_review_result", None)
        with c2:
            if st.button("🔄 Reset Practice", key="prep_reset"):
                st.session_state.prep_question_history = []
                st.session_state.prep_current_question = ""
                st.session_state.prep_question_count = 0
                st.session_state.pop("prep_answer", None)
                st.session_state.pop("prep_review_result", None)

        st.metric("Questions Practiced", st.session_state.prep_question_count)

        # Concept rubric and concise model answers for common interview questions.
        concept_rules = [
            (r"group\s*by", ["group", "aggregate", "count", "sum", "avg", "category", "rows"],
             "GROUP BY groups rows that share the same value in one or more columns. It is commonly used with aggregate functions such as COUNT(), SUM(), AVG(), MIN(), and MAX() to calculate a result for each group."),
            (r"where.*having|having.*where", ["where", "before", "group", "having", "after", "aggregate", "filter"],
             "WHERE filters individual rows before grouping. HAVING filters groups after GROUP BY, often using aggregate conditions such as COUNT(*) > 1."),
            (r"primary key", ["unique", "identify", "row", "null"],
             "A primary key uniquely identifies each row in a table. It must contain unique values and cannot be NULL."),
            (r"foreign key", ["reference", "table", "relationship", "primary key"],
             "A foreign key is a column or set of columns that references a key in another table. It helps maintain referential integrity between related tables."),
            (r"inner join", ["matching", "rows", "both", "tables"],
             "INNER JOIN returns rows with matching values in both tables, based on the join condition."),
            (r"left join", ["all rows", "left", "matching", "null"],
             "LEFT JOIN returns every row from the left table and matching rows from the right table. When no match exists, right-table columns are NULL."),
            (r"sql used|what is sql", ["query", "database", "retrieve", "insert", "update"],
             "SQL (Structured Query Language) is used to query and manage relational databases. It can retrieve, insert, update, and delete data, and define database structures."),
            (r"list and a tuple|difference between a list and a tuple", ["mutable", "immutable", "change", "square bracket", "parentheses"],
             "A list is mutable, so its elements can be changed, and it is usually written with square brackets. A tuple is immutable and is usually written with parentheses."),
            (r"what is python", ["programming", "language", "readable", "automation"],
             "Python is a high-level, general-purpose programming language known for readable syntax. It is used in automation, web development, data analysis, and machine learning."),
            (r"what is a function|what is function", ["reusable", "block", "code", "parameter", "return"],
             "A function is a reusable block of code that performs a specific task. It can accept parameters and return a result, which helps reduce repetition and improve organization."),
            (r"machine learning", ["data", "learn", "pattern", "prediction", "model"],
             "Machine Learning is a field of AI where algorithms learn patterns from data to make predictions or decisions without being explicitly programmed for every case."),
            (r"overfitting", ["training", "unseen", "generalize", "test", "noise"],
             "Overfitting happens when a model learns the training data too closely, including noise, and performs poorly on unseen data. It can be reduced with validation, regularization, simpler models, or more representative data."),
            (r"classification and regression", ["classification", "category", "class", "regression", "continuous", "value"],
             "Classification predicts a category or class, such as approved or rejected. Regression predicts a numerical value, such as crop yield or house price."),
            (r"training and testing|training set.*testing", ["train", "test", "unseen", "evaluate", "generalization"],
             "The training set is used to fit the model. The test set provides an estimate of how well it performs on unseen data, helping us assess generalization."),
            (r"random forest", ["decision tree", "trees", "ensemble", "vote", "average"],
             "Random Forest is an ensemble model that combines many decision trees. For classification, trees vote; for regression, their predictions are commonly averaged, improving robustness compared with a single tree."),
            (r"tell me about yourself", ["education", "skills", "project", "goal"],
             "I am a third-year B.E. student in Artificial Intelligence and Data Science. I am developing my skills in Python, SQL, data analysis, and machine learning, and I have worked on projects that apply these skills to practical problems. I am looking for an opportunity to learn, contribute, and grow professionally."),
            (r"strength", ["strength", "example", "improve", "team"],
             "One of my strengths is being willing to learn and work consistently. For example, when I face an unfamiliar topic, I break it into smaller parts, practise, and ask for feedback. This helps me improve step by step."),
            (r"weakness", ["improve", "working", "practice", "progress"],
             "One area I am improving is my confidence when explaining technical ideas. I am working on it by practising short explanations, preparing examples, and asking for feedback."),
            (r"project", ["problem", "role", "tools", "result", "learned"],
             "I would explain my project by covering the problem, the goal, the tools I used, my contribution, the result, and what I learned. I would also mention one challenge and how I addressed it."),
        ]

        def analyze_answer(question, answer):
            q, a = question.lower(), answer.lower()
            words = re.findall(r"\b[\w+#.-]+\b", answer)
            word_count = len(words)
            matched_rule = next((rule for rule in concept_rules if re.search(rule[0], q)), None)
            expected = matched_rule[1] if matched_rule else []
            model_answer = matched_rule[2] if matched_rule else sample_professional_answer(question)
            # Keyword matching uses meaningful terms, not only total word count.
            keyword_hits = [kw for kw in expected if kw in a]
            keyword_score = round(100 * len(keyword_hits) / len(expected)) if expected else 0
            sentence_parts = [x.strip() for x in re.split(r"(?<=[.!?])\s+", answer.strip()) if x.strip()]
            grammar_issues = []
            if answer.strip() and answer.strip()[0].islower():
                grammar_issues.append("Start your first sentence with a capital letter.")
            if answer.strip() and answer.strip()[-1] not in ".!?":
                grammar_issues.append("Finish the answer with suitable punctuation.")
            if re.search(r"\bi (is|are|were|have|has)\b", a):
                grammar_issues.append("Check subject–verb agreement, for example, use ‘I am’ rather than ‘I is’.")
            fillers = [x for x in ["umm", "uh", "like", "basically", "actually"] if re.search(rf"\b{re.escape(x)}\b", a)]
            if fillers:
                grammar_issues.append("Reduce filler words such as " + ", ".join(fillers) + ".")
            has_example = any(x in a for x in ["for example", "for instance", "such as", "in my project", "e.g.", "one example"])
            has_reason = any(x in a for x in ["because", "therefore", "so that", "which helps", "as a result"])
            professional_phrases = any(x in a for x in ["i worked", "i developed", "i learned", "i would", "the main purpose", "this helps", "for example", "in my project"])
            clarity_score = 0
            if word_count >= 20: clarity_score += 30
            if len(sentence_parts) >= 2: clarity_score += 20
            if has_example: clarity_score += 25
            if has_reason: clarity_score += 15
            if professional_phrases: clarity_score += 10
            clarity_score = min(100, clarity_score)
            # Overall score combines answer-specific keyword coverage and communication structure.
            if expected:
                score = round(keyword_score * 0.65 + clarity_score * 0.35)
            else:
                score = clarity_score
            return {"words": word_count, "expected": expected, "hits": keyword_hits,
                    "keyword_score": keyword_score, "clarity_score": clarity_score,
                    "score": score, "grammar_issues": grammar_issues,
                    "has_example": has_example, "has_reason": has_reason,
                    "professional": professional_phrases, "model_answer": model_answer,
                    "sentence_count": len(sentence_parts)}

        if st.session_state.prep_current_question:
            st.markdown("### 🎤 Your Interview Question")
            st.info(st.session_state.prep_current_question)
            answer = st.text_area("Write your answer", key="prep_answer", height=160,
                                  placeholder="Answer in your own words. Explain the concept, add a relevant example, and say why it matters...")
            if st.button("✅ Analyze My Answer", key="prep_review"):
                if answer.strip():
                    st.session_state.prep_review_result = analyze_answer(st.session_state.prep_current_question, answer.strip())
                    review_data = st.session_state.prep_review_result
                    save_practice("Interview Prep", st.session_state.prep_current_question, answer.strip(),
                                  review_data.get("score"), review_data)
                    st.success("Your answer and feedback are available in My Saved Practice for this session only.")
                else:
                    st.warning("Write your answer before reviewing.")

            result = st.session_state.get("prep_review_result")
            if result:
                st.markdown("### 📊 Answer Feedback")
                m1, m2, m3 = st.columns(3)
                m1.metric("Practice score", f"{result['score']}/100")
                m2.metric("Relevant keyword coverage", f"{result['keyword_score']}%" if result['expected'] else "General rubric")
                m3.metric("Word count", result['words'])
                if result['expected']:
                    st.markdown("#### 🔑 Important keywords")
                    st.write("**Detected:** " + (", ".join(result['hits']) if result['hits'] else "No expected keywords detected yet."))
                    missing = [x for x in result['expected'] if x not in result['hits']]
                    st.write("**Consider including:** " + (", ".join(missing) if missing else "Good coverage of the main concepts."))
                st.markdown("#### ✍️ Grammar & communication")
                if result['grammar_issues']:
                    for issue in result['grammar_issues']:
                        st.write("- " + issue)
                else:
                    st.success("No basic grammar flags detected. Read it aloud once to check natural flow.")
                if result['words'] < 20:
                    st.warning("Your answer may be too short. Try: definition → how/why it works → example → conclusion.")
                elif result['words'] > 150:
                    st.info("Your answer is quite long. Keep the main point first and remove repeated details.")
                else:
                    st.success("Your answer length is reasonable. Make sure each sentence adds a useful point.")
                if not result['has_example']:
                    st.info("Example tip: introduce one with ‘For example…’ or describe a real project or situation.")
                if not result['has_reason']:
                    st.info("Explain why the concept matters using ‘because’, ‘this helps’, or ‘as a result’.")
                if not result['professional']:
                    st.info("Professional wording tip: use clear phrases such as ‘The main purpose is…’, ‘In my project…’, or ‘I used… because…’.")
                improved = improve_interview_answer(st.session_state.prep_current_question, st.session_state.get("prep_answer", ""))
                if isinstance(improved, tuple):
                    improved_text, improvement_tip = improved
                else:
                    improved_text, improvement_tip = improved, ""
                st.markdown("#### ✨ Corrected & Improved Version of Your Answer")
                st.write(improved_text)
                st.caption("Basic rule-based English cleanup. Please check that the wording still matches what you really mean.")
                st.info(improvement_tip)
                st.markdown("#### 🧑‍💼 Example of a professional answer")
                st.write(result['model_answer'])
                st.caption("The score is an approximate, rule-based practice aid. It checks selected keywords and communication signals; it cannot reliably judge every technically correct answer or fully understand grammar like a human interviewer.")
        else:
            st.info("Click **Ask Me a Question** to begin your interview practice.")

    elif tool_name == "Free Voice Interview":
        st.markdown("### 🎙️ Free Voice Interview")
        st.write("The interviewer will ask you one question at a time. Answer it, review your feedback, then click **Next Question**. There is no fixed question limit.")

        # A free, template-based generator: it can keep creating combinations without a paid API.
        categories = {
            "HR / Introduction": [
                "Tell me about yourself", "What are your strengths", "What is one area you are improving",
                "Why should we hire you", "Why did you choose AI and Data Science", "What motivates you",
                "How do you handle pressure", "Describe a time you learned something difficult",
                "What are your career goals", "How do you manage your time", "How do you respond to feedback",
                "What makes you a good teammate", "Tell me about a mistake and what you learned",
                "How would your classmates describe you", "Why are you interested in this internship"
            ],
            "Python / Technical": [
                "What is Python and where is it useful", "Explain the difference between a list and a tuple",
                "What is a dictionary in Python", "What is a function and why do we use it",
                "Explain mutable and immutable data types", "What is exception handling",
                "What is the difference between a for loop and a while loop", "What is object-oriented programming",
                "What is the purpose of a Python library", "How would you debug a Python program",
                "What is the difference between a syntax error and a logical error", "What is SQL used for",
                "Explain a primary key", "What is the difference between WHERE and HAVING in SQL"
            ],
            "AI / Machine Learning": [
                "What is Machine Learning", "Explain supervised and unsupervised learning",
                "What is the difference between classification and regression", "What is overfitting",
                "Why do we split data into training and testing sets", "What is a feature in a dataset",
                "What is data preprocessing", "What is a confusion matrix", "Explain accuracy, precision and recall",
                "What is a Random Forest model", "Why do we encode categorical data",
                "What is the purpose of a validation set", "How can missing values be handled",
                "What is the difference between AI, ML and Deep Learning", "How would you explain an ML result to a non-technical person"
            ],
            "Projects": [
                "Explain a project you have developed", "What problem does your project solve",
                "Why did you choose this project", "Which technologies did you use and why",
                "What was your role in the project", "What was the biggest challenge in your project",
                "How did you test your project", "How did you evaluate your model",
                "What would you improve if you had more time", "What did you learn from building the project",
                "How would you explain your project to a beginner", "How did you handle errors or unexpected results",
                "What makes your project useful", "How could your project be used in the real world"
            ],
            "Situational / Behavioural": [
                "What would you do if you did not understand a task", "How would you handle a disagreement in a team",
                "What would you do if you had two deadlines on the same day", "How do you learn a new technology",
                "How would you respond if your project failed during a demo", "How do you check whether information is reliable",
                "What would you do if you made an error in your work", "How would you help a teammate who is stuck",
                "How do you stay organized during a busy week", "Describe a time you solved a problem"
            ]
        }
        category = st.selectbox("Interview type", list(categories), key="voice_interview_category")
        difficulty = st.select_slider("Difficulty", options=["Beginner", "Intermediate", "Advanced"], value="Beginner", key="voice_interview_difficulty")

        # Rotate through questions without asking the user to choose a question.
        if "voice_q_history" not in st.session_state:
            st.session_state.voice_q_history = []
        if "voice_current_question" not in st.session_state:
            st.session_state.voice_current_question = ""
        if "voice_current_category" not in st.session_state:
            st.session_state.voice_current_category = category

        def make_question(cat, level):
            base = random.choice(categories[cat])
            if level == "Beginner":
                prefixes = ["", "In simple words, ", "As a student, "]
                endings = ["?", "? Give a short example.", "? Explain it in your own words."]
            elif level == "Intermediate":
                prefixes = ["", "Please explain clearly: ", "From your learning or project experience, "]
                endings = ["?", "? Include an example.", "? Explain your reasoning."]
            else:
                prefixes = ["", "Think critically and explain: ", "In a real workplace situation, "]
                endings = ["?", "? Discuss the trade-offs and give an example.", "? Explain your approach step by step."]
            q = random.choice(prefixes) + base[0].lower() + base[1:] + random.choice(endings)
            return q[0].upper() + q[1:]

        left, right = st.columns(2)
        with left:
            if st.button("▶️ Start / Next Question", type="primary", key="voice_next_question"):
                # Avoid immediate repeats; the bank and prompt variations allow continued practice.
                candidate = make_question(category, difficulty)
                attempts = 0
                while candidate in st.session_state.voice_q_history[-12:] and attempts < 20:
                    candidate = make_question(category, difficulty)
                    attempts += 1
                st.session_state.voice_current_question = candidate
                st.session_state.voice_current_category = category
                st.session_state.voice_q_history.append(candidate)
                st.session_state.voice_answer_reviewed = False
        with right:
            st.metric("Questions asked this session", len(st.session_state.voice_q_history))

        question = st.session_state.voice_current_question
        if question:
            st.markdown("#### 🗣️ Interviewer asks:")
            st.info(question)
            question_json = json.dumps(question)
            speech_html = f"""
            <div style="background:#17132d;padding:12px;border-radius:12px;color:white;font-family:Arial,sans-serif">
              <button onclick="speakQuestion()" style="background:linear-gradient(90deg,#832eff,#155fff);color:white;border:0;padding:10px 15px;border-radius:8px;cursor:pointer">🔊 Read Question</button>
              <button onclick="stopQuestion()" style="background:#39334f;color:white;border:0;padding:10px 14px;border-radius:8px;cursor:pointer;margin-left:8px">⏹ Stop</button>
              <script>
                const questionText = {question_json};
                function speakQuestion() {{
                  if (!('speechSynthesis' in window)) {{ alert('Text-to-speech is not supported in this browser.'); return; }}
                  window.speechSynthesis.cancel();
                  const utterance = new SpeechSynthesisUtterance(questionText);
                  utterance.lang = 'en-IN'; utterance.rate = 0.9;
                  window.speechSynthesis.speak(utterance);
                }}
                function stopQuestion() {{ if ('speechSynthesis' in window) window.speechSynthesis.cancel(); }}
              </script>
            </div>"""
            components.html(speech_html, height=58)

            st.markdown("#### 🎤 Your answer")
            mic_html = """
            <div style="background:#17132d;padding:13px;border-radius:12px;color:white;font-family:Arial,sans-serif">
              <button onclick="startListening()" style="background:linear-gradient(90deg,#832eff,#155fff);color:white;border:0;padding:10px 15px;border-radius:8px;cursor:pointer">🎙️ Start Speaking</button>
              <button onclick="stopListening()" style="background:#39334f;color:white;border:0;padding:10px 14px;border-radius:8px;cursor:pointer;margin-left:8px">⏹ Stop</button>
              <p id="status" style="margin:10px 0">Allow microphone access when prompted.</p>
              <textarea id="transcript" rows="4" placeholder="Your spoken answer appears here..." style="width:100%;box-sizing:border-box;padding:10px;border-radius:8px"></textarea>
              <button onclick="copyTranscript()" style="background:#39334f;color:white;border:0;padding:9px 13px;border-radius:8px;cursor:pointer;margin-top:8px">📋 Copy Transcript</button>
              <script>
                let recognition = null;
                function startListening() {
                  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
                  if (!SR) { document.getElementById('status').innerText = 'Speech recognition is not supported here. Type your answer below.'; return; }
                  if (recognition) { try { recognition.stop(); } catch(e) {} }
                  recognition = new SR(); recognition.lang = 'en-IN'; recognition.continuous = true; recognition.interimResults = true;
                  recognition.onstart = () => document.getElementById('status').innerText = 'Listening... speak clearly.';
                  recognition.onresult = function(event) { let text = ''; for (let i = 0; i < event.results.length; i++) text += event.results[i][0].transcript + ' '; document.getElementById('transcript').value = text.trim(); };
                  recognition.onerror = function(event) { document.getElementById('status').innerText = 'Microphone error: ' + event.error; };
                  recognition.onend = () => document.getElementById('status').innerText = 'Stopped. Copy transcript and paste below.';
                  try { recognition.start(); } catch(e) { document.getElementById('status').innerText = 'Could not start microphone. Try again.'; }
                }
                function stopListening() { if (recognition) recognition.stop(); }
                function copyTranscript() { const field = document.getElementById('transcript'); field.select(); field.setSelectionRange(0, 99999); try { document.execCommand('copy'); document.getElementById('status').innerText = 'Transcript copied. Paste below.'; } catch(e) { document.getElementById('status').innerText = 'Select and copy the transcript manually.'; } }
              </script>
            </div>"""
            components.html(mic_html, height=265)

            answer = st.text_area("Paste your transcript here or type your answer", height=130, key="free_voice_interview_answer", placeholder="Answer the interviewer in your own words...")
            if st.button("📊 Review Answer", key="free_voice_review_button"):
                if not answer.strip():
                    st.warning("Please speak and paste the transcript, or type your answer first.")
                else:
                    words = answer.split()
                    word_count = len(words)
                    normalized = re.sub(r"[^a-z0-9\s]", " ", answer.lower())
                    terms_by_category = {
                        "HR / Introduction": ["student", "skills", "project", "learning", "experience", "career", "team", "goal", "example"],
                        "Python / Technical": ["python", "function", "data", "list", "tuple", "error", "sql", "example", "program"],
                        "AI / Machine Learning": ["model", "data", "training", "testing", "feature", "accuracy", "classification", "regression", "example"],
                        "Projects": ["project", "problem", "python", "model", "dataset", "result", "challenge", "evaluation", "technology", "example"],
                        "Situational / Behavioural": ["team", "problem", "solution", "communication", "priority", "learned", "example", "result", "feedback"]
                    }
                    terms = terms_by_category[st.session_state.voice_current_category]
                    found = [term for term in terms if term in normalized]
                    score = min(100, round(min(word_count / 45, 1) * 40 + (len(found) / len(terms)) * 60))
                    save_practice("Free Voice Interview", question, answer.strip(), score,
                                  {"word_count": word_count, "detected_terms": found, "category": st.session_state.voice_current_category})
                    st.success("Your voice-interview answer and feedback are available in My Saved Practice for this session only.")
                    st.markdown("### 📋 Practice Feedback")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Basic practice score", f"{score}/100")
                    c2.metric("Word count", word_count)
                    c3.metric("Relevant terms", f"{len(found)}/{len(terms)}")
                    st.progress(score / 100, text="Rule-based practice score")
                    if word_count < 15:
                        st.warning("Your answer is quite short. Try adding your main point and one example.")
                    elif len(found) < 2:
                        st.info("Add more details directly related to the question. Explain your reasoning or give an example.")
                    else:
                        st.success("Nice practice! Make sure your answer is accurate, clear, and based on your real experience.")
                    st.write("**Detected relevant terms:** " + (", ".join(found) if found else "None of the configured terms were detected."))
                    improved = improve_interview_answer(question, answer)
                    if isinstance(improved, tuple):
                        improved_text, improvement_tip = improved
                    else:
                        improved_text, improvement_tip = improved, ""
                    st.markdown("#### ✨ Your Corrected & Improved Answer")
                    st.write(improved_text)
                    st.caption("This makes basic wording and punctuation improvements only. Check that it preserves your meaning.")
                    st.info(improvement_tip)
                    st.markdown("#### 🧑‍💼 Sample professional answer")
                    st.write(sample_professional_answer(question))
                    st.caption("Use this as a guide, then edit it to match your real background and experience.")
                    st.markdown("#### ✅ Self-review")
                    st.write("- Did I answer the question directly?")
                    st.write("- Did I speak clearly and use complete sentences?")
                    st.write("- Did I give an example where useful?")
                    st.write("- Did I avoid memorized answers and use my own words?")
                    st.caption("This free tool creates questions from built-in templates and checks answer length/keywords. It does not use a paid AI API or verify factual correctness. Browser speech recognition depends on browser support and may require internet access.")


def open_tool(tool_name):
    st.session_state.selected_tool = tool_name
    st.session_state.page = "🧰 AI Tools"



# ------------------------- Main pages ----------------------
if st.session_state.page == "📚 My Saved Practice":
    st.markdown("# 📚 My Saved Practice")
    st.write("Practice answers are kept temporarily in this browser session only. They are not stored in a database or file.")
    history_rows = load_practice_history()
    if not history_rows:
        st.info("No saved practice yet. Analyze an answer in Interview Prep or review an answer in Free Voice Interview to save it here.")
    else:
        st.metric("Saved answers", len(history_rows))
        for row in history_rows:
            title = f"{row['tool']} • {row['created_at']}" + (f" • Score: {row['score']}/100" if row['score'] is not None else "")
            with st.expander(title):
                st.markdown("**Question**")
                st.write(row["question"])
                st.markdown("**Your answer**")
                st.write(row["answer"])
                if row["feedback_json"]:
                    try:
                        feedback = json.loads(row["feedback_json"])
                        if feedback.get("hits") is not None:
                            st.write("**Detected keywords:** " + (", ".join(feedback.get("hits", [])) or "None detected"))
                            st.write("**Grammar / communication suggestions:**")
                            for issue in feedback.get("grammar_issues", []):
                                st.write("- " + issue)
                        elif feedback.get("detected_terms") is not None:
                            st.write("**Detected terms:** " + (", ".join(feedback.get("detected_terms", [])) or "None detected"))
                    except (ValueError, TypeError):
                        pass
    st.caption("Session-only storage: this practice history clears when the session ends or the app is restarted.")

if st.session_state.page == "🏠 Home":
    show_hero()
    st.markdown('<div class="section-title">✨ AI Tools</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Choose a tool and get started!</div>', unsafe_allow_html=True)

    search = st.text_input(
        "Search tools",
        placeholder="🔍 Search tools...",
        label_visibility="collapsed",
    )
    matches = [
        name for name, (icon, description) in TOOLS.items()
        if search.casefold() in f"{name} {description}".casefold()
    ]

    if not matches:
        st.info("No matching tools found. Try another search.")
    else:
        for start in range(0, len(matches), 3):
            cols = st.columns(3, gap="medium")

            for col, name in zip(cols, matches[start:start + 3]):
                icon, description = TOOLS[name]

                with col:
                    st.markdown(
                        f"""
                        <div class="tool-card">
                          <div class="tool-icon">{icon}</div>
                          <h3>{html.escape(name)}</h3>
                          <p>{html.escape(description)}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.button(
                        f"Explore {name} →",
                        key=f"open_{name}",
                        on_click=open_tool,
                        args=(name,),
                    )

    st.markdown(
        """
        <div style="margin-top:18px;padding:16px;border:1px solid #5144d4;
        border-radius:14px;text-align:center;background:linear-gradient(90deg,#271064,#102d73);color:white;">
          ✨ More AI tools are coming soon!
        </div>
        """,
        unsafe_allow_html=True,
    )

elif st.session_state.page == "🧰 AI Tools":
    st.markdown(
        '<div class="section-title">🧰 Explore AI Tools</div>',
        unsafe_allow_html=True,
    )

    tool_names = list(TOOLS.keys())

    current_index = (
        tool_names.index(st.session_state.selected_tool)
        if st.session_state.selected_tool in tool_names
        else 0
    )

    selected = st.selectbox(
        "Choose a tool",
        tool_names,
        index=current_index,
        key="tool_selector",
    )

    st.session_state.selected_tool = selected

    st.divider()

    # Visible navigation button so users can return to the Home dashboard.
    back_col, _ = st.columns([1, 5])
    with back_col:
        if st.button("⬅️ Back to Home", key="back_to_home_button", use_container_width=True):
            st.session_state.page = "🏠 Home"
            st.rerun()

    show_tool(selected)


elif st.session_state.page == "👩‍💻 About":
    st.markdown(
        '<div class="section-title">👩‍💻 About Urjaa AI Hub</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero">
            <h2>Technology made simpler. 💜</h2>
            <p class="hero-description">
                Urjaa AI Hub is a student-focused project that brings study,
                programming, career exploration, and productivity tools together.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🛠️ Technologies")
    st.write("• Python")
    st.write("• Streamlit")
    st.write("• HTML and CSS")
    st.write("• AI and Machine Learning concepts")

    st.markdown("### 🎯 Mission")
    st.write(
        "To help students explore technology and build practical skills."
    )


elif st.session_state.page == "📩 Contact":
    st.markdown(
        '<div class="section-title">📩 Contact</div>',
        unsafe_allow_html=True,
    )

    st.write("Have feedback or an idea for a new tool?")

    name = st.text_input("Your name")
    email = st.text_input("Your email")
    message = st.text_area("Your message")

    if st.button("Prepare Message", key="contact_button"):
        if name.strip() and email.strip() and message.strip():
            st.success("Your message is ready.")

            st.write("**Name:**", name)
            st.write("**Email:**", email)
            st.write("**Message:**", message)

            st.info(
                "This prototype does not send or store messages; "
                "an email service can be connected later."
            )
        else:
            st.warning("Please complete all three fields.")


st.markdown(
    """
    <div class="footer">
        Created by Urjaa | AI &amp; Data Science 💜<br>
        Learning • Building • Growing
    </div>
    """,
    unsafe_allow_html=True,
)
