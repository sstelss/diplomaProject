from random import *
import networkx as nx
import numpy as np
import math
from time import time
from threading import Thread

L = 0
T = []

# рассиояние между точками a и b
def Distance(a, b):
    a = int(math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))
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
            id, x, y = tokens[0],tokens[1],tokens[2]
            id, x, y = int(id), float(x), float(y)
            coords[id] = (x,y)
        except:
            pass
    # print('coord=', coords)

    G = nx.Graph()
    ids = list(coords.keys())
    for i in range(len(ids)):
        # расстояние будем искать для всех последующих вершин
        for j in range(i+1, len(ids)):
            G.add_edge(ids[i], ids[j], weight=Distance(coords[ids[i]], coords[ids[j]]))
            G[ids[i]][ids[j]]['ant'] = []
    return G


# класс муравья
class Ant():
    def __init__(self, start_vertex, number):
        self.start_v = start_vertex #вершина в которую посадили муравья
        self.number = number #номер муравья
        self.now_vertex = 0 #текущая вершина
        self.L = 0  #длина пройденного пути
        self.T = [] #пройденный путь


def find_way(ant, G, alpha, beta, gamma,  Q):

    ant.now_vertex = ant.start_v #каждый муравей начинает путь с вершины в которую его посадили
    ant.T = [ant.start_v] #запоминает эту вершину как уже посещенную
    ant.L = 0 #и понимает что не прошел еще никакого расстояния

    while True:
    #строим список всех вершин в которые муравьишка может пойти из текущей
        may_go = [k for k in G[ant.now_vertex] if ant.T.count(k) == 0]
        if len(may_go) == 0:
            break
        # print("Ant number ", self.number, "may_go = ", may_go)

        #считаем вероятности Р для каждой вершины
        P = []
        temp = 0
        # знаменатель один для каждой вершины
        for i in may_go:
            temp += ((Q / G[ant.now_vertex][i]['weight']) ** beta) * ((G[ant.now_vertex][i]['pheromon']) ** alpha) * ((G[ant.now_vertex][i]['gen_mem']) ** gamma)
        # числитель
        for i in may_go:
            p_temp = (((Q / G[ant.now_vertex][i]['weight']) ** beta) * ((G[ant.now_vertex][i]['pheromon']) ** alpha) * ((G[ant.now_vertex][i]['gen_mem']) ** gamma)) / temp
            P.append(p_temp)
        # print("Ant number",ant.number, "have P = ", P)

        #реализация случайности
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


    #добавим возврат в начальную вершину
    ant.T.append(ant.T[0])
    ant.L += G[ant.now_vertex][ant.T[0]]['weight']

    # print("L= ", ant.L)
    # print("T= ", ant.T,"\n\n")



def cross(m_ant, P, n):
#выберем n особей из m_ant согласно вероятностям P
    agents = np.random.choice(m_ant, n, replace=False,  p=P)
    # print("полный список")
    # for a in m_ant:
    #     print(" ", a.L, end=" ")
    # print()
    # print("Выбраны агенты: ")
    # for i in agents:
    #     print("Number: ", i.number)
    #     print("L = ", i.L)


    # скрещивание каждой пары
    child = []

    for i in range(0, n, 2):
        # убрем возврат в начальную точку
        agents[i].T.pop(len(agents[i].T)-1)
        agents[i+1].T.pop(len(agents[i+1].T) - 1)
        # print("T =", agents[i].T)
        # print("T =", agents[i+1].T)

        #выбираем случайную точку разреза
        k = randint(2, len(agents[i].T)-2)
        # print("Точка разреза: ", k)
        # для удобства
        S = agents[i]
        T = agents[i+1]

        # цикл от 0 до точки разреза
        # print("S=", S.T)
        # print("T=", T.T)
        for t in range(k):
            #найдем индекс вхождения t-го эл-та T в S
            index = S.T.index(T.T[t])
            # print("index = ", index)

            S.T[t], S.T[index] = S.T[index], S.T[t]
        child.append(S.T)
    # print("child", child)
    return child


def mutation(child):
    #для каждой особи
    for i in child:
        # выберем 3 точки a, b, c
        b = randint(2, len(i)-2)
        a = randint(0, b-1)
        c = randint(b+1, len(i)-1)
        # print("a=", a, "b=", b, "c=",c)

        # print("t-before=", i)
        i[a], i[b] = i[b], i[a]
        i[a], i[c] = i[c], i[a]
        # print("t-after=", i)



def check_best_way(G, arr):
    global L
    global T
    l = 0
    arr.append(arr[0])
    # print("arr=", arr)

    for i in range(len(arr)-1):
        l += G[arr[i]][arr[i+1]]['weight']
        # print("l=", l)
        # print("g[width] = ", G[arr[i]][arr[i+1]]['weight'])
    # print("len = ", l)
    if l < L:
        L = l
        T = arr[:]
    arr.pop(len(arr)-1)
    # print("arr end=", arr)



