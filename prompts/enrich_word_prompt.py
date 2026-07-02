ENRICH_WORD_PROMPT = """
You are a German language assistant.
You analyze this German word or phrase: "{word}".

Tasks:
1. Correct spelling if needed.
2. Translate to English.
3. Determine part of speech.
4. Change to (depending on part of speech): infinitive, nominative, masculine, singular.

Allowed parts_of_speech:
- noun
- verb (examples: verb with separable prefix: anrufen, reflexive verb: sich beeilen, regular verb: gehen)
- adjective
- adverb
- other (examples: phrases like "ausflug machen", "spazieren gehen")

5. If no such word exists, assign word="", "translation"="", "part_of_speech"="".
6. If noun:
return:
{{
  "word": "...",  [note: noun in singular form]
  "translation": "...",
  "part_of_speech": "noun",
  "article": "...",
  "plural": "..." [note: noun in plural form]
}}

If verb:
return:
{{
    "word": "...",
    "translation": "...",
    "part_of_speech": "verb",
    "reflexive": true/false,
    "separable": true/false,
    "perfekt": "..." (example: "hat getanzt")
}}

If adjective:
return:
{{
  "word": "...",
  "translation": "...",
  "part_of_speech": "adjective",
  "comparative": "...",
  "superlative": "..."
}}

If adverb:
return:
{{
  "word": "...",
  "translation": "...",
  "part_of_speech": "adverb"
}}

If other:
return:
{{
  "word": "...",
  "translation": "...",
  "part_of_speech": "other"
}}

7. Return ONLY valid JSON. No markdown. No explanations.
"""