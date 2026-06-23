import json
import random
from typing import NotRequired, TypedDict

class WordData(TypedDict):
    word: str
    translation: str
    part_of_speech: str
    article: NotRequired[str]
    plural: NotRequired[str]
    reflexive: NotRequired[bool]
    separable: NotRequired[bool]
    perfect: NotRequired[str]
    comparative: NotRequired[str]
    superlative: NotRequired[str]

class Vocabulary:
    def __init__(self) -> None:
        with open("vocab.json", "r", encoding="utf-8") as f:
            self._vocabulary = json.load(f)
            print("type of self._vocabulary: ", type(self._vocabulary))  # type of self._vocabulary:  <class 'list'>
        self._word_index = None

    def get_word(self) -> WordData:
        """Sample a random word from vocabulary."""
        return random.choice(self._vocabulary)

    def get_word_data(self, word: str) -> WordData:
        """Look up a specific word from vocabulary."""
        if self._word_index is None:
            self._word_index = {word_data["word"]: word_data for word_data in self._vocabulary}
            # print("self._word_index: ", self._word_index)  # returns ALL words from dict, ex, {'wandern': {'word': 'wandern', 'translation': 'to hike', 'part_of_speech': 'verb', 'reflexive': False, 'separable': False, 'perfekt': 'ist gewandert'}}
            print("self._word_index[word]: ", self._word_index[word])  # returns all data exactly for "wandern"
        return self._word_index[word]