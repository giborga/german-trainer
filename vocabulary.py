import json
import random
from typing import NotRequired, TypedDict

from study_sessions import get_latest_session_dates
from word_utils import process_word

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
            self._vocabulary = json.load(f)
            # print("type of self._vocabulary: ", type(self._vocabulary))  # type of self._vocabulary:  <class 'list'>
        self._word_index = None

    def get_word(self) -> WordData:
        """sample a random word from vocabulary"""
        return random.choice(self._vocabulary)

    def get_word_data(self, word: str) -> WordData:
        """look up a specific word from vocabulary"""
        processed_word = process_word(word)
        print("processed_word: ", processed_word)

        if self._word_index is None:
            self._word_index = {process_word(word_data["word"]): word_data for word_data in self._vocabulary}  # all words from vocabulary, ex, {'wandern': {'word': 'wandern', 'translation': 'to hike', 'part_of_speech': 'verb', 'reflexive': False, 'separable': False, 'perfekt': 'ist gewandert'}}

        if processed_word not in self._word_index:
            raise ValueError(f"Word {word} not in vocabulary.")

        return self._word_index[processed_word]

    # use later
    def get_words_added_on(self, date: str) -> list[WordData]:
        """get words added on a particular date"""
        words_added_on = [word_data for word_data in self._vocabulary if word_data.get("date_added") == date]
        return words_added_on

    def get_latest_words(self, limit: int = 5) -> list[WordData]:
        """get words from the last 5 study sessions"""
        latest_dates = get_latest_session_dates(limit)

        if not latest_dates:
            return []

        latest_words = [word_data for word_data in self._vocabulary if word_data["date_added"] in latest_dates]

        return latest_words