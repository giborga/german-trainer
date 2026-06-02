from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import sys

# load api key
load_dotenv()

# call llm api
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# load existing vocabulary
def load_vocab():

    # if file does not exist yet
    if not os.path.exists("vocab.json"):
        return []

    with open("vocab.json", "r", encoding="utf-8") as file:
        return json.load(file)  # return list of dict


# save vocabulary
def save_vocab(vocab):

    # complete overwrite
    with open("vocab.json", "w", encoding="utf-8") as file:
        json.dump(vocab, file, ensure_ascii=False, indent=2)


# ask LLM to enrich word
def enrich_word(word):

    prompt = f"""
You are a German language assistant.
You analyze this German word or phrase: "{word}".

Tasks:
1. Correct spelling if needed.
2. Translate to English.
3. Determine part of speech.

Allowed parts_of_speech:
- noun
- verb
- adjective
- adverb
- other

4. If there is a phrase with several parts of speech, assign parts_of_speech="other".
5. If no such word exists, assign word="", "translation"="", "part_of_speech"="".
6. If parts_of_speech=noun, add a correct article to the word.

Return ONLY valid JSON:

{{
  "word": "...",
  "translation": "...",
  "part_of_speech": "..."
}}

No markdown. No explanations.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You analyze German vocabulary."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)


# prevent duplicates
def word_exists(vocab, new_word):

    for item in vocab:
        if item["word"].lower() == new_word.lower():
            return True

    return False


# main logic
def main():

    # validate arguments
    if len(sys.argv) < 3:
        print('Usage:')
        print('python add_words.py add "word1, word2, phrase1"')
        return

    command = sys.argv[1]

    if command != "add":
        print("Unknown command.")
        return

    # parse words
    raw_words = sys.argv[2]
    words = [w.strip() for w in raw_words.split(",")]

    # load existing vocab
    vocab = load_vocab()

    # process each word
    for word in words:

        print(f"\nProcessing: {word}")

        try:
            enriched = enrich_word(word)

            corrected_word = enriched["word"]

            # handle words that can't be recognized by llm
            if not corrected_word:
                print(f"\n \"{word}\" does not exist")
                continue

            # skip duplicates
            if word_exists(vocab, corrected_word):
                print(f"Skipped duplicate: {corrected_word}")
                continue

            vocab.append(enriched)

            print("Added:")
            print(json.dumps(enriched, ensure_ascii=False, indent=2))

        except Exception as e:
            print(f"Error processing '{word}':")
            print(e)

        # save updated vocab
        save_vocab(vocab)

        print("\nVocabulary updated successfully.")


if __name__ == "__main__":
    main()