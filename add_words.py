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
- verb (examples: verb with separable prefix: anrufen, reflexive verb: sich beeilen, regular verb: gehen)
- adjective
- adverb
- other (examples: phrases like "ausflug machen", "spazieren gehen")

5. If no such word exists, assign word="", "translation"="", "part_of_speech"="".
6. If noun:
return:
{{
  "word": "...",  [note: noun in singular form]
  "translation": "...",
  "part_of_speech": "noun",
  "article": "...",
  "plural": "..." [note: noun in plural form]
}}

If verb:
return:
{{
    "word": "...",
    "translation": "...",
    "part_of_speech": "verb",
    "reflexive": true/false,
    "separable": true/false,
    "perfekt": "..." (example: "hat getanzt")
}}

If adjective:
return:
{{
  "word": "...",
  "translation": "...",
  "part_of_speech": "adjective",
  "comparative": "...",
  "superlative": "..."
}}

If adverb:
return:
{{
  "word": "...",
  "translation": "...",
  "part_of_speech": "adverb"
}}

If other:
return:
{{
  "word": "...",
  "translation": "...",
  "part_of_speech": "other"
}}

7. Return ONLY valid JSON. No markdown. No explanations.
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


# validate metadata returned by llm
def validate_metadata(data):
    pos = data["part_of_speech"]

    if pos == "noun":
        required = [
            "word",
            "translation",
            "article",
            "plural"]

    if pos == "verb":
        required = [
            "word",
            "translation",
            "reflexive",
            "separable",
            "perfekt"]

    if pos == "adjective":
        required = [
            "word",
            "translation",
            "comparative",
            "superlative"
        ]

    if pos == "adverb":
        required = [
            "word",
            "translation"]

    if pos == "other":
        required = [
            "word",
            "translation"]

    for field in required:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    # print("Metadata validated")
    return True


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

            validate_metadata(enriched)
            vocab.append(enriched)

            print("Added:")
            print(json.dumps(enriched, ensure_ascii=False, indent=2))

            # save updated vocab
            save_vocab(vocab)

            print("\nVocabulary updated successfully.")

        except Exception as e:
            print(f"Error processing '{word}':")
            print(e)

if __name__ == "__main__":
    main()