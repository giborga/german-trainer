from exercises.base_exercise import BaseExercise

class VerbExercise(BaseExercise):

    def generate_exercise(self):
        word = self.word_data["word"]

        if self.word_data["reflexive"]:
            prompt = f"""
You help a student to learn and remember reflexive German verbs on levels A1-A2 providing an exercise and a correct answer.
The german reflexive verb is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 exercise.
2. Generate an exercise.
3. Generate correct answer.
4. Return ONLY JSON:
{{
  "exercise": "...",
  "answer": "..."
}}
5. Examples of an exercise and an answer:
Exercise_1: "Complete the sentence: Ich __________ mich, weil der Zug gleich kommt."
Answer_1: "beeile"
Exercise_2: "Complete the sentence: Ich __________ mich gestern nicht gut __________."
Answer_2: "habe, gefühlt"
6. Exercise is written in English.
"""
        if self.word_data["separable"]:
            prompt = f"""
You help a student to learn and remember separable German verbs on levels A1-A2 providing an exercise and a correct answer.
The german verb with separable prefix is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 fill-in-blank exercise that practices a German verb with a separable prefix.
2. Generate an exercise.
3. Generate a correct answer.
4. Return ONLY JSON:
{{
  "exercise": "...",
  "answer": "..."
}}
5. Examples of an exercise and an answer:
Exercise: "Complete the sentence: Wann __________ du deine Eltern __________?"
Answer: "rufst, an"
6. Exercise written in English.
"""
        else:
            prompt = f"""
You help a student to learn and remember German verbs on levels A1-A2 providing an exercise and a correct answer.
The german verb is: {word}.
Rules for exercise and answer generation:
1. Create ONE A2 fill-in-blank exercise that practices a German verb in Perfekt form (haben/sein + Partizip II).
2. Generate an exercise.
3. Generate correct answer. 
4. Return ONLY JSON:
{{
  "exercise": "...",
  "answer": "..."
}}
5. Examples of an exercise and an answer:
Exercise: "Complete the sentence: Sie __________ das Essen __________."
Answer: "hat, gekocht"

6. Exercise is written in English.
"""
        return self.call_llm(prompt)

    # def check_exercise(self, user_answer, correct_answer):
    #     return user_answer.strip().lower() == correct_answer.strip().lower()

