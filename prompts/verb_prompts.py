REFLEXIVE_AND_SEPARABLE_VERB_PROMPT = """
You help a student to learn and remember reflexive and separable German verbs on level A2.
The german verb is: {word}.
Rules for exercise and answer generation:
1. Create one A2 exercise.
2. Generate an instruction for the exercise in English.
3. Provide full sentence in German.
4. Generate list of missing verb parts, that will be used later for fill-in blank exercise.
5. Return only JSON:
{{
  "instruction": "...",
  "sentence": "...",
  "missing_words": "..."
}}
6. While creating "missing_words", use the verb and its parts in a correct form and order for the sentence.
7. Examples of correctly generated exercises:
Exercise_1 - correct usage in perfect tense:
{{
  "instruction": "Complete the sentence:",
  "sentence": "Ich habe mich gestern nicht gut gefühlt.",
  "missing_words": ["mich", "gefühlt"]
}}
Exercise_2  - verb + reflexive part:
{{
  "instruction": "Complete the sentence:",
  "sentence": "Am Morgen ziehe ich mich schnell an, bevor ich zur Arbeit gehe.",
  "missing_words": ["ziehe", "mich", "an"]
}}
"""

REFLEXIVE_VERB_PROMPT = """
You help a student to learn and remember reflexive German verbs on level A2.
The german reflexive verb is: {word}.
Rules for exercise and answer generation:
1. Create one A2 exercise.
2. Generate an instruction for the exercise in English.
3. Provide full sentence in German.
4. Generate list of missing verb parts, that will be used later for fill-in blank exercise.
5. Return only JSON:
{{
  "instruction": "...",
  "sentence": "...",
  "missing_words": "..."
}}
6. While creating "missing_words", use the verb and its reflexive part in a correct form and order for the sentence.
7. Examples of correctly generated exercises:
Exercise_1 - reflexive part + verb:
{{
  "instruction": "Complete the sentence:",
  "sentence": "Ich habe mich gestern nicht gut gefühlt.",
  "missing_words": ["mich", "gefühlt"]
}}
Exercise_2  - verb + reflexive part:
{{
    "instruction": "Complete the sentence:",
    "sentence": "Wir unterhalten uns oft im Park.",
    "missing_words": ["unterhalten", "uns"]
}}
"""

SEPARABLE_VERB_PROMPT = """
You help a student to learn and remember separable German verbs on level A2.
The german separable verb is: {word}.
Rules for exercise and answer generation:
1. Create one A2 exercise.
2. Generate an instruction for the exercise in English.
3. Provide full sentence in German.
4. Generate list of missing verb parts, that will be used later for fill-in blank exercise.
5. Return only JSON:
{{
  "instruction": "...",
  "sentence": "...",
  "missing_words": "..."
}}
6. While creating "missing_words", use the verb and its separable part in a correct form and order for the sentence.
7. Examples of correctly generated exercises:
Exercise_1 - missing separable part:
{{
    "instruction": "Complete the sentence:",
    "sentence": "Wann rufst du deine Eltern an?",
    "missing_words": ["rufst", "an"]
}}

Exercise_2 - correct usage in perfect tense:
{{
    "instruction": "Complete the sentence:",
    "sentence": "Mir ist gestern plötzlich ein guter Gedanke eingefallen.",
    "missing_words": ["ist", "eingefallen"]
}}
"""

DEFAULT_VERB_PROMPT = """
You help a student to learn and remember German verbs on level A2.
The german verb is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 exercise that practices a German verb in Perfekt form (haben/sein + Partizip II).
2. Generate an instruction for the exercise in English.
3. Provide full sentence in German.
4. Generate list of missing words, that will be used later for fill-in blank exercise.
5. Return only JSON:
{{
  "instruction": "...",
  "sentence": "...",
  "missing_words": "..."
}}
6. While creating "missing_words", use verbs in a correct form and order from the sentence.
7. Examples of correctly generated exercises:
Exercise_1 - correct usage in perfect tense:
{{
    "instruction": "Complete the sentence:",
    "sentence": "Mir ist gestern plötzlich ein guter Gedanke eingefallen.",
    "missing_words": ["ist", "eingefallen"]
}}
Exercise_2 - correct usage in perfect tense:
{{
    "instruction": "Complete the sentence:",
    "sentence": "Sie hat das Essen gekocht.",
    "missing_words": ["hat", "gekocht"]
}}
"""