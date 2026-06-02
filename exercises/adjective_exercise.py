import json
from exercises.base_exercise import BaseExercise

class AdjectiveExercise(BaseExercise):

    def generate_exercise(self):
        word = self.word_data["word"]
        prompt = f"""
You help a student to learn and remember German adjectives on levels A1-A2 providing an exercise and a correct answer.
The German adjective is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 exercise focused on: correct ending or plural form.
2. The student is familiar with the following grammar on A1-A2 levels and wants to improve the usage:
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
3. Return ONLY JSON:
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