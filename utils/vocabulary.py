import streamlit as st
import random
from time import sleep
import pandas as pd
from utils.ai import generate_new_word

# Update the next_word() function to include level filtering
def next_word():
    """Get the next word to display"""
    with st.spinner("Generating a new word..."):
        # Reset the answer field
        st.session_state.user_answer = ""
        
        if st.session_state.viewing_saved:
            # Get word from saved collection
            collection = st.session_state.saved_collections[st.session_state.current_collection]
            if collection:
                st.session_state.current_word = random.choice(collection)
            else:
                st.session_state.current_word = random.choice(st.session_state.vocabulary)
                st.session_state.viewing_saved = False
        else:
            # Generate a completely new word
            category = st.session_state.filter_category if st.session_state.filter_category != "All" else None
            level = st.session_state.level_filter if st.session_state.level_filter != "All" else None
            new_word = generate_new_word(category, level)
            
            if new_word and all(key in new_word for key in ["german", "english", "article", "category", "level"]):
                # Check if word already exists
                if not any(w["german"] == new_word["german"] for w in st.session_state.vocabulary):
                    st.session_state.vocabulary.append(new_word)
                    st.session_state.current_word = new_word
                    
                    # Add to history dataframe
                    st.session_state.history_df = pd.concat([
                        st.session_state.history_df, 
                        pd.DataFrame([new_word])
                    ], ignore_index=True)
                else:
                    # If word already exists, pick a random one that matches the filters
                    filtered_vocab = [w for w in st.session_state.vocabulary 
                                     if (category is None or w["category"] == category) and
                                        (level is None or w.get("level") == level)]
                    if filtered_vocab:
                        st.session_state.current_word = random.choice(filtered_vocab)
                    else:
                        st.session_state.current_word = random.choice(st.session_state.vocabulary)
            else:
                # If generation failed, pick a random one that matches the filters
                filtered_vocab = [w for w in st.session_state.vocabulary 
                                 if (category is None or w["category"] == category) and
                                    (level is None or w.get("level") == level)]
                if filtered_vocab:
                    st.session_state.current_word = random.choice(filtered_vocab)
                else:
                    st.session_state.current_word = random.choice(st.session_state.vocabulary)
    
    st.session_state.show_answer = False
    st.session_state.feedback = None

def check_answer():
    """Check if the user's answer is correct"""
    user_answer = st.session_state.user_answer.strip().lower()
    correct_answer = st.session_state.current_word["english"].lower()
    
    st.session_state.total_attempts += 1
    
    if user_answer == correct_answer:
        st.session_state.score += 1
        st.session_state.feedback = "correct"
        # Wait briefly before showing a new word
        sleep(0.8)
        next_word()
    else:
        st.session_state.feedback = "incorrect"

def reveal_answer():
    """Show the answer to the current word"""
    st.session_state.show_answer = True