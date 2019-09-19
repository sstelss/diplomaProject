from random import *
import math
from time import time


class Bee():
    def __init__(self, way, lenght, number):
        self.T = way
        self.L = lenght
        self.number = number

# рассиояние между точками a и b
def Distance(a, b):
    a = int(math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))
    return a


# функция получения списка координат из файла
def ReadPointGraph(path):
    with open(path, "rt") as f:
        lines = f.readlines()
    # strip - удаляет пробельные символы в начале и в конце строки
    lines = [x.strip() for x in lines]

    # coords - это словарь, ключ - порядковый номер с 1, а содержание две вершины кортеджем
    coords = []
    number = []
    for line in lines:
        # split - разбивает строку по пробелам и сует каждый обьект в список
        tokens = line.split()
        try:
            coords.append([float(tokens[1]), float(tokens[2])])
            number.append(int(tokens[0]))
        except:
            pass
    # print('coord=', coords)

    return coords, number


def rand_one_way(temp):
    l = temp[:]
    shuffle(l)
    return l


def get_l(G, point):
    t = 0
    for i in range(len(point) - 1):
        t += Distance(G[point[i]-1], G[point[i+1]-1])
    t += Distance(G[point[-1]-1], G[point[0]-1])
    return t

def byL_key(bee):
    return bee.L


# функция исследования маршрута way
def reseach_way(way):
    i = randint(0, len(way.T))
    j = randint(0, len(way.T))

    if i > j:
        i, j = j, i

    a = way.T[0:i]
    b = way.T[i:j]
    b.reverse()
    c = way.T[j:len(way.T)]
    return a + b + c


def run(path, n = 100, amount = 1000):
    # всего пчел в колонии
    # n = 100
    # count = 12
    L = 9999999999
    T = []


    # начальный с координатами и номерами с 1
    arr, start_numbers = ReadPointGraph(path)
    # print("arr:", arr)
    # print("numbers: ", start_numbers)

    start_t = time()
    # 1/2 от всех пчел получают случайные решения
    base_res = int(0.5 * n)
    my_bee = []
    for i in range(base_res):
        prom = rand_one_way(start_numbers)
        my_bee.append(Bee(prom, get_l(arr, prom), i))

    # сортируем список по длине
    t = sorted(my_bee, key=byL_key)
    my_bee = t[:]

    # проверка на лучшее решение, т.к. список осортирован достаточно проверить первый элемент
    if my_bee[0].L < L:
        L = my_bee[0].L
        T = my_bee[0].T[:]

    # оставшиеся пчелы вылетают на разработку лучших участков, количество лучшихявляется 1/3 первых из отсортированного списка
    # попадают на лучший участок с вероятность 0.6, если нет то получают случайный

    for i in range(base_res, n):
        if random() > 0.4:
            tm = reseach_way(choice(my_bee[:int(0.3 * len(my_bee))]))
            my_bee.append(Bee(tm, get_l(arr, tm), i))
        else:
            tm = rand_one_way(start_numbers)
            my_bee.append(Bee(tm, get_l(arr, tm), i))


    # сортируем список по длине
    t = sorted(my_bee, key=byL_key)
    my_bee = t[:]

    # проверка на лучшее решение, т.к. список осортирован достаточно проверить первый элемент
    if my_bee[0].L < L:
        L = my_bee[0].L
        T = my_bee[0].T[:]


    # основная часть
    for itter in range(amount):
        for i in range(len(my_bee)):
            test = random()
            if  test > 0.4:
                tm = reseach_way(choice(my_bee[:int(0.3 * len(my_bee))]))
                my_bee.append(Bee(tm, get_l(arr, tm), i))
            elif 0.3 < test < 0.4:
                tm = rand_one_way(start_numbers)
                my_bee.append(Bee(tm, get_l(arr, tm), i))
            else:
                tm = reseach_way(choice(my_bee[int(0.3 * len(my_bee)):]))
                my_bee.append(Bee(tm, get_l(arr, tm), i))

        # сортируем список по длине
        t = sorted(my_bee, key=byL_key)
        my_bee = t[:]

        # проверка на лучшее решение, т.к. список осортирован достаточно проверить первый элемент
        if my_bee[0].L < L:
            L = my_bee[0].L
            T = my_bee[0].T[:]

        # удаляем лишние элементы
        for i in range(n, len(my_bee)-1):
            my_bee.pop(n)


    finish_t = time() - start_t
    # print("Пчелиный алгоритм завершил работу за", finish_t)
    # print("L = ", L)
    # print("T = ", T)
    return ("BestLenght= ", L, "BestPath: ", T, "It have done for", finish_t)



