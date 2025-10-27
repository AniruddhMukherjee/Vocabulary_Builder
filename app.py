import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import re
import random
from time import sleep

# Configure the page
st.set_page_config(
    page_title="German Vocabulary Builder",
    page_icon="🇩🇪",
    layout="wide"
)

# Word generation prompt template with level support
WORD_GENERATION_PROMPT = """
Generate 1 German vocabulary word{category_prompt}{level_prompt} with its English translation.
Make sure the word is NOT one of these existing words: {existing_words}

For the word, provide:
1. The German word (include the article der/die/das for nouns)
2. The English translation
3. The article (der/die/das) if it's a noun, otherwise leave blank
4. The category (animals, food, places, verbs, etc.)
5. The CEFR level (A1, A2, B1, B2, C1, C2) - where:
   - A1: Absolute beginner vocabulary (very basic, everyday words)
   - A2: Elementary vocabulary (common, everyday expressions)
   - B1: Intermediate vocabulary (familiar matters, work, school, leisure)
   - B2: Upper intermediate vocabulary (complex topics, technical discussions)
   - C1: Advanced vocabulary (complex texts, implicit meaning, specialized)
   - C2: Proficiency vocabulary (very advanced, nuanced, academic)

Format the response as JSON with these exact keys: "german", "english", "article", "category", "level"
Example format:
{{"german": "der Hund", "english": "dog", "article": "der", "category": "animals", "level": "A1"}}
"""

# Example sentences prompt template
EXAMPLE_SENTENCES_PROMPT = """
Generate 2 short, simple example sentences in German using the word "{german}" with English translations.
Format each as:
German: [sentence]
English: [translation]

Make the sentences appropriate for a {level} level German learner.
"""

# Define CEFR levels and their descriptions
CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
LEVEL_DESCRIPTIONS = {
    "A1": "Absolute beginner vocabulary (very basic, everyday words)",
    "A2": "Elementary vocabulary (common, everyday expressions)",
    "B1": "Intermediate vocabulary (familiar matters, work, school, leisure)",
    "B2": "Upper intermediate vocabulary (complex topics, technical discussions)",
    "C1": "Advanced vocabulary (complex texts, implicit meaning, specialized)",
    "C2": "Proficiency vocabulary (very advanced, nuanced, academic)"
}

# Article color mapping
ARTICLE_COLORS = {
    "der": "#4287f5",  # Blue
    "die": "#f542a7",  # Pink
    "das": "#42f54b",  # Green
    "": "#0078D7"      # Default blue
}

#
# Utility Functions
#

def configure_genai():
    """Configure the Gemini API"""
    try:
        # Check if we have an API key in session state
        if 'api_key' in st.session_state and st.session_state.api_key:
            api_key = st.session_state.api_key
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-2.5-flash')
        else:
            # No API key found
            return None
    except Exception as e:
        st.error(f"Error configuring Gemini API: {str(e)}")
        st.info("Please check your API key and try again.")
        return None

def generate_new_word(model, category=None, level=None):
    """Generate a new German vocabulary word using Gemini API"""
    category_prompt = f" in the category '{category}'" if category and category != "All" else ""
    level_prompt = f" for language level '{level}'" if level and level != "All" else ""
    
    # Get all existing German words to avoid duplication
    existing_words = set(word["german"] for word in st.session_state.vocabulary)
    
    prompt = WORD_GENERATION_PROMPT.format(
        category_prompt=category_prompt,
        level_prompt=level_prompt,
        existing_words=', '.join(existing_words) if existing_words else "none"
    )
    
    try:
        response = model.generate_content(prompt)
        try:
            # Try to parse as JSON directly
            new_word = json.loads(response.text)
            if isinstance(new_word, list) and len(new_word) > 0:
                new_word = new_word[0]
            if "level" not in new_word and level:
                new_word["level"] = level
            return new_word
        except json.JSONDecodeError:
            # If parsing fails, try to extract JSON content from response
            json_match = re.search(r'{.*}', response.text, re.DOTALL)
            if json_match:
                try:
                    new_word = json.loads(json_match.group(0))
                    if "level" not in new_word and level:
                        new_word["level"] = level
                    return new_word
                except:
                    return None
            return None
    except Exception as e:
        st.error(f"Error generating vocabulary: {str(e)}")
        return None

def generate_examples(word, model):
    """Generate example sentences using the word"""
    prompt = EXAMPLE_SENTENCES_PROMPT.format(
        german=word['german'],
        level=word.get('level', 'A1')
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating examples: {str(e)}"

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

def next_word():
    """Get the next word to display"""
    model = st.session_state.model
    
    with st.spinner("Generating a new word..."):
        # Reset the answer field
        st.session_state.user_answer = ""
        
        if st.session_state.viewing_saved:
            # Get word from saved collection
            collection = st.session_state.saved_collections[st.session_state.current_collection]
            if collection:
                st.session_state.current_word = random.choice(collection)
            else:
                # If collection is empty, generate a new word
                st.session_state.viewing_saved = False
                category = st.session_state.filter_category if st.session_state.filter_category != "All" else None
                level = st.session_state.level_filter if st.session_state.level_filter != "All" else None
                new_word = generate_new_word(model, category, level)
                
                if new_word and all(key in new_word for key in ["german", "english", "article", "category", "level"]):
                    st.session_state.vocabulary.append(new_word)
                    st.session_state.current_word = new_word
                    
                    # Add to history dataframe
                    st.session_state.history_df = pd.concat([
                        st.session_state.history_df, 
                        pd.DataFrame([new_word])
                    ], ignore_index=True)
        else:
            # Generate a completely new word
            category = st.session_state.filter_category if st.session_state.filter_category != "All" else None
            level = st.session_state.level_filter if st.session_state.level_filter != "All" else None
            new_word = generate_new_word(model, category, level)
            
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
                        # If no matches, try to get a new word again
                        if st.session_state.vocabulary:
                            st.session_state.current_word = random.choice(st.session_state.vocabulary)
                        else:
                            # If vocabulary is still empty, try once more without filters
                            new_word = generate_new_word(model, None, None)
                            if new_word:
                                st.session_state.vocabulary.append(new_word)
                                st.session_state.current_word = new_word
                                st.session_state.history_df = pd.concat([
                                    st.session_state.history_df, 
                                    pd.DataFrame([new_word])
                                ], ignore_index=True)
            else:
                # If generation failed, pick a random one that matches the filters
                filtered_vocab = [w for w in st.session_state.vocabulary 
                                 if (category is None or w["category"] == category) and
                                    (level is None or w.get("level") == level)]
                if filtered_vocab:
                    st.session_state.current_word = random.choice(filtered_vocab)
                elif st.session_state.vocabulary:
                    st.session_state.current_word = random.choice(st.session_state.vocabulary)
                else:
                    # If vocabulary is still empty, try once more without filters
                    new_word = generate_new_word(model, None, None)
                    if new_word:
                        st.session_state.vocabulary.append(new_word)
                        st.session_state.current_word = new_word
                        st.session_state.history_df = pd.concat([
                            st.session_state.history_df, 
                            pd.DataFrame([new_word])
                        ], ignore_index=True)
    
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

def add_vocabulary():
    """Add a new vocabulary word manually"""
    new_word = {
        "german": st.session_state.new_german.strip(),
        "english": st.session_state.new_english.strip(),
        "article": st.session_state.new_article.strip(),
        "category": st.session_state.new_category.strip(),
        "level": st.session_state.new_level
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

def reset_score():
    """Reset the score counter"""
    st.session_state.score = 0
    st.session_state.total_attempts = 0

def set_category_filter():
    """Apply the selected category filter"""
    st.session_state.filter_category = st.session_state.category_filter
    st.session_state.viewing_saved = False
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

#
# CSS Styling
#

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

#
# UI Components 
#

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
        st.rerun()

def render_sidebar(model):
    """Render the sidebar with statistics and settings"""
    with st.sidebar:
        # API Key Configuration Section - Always at the top
        st.header("API Configuration")
        
        # Check if API key exists in session state
        if 'api_key' in st.session_state and st.session_state.api_key:
            st.success("Gemini API key is configured")
            if st.button("Change API Key"):
                # Reset the API key
                st.session_state.api_key = ""
                st.rerun()
        else:
            # Show API key input
            api_key = st.text_input("Enter your Gemini API Key:", type="password", key="input_api_key")
            if st.button("Save API Key"):
                if api_key:
                    st.session_state.api_key = api_key
                    st.success("API key saved! Refreshing app...")
                    st.rerun()
                else:
                    st.error("Please enter a valid API key")
        
        # API Key Help Expander
        with st.expander("How to get a Gemini API Key"):
            st.markdown("""
            ### Getting a Gemini API Key
            
            1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Sign in with your Google account
            3. Click on "Get API key" on the top right
            4. Create a new API key by following the prompts
            5. Copy the generated API key and paste it above
            
            **Note:** Keep your API key secret and don't share it publicly.
            
            The free tier includes:
            - Up to 60 queries per minute
            - Access to Gemini Pro and other models
            
            For more details, visit [Google AI documentation](https://ai.google.dev/tutorials/setup).
            """)
        
        # Only show the rest of the sidebar if API key is configured
        if not model:
            st.warning("Please provide a valid API key to use the app")
            return
        
        # Add a separator between API configuration and other sections
        st.divider()
        
        # Rest of the sidebar remains the same
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

#
# Initialize Session State
#

def init_session_state():
    """Initialize all session state variables"""
    # Empty vocabulary list - no default words
    if "vocabulary" not in st.session_state:
        st.session_state.vocabulary = []
    
    if "current_word" not in st.session_state:
        # We'll populate this with a Gemini-generated word in the main function
        st.session_state.current_word = {}
    
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
    
    if "level_filter" not in st.session_state:
        st.session_state.level_filter = "All"
    
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
        # Initialize empty dataframe to store all words history
        st.session_state.history_df = pd.DataFrame(columns=["german", "english", "article", "category", "level"])
    
    if "has_initial_word" not in st.session_state:
        st.session_state.has_initial_word = False
        
    # No default API key - we want to ensure user always provides their own
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

#
# Main Application Function
#

def main():
    # Apply custom CSS styles
    apply_styles()
    
    # Initialize session state
    init_session_state()
    
    # App title and description
    st.title("🇩🇪 German Vocabulary Builder")
    st.markdown("Learn German vocabulary with AI-powered flashcards")
    
    # Initialize Gemini
    model = configure_genai()
    
    # Store model in session state for future use if available
    if model:
        st.session_state.model = model
    
    # Render sidebar (always render sidebar even if model is None)
    render_sidebar(model)
    
    # Check if model is available before proceeding with the main content
    if model is None:
        st.info("Please provide a valid Gemini API key in the sidebar to use this app.")
        return
    
    # Generate first word if we don't have one yet and we have a valid model
    if not st.session_state.has_initial_word:
        with st.spinner("Generating your first vocabulary word..."):
            new_word = generate_new_word(model)
            if new_word and all(key in new_word for key in ["german", "english", "article", "category", "level"]):
                st.session_state.vocabulary.append(new_word)
                st.session_state.current_word = new_word
                st.session_state.history_df = pd.concat([
                    st.session_state.history_df, 
                    pd.DataFrame([new_word])
                ], ignore_index=True)
                st.session_state.has_initial_word = True
            else:
                st.error("Failed to generate the first word. Please check your API key and try again.")
                return
    
    # Main content - Card display or Table view
    if st.session_state.show_vocab_table:
        render_vocabulary_table()
    else:
        render_flashcard_view(model)

if __name__ == "__main__":
    main()