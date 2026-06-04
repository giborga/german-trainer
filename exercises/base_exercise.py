import json

class BaseExercise:
    def __init__(self, word_data, client, model):
        self.word_data = word_data
        self.client = client
        self.model = model

    def call_llm(self, prompt, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                    "content": "You are a trainer of German language."},
                {"role": "user",
                    "content": prompt}
            ],
            temperature=temperature
        )

        return json.loads(response.choices[0].message.content)

    def generate_exercise(self):
        raise NotImplementedError()

    def check_exercise(self, exercise, user_answer, correct_answer):
        raise NotImplementedError()