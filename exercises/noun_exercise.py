from exercises.base_exercise import BaseExercise
from prompts.noun_prompts import NOUN_PROMPT

class NounFillInBlankExercise(BaseExercise):

    def _build_prompt(self) -> str:
        word = self.word_data["word"]
        article = self.word_data["article"]
        plural = self.word_data["plural"]
        return NOUN_PROMPT.format(word=word, article=article, plural=plural)

    def generate_exercise(self):
        prompt = self._build_prompt()
        raw_exercise_data = self.call_llm(prompt)
        print(raw_exercise_data)

        return self.censor_exercise(raw_exercise_data)

    # def check_exercise(self, user_answer, correct_answer):
    #     pass