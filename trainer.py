import argparse
import os
from collections.abc import Iterable

from openai import OpenAI
from dotenv import load_dotenv

from config import MODEL
from exercise_factory import create_exercise
from vocabulary import Vocabulary, WordNotFoundError, WordData

# load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-n", "--number", type=int, default=5, help="Number of exercises")
    arg_parser.add_argument("-w", "--word", help="Request exercise with a specific word")
    arg_parser.add_argument("-l", "--latest", action="store_true", help="Exercise words from the 5 latest sessions")
    arg_parser.add_argument("-e", "--exercise_type", choices=["default", "article"], default="default",
                            help="Exercise type to choose")

    args = arg_parser.parse_args()
    print("args: ", args)

    vocab = Vocabulary()  # vocabulary object

    exercise_type = args.exercise_type
    # print("exercise_type: ", exercise_type)

    if exercise_type != "default":
        if exercise_type == "article":
            vocabulary = vocab.get_words_by_part_of_speech("noun")

        def sample_word_data() -> Iterable[WordData]:
            while True:
                yield vocab.get_word(vocabulary)

    elif args.word is not None:
        try:
            word_data = vocab.get_word_data(args.word)  # WordData

        except WordNotFoundError as e:  # должно быть локализовано там где возникает ошибка
            raise ValueError(str(e))

        def sample_word_data() -> Iterable[WordData]:
            return [
                word_data]  # [{'word': 'wandern', 'translation': 'to hike', 'part_of_speech': 'verb', 'reflexive': False, 'separable': False, 'perfekt': 'ist gewandert'}]

    elif args.latest:
        latest_words = vocab.get_latest_words()

        def sample_word_data():
            yield from latest_words

    else:
        def sample_word_data() -> Iterable[WordData]:
            print("in sample_word_data for random vocabulary")
            while True:
                yield vocab.get_word(vocabulary=None)

    print("\nGerman Trainer started. Type CTRL+C to exit.\n")
    count = 0

    for word_data in sample_word_data():

        # print("word_data: ", word_data)  # {'word': 'wandern', 'translation': 'to hike', 'part_of_speech': 'verb', 'reflexive': False, 'separable': False, 'perfekt': 'ist gewandert'}
        print(f"\nWORD: {word_data['word']}\n")  # wandern

        # 1. create exercise object
        exercise_obj = create_exercise(word_data, client, MODEL, exercise_type)

        # 2. generate a particular type of exercise
        exercise_data = exercise_obj.generate_exercise_data()

        exercise = exercise_obj.build_exercise(exercise_data)
        print("Exercise: ", "\n" + exercise)

        # 3. enter answer
        user_answer = exercise_obj.get_user_answer(exercise_data)  # list

        # 4. check answer
        is_correct = exercise_obj.check_exercise(exercise_data, user_answer)

        if is_correct:
            print("✅ Correct!")
        else:
            # 5. Explain mistake
            print("❌ Incorrect")
            explanation = exercise_obj.get_feedback(exercise_data, user_answer, client, MODEL)
            print("Explanation: ", explanation)

        count += 1

        if count == args.number:
            break


if __name__ == "__main__":
    main()
