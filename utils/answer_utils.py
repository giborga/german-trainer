import re

from utils.llm_utils import call_llm
from word_utils import remove_umlaut_word, normalize_word

# count expected length of user's answer
def count_gaps(sentence: str) -> int:
    print("number of gaps", len(re.findall("___", sentence)))
    return len(re.findall("___", sentence))


# ask for user's answer and provide 3 attempts for filling gaps
def prompt_user_answer(expected_length: int, max_attempts: int = 3) -> str:
    for num_attempts in range(max_attempts):
        user_answer = parse_user_answer(input("Answer: "))

        if len(user_answer) == expected_length:
            return user_answer
        print(f"Please provide exactly {expected_length} words.")

    raise ValueError(f"Sentence contains {expected_length} gaps, but only {len(user_answer)} words were provided.")


# list words from user's answer
def parse_user_answer(raw_answer: str) -> list:
    return re.findall(r"\b\w+(?:[-']\w+)*\b", raw_answer)


# fill-in gaps in sentence by user's answer
def fill_gaps(user_answer: list, sentence: str) -> str:
    """
    :param user_answer: ['ziehe', 'mich', 'an']
    :param sentence: 'Am Morgen ___ ich ___ schnell ___, weil ich keine Zeit habe.'
    :return: 'Am Morgen ziehe ich mich schnell an, weil ich keine Zeit habe.'
    """
    words_iter = iter(user_answer)
    return re.sub(r"___", lambda match: next(words_iter), sentence)


# check exercise
def check_fill_in_blank_exercise(correct_answer: list, user_answer: list) -> bool:
    normalized_correct_answer = [normalize_word(remove_umlaut_word(word)) for word in correct_answer]
    normalized_user_answer = [normalize_word(remove_umlaut_word(word)) for word in user_answer]
    return normalized_correct_answer == normalized_user_answer


# explain mistake if the answer is incorrect
def explain_mistake_fill_in_blank_exercise(correct_answer: str, user_answer: str, client, model: str) -> str:
    prompt = f"""
        Correct answer: {correct_answer}
        Student answer: {user_answer}
        Explain the mistake in English. Maximum 2 sentences.
        """
    response = call_llm(prompt, client, model, temperature=0)
    # print("response: ", response)
    # print("type response.choices[0].message.content", type(response.choices[0].message.content))
    return response