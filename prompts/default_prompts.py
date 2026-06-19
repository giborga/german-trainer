DEFAULT_PROMPT = """
You help a student to learn and remember German words and phrases on level A2.
The German word/phrase is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 exercise.
2. Generate an instruction for the exercise in English.
3. Generate list of missing words, that will be used later.
4. Return only JSON:
{{
  "instruction": "...",
  "sentence": "...",
  "missing_words": "..."
}}
5. While creating "missing_words", use the words in a correct form and order for the sentence.
6. Examples of correctly generated exercises:
Exercise_1:
{{
  "instruction": "Build a correct sentence:",
  "sentence": "Maria war aus dem Häuschen, als sie die gute Nachricht bekam.",
  "missing_words": ["aus", "dem", "Häuschen"]
}}
Exercise_2:
{{
  "instruction": "Use correct form of word/phrase:",
  "sentence": "Ich habe immer viel Spaß beim Wandern.",
  "missing_words": ["habe", "Spaß"]
}}
7. Do not create gaps in "sentence".
8. For "missing_words" use only forms and parts of the word or phrase the student is learning.
"""

EXERCISE_TO_ADD_LATER = """
Exercise_3:
{{
  "instruction": "Build a correct sentence: während / liest / er / frühstückt / die Zeitung / er",
  "sentence": "Er liest die Zeitung, während er frühstückt.",
  "missing_words": ["Er", "liest", "die", "Zeitung", "während", "er", "frühstückt"]
}}
"""