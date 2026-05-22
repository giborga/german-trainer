import sys
import os

# sys gives access to command-line arguments through argv
# sys.argv - It is a list of everything typed in the terminal
# print(sys.argv)

# Check if user provided arguments
if len(sys.argv) < 3:
    print('Usage:')
    print('python add_words.py add: "word1, word2, phrase"')
    exit()

# Read command
command = sys.argv[1]
# print(command)

# Read words
words_input = sys.argv[2]
# print(words_input)

# Validate command
if command != "add":
    print('Unknown command.')
    exit()

# Split words by comma
words = [word.strip() for word in words_input.split(",")]
# print(words)

# read existing words from file
existing_words = set()

if os.path.exists("/Users/ingeborga/study/german-trainer/vocab.txt"):
    with open("vocab.txt", "r", encoding="utf-8") as file:
        for line in file:
            existing_words.add(line.strip().lower())
        file.close()

print(existing_words)

new_words = []

# Save words to file - "a" is append mode
with open("vocab.txt", "a", encoding="utf-8") as file:
    for word in words:
        if word.lower() not in existing_words:
            file.write("\n" + word)
            new_words.append(word)

print("Words added successfully:")
for word in new_words:
    print("-", word)