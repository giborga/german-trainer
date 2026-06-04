from exercises.base_exercise import BaseExercise

class AdjectiveExercise(BaseExercise):

    def generate_exercise(self):
        word = self.word_data["word"]
        prompt = f"""
You help a student to learn and remember German adjectives on levels A1-A2 providing an exercise and a correct answer.
The German adjective is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 exercise focused on: correct ending or correct komparativ/superlativ form.
2. The student is familiar with the following grammar on A2 level and wants to improve the usage:
- komparativ, superlativ,
- akkusativ und dativ Artikel,
- Possesivartikel im dativ,
- Adjektive nach dem bestimmen Artikel.
3. Return ONLY JSON:
{{
  "exercise": "...",
  "answer": "..."
}}
4. Examples of an exercise and an answer:
Exercise_1: "Use advective with correct ending: Der _______ Hund spielt im Garten."
Answer_1: "große"
Exercise_2: "Complete the sentence: Ich kaufe den _______ Tisch für mein Arbeitszimmer."
Answer_2: "alten"
Exercise_3: "Complete the sentence: Ich spreche mit der _______ Lehrerin über die Prüfung."
Answer_3: "freundlichen"
5. Exercise is written in English.
"""
        return self.call_llm(prompt)

    # def check_exercise(self, user_answer, correct_answer):
    #     return (user_answer.strip().lower() == correct_answer.strip().lower())