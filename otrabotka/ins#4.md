**Encrypt This! — описание работы**

В этой задаче нужно зашифровать текст по определённым правилам. Сначала я разделил текст на слова с помощью `split()`. Потом первую букву каждого слова перевёл в ASCII код через `ord()`. После этого поменял местами вторую и последнюю буквы, если слово больше двух символов. В конце собрал все слова обратно в одну строку с помощью `join()`.

**Источники:**
- Codewars — Encrypt This!: https://www.codewars.com/kata/5277c8a221e209d3f6000b56
- Python Documentation — `ord()`: https://docs.python.org/3/library/functions.html#ord
- Python Documentation — методы строк: https://docs.python.org/3/library/stdtypes.html#string-methods

Я использовал эти источники, чтобы понять как работают строки, разделение слов и перевод букв в ASCII код.