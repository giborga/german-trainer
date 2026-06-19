from exercises.base_exercise import BaseExercise
from prompts.verb_prompts import (REFLEXIVE_AND_SEPARABLE_VERB_PROMPT, REFLEXIVE_VERB_PROMPT, SEPARABLE_VERB_PROMPT, DEFAULT_VERB_PROMPT)

class VerbFillInBlankExercise(BaseExercise):

    def _build_prompt(self):
        word = self.word_data["word"]

        if self.word_data["separable"] and self.word_data["reflexive"]:
            return REFLEXIVE_AND_SEPARABLE_VERB_PROMPT.format(word=word)

        if self.word_data["separable"]:
            return SEPARABLE_VERB_PROMPT.format(word=word)

        if self.word_data["reflexive"]:
            return REFLEXIVE_VERB_PROMPT.format(word=word)

        return DEFAULT_VERB_PROMPT.format(word=word)

    def generate_exercise(self):
        prompt = self._build_prompt()
        raw_exercise_data = self.call_llm(prompt)
        print("raw_exercise_data: ", raw_exercise_data)

        return self.censor_exercise(raw_exercise_data)

    # def check_exercise(self, user_answer, correct_answer):
    #     pass