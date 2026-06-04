import json
from exercises.base_exercise import BaseExercise

class NounExercise(BaseExercise):

    def generate_exercise(self):
        word = self.word_data["word"]
        article = self.word_data["article"]
        plural = self.word_data["plural"]

        prompt = f"""
You help a student to learn and remember German nouns on level A2 providing an exercise and a correct answer.
The German noun is: {word}.
Correct article is: {article}.
Plural form: {plural}.
Rules for exercise and answer generation:
1. Generate ONE A2 exercise.
2. Generate a correct answer.
3. Examples of an exercise and an answer for noun article:
Exercise_1: "Complete with correct article: ___ große Hund spielt im Garten."
Answer_1: "der"
Exercise_2: "Complete with correct article: Ich kaufe ___ alten Tisch für mein Arbeitszimmer."
Answer_2: "den"
Exercise_3: "Complete with correct article: Ich spreche mit ___ freundlichen Lehrerin über die Prüfung."
Answer_3: "der"
4. Examples of an exercise and an answer for noun plural form:
Exercise_1: "Complete with correct plural form: Im Herbst fallen viele _______ von den Bäumen."
Answer_1: "Blätter"
Exercise_2: "Complete with correct plural form: Am Wochenende besuchen wir verschiedene _____ in Berlin."
Answer_2: "Museen"
5. Exercise is written in English.
6. Return ONLY JSON:
{{
  "exercise": "...",
  "answer": "..."
}}
"""

        return self.call_llm(prompt)

    # def check_exercise(self, user_answer, correct_answer):
    #     return (user_answer.strip().lower() == correct_answer.strip().lower())