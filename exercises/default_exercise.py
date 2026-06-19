from exercises.base_exercise import BaseExercise
from prompts.default_prompts import DEFAULT_PROMPT

class DefaultExercise(BaseExercise):

    def _build_prompt(self):
        word = self.word_data["word"]
        prompt = DEFAULT_PROMPT.format(word=word)
        return prompt

    def generate_exercise(self):
        prompt = self._build_prompt()
        raw_exercise_data = self.call_llm(prompt)
        return self.censor_exercise(raw_exercise_data)

    # def check_exercise(self, exercise, user_answer, correct_answer):
    #     pass