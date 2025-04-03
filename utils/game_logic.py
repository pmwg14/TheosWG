import random
import requests

def load_word_list():
    with open("data/english_words_age_8_16.txt", "r") as f:
        words = [line.strip().lower() for line in f.readlines()]
    return words

def is_valid_word(word, word_list, game_log):
    return word in word_list and word not in game_log

def get_valid_word(start_letter, word_list, game_log):
    candidates = [w for w in word_list if w.startswith(start_letter) and w not in game_log]
    return random.choice(candidates) if candidates else None

def get_hint(start_letter, word_list, game_log):
    return [w for w in word_list if w.startswith(start_letter) and w not in game_log][:5]

def get_definition(word):
    try:
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if r.status_code == 200:
            data = r.json()
            return data[0]['meanings'][0]['definitions'][0]['definition']
    except:
        return None