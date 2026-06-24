import argparse
import os
import re

from openai import OpenAI
from dotenv import load_dotenv

from config import MODEL
from exercise_factory import create_exercise
from vocabulary import Vocabulary

# load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def count_gaps(sentence: str) -> int:
    print("number of gaps", len(re.findall("___", sentence)))
    return len(re.findall("___", sentence))

# list words from answer
def parse_user_answer(raw_answer: str) -> list:
    print("Parsing user answer: ", re.findall(r"\b\w+(?:[-']\w+)*\b", raw_answer))
    return re.findall(r"\b\w+(?:[-']\w+)*\b", raw_answer)

# check if number of words in answer matches number of gaps in sentence
def has_expected_word_count(user_answer: list, expected_length: int) -> bool:
    print("len(user_answer) == expected_length: ", len(user_answer) == expected_length)
    return len(user_answer) == expected_length

# ask for user's answer and provide 3 attempts for filling gaps
def prompt_user_answer(expected_length: int, max_attempts: int = 3):
    for num_attempts in range(max_attempts):
        user_answer = parse_user_answer(input("Answer: "))

        print("user_answer: ", user_answer)
        print("expected_length: ", expected_length)
        if has_expected_word_count(user_answer, expected_length):
            return user_answer

        else:
            print(f"Please provide exactly {expected_length} words.")

    raise ValueError(f"Sentence contains {expected_length} gaps, but only {len(user_answer)} words were provided.")

# check answer
def check_exercise_locally(correct_answer, user_answer):

    def normalize(answer):
        return [word.strip().lower().replace("  ", " ") for word in answer]

    def remove_umlaut(answer):
        table = str.maketrans(
            {"ä": "a", "ö": "o", "ü": "u", "Ä": "A", "Ö": "O", "Ü": "U", "ß": "ss"}
        )
        return [word.translate(table) for word in answer]

    return normalize(remove_umlaut(correct_answer)) == normalize(remove_umlaut(user_answer))

# fill-in gaps in sentence by user's answer
def fill_gaps(answer: list, sentence: str) -> str:
    """
    :param answer: ['ziehe', 'mich', 'an']
    :param sentence: 'Am Morgen ___ ich ___ schnell ___, weil ich keine Zeit habe.'
    :return: 'Am Morgen ziehe ich mich schnell an, weil ich keine Zeit habe.'
    """
    words_iter = iter(answer)
    return re.sub(r"___", lambda match: next(words_iter), sentence)

# explain mistake only if the answer is incorrect
def explain_mistake(correct_answer, user_answer, client, model):
    prompt = f"""
        Correct answer: {correct_answer}
        Student answer: {user_answer}
        Explain the mistake in English. Maximum 5 sentences.
        """
    response = client.chat.completions.create(model=model, messages=[
        {"role": "system", "content": "You are a trainer of German language."},
        {"role": "user", "content": prompt}], temperature=0)

    return response.choices[0].message.content


# main loop
def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-n", "--number", type=int, default=5, help="Number of exercises")
    arg_parser.add_argument("-w", "--word", help="Request exercise with a specific word")
    args = arg_parser.parse_args()
    print("args: ", type(args), args)  # <class 'argparse.Namespace'> Namespace(number=5, word='wandern')

    vocab = Vocabulary()
    print("vocab: ", vocab)  # <vocabulary.Vocabulary object at 0x106c59c10>

    if args.word is not None:
        word_data = vocab.get_word_data(args.word)
        print("word_data: ", word_data)  # {'word': 'wandern', 'translation': 'to hike', 'part_of_speech': 'verb', 'reflexive': False, 'separable': False, 'perfekt': 'ist gewandert'}

        def sample_word_data():
            yield from [word_data]

    else:
        def sample_word_data():
            while True:
                yield vocab.get_word()

    print("\nGerman Trainer started. Type CTRL+C to exit.\n")
    count = 0

    for word_data in sample_word_data():
        print(f"\nWORD: {word_data['word']}\n")  # wandern

        # 1. create exercise object
        exercise_obj = create_exercise(word_data, client, MODEL)

        # 2. generate a particular type of exercise
        exercise_data = exercise_obj.generate_exercise()

        full_sentence = exercise_data["full_sentence"]
        instruction = exercise_data["instruction"]
        sentence = exercise_data["sentence"]
        correct_answer = exercise_data["missing_words"]

        exercise = instruction + " " + sentence
        print("Exercise: ", "\n" + exercise)

        # 3. enter answer
        user_answer = prompt_user_answer(expected_length=count_gaps(sentence))
        # 4. check answer
        is_correct = check_exercise_locally(correct_answer, user_answer)

        if is_correct:
            print("✅ Correct!")
        else:
            # 5. Explain mistake
            filled_user_answer = fill_gaps(user_answer, sentence)
            explanation = explain_mistake(full_sentence, filled_user_answer, client, MODEL)
            print("❌ Incorrect")
            print(f"\nCorrect answer: {full_sentence}")
            print(f"\nExplanation: {explanation}")

        count += 1
        print("args.number: ", args.number)

        if count == args.number:
            break


if __name__ == "__main__":
    main()