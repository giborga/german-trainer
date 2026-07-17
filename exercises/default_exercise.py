from typing_extensions import override

from exercises.fill_in_blank_exercise import FillInBlankExercise
from prompts.default_prompts import DEFAULT_PROMPT


class DefaultExercise(FillInBlankExercise):

    @override
    def _build_prompt(self):
        word = self.word_data["word"]
        return DEFAULT_PROMPT.format(word=word)