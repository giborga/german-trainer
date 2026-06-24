NOUN_PROMPT = """
You help a student to learn and remember German nouns on level A2.
The German noun is: {word}.
Correct article is: {article}.
Plural form is: {plural}.
Rules for exercise and answer generation:
1. Create one A2 exercise.
2. Generate an "instruction" for the exercise in English.
3. Provide full "sentence" in German.
4. Generate list of "missing_words", that will be used later.
5. "missing_words" may be an article or noun's plural form.
6. While creating "missing_words", use the noun and its article in a correct form and order for the sentence.
5. Return only JSON:
{{
  "instruction": "...",
  "sentence": "...",
  "missing_words": "..."
}}
7. Examples of correctly generated article exercises:
Exercise_1:
{{
  "instruction": "Complete with correct article:",
  "sentence": "Der große Hund spielt im Garten.",
  "missing_words": ["Der"]
}}
Exercise_2:
{{
  "instruction": "Complete with correct article:",
  "sentence": "Ich kaufe den alten Tisch für mein Arbeitszimmer.",
  "missing_words": ["den"]
}}
Exercise_3:
{{
  "instruction": "Complete with correct article:",
  "sentence": "Ich spreche mit der freundlichen Lehrerin über die Prüfung.",
  "missing_words": ["der"]
}}
8. Examples of correctly generated plural form exercises:
Exercise_1: 
{{
  "instruction": "Complete with correct plural form:",
  "sentence": "Im Herbst fallen viele Blätter von den Bäumen.",
  "missing_words": ["Blätter"]
}}
Exercise_2: 
{{
  "instruction": "Complete with correct plural form:",
  "sentence": "Am Wochenende besuchen wir verschiedene Museen in Berlin.",
  "missing_words": ["Museen"]
}}
"""
