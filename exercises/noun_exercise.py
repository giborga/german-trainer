import json

from exercises.base_exercise import BaseExercise
from prompts.noun_prompts import NOUN_PROMPT

from word_utils import normalize_word, remove_umlaut_word
from utils.answer_utils import count_gaps, prompt_user_answer, check_fill_in_blank_exercise, fill_gaps, \
    explain_mistake_fill_in_blank_exercise
from utils.llm_utils import call_llm

class NounFillInBlankExercise(BaseExercise):

    def _build_prompt(self) -> str:
        word = self.word_data["word"]
        article = self.word_data["article"]
        plural = self.word_data["plural"]
        translation = self.word_data["translation"]
        return NOUN_PROMPT.format(word=word, article=article, plural=plural)

    def generate_exercise_data(self) -> dict:
        """
        :return:
        {"instruction": "...",
        "full_sentence": "...",
        "sentence": "... ___ ... ___",
        "missing_words": ['...', '...']}
        """
        prompt = self._build_prompt()
        client = self.client
        model = self.model

        raw_exercise_data = json.loads(call_llm(prompt, client, model))  # json string -> python dict
        print("raw_exercise_data noun: ", raw_exercise_data)
        return self.censor_exercise(raw_exercise_data)

    def build_exercise(self, exercise_data: dict) -> str:
        return exercise_data["instruction"] + " " + exercise_data["sentence"]

    def get_user_answer(self, exercise_data: dict) -> str:
        expected_length = count_gaps(exercise_data["sentence"])
        user_answer = prompt_user_answer(expected_length)  # list
        return user_answer

    def check_exercise(self, exercise_data: dict, user_answer: list) -> bool:
        return check_fill_in_blank_exercise(exercise_data["missing_words"], user_answer)

    def get_feedback(self, exercise_data: dict, user_answer: list, client, model) -> str:
        correct_answer = exercise_data["full_sentence"]
        filled_user_answer = fill_gaps(user_answer, exercise_data["sentence"])
        return explain_mistake_fill_in_blank_exercise(correct_answer, filled_user_answer, client, model)


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