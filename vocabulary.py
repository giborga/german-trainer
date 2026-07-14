import json
import random
from typing import NotRequired, TypedDict

from study_sessions import get_latest_session_dates
from word_utils import process_word


class WordNotFoundError(ValueError):
    pass

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
    date_added: NotRequired[str]

class Vocabulary:
    def __init__(self) -> None:
        """load all words from vocabulary"""
        with open("vocab.json", "r", encoding="utf-8") as f:
            self._vocabulary = json.load(f)  # list
        self._word_index = None

    def get_words_by_part_of_speech(self, pos: str) -> list[WordData]:
        pos_vocabulary = [word_data for word_data in self._vocabulary if word_data["part_of_speech"] == pos]
        return pos_vocabulary

    def get_word(self, vocabulary: list[WordData]) -> WordData:
        """sample a random word from a vocabulary"""
        if vocabulary is None:
            return random.choice(self._vocabulary)
        return random.choice(vocabulary)

    def get_word_data(self, word: str) -> WordData:
        """
        :param word: 'wandern'
        :return: {'word': 'wandern', 'translation': 'to hike', 'part_of_speech': 'verb', 'reflexive': False, 'separable': False, 'perfekt': 'ist gewandert'}
        """
        processed_word = process_word(word)
        print("processed_word: ", processed_word)

        if self._word_index is None:
            self._word_index = {process_word(word_data["word"]): word_data for word_data in self._vocabulary}  # all words from vocabulary, ex, {'wandern': {'word': 'wandern', 'translation': 'to hike', 'part_of_speech': 'verb', 'reflexive': False, 'separable': False, 'perfekt': 'ist gewandert'}}

        if processed_word not in self._word_index:
            raise WordNotFoundError(f"Word {word} not in vocabulary.")

        return self._word_index[processed_word]

    def get_latest_words(self, limit: int = 5) -> list[WordData]:
        """get words from the last 5 study sessions"""
        latest_dates = get_latest_session_dates(limit)

        if not latest_dates:
            raise WordNotFoundError(f"Words not found for dates {latest_dates}.")

        latest_words = [word_data for word_data in self._vocabulary if word_data["date_added"] in latest_dates]

        return latest_words