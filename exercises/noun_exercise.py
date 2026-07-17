from typing_extensions import override

from exercises.base_exercise import BaseExercise
from exercises.fill_in_blank_exercise import FillInBlankExercise
from prompts.noun_prompts import NOUN_PROMPT

from word_utils import normalize_word, remove_umlaut_word


class NounFillInBlankExercise(FillInBlankExercise):

    @override
    def _build_prompt(self) -> str:
        word = self.word_data["word"]
        article = self.word_data["article"]
        plural = self.word_data["plural"]
        translation = self.word_data["translation"]
        return NOUN_PROMPT.format(word=word, article=article, plural=plural)


class NounArticleExercise(BaseExercise):
    def generate_exercise_data(self) -> dict:
        return {"instruction": "Write the correct article for:",
                "noun": self.word_data["word"],
                "translation": self.word_data["translation"],
                "correct_article": self.word_data["article"]}

    def build_exercise(self, exercise_data: dict) -> str:
        return exercise_data["instruction"] + " " + exercise_data["noun"]

    def get_user_answer(self, exercise_data: dict) -> str:
        return input("Answer: ").strip()

    def check_exercise(self, exercise_data: dict, user_answer: str) -> bool:
        correct_article = exercise_data["correct_article"]
        normalized_correct_answer = normalize_word(remove_umlaut_word(correct_article))
        normalized_user_answer = normalize_word(remove_umlaut_word(user_answer))
        return normalized_correct_answer == normalized_user_answer

    def get_feedback(self, exercise_data: dict, user_answer=None, client=None, model=None) -> str:
        return f"\nCorrect article: {exercise_data['correct_article']}, \nTranslation: {exercise_data['translation']}"