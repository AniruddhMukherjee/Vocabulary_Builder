import streamlit as st
from utils.session import init_session_state
from utils.ai import configure_genai
from components.sidebar import render_sidebar
from components.flashcard import render_flashcard_view
from components.vocabulary_table import render_vocabulary_table
from styles import apply_styles

def main():
    # Apply custom CSS styles
    apply_styles()
    
    # Initialize session state
    init_session_state()
    
    # Initialize Gemini
    model = configure_genai()
    
    # App title and description
    st.title("🇩🇪 German Vocabulary Builder")
    st.markdown("Learn German vocabulary with AI-powered flashcards")
    
    # Render sidebar
    render_sidebar(model)
    
    # Main content - Card display or Table view
    if st.session_state.show_vocab_table:
        render_vocabulary_table()
    else:
        render_flashcard_view(model)

if __name__ == "__main__":
    main()