import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        /* Dark theme styling */
        .stApp {
            background-color: #1E1E1E;
            color: #E0E0E0;
        }
        div[data-testid="stSidebar"] {
            background-color: #252526;
        }
        .stTextInput > div > div > input {
            background-color: #2D2D30;
            color: #E0E0E0;
        }
        .stButton > button {
            background-color: #0078D7;
            color: white;
        }
        .stSelectbox > div > div > select {
            background-color: #2D2D30;
            color: #E0E0E0;
        }
        .vocabulary-card {
            background-color: #252526;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
            border: 1px solid #3E3E42;
        }
        /* Color-coded for articles */
        .german-word-der {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #4287f5; /* Blue for der */
        }
        .german-word-die {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #f542a7; /* Pink for die */
        }
        .german-word-das {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #42f54b; /* Green for das */
        }
        .german-word-other {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #0078D7; /* Default blue for verbs and others */
        }
        .category-tag {
            background-color: #3E3E42;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 14px;
            color: #E0E0E0;
        }
        /* Table styling */
        .vocab-table {
            width: 100%;
            border-collapse: collapse;
        }
        .vocab-table th {
            background-color: #3E3E42;
            color: #E0E0E0;
            padding: 8px;
            text-align: left;
        }
        .vocab-table td {
            padding: 8px;
            border-bottom: 1px solid #3E3E42;
        }
        .vocab-table tr:hover {
            background-color: #2D2D30;
        }
        /* Article colors in table */
        .der-text {
            color: #4287f5;
            font-weight: bold;
        }
        .die-text {
            color: #f542a7;
            font-weight: bold;
        }
        .das-text {
            color: #42f54b;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)