# G - граф
# count - кол-во муравьев
def colony(G, count, alpha, beta, gamma, Q, t_live, p=0):

    n = G.number_of_nodes()
    global T
    global L
    t = 0

    #разбросаем случайное колво феромона по всем ребрам
    #костыль!!!
    for i in range(1,n+1):
        for j in range(1,n+1):
            #если путь сам в себя
            if i != j:
                G[i][j]['pheromon'] = random()
                G[i][j]['gen_mem'] = 1
                # G[i][j]['pheromon'] = 0.0001

    #разложим муравьев по вершинам
    #можно сделать через numpy.random.choice
    my_ant = [] #список всех муравьев
    temp_pull = []
    for k in range(1, n+1):
        temp_pull.append(k)
    # print("temp_pull: ", temp_pull)

    for i in range(count):
        vert = choice(temp_pull) #выбираем случайную вершину из пулла
        my_ant.append(Ant(vert, i))
        my_ant[i].T.append(vert)  # внесли в память муравья начальную вершину
        temp_pull.pop(temp_pull.index(vert))
        # print("Для муравья номер", i,"выбрана вершина", vert)
        # print("Остались вершины: ", temp_pull)

    #зададим произвольный путь и найдем его длину
    for i in range(1,n):
        T.append(i)
        L += G[i][i+1]['weight'] + 55

    T.append(n)
    T.append(1)
    L += G[1][n]['weight']
    # print("T= ", T, "L = ", L)

    #цикл по времени жизни колонии
    while t < t_live:

        list_th = []
        #цикл по всем муравьям
        num_a = 0
        while num_a < count:

            th = Thread(target=find_way, args=(my_ant[num_a], G, alpha, beta, gamma, Q))
            list_th.append(th)
            th.start()
            # print("Муравей номер", my_ant[num_a].number, "Прошел путь ", my_ant[num_a].T, "Длиной ", my_ant[num_a].L)
            num_a += 1

        for l in list_th:
            l.join()
#########################################################################
        #пересчитываем феромон для каждого муравья
        # for n in my_ant:
        #     for i in range(len(n.T)-1):
        #         print("aAfter pherimon = ", G[n.T[i]][n.T[i+1]]['pheromon'])
        #         t_new = (1 - p) * G[n.T[i]][n.T[i+1]]['pheromon'] + Q / n.L
        #         G[n.T[i]][n.T[i+1]]['pheromon'] = t_new
        #         print("Before pheromone = ", t_new)

        for i in range(1, n):
            for j in range(i+1, n+1):
                d_t = 0
                for k in G[i][j]['ant']:
                    d_t += 1/k.L
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
            num_a += 1

        ###################################################new additly
        # print()
        # print()

        # оценка маршутов
        e = []
        for i in my_ant:
            e.append(n/i.L)
        # print("e =", e)

        # селекция решений
        e_ave = 0 #средние значение оценок популяции
        e_max = max(e)
        for i in e:
            e_ave += i
        e_ave /= len(e)

        # print("e_ave =", e_ave)
        # print("e_max =", e_max)

        f = []
        X = 10 #параметр масштабирования
        for i in e:
            # print("i=",i)
            temp = (X*((i - e_ave) + (e_max - i)) * e_ave) / (e_max - e_ave)
            f.append(temp)
        # print("f =", f)

        # веротности Р
        temp = 0
        P = []
        for i in f:
            temp += i
        for i in f:
            P.append(i/temp)
        # print("P = ", P)

        # кроссинговер выбираем k особей для скрещивания согласно вероятности P
        my_ant_copy = my_ant[:]
        child = cross(my_ant_copy, P, 20)
        #
        #проверка лучшего маршрута
        #
        for k in child:
            check_best_way(G, k)
        #
        mutation(child)
        # print("mut_child: ", child)
        #
        # проверка лучшего маршрута
        for k in child:
            check_best_way(G, k)
        #
        # обновляем генетическую информацию
        for i in range(1, n):
            for j in range(i+1, n+1):
                d_t = 0
                for k in G[i][j]['ant']:
                    d_t += 1/k.L
                G[i][j]['gen_mem'] += d_t

        t += 1

    # print()
    # print("Лучший путь, найденный муравьями с потоками, имеет длину", L, "И состоит из вершин: ", T)
    # return L, T



def run(path, alpha=0.7, beta=1.3, gamma=0.3, count=38, t_live=5, p=0.7, Q=1):
    G = ReadPointGraph(path)
    # L = 0
    # T = []

    start_t = time()
    colony(G, count, alpha, beta, gamma, Q, t_live, p)
    finish_t = time()
    # print("It have done for", finish_t - start_t)
    return ("BestLenght= ", L, "BestPath: ", T, "It have done for", finish_t - start_t)