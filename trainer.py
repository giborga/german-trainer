from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import random
import json
from config import MODEL
from exercise_factory import create_exercise

# load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# load vocabulary
def load_vocab():
    with open("vocab.json", "r", encoding="utf-8") as f:
        return json.load(f)

# pick random word
def get_word(vocab) -> dict:
    return random.choice(vocab)

def count_gaps(sentence: str) -> int:
    return len(re.findall("___", sentence))

# list words from answer
def parse_user_answer(raw_answer: str) -> list:
    return re.findall(r"\b\w+(?:[-']\w+)*\b", raw_answer)

# check if number of words in answer matches number of gaps in sentence
def has_expected_word_count(user_answer: list, expected_length: int) -> bool:
    return len(user_answer) == expected_length

# ask for user's answer and provide 3 attempts for filling gaps
def prompt_user_answer(expected_length: int, max_attempts: int = 3):
    for num_attempts in range(max_attempts):
        user_answer = parse_user_answer(input("Answer: "))

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
    vocab = load_vocab()
    print("\nGerman Trainer started. Type CTRL+C to exit.\n")
    count = 0

    while count <= 5:  # play with 5 words only
        word_data = get_word(vocab)
        print(f"\nWORD: {word_data['word']}\n")

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


if __name__ == "__main__":
    main()