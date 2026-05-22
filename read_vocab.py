# Open vocabulary file
with open("vocab.txt", "r", encoding="utf-8") as file:
    words = file.readlines()
    print(words)

# Clean line endings
words = [word.strip() for word in words]

# Print words
print("Your vocabulary:\n")

for index, word in enumerate(words, start=1):
    print(f"{index}. {word}")