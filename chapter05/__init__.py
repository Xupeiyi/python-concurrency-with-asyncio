def load_common_words() -> list[str]:
    with open('common_words.txt') as f:
        return f.readlines()