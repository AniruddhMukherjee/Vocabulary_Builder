import streamlit as st
from utils.vocabulary import check_answer, reveal_answer, next_word
from utils.data_manager import save_word, get_word_class
from utils.ai import generate_examples

def render_flashcard_view(model):
    """Render the flashcard view"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Create a card-like container
        card = st.container()
        with card:
            # Get the appropriate word class based on the article
            word_class = get_word_class(st.session_state.current_word)
            
            st.markdown(f"""
            <div class="vocabulary-card">
                <div class="{word_class}">{st.session_state.current_word["german"]}</div>
                <div class="category-tag">{st.session_state.current_word["category"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Input for answer
            st.text_input("Your translation:", key="user_answer", on_change=check_answer)
            
            # Show feedback
            if st.session_state.feedback == "correct":
                st.success("Correct! 🎉")
            elif st.session_state.feedback == "incorrect":
                st.error("Try again! 😕")
                
            # Buttons
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.button("Show Answer", on_click=reveal_answer)
            with col_b:
                st.button("Next Word", on_click=next_word)
            with col_c:
                st.button("Save Word", on_click=save_word)
            
            # Show answer and examples if requested
            if st.session_state.show_answer:
                st.markdown(f"""
                <div style="background-color: #252526; padding: 15px; border-radius: 5px; border: 1px solid #3E3E42;">
                    <h3 style="color: #E0E0E0;">Answer</h3>
                    <p style="color: #E0E0E0; font-size: 18px;">{st.session_state.current_word['english']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.spinner("Generating example sentences..."):
                    examples = generate_examples(st.session_state.current_word, model)
                    st.markdown(f"""
                    <div style="background-color: #252526; padding: 15px; border-radius: 5px; margin-top: 15px; border: 1px solid #3E3E42;">
                        <h3 style="color: #E0E0E0;">Example Sentences</h3>
                        <pre style="background-color: #2D2D30; padding: 10px; border-radius: 5px; color: #E0E0E0; white-space: pre-wrap;">{examples}</pre>
                    </div>
                    """, unsafe_allow_html=True)