def digital_root(n):
    # Повторяю пока число не станет однозначным
    while n >= 10:
        n = sum(int(digit) for digit in str(n))
    return n