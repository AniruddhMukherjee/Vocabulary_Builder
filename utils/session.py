import streamlit as st
import random
import pandas as pd
from config import DEFAULT_VOCAB

def init_session_state():
    """Initialize all session state variables"""
    if "vocabulary" not in st.session_state:
        st.session_state.vocabulary = DEFAULT_VOCAB
        # Add default levels to existing vocabulary
        for word in st.session_state.vocabulary:
            if "level" not in word:
                # Assign default levels based on categories
                if word["category"] in ["animals", "places", "food"]:
                    word["level"] = "A1"
                else:
                    word["level"] = "A2"
    
    # Add this to init_session_state() in session.py
    if "level_filter" not in st.session_state:
        st.session_state.level_filter = "All"

    if "current_word" not in st.session_state:
        st.session_state.current_word = random.choice(st.session_state.vocabulary)
    
    if "score" not in st.session_state:
        st.session_state.score = 0
    
    if "total_attempts" not in st.session_state:
        st.session_state.total_attempts = 0
    
    if "feedback" not in st.session_state:
        st.session_state.feedback = None
    
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    
    if "filter_category" not in st.session_state:
        st.session_state.filter_category = "All"
    
    if "selected_level" not in st.session_state:
        st.session_state.selected_level = "All"
    
    if "saved_words" not in st.session_state:
        st.session_state.saved_words = []
    
    if "saved_collections" not in st.session_state:
        st.session_state.saved_collections = {"Default": []}
    
    if "current_collection" not in st.session_state:
        st.session_state.current_collection = "Default"
    
    if "viewing_saved" not in st.session_state:
        st.session_state.viewing_saved = False
    
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = ""
    
    if "collection_name" not in st.session_state:
        st.session_state.collection_name = ""
    
    if "show_vocab_table" not in st.session_state:
        st.session_state.show_vocab_table = False
    
    if "history_df" not in st.session_state:
        # Initialize dataframe to store all words history
        temp_vocab = DEFAULT_VOCAB.copy()
        # Add level if not present in default vocabulary
        for word in temp_vocab:
            if "level" not in word:
                if word["category"] in ["animals", "places", "food"]:
                    word["level"] = "A1"
                else:
                    word["level"] = "A2"
        st.session_state.history_df = pd.DataFrame(temp_vocab)

def reset_score():
    """Reset the score counter"""
    st.session_state.score = 0
    st.session_state.total_attempts = 0

def set_category_filter():
    """Apply the selected category filter"""
    st.session_state.filter_category = st.session_state.category_filter
    st.session_state.viewing_saved = False
    from utils.vocabulary import next_word
    next_word()

def set_level_filter():
    """Apply the selected level filter"""
    st.session_state.selected_level = st.session_state.level_filter
    st.session_state.viewing_saved = False
    from utils.vocabulary import next_word
    next_word()

def apply_filters():
    """Apply both category and level filters"""
    st.session_state.filter_category = st.session_state.category_filter
    st.session_state.selected_level = st.session_state.level_filter
    st.session_state.viewing_saved = False
    from utils.vocabulary import next_word
    next_word()

def toggle_vocab_table():
    """Toggle the vocabulary table view"""
    st.session_state.show_vocab_table = not st.session_state.show_vocab_table

def view_saved_words():
    """Switch to saved words view"""
    st.session_state.viewing_saved = True
    collection = st.session_state.current_collection
    
    # If collection is empty, show warning
    if not st.session_state.saved_collections[collection]:
        st.warning(f"Collection '{collection}' is empty. Please save some words first.")
        st.session_state.viewing_saved = False
    else:
        st.session_state.current_word = random.choice(st.session_state.saved_collections[collection])
        st.session_state.show_answer = False
        st.session_state.feedback = None
        st.session_state.user_answer = ""

def view_all_words():
    """Switch to all words view"""
    st.session_state.viewing_saved = False
    from utils.vocabulary import next_word
    next_word()

def create_collection():
    """Create a new collection of words"""
    name = st.session_state.collection_name.strip()
    if name and name not in st.session_state.saved_collections:
        st.session_state.saved_collections[name] = []
        st.session_state.current_collection = name
        st.session_state.collection_name = ""
        st.success(f"Created new collection: {name}")
    elif name in st.session_state.saved_collections:
        st.error("Collection with this name already exists.")
    else:
        st.error("Please enter a collection name.")