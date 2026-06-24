from exercises.base_exercise import BaseExercise
from prompts.adjective_prompts import ADJECTIVE_PROMPT

class AdjectiveFillInBlankExercise(BaseExercise):

    def _build_prompt(self) -> str:
        word = self.word_data["word"]
        comparative = self.word_data["comparative"]
        superlative = self.word_data["superlative"]
        return ADJECTIVE_PROMPT.format(word=word, comparative=comparative, superlative=superlative)

    def generate_exercise(self):
        prompt = self._build_prompt()
        raw_exercise_data = self.call_llm(prompt)
        print("raw_exercise_data adj: ", raw_exercise_data)

        return self.censor_exercise(raw_exercise_data)

    # def check_exercise(self, user_answer, correct_answer):
    #     return (user_answer.strip().lower() == correct_answer.strip().lower())