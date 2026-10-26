def encrypt_this(text):
    result = []

    for word in text.split():
        # Первую букву меняю на ASCII код
        word = str(ord(word[0])) + word[1:]

        # Меняю местами вторую и последнюю букву
        if len(word) > 2:
            word = word[:2] + word[-1] + word[3:-1] + word[2]

        result.append(word)

    return " ".join(result)