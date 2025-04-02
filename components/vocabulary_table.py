import streamlit as st
import pandas as pd
from utils.data_manager import get_article_class

def render_vocabulary_table():
    """Render the vocabulary table view using streamlit's native dataframe"""
    st.header("Complete Vocabulary List")
    
    # Create a dataframe for display
    df = st.session_state.history_df.copy()
    
    # Add styling for the articles if needed
    def highlight_articles(val):
        if val == 'der':
            return 'color: #4287f5'  # Blue
        elif val == 'die':
            return 'color: #f542a7'  # Pink
        elif val == 'das':
            return 'color: #42f54b'  # Green
        return ''
    
    # Apply styling (optional)
    styled_df = df.style.applymap(highlight_articles, subset=['article'])
    
    # Display the dataframe with fixed height and width
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400  # Adjust height as needed
    )
    
    # Add a button to go back to flashcard view
    if st.button("Return to Flashcards", key="return_to_flashcards"):
        st.session_state.show_vocab_table = False
        st.experimental_rerun()