from typing_extensions import override

from exercises.fill_in_blank_exercise import FillInBlankExercise
from prompts.adjective_prompts import ADJECTIVE_PROMPT

class AdjectiveFillInBlankExercise(FillInBlankExercise):

    @override
    def _build_prompt(self) -> str:
        word = self.word_data["word"]
        comparative = self.word_data["comparative"]
        superlative = self.word_data["superlative"]
        return ADJECTIVE_PROMPT.format(word=word, comparative=comparative, superlative=superlative)