from openai import OpenAI
from dotenv import load_dotenv
import os
import random
import json
from config import MODEL

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# Load vocabulary
def load_vocab():
    with open("vocab.txt", "r", encoding="utf-8") as f:
        words = [w.strip() for w in f.readlines() if w.strip()]
    return words

# Pick random word
def get_word(words):
    return random.choice(words)


# Generate exercise from LLM
def generate_exercise(word):
    prompt = f"""
You help a student to learn and remember new German words on levels A1-A2.
Assume that the student is mostly familiar with A1 vocabulary. Now they are learning A2 vocabulary.
Create ONE exercise for the word: "{word}".
Use A1-A2 vocabulary for that.
Rules:
1. Type of exercises: 
"translate from english to german",
"fill a gap in sentence",
"choose correct verb form",
"write a correct article",
"write a correct preposition",
"write a plural form of a noun".

2. The student is familiar with the following grammar on A1-A2 levels and wants to improve the usage:
- reflexive verben,
- nebensatz mit 'wenn' 'weil' 'dann' 'dass',
- vergleiche mit 'als' 'wie',
- komparativ, superlativ,
- modalverben,
- modalverben in Präteritum,
- akkusativ und dativ artikel,
- possesivartikel im dativ,
- genitiv: name+s,
- perfekt: satzklemmer,
- partizip II.

3. Choose type and logical grammar of an exercise depending on the chosen word.

4. Provide ONLY JSON output in this format:
{{
  "exercise": "...",
  "answer": "..."
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a German language teacher."},
            {"role": "user", "content": prompt}
        ],
        temperature=1
    )
    # print("response.choices[0]:", response.choices[0])
    return json.loads(response.choices[0].message.content)  # response.choices[0]: Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='{\n  "exercise": "Übersetze ins Deutsche: \'The waterfall is beautiful.\'",\n  "answer": "Der Wasserfall ist schön."\n}', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))


# Check answer
def check_answer(exercise, correct_answer, user_answer):

    prompt = f"""
You are a German teacher.
Exercise: {exercise}
Correct answer: {correct_answer}
Student answer: {user_answer}

Task:
1. Check if student answer is correct.
2. If correct, reply ONLY:
{{"result": "correct"}}

3. If incorrect, reply:
{{
  "result": "incorrect",
  "correct_answer": "...",
  "explanation": "..."
}}

4. Return only JSON.
5. Explanation should be in English.
6. Wrong capitalization of words is not considered as a mistake.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You check German exercises."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)


# Main loop
def main():
    words = load_vocab()
    # print(words)

    print("\nGerman Trainer started. Type CTRL+C to exit.\n")

    count = 0

    while count <= 5:  # play with 5 words only
        word = get_word(words)

        print(f"\nWORD: {word}\n")

        # 1. generate exercise
        raw = generate_exercise(word)
        # print("RAW LLM OUTPUT:\n")
        # print(raw)

        exercise = raw["exercise"]
        correct_answer = raw["answer"]

        print(exercise)

        # 2. enter answer
        user_answer = input("Answer: ")

        # 3. check answer
        result = check_answer(exercise, correct_answer, user_answer)

        if result["result"] == "correct":
            print("✅ Correct!")
        else:
            print("❌ Incorrect")
            print("\nCorrect answer:")
            print(result["correct_answer"])
            print("\nExplanation:")
            print(result["explanation"])

        count += 1


if __name__ == "__main__":
    main()