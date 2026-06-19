from exercises.verb_exercise import VerbFillInBlankExercise
from exercises.noun_exercise import NounFillInBlankExercise
from exercises.adjective_exercise import AdjectiveExercise
from exercises.default_exercise import DefaultExercise

def create_exercise(word_data, client, model):
    pos = word_data["part_of_speech"]

    if pos == "verb":
        return VerbFillInBlankExercise(word_data, client, model)
    if pos == "noun":
        return NounFillInBlankExercise(word_data, client, model)
    if pos == "adjective":
        return AdjectiveExercise(word_data, client, model)

    return DefaultExercise(word_data, client, model)