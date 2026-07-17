from typing_extensions import override

from exercises.fill_in_blank_exercise import FillInBlankExercise
from prompts.verb_prompts import (REFLEXIVE_AND_SEPARABLE_VERB_PROMPT, REFLEXIVE_VERB_PROMPT, SEPARABLE_VERB_PROMPT, DEFAULT_VERB_PROMPT)


class VerbFillInBlankExercise(FillInBlankExercise):

    @override
    def _build_prompt(self):
        word = self.word_data["word"]

        if self.word_data["separable"] and self.word_data["reflexive"]:
            return REFLEXIVE_AND_SEPARABLE_VERB_PROMPT.format(word=word)

        if self.word_data["separable"]:
            return SEPARABLE_VERB_PROMPT.format(word=word)

        if self.word_data["reflexive"]:
            return REFLEXIVE_VERB_PROMPT.format(word=word)

        return DEFAULT_VERB_PROMPT.format(word=word)