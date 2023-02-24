# Функции для классификации строк вывода
import datetime


# Нормальное состояние
def i():
    return '\033[37mI \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Предупреждение
def w():
    return '\033[33mW \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Ошибка
def e():
    return '\033[31mE \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Успех
def s():
    return '\033[32mS \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
