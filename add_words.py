from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import sys
from datetime import date

from prompts.enrich_word_prompt import ENRICH_WORD_PROMPT
from study_sessions import save_session

# load api key
load_dotenv()

# call llm api
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# load existing vocabulary
def load_vocab() -> list[dict]:
    # if file does not exist yet
    if not os.path.exists("vocab.json"):
        return []

    with open("vocab.json", "r", encoding="utf-8") as file:
        return json.load(file)


# save vocabulary
def save_vocab(vocab):
    # complete overwrite
    with open("vocab.json", "w", encoding="utf-8") as file:
        json.dump(vocab, file, ensure_ascii=False, indent=2)


# add "date_added" field to word data
def add_date_added(word_data: dict) -> dict:
    if "date_added" not in word_data:
        word_data["date_added"] = date.today().isoformat()
    return word_data


# ask LLM to enrich word
def enrich_word(word) -> dict:
    prompt = ENRICH_WORD_PROMPT.format(word=word)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "system", "content": "You analyze German vocabulary."},
            {"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message.content
    return add_date_added(json.loads(content))


# validate metadata returned by llm
def validate_metadata(data):
    pos = data["part_of_speech"]

    if pos == "noun":
        required = ["word", "translation", "article", "plural", "date_added"]
    elif pos == "verb":
        required = ["word", "translation", "reflexive", "separable", "perfekt", "date_added"]
    elif pos == "adjective":
        required = ["word", "translation", "comparative", "superlative", "date_added"]
    elif pos == "adverb":
        required = ["word", "translation", "date_added"]
    elif pos == "other":
        required = ["word", "translation", "date_added"]

    for field in required:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    return True


# prevent duplicates
def word_exists(vocab: list[dict], new_word: str) -> bool:
    for item in vocab:
        if item["word"].lower() == new_word.lower():
            return True
    return False


# main logic
def main():

    # validate arguments
    if len(sys.argv) < 3:
        print('Usage:')
        print('python add_words.py add "word1, word2, phrase1, ..."')
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
            enriched_word = enrich_word(word)

            corrected_word = enriched_word["word"]

            # handle words that can't be recognized by llm
            if not corrected_word:
                print(f"\n \"{word}\" does not exist")
                continue

            # skip duplicates
            if word_exists(vocab, corrected_word):
                print(f"Skipped duplicate: {corrected_word}")
                continue

            # validate metadata
            validate_metadata(enriched_word)

            # add new word to vocabulary
            vocab.append(enriched_word)
            print("Added:")
            print(json.dumps(enriched_word, ensure_ascii=False, indent=2))

            # save updated vocabulary
            save_vocab(vocab)

            # save study session date
            save_session(enriched_word["date_added"])

            print("\nVocabulary updated successfully.")

        except Exception as e:
            print(f"Error processing '{word}':")
            print(e)

if __name__ == "__main__":
    main()