from random import *
import numpy as np
import matplotlib.pyplot as plt
from time import time

# функция получения списка координат из файла
def ReadPointGraph(path):
    with open(path, "rt") as f:
        lines = f.readlines()
    # strip - удаляет пробельные символы в начале и в конце строки
    lines = [x.strip() for x in lines]

    # coords - это словарь, ключ - порядковый номер с 1, а содержание две вершины кортеджем
    coords = []
    for line in lines:
        # split - разбивает строку по пробелам и сует каждый обьект в список
        tokens = line.split()
        try:
            coords.append([float(tokens[1]), float(tokens[2]), int(tokens[0])])
        except:
            pass
    # print('coord=', coords)

    return coords

# строим на графике точки из cor, границы графика от a до b по оси абсцисс и ординат
def plot(cor, start_x=0, finish_x=10000, start_y=0, finish_y=10000, edge=True):
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    plt.title("Точки")
    plt.grid(True)
    if(edge):
        plt.axis([start_x, finish_x, start_y, finish_y])
    temp = np.array(cor + [cor[0]])
    # print("temp=",temp)
    # np.array[:,0] - вернет список из нулевых значений каждого подсписка
    # plt.plot с значенем 'o-' построит кривую по заданым координатам и выделит точки кружочками, первая переменная - значения иксов, второя - игреков
    plt.plot(temp[:,0], temp[:,1], 'o-')
    plt.show()

# функция изменения температуры
def DecreaseTemperature(initTemp, i):
    return initTemp * 0.1 / i

# функция определения вероятности перехода в неоптимальное состояние
def GetTransitionProbability(dE, T):
    return np.exp(-dE / T)

# функция решающая будет ли совершен переход в новое состояние
def is_Trnsaction(prob):
    if prob > 1 or prob < 0:
        print("error!!!!!!!!!!!!!!!!!")
        exit()
    value = random()
    if value <= prob:
        return 1
    else:
        return 0

# А - координаты i-й точки    В - координаты i+1 точки;  обычное Эвклидово расстояние;
def Metric(A, B):
    return ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5

# points - массив координат, считаем энергию для данного состояния(т.е. общее растояние)
def CalculateEnergy(points):
    n = len(points)
    E = 0
    for i in range(n-1):
        E += Metric(points[i], points[i+1])
    # возврат к начальной точке, работает только в полносвязных графах
    E += Metric(points[n-1], points[0])
    return E

# создание нового сосояния, на основе points; выбирается случайный промежуток в массиве и реверсируется
def GenerateStateCandidate(points):
    i = randint(0, len(points))
    j = randint(0, len(points))

    if i > j:
        i, j = j, i

    a = points[0:i]
    b = points[i:j]
    b.reverse()
    c = points[j:len(points)]
    return a + b + c

# найти путь по номерам координат из points, возвращает список последовательно идущих номеров
def find_path(points):
    path = []
    for i in range(len(points)):
        path.append(points[i][2])
    return path

# начальные значения
'''
    a - левая граница нашего графика и подбора точек
    b - правая граница нашего графика и подбора точек
    n - кол-во точек(используется для рандома)
    startT - температура с которой начинаем
    endT - температура, достигнув которой закончим цикл
'''

def run(path, startT=10, endT= 0.00001, paint=0):
    from_x = 0
    finish_x = 80
    from_y = 0
    finish_y = 80


    # points = chose_point(n, a, b)
    points = ReadPointGraph(path)
    # print(points)

    # отобразим точки и случайный маршут(здесь всегда берется от 0 до n-1)
    if paint == 1:
        #если edge = True то для границ графика используются from_x, finish_x, from_y, finish_y
        plot(points, from_x, finish_x, from_y, finish_y, edge=False)
    start_t = time()
    # state - последовательность номеров точек
    state = find_path(points)
    # print("state= ", state)
    # подсчет энергии для данного состояния
    currentEnergy = CalculateEnergy(points)
    # print("currentEnergy= ", currentEnergy)
    # задаем начальное значение Т
    T = startT
    # переменные для "ловли" лучшего маршута
    BestPath = state
    BestEnergy = currentEnergy

    # введем ограничение по итерациям
    for i in range(1, 100000):
        # создаем состояние-кандидат
        stateCandidate = GenerateStateCandidate(points)
        #     находим энергию(длину пути) состояния кандидата
        candidateEnergy = CalculateEnergy(stateCandidate)

        # если состояние кандидат имеет лучшую энергию(длину пути), то переходим в это состояние, если нет то переход будет осуществлен с вероятностью p
        if candidateEnergy < currentEnergy:
            currentEnergy = candidateEnergy
            points = stateCandidate[:]
            state = find_path(points)
        else:
            # подсчет вероятности р с которой будет совершен переход
            p = GetTransitionProbability(candidateEnergy - currentEnergy, T)
            if is_Trnsaction(p):
                currentEnergy = candidateEnergy
                points = stateCandidate[:]
                state = find_path(points)
        # "ловля" лучшего решения
        if currentEnergy < BestEnergy:
            BestEnergy = currentEnergy
            BestPath = state

        # изменение температуры происходит согласно заданой функции
        T = DecreaseTemperature(startT, i)

        # если достигли температуры выхода, то выходим
        if T <= endT:
            break

    # выведем и отобразим лучший маршут
    finish_t = time()
    # print("BestEnergy= ", BestEnergy)
    # print("BestPath: ", BestPath)
    # print("It have done for", finish_t - start_t)
    plt.figure()
    if paint == 1:
        plot(points, from_x, finish_x, from_y, finish_y, edge=False)
    return ("BestEnergy= ", BestEnergy, "BestPath: ", BestPath, "It have done for", finish_t - start_t)