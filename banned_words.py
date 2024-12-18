import string

banned_words = []

def ban_word(word: str):
    word = word.lower()
    banned_words.append(word)

def check_banned_words_in_text(text: str) -> bool:
    text = text.lower()
    words_in_text = [w.strip(string.punctuation) for w in text.split()]
    for word in banned_words:
        if word in words_in_text:
            return True
    return False