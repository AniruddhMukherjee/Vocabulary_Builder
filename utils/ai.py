import streamlit as st
import google.generativeai as genai
import json
import re
from config import WORD_GENERATION_PROMPT, EXAMPLE_SENTENCES_PROMPT

def configure_genai():
    """Configure the Gemini API"""
    try:
        api_key = st.secrets["gemini"]["api_key"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error configuring Gemini API: {str(e)}")
        st.info("Make sure you have added your Gemini API key to the secrets.toml file under [gemini]")
        st.stop()

import streamlit as st
import google.generativeai as genai
import json
import re
from config import WORD_GENERATION_PROMPT, EXAMPLE_SENTENCES_PROMPT

def configure_genai():
    """Configure the Gemini API"""
    try:
        api_key = st.secrets["gemini"]["api_key"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error configuring Gemini API: {str(e)}")
        st.info("Make sure you have added your Gemini API key to the secrets.toml file under [gemini]")
        st.stop()

def generate_new_word(category=None, level=None):
    """Generate a new German vocabulary word using Gemini API"""
    model = configure_genai()
    category_prompt = f" in the category '{category}'" if category and category != "All" else ""
    level_prompt = f" for language level '{level}'" if level and level != "All" else ""
    
    # Get all existing German words to avoid duplication
    existing_words = set(word["german"] for word in st.session_state.vocabulary)
    
    prompt = WORD_GENERATION_PROMPT.format(
        category_prompt=category_prompt,
        level_prompt=level_prompt,
        existing_words=', '.join(existing_words)
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
        level=word.get('level', 'A1')  # Add level for the example sentences
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating examples: {str(e)}"