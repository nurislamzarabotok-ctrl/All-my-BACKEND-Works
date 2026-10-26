def is_pangram(s):
    # Делаю все буквы маленькими
    letters = set(s.lower())
    alphabet = set("abcdefghijklmnopqrstuvwxyz")

    # Проверяю есть ли все буквы алфавита
    return alphabet <= letters