import re


class BaseExercise:
    def __init__(self, word_data, client, model):
        self.word_data = word_data
        self.client = client
        self.model = model

    def generate_exercise(self) -> dict:
        raise NotImplementedError()

    def build_exercise(self, exercise_data: dict) -> str:
        raise NotImplementedError()

    def get_user_answer(self, exercise_data: dict) -> str :
        raise NotImplementedError()

    def check_exercise(self, exercise_data: dict, user_answer: str) -> bool:
        raise NotImplementedError()

    def get_feedback(self, exercise_data: dict, user_answer: list, client, model):
        raise NotImplementedError()


    @staticmethod
    def censor_exercise(exercise_data: dict):
        """
        :param exercise_data:
            {'instruction': 'Complete the sentence:',
            'sentence': 'Am Morgen zieht sie sich schnell an, bevor sie zur Arbeit geht.',
            'missing_words': ['zieht', 'sich']}
        :return:
            {'instruction': 'Complete the sentence:',
            'sentence': 'Am Morgen ___ sie ___ schnell an, bevor sie zur Arbeit geht.',
            'missing_words': ['zieht', 'sich'],
            'full_sentence': 'Am Morgen zieht sie sich schnell an, bevor sie zur Arbeit geht.'}
        """
        exercise_data["full_sentence"] = exercise_data["sentence"]  # store full sentence
        sentence = exercise_data["sentence"]  # sentence to censor
        missing_words = exercise_data["missing_words"]

        def censor(phrase: str, word: str) -> str:
            return re.sub(rf"\b{word}\b", "___", phrase, flags=re.IGNORECASE)

        for w in missing_words:
            sentence = censor(sentence, w)

        exercise_data["sentence"] = sentence
        print("exercise_data: ", exercise_data)

        return exercise_data