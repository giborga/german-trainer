"""
normalize spacing / lowercase
replace umlauts
combine them into one normalized form
"""

def normalize_word(word: str) -> str:
    return word.strip().lower().replace("  ", " ")


def remove_umlaut_word(word: str) -> str:
    table = str.maketrans({"ä": "a", "ö": "o", "ü": "u", "Ä": "A", "Ö": "O", "Ü": "U", "ß": "ss"})
    return word.translate(table)


def process_word(word: str) -> str:
    return normalize_word(remove_umlaut_word(word))