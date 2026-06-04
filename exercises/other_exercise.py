from exercises.base_exercise import BaseExercise

class OtherExercise(BaseExercise):

    def generate_exercise(self):
        word = self.word_data["word"]
        prompt = f"""
            You help a student to learn and remember German words and phrases on levels A1-A2 providing an exercise and a correct answer.
            The German word/phrase is: {word}.
            Rules for exercise and answer generation:
            1. Create ONE A2 exercise.
            2. Create a correct answer.
            3. Return ONLY JSON:
            {{
              "exercise": "...",
              "answer": "..."
            }}
            4. Examples of an exercise and an answer:
            Exercise_1: "Build a correct sentence: Maria war __________, als sie die gute Nachricht bekam."
            Answer_1: "aus dem Häuschen"
            Exercise_2: "Use correct form of word/phrase: Ich __________ immer viel __________ beim Wandern."
            Answer_2: "habe, Spaß"
            Exercise_3: "Build a correct sentence: während / liest / er / frühstückt / die Zeitung / er"
            Answer_3: "Er liest die Zeitung, während er frühstückt."
            5. Exercise prompt is written in English. Exercise is written in German.
            """
        return self.call_llm(prompt)

    def check_exercise(self, exercise, user_answer, correct_answer):
        # return (user_answer.strip().lower() == correct_answer.strip().lower())
        print("Inside check_exercise")
        print(exercise, user_answer, correct_answer)
        prompt = f"""
            You are a teacher of German language.
            Exercise: {exercise}
            Correct answer: {correct_answer}
            Student answer: {user_answer}
            Task:
            2. Compare Correct answer and Student answer.
            3. return "correct" if the answer is correct, otherwise return "incorrect" in JSON.
            4. return ONLY JSON:
            {{"result": "..."}}
            5. Wrong capitalization of words, missing umlauts, wrong punctuation marks are not considered a mistake.
            6. Exercise is written in English.
            """
        if self.call_llm(prompt)["result"] == "correct":
            return True
        return False