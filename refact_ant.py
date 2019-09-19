from random import *
import networkx as nx
import numpy as np
import math
from time import time
from threading import Thread

from multiprocessing import Process


# расстояние между точками a и b
def distance(a, b):
    a = int(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))
    return a


# считываем граф из документа
def ReadPointGraph(path):
    with open(path, "rt") as f:
        lines = f.readlines()
    # strip - удаляет пробельные символы в начале и в конце строки
    lines = [x.strip() for x in lines]

    # coords - это словарь, ключ - порядковый номер с 1, а содержание две вершины кортеджем
    coords = {}
    for line in lines:
        # split - разбивает строку по пробелам и сует каждый обьект в список
        tokens = line.split()
        try:
            id, x, y = tokens[0], tokens[1], tokens[2]
            id, x, y = int(id), float(x), float(y)
            coords[id] = (x, y)
        except:
            pass
    # print('coord=', coords)

    G = nx.Graph()
    ids = list(coords.keys())
    for i in range(len(ids)):
        # расстояние будем искать для всех последующих вершин
        for j in range(i + 1, len(ids)):
            G.add_edge(ids[i], ids[j], weight=distance(coords[ids[i]], coords[ids[j]]))
            G[ids[i]][ids[j]]['ant'] = []
    return G


# класс муравья
class Ant():
    def __init__(self, start_vertex, number):
        self.start_v = start_vertex  # вершина в которую посадили муравья
        self.number = number  # номер муравья
        self.now_vertex = 0  # текущая вершина
        self.L = 0  # длина пройденного пути
        self.T = []  # пройденный путь


def find_way(ant, G, alpha, beta, Q, p):
    ant.now_vertex = ant.start_v  # каждый муравей начинает путь с вершины в которую его посадили
    ant.T = [ant.start_v]  # запоминает эту вершину как уже посещенную
    ant.L = 0  # и понимает что не прошел еще никакого расстояния

    while True:
        # строим список всех вершин в которые муравьишка может пойти из текущей
        may_go = [k for k in G[ant.now_vertex] if ant.T.count(k) == 0]
        if len(may_go) == 0:
            break
        # print("Ant number ", self.number, "may_go = ", may_go)

        # считаем вероятности Р для каждой вершины
        P = []
        temp = 0
        # знаменатель один для каждой вершины
        for i in may_go:
            temp += ((Q / G[ant.now_vertex][i]['weight']) ** beta) * (
                    (G[ant.now_vertex][i]['pheromon']) ** alpha)
        # числитель
        for i in may_go:
            p_temp = (((Q / G[ant.now_vertex][i]['weight']) ** beta) * (
                G[ant.now_vertex][i]['pheromon']) ** alpha) / temp
            P.append(p_temp)
        # print("Ant number",ant.number, "have P = ", P)

        # реализация случайности
        i_m_go = np.random.choice(may_go, 1, p=P)
        i_m_go = int(i_m_go)
        # print("Выбрана вершина ", i_m_go)
        ant.T.append(i_m_go)
        ant.L += G[ant.now_vertex][i_m_go]['weight']
        # print("Теперь путь, который прошел муравей №", self.number, "Равен ", self.L, "И состоит из вершин", self.T)
        #########################################################################
        # G[ant.now_vertex][i_m_go]['ant'] += [ant.number]
        G[ant.now_vertex][i_m_go]['ant'] += [ant]
        #########################################################################
        # меняем текущую вершину
        ant.now_vertex = i_m_go

    # добавим возврат в начальную вершину
    ant.T.append(ant.T[0])
    ant.L += G[ant.now_vertex][ant.T[0]]['weight']

    # print("L= ", ant.L)
    # print("T= ", ant.T,"\n\n")


# G - граф
# count - кол-во муравьев
def colony(G, count, alpha, beta, Q, t_live, e=0, p=0):
    n = G.number_of_nodes()
    T = []
    L = 0
    t = 0

    # разбросаем случайное колво феромона по всем ребрам
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # если путь сам в себя
            if i != j:
                G[i][j]['pheromon'] = random()
                # G[i][j]['pheromon'] = 0.0001

    # разложим муравьев по вершинам
    # можно сделать через numpy.random.choice
    my_ant = []  # список всех муравьев
    temp_pull = []
    for k in range(1, n + 1):
        temp_pull.append(k)
    # print("temp_pull: ", temp_pull)

    for i in range(count):
        vert = choice(temp_pull)  # выбираем случайную вершину из пулла
        my_ant.append(Ant(vert, i))
        my_ant[i].T.append(vert)  # внесли в память муравья начальную вершину
        temp_pull.pop(temp_pull.index(vert))
        # print("Для муравья номер", i,"выбрана вершина", vert)
        # print("Остались вершины: ", temp_pull)

    # зададим произвольный путь и найдем его длину
    for i in range(1, n):
        T.append(i)
        L += G[i][i + 1]['weight'] + 55

    T.append(n)
    T.append(1)
    L += G[1][n]['weight']
    # print("T= ", T, "L = ", L)

    # цикл по времени жизни колонии
    while t < t_live:
        list_th = []
        # цикл по всем муравьям
        num_a = 0
        while num_a < count:

            th = Process(target=find_way, args=(my_ant[num_a], G, alpha, beta, Q, p))
            list_th.append(th)
            th.start()
            # print("Муравей номер", my_ant[num_a].number, "Прошел путь ", my_ant[num_a].T, "Длиной ", my_ant[num_a].L)
            num_a += 1

        for l in list_th:
            l.join()
        #########################################################################
        # пересчитываем феромон для каждого муравья
        # for n in my_ant:
        #     for i in range(len(n.T)-1):
        #         print("aAfter pherimon = ", G[n.T[i]][n.T[i+1]]['pheromon'])
        #         t_new = (1 - p) * G[n.T[i]][n.T[i+1]]['pheromon'] + Q / n.L
        #         G[n.T[i]][n.T[i+1]]['pheromon'] = t_new
        #         print("Before pheromone = ", t_new)

        for i in range(1, n):
            for j in range(i + 1, n + 1):
                d_t = 0
                for k in G[i][j]['ant']:
                    d_t += 1 / k.L
                G[i][j]['pheromon'] = (1 - p) * G[i][j]['pheromon'] + d_t
        #########################################################################

        # отлавливаем лучшие решения
        num_a = 0
        while num_a < count:
            if my_ant[num_a].L < L:
                L = my_ant[num_a].L
                for i in range(len(my_ant[num_a].T)):
                    T[i] = my_ant[num_a].T[i]
                # print("New T= ", T, "L = ", L)
                # print("Iteration number", t)

            # #Элитные муравьи увеличивают кол-во феромона на лучшем пути
            # for i in range(len(T) - 1):
            #     tk = e * G[T[i]][T[i+1]]['pheromon'] + (Q / L)
            #     G[T[i]][T[i+1]]['pheromon'] = tk

            num_a += 1
        t += 1

    # print("Лучший путь, найденный муравьями с потоками, имеет длину", L, "И состоит из вершин: ", T)
    return L, T


def run(path, alpha=0.7, beta=1.3, count=38, t_live=5, e=10, p=0.7, Q=1):
    G = ReadPointGraph(path)
    start_t = time()
    L, T = colony(G, count, alpha, beta, Q, t_live, e, p)
    finish_t = time()
    # print("It have done for", finish_t - start_t)
    return ("BestLenght= ", L, "BestPath: ", T, "It have done for", finish_t - start_t)


if __name__ == '__main__':
    print(run("graph/dj38.tsp.txt"))