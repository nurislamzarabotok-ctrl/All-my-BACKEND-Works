def persistence(num):
    count = 0
    while num >= 10:
        result = 1
        for digit in str(num):
            result *= int(digit)
        num = result
        count += 1
    return count