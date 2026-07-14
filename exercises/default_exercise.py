from exercises.base_exercise import BaseExercise
from prompts.default_prompts import DEFAULT_PROMPT
import json

from utils.answer_utils import count_gaps, prompt_user_answer, check_fill_in_blank_exercise, fill_gaps, \
    explain_mistake_fill_in_blank_exercise
from utils.llm_utils import call_llm

class DefaultExercise(BaseExercise):

    def _build_prompt(self):
        word = self.word_data["word"]
        return DEFAULT_PROMPT.format(word=word)

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
        print("raw_exercise_data default: ", raw_exercise_data)
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
        # print("Correct answer: ", correct_answer)
        # print("filled_user_answer: ", filled_user_answer)
        return explain_mistake_fill_in_blank_exercise(correct_answer, filled_user_answer, client, model)