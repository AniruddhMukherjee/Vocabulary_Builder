import streamlit as st
from utils.session import reset_score, set_category_filter, view_saved_words, view_all_words, create_collection, toggle_vocab_table
from utils.data_manager import add_vocabulary, export_vocab

def render_sidebar(model):
    """Render the sidebar with statistics and settings"""
    with st.sidebar:
        st.header("Statistics")
        accuracy = (st.session_state.score / st.session_state.total_attempts * 100) if st.session_state.total_attempts > 0 else 0
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score", f"{st.session_state.score}/{st.session_state.total_attempts}")
        with col2:
            st.metric("Accuracy", f"{accuracy:.1f}%")
        
        if st.session_state.total_attempts > 0:
            st.button("Reset Score", on_click=reset_score, key="reset_score_button")
        
        st.header("Settings")
        
        # Category filter
        categories = ["All"] + list(set(word["category"] for word in st.session_state.vocabulary))
        st.selectbox("Filter by category:", categories, key="category_filter", 
                     index=categories.index(st.session_state.filter_category) if st.session_state.filter_category in categories else 0)
        
        levels = ["All", "A1", "A2", "B1", "B2", "C1", "C2"]
        st.selectbox("Filter by level:", levels, key="level_filter", 
                    index=levels.index(st.session_state.level_filter) if st.session_state.level_filter in levels else 0)
        
        # Single Apply Filter button for both category and level filters
        st.button("Apply Filter", on_click=set_category_filter, key="apply_filter_button")
        
        # Saved Collections section
        st.header("Saved Collections")
        
        # Create new collection
        st.text_input("New Collection Name:", key="collection_name")
        st.button("Create Collection", on_click=create_collection, key="create_collection_button")
        
        # Select current collection
        collections = list(st.session_state.saved_collections.keys())
        st.selectbox("Select Collection:", collections, key="current_collection", 
                    index=collections.index(st.session_state.current_collection) if st.session_state.current_collection in collections else 0)
        
        # View buttons
        col_a, col_b = st.columns(2)
        with col_a:
            st.button("View Saved", on_click=view_saved_words, 
                     disabled=len(st.session_state.saved_collections[st.session_state.current_collection]) == 0,
                     key="view_saved_button")
        with col_b:
            st.button("View All", on_click=view_all_words, disabled=not st.session_state.viewing_saved,
                     key="view_all_button")
        
        # Display mode indicator
        if st.session_state.viewing_saved:
            st.info(f"Viewing saved words from '{st.session_state.current_collection}'")
        
        # Manually add vocabulary
        st.header("Add Vocabulary Manually")
        st.text_input("German Word:", key="new_german")
        st.text_input("English Translation:", key="new_english")
        st.text_input("Article (der/die/das):", key="new_article")
        st.text_input("Category:", key="new_category")
        levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        st.selectbox("Level:", levels, key="new_level")
        st.button("Add Word", on_click=add_vocabulary, key="add_word_button")
        
        # Button to view all vocabulary as a table
        st.button("View All Vocabulary Table", on_click=toggle_vocab_table, key="view_vocab_table_button")
        
        # Export vocabulary
        st.download_button(
            label="Export Vocabulary (CSV)",
            data=export_vocab(),
            file_name="german_vocabulary.csv",
            mime="text/csv",
            key="export_vocab_button"
        )
        
        # Current vocabulary count
        st.caption(f"Total vocabulary words: {len(st.session_state.vocabulary)}")
        
        # Saved words count
        collection = st.session_state.current_collection
        st.caption(f"Words in '{collection}' collection: {len(st.session_state.saved_collections[collection])}")