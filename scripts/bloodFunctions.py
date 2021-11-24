# Подключение функций
import bloodFunctions as s

# Инициализация spi
s.initSpiAdc()

# Проведение эксперимента
print("Начало эксперимента")
a = input()
print("Необходимо выполнить калибровку")
print("Введите y для продолжения")
for i in range(4):
    if input() == "y":
        print("Введите давление")
        s.calibraton(input())

print("-----Эксперимент №1-----")
print("Введите y для продолжения")
if input() == "y":
    print("Введите состояние человека:")
    experiment_name = input()
    s.experiment(experiment_name)
    print("Эксперимент 1 завершен")
print("-----Эксперимент №2-----")
print("Введите y для продолжения")
if input == "y":
    print("Введите состояние человека:")
    experiment_name = input()
    s.experiment(experiment_name)
    print("Эксперимент 2 завершен")
