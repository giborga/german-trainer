ADJECTIVE_PROMPT = """

You help a student to learn and remember German words on level A2.
The German word is: {word}.
Correct comparative form: {comparative}.
Correct superlative form: {superlative}.

Rules for exercise generation:
1. Create one A2 exercise.
2. Generate an "instruction" for the exercise in English.
3. Provide FULL "sentence" in German with no gaps.
4. Generate list of "missing_words".
5. In "missing_words", use the adjective in a correct form for the sentence.
6. In "missing_words", if superlative form is used with "am", "am" and "adjective" are considered to be 2 separate words.
7. Return only JSON:
{{
  "instruction": "...",
  "sentence": "...",
  "missing_words": ["...", "..."]
}}
8. Examples of correctly generated article exercises:
Exercise_1:
{{
  "instruction": "Use advective with correct ending:",
  "sentence": "Der große Hund spielt im Garten.",
  "missing_words": ["große"]
}}
Exercise_2:
{{
  "instruction": "Use advective with correct ending:",
  "sentence": "Ich kaufe den alten Tisch für mein Arbeitszimmer.",
  "missing_words": ["alten"]
}}
Exercise_3: 
{{
  "instruction": "Use advective with correct ending:",
  "sentence": "Ich spreche mit der freundlichen Lehrerin über die Prüfung.",
  "missing_words": ["freundlichen"]
}}
Exercise_4: 
{{
  "instruction": "Use advective with correct ending:",
  "sentence": "Er ist ein sehr netter Mensch.",
  "missing_words": ["netter"]
}}
Exercise_5: 
{{
  "instruction": "Use advective with correct ending:",
  "sentence": "Das ist eine leichte Aufgabe.",
  "missing_words": ["leichte"]
}}
Exercise_6: 
{{
  "instruction": "Use advective with correct ending:",
  "sentence": "Darf ich auch ein kleines Stück Kuchen haben?",
  "missing_words": ["kleines"]
}}
Exercise_7: 
{{
  "instruction": "Use correct adjective form:",
  "sentence": "Für die Prüfung ist es am wichtigsten, regelmäßig zu lernen.",
  "missing_words": ["am", "wichtigsten"]
}}
"""