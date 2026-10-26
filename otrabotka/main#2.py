#поиск букв по шаблону
import re
#ну это тоже как первое задание но как бы с исключением к символам "-_"
def camel_case(text):
    return re.sub(r"[-_]([a-zA-Z])", lambda x: x.group(1).upper(), text)

print(camel_case("the-stealth-warrior"))
print(camel_case("The_Stealth_Warrior")) 
print(camel_case("The_Stealth-Warrior")) 