import networkx as nx
from random import *
import numpy as np
from math import *
import matplotlib.pyplot as plt


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


def plot(cor, start_x=0, finish_x=10000, start_y=0, finish_y=10000, edge=True):
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    plt.title("Точки")
    plt.grid(True)
    if(edge):
        plt.axis([start_x, finish_x, start_y, finish_y])
    temp = np.array(cor + [cor[0]])
    print("temp=",temp)
    # np.array[:,0] - вернет список из нулевых значений каждого подсписка
    # plt.plot с значенем 'o-' построит кривую по заданым координатам и выделит точки кружочками, первая переменная - значения иксов, второя - игреков
    plt.plot(temp[:,0], temp[:,1], 'o-')
    plt.show()


points = ReadPointGraph("graph/lu980.tsp.txt")
print(points)
n = [46, 48, 52, 53, 58, 56, 61, 51, 55, 49, 44, 42, 50, 47, 37, 27, 19, 15, 12, 9, 10, 5, 11, 14, 7, 16, 13, 23, 25, 17, 24, 26, 21, 33, 28, 60, 57, 64, 77, 79, 81, 83, 92, 96, 93, 95, 97, 107, 108, 112, 110, 106, 105, 118, 117, 121, 120, 116, 115, 124, 123, 128, 160, 166, 162, 158, 159, 165, 168, 170, 171, 167, 155, 148, 143, 131, 135, 129, 133, 141, 144, 150, 153, 154, 157, 139, 86, 85, 98, 111, 104, 101, 99, 94, 89, 90, 63, 65, 20, 59, 62, 82, 36, 8, 6, 1, 2, 3, 68, 66, 67, 73, 70, 45, 22, 29, 34, 38, 43, 41, 54, 35, 32, 31, 40, 39, 30, 75, 72, 69, 74, 78, 91, 80, 71, 76, 87, 102, 103, 100, 84, 88, 147, 152, 175, 182, 194, 190, 179, 172, 173, 174, 192, 181, 184, 186, 183, 187, 180, 178, 177, 189, 191, 188, 164, 161, 163, 176, 169, 156, 126, 125, 127, 134, 132, 130, 142, 137, 140, 145, 146, 149, 138, 119, 109, 113, 114, 122, 136, 151, 185, 193, 4, 18, 46]

temp1 = []
for i in n:
    temp1.append(points[i-1])
print("temp1=", temp1)
plot(temp1, edge=False)



