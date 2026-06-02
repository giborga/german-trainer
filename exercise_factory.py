from exercises.verb_exercise import VerbExercise
from exercises.noun_exercise import NounExercise
from exercises.adjective_exercise import AdjectiveExercise
from exercises.other_exercise import OtherExercise

def create_exercise(word_data, client, model):
    pos = word_data["part_of_speech"]

    if pos == "verb":
        return VerbExercise(word_data, client, model)
    if pos == "noun":
        return NounExercise(word_data, client, model)
    if pos == "adjective":
        return AdjectiveExercise(word_data, client, model)

    return OtherExercise(word_data, client, model)