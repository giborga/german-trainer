import json
from exercises.base_exercise import BaseExercise

class VerbExercise(BaseExercise):

    def generate_exercise(self):
        word = self.word_data["word"]
        prompt = f"""
You help a student to learn and remember German verbs on levels A1-A2 providing an exercise and a correct answer.
The german verb is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 exercise.
2. if the verb is reflexive (example: ’sich beeilen’), generate an exercise in style: "Complete the sentence: Ich __________ mich, weil der Zug gleich kommt."
3. If the verb has a separable prefix (example: ’anrufen’), generate an exercise in style: "Complete the sentence: Wann __________ du deine Eltern __________?"
4. If verb is not reflexive and has no separable prefix (example: "gehen"), generate an exercise in style: "Write a correct Perfekt verb form: Wir __________ am Strand spazieren __________."
5. The student is familiar with the following grammar on A1-A2 levels and wants to improve the usage:
- reflexive verben,
- nebensatz mit 'wenn' 'weil' 'dann' 'dass',
- vergleiche mit 'als' 'wie',
- komparativ, superlativ,
- modalverben,
- modalverben in Präteritum,
- akkusativ und dativ artikel,
- possesivartikel im dativ,
- genitiv: name+s,
- perfekt: satzklemmer,
- partizip II.

6. Return ONLY JSON:
{{
  "exercise": "...",
  "answer": "..."
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a German language trainer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return json.loads(response.choices[0].message.content)

    def check_exercise(self, user_answer, correct_answer):
        return (user_answer.strip().lower() == correct_answer.strip().lower())

