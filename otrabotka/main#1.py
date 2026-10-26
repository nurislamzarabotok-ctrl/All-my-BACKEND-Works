import re #Подключаю некий инструмент, ну это типо для поиска букв по шаблону

def solution(s):
    return re.sub(r"([A-Z])", r" \1", s) #то есть re,sub() находит каждый Заглавный английскую букву и ставит пробелл

print(solution("camelCasing"))
print(solution("identifier"))
print(solution(""))
print(solution("HelloWorldTest"))