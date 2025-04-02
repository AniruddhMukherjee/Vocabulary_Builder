import streamlit as st
import pandas as pd

def add_vocabulary():
    """Add a new vocabulary word manually"""
    new_word = {
        "german": st.session_state.new_german.strip(),
        "english": st.session_state.new_english.strip(),
        "article": st.session_state.new_article.strip(),
        "category": st.session_state.new_category.strip(),
        "level": st.session_state.new_level.strip() if "new_level" in st.session_state else "A1"
    }
    
    if new_word["german"] and new_word["english"]:
        st.session_state.vocabulary.append(new_word)
        # Also add to history dataframe
        st.session_state.history_df = pd.concat([
            st.session_state.history_df, 
            pd.DataFrame([new_word])
        ], ignore_index=True)
        
        st.session_state.new_german = ""
        st.session_state.new_english = ""
        st.session_state.new_article = ""
        st.session_state.new_category = ""
        if "new_level" in st.session_state:
            st.session_state.new_level = ""
        st.success("New vocabulary added!")

def export_vocab():
    """Export vocabulary to CSV"""
    return st.session_state.history_df.to_csv(index=False).encode('utf-8')

def save_word():
    """Save current word to the selected collection"""
    word = st.session_state.current_word
    collection = st.session_state.current_collection
    
    # Add to collection if not already there
    if word not in st.session_state.saved_collections[collection]:
        st.session_state.saved_collections[collection].append(word)
        st.success(f"Word saved to '{collection}' collection!")
    else:
        st.info("This word is already in this collection.")

def get_word_class(word):
    """Determine the CSS class for a word based on its article"""
    article = word.get("article", "").lower()
    if article == "der":
        return "german-word-der"
    elif article == "die":
        return "german-word-die"
    elif article == "das":
        return "german-word-das"
    else:
        return "german-word-other"

def get_article_class(article):
    """Get the CSS class for an article"""
    article = article.lower() if article else ""
    if article == "der":
        return "der-text"
    elif article == "die":
        return "die-text"
    elif article == "das":
        return "das-text"
    return ""