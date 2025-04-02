# Sample vocabulary data to start with
DEFAULT_VOCAB = [
    {"german": "der Hund", "english": "dog", "article": "der", "category": "animals", "level": "A1"},
    {"german": "die Katze", "english": "cat", "article": "die", "category": "animals", "level": "A1"},
    {"german": "das Haus", "english": "house", "article": "das", "category": "places", "level": "A1"},
    {"german": "gehen", "english": "to go", "article": "", "category": "verbs", "level": "A1"},
    {"german": "essen", "english": "to eat", "article": "", "category": "verbs", "level": "A1"},
]

# Article color mapping
ARTICLE_COLORS = {
    "der": "#4287f5",  # Blue
    "die": "#f542a7",  # Pink
    "das": "#42f54b",  # Green
    "": "#0078D7"      # Default blue
}

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