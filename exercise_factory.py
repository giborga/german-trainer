from exercises.verb_exercise import VerbFillInBlankExercise
from exercises.noun_exercise import NounFillInBlankExercise
from exercises.noun_exercise import NounArticleExercise
from exercises.adjective_exercise import AdjectiveFillInBlankExercise
from exercises.default_exercise import DefaultExercise
from vocabulary import WordData


def create_exercise(word_data: WordData, client, model, exercise_type: str):
    pos = word_data["part_of_speech"]

    if exercise_type == "article":
        return NounArticleExercise(word_data, client, model)
    elif pos == "verb":
        return VerbFillInBlankExercise(word_data, client, model)
    elif pos == "noun":
        return NounFillInBlankExercise(word_data, client, model)
    elif pos == "adjective":
        return AdjectiveFillInBlankExercise(word_data, client, model)

    return DefaultExercise(word_data, client, model)