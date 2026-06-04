from openai import OpenAI
from dotenv import load_dotenv
import os
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
def get_word(vocab):
    return random.choice(vocab)


# check answer
def check_exercise_locally(correct_answer, user_answer):

    def normalize(text):
        return text.strip().lower().replace("  ", " ")

    def remove_umlaut(text):
        table = str.maketrans(
            {"ä": "a", "ö": "o", "ü": "u", "Ä": "A", "Ö": "O", "Ü": "U", "ß": "ss"}
        )
        return text.translate(table)

    return normalize(remove_umlaut(correct_answer)) == normalize(remove_umlaut(user_answer))


# explain mistake only if the answer is incorrect
def explain_mistake(exercise, correct_answer, user_answer, client, model):
    prompt = f"""
Exercise: {exercise}
Correct answer: {correct_answer}
Student answer: {user_answer}
Explain the mistake in English.
Maximum 5 sentences.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
                "content": "You are a trainer of German language."},
            {"role": "user",
                "content": prompt}
        ],
        temperature=0
    )

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
        exercise = exercise_data["exercise"]
        correct_answer = exercise_data["answer"]
        print("Exercise: ", exercise)

        # 3. enter answer
        user_answer = input("Answer: ")

        # 4. check answer
        if word_data["part_of_speech"] == "other":
            is_correct = exercise_obj.check_exercise(exercise, user_answer, correct_answer)
        else:
            is_correct = check_exercise_locally(correct_answer, user_answer)

        if is_correct:
            print("✅Correct!")
        else:
            explanation = explain_mistake(exercise, correct_answer, user_answer, client, MODEL)
            print("❌Incorrect")
            print(f"\nExplanation: {explanation}")

        print(f"\nCorrect answer: {correct_answer}")
        count += 1


if __name__ == "__main__":
    main()