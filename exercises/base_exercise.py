import json
import re

class BaseExercise:
    def __init__(self, word_data, client, model):
        self.word_data = word_data
        self.client = client
        self.model = model

    def call_llm(self, prompt, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are a trainer of German language."},
                      {"role": "user", "content": prompt}],
            temperature=temperature
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    def censor_exercise(exercise_data):
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
        return exercise_data

    def generate_exercise(self):
        raise NotImplementedError()

    def check_exercise(self, exercise, user_answer, correct_answer):
        raise NotImplementedError()