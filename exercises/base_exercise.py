class BaseExercise:
    def __init__(self, word_data, client, model):
        self.word_data = word_data
        self.client = client
        self.model = model

    def generate_exercise(self):
        raise NotImplementedError()

    def check_exercise(self, user_answer, correct_answer):
        raise NotImplementedError()