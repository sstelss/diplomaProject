import networkx as nx
import re
import math


def Distance(a, b):
    a = int(math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))
    return a


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
    temp = []
    G = nx.Graph()
    ids = list(coords.keys())
    for i in range(len(ids)):
        # расстояние будем искать для всех последующих вершин
        for j in range(i+1, len(ids)):
            G.add_edge(ids[i], ids[j], weight=Distance(coords[ids[i]], coords[ids[j]]))
        temp.append(list(coords[ids[i]]))
    # print('G=', G)
    # print(temp)
    return G, temp


def ReadMatrixGraph(path):
    with open(path, "rt") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    n = -1
    pos = 0
    while not (pos == len(lines)):
        cur = lines[pos]
        pos+=1
        found = re.match("DIMENSION[^0-9]*(\\d+)", cur)
        if found:
            n = int(found.group(1))
            break
    assert n != -1, "Invalid input file"

    while not (pos == len(lines)):
        cur = lines[pos]
        pos+=1
        if len(cur.split()) == n:
            pos -= 1
            break
    assert pos < len(lines), "Invalid input file"

    G = nx.DiGraph()
    for i in range(n):
        cur = lines[pos]
        pos+=1
        cur = cur.split()
        for j in range(n):
            if cur[j] == "-1":continue
            G.add_edge(i+1,j+1,weight=float(cur[j]))
    return G


def ReadEdgeGraph(path):
    with open(path, "rt") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    G = nx.DiGraph()
    for line in lines:
        tokens = line.split()
        if len(tokens) == 2:
            try:
                a, b = int(tokens[0]), int(tokens[1])
                G.add_edge(a,b)
            except:
               pass
    return G


def ReadCSPProblemStatment(path):
    with open(path, "rt") as f:
        lines = f.readlines()
    lines = [x.strip().split() for x in lines]

    pos = 0
    try:
        assert len(lines[pos]) <= 2
        assert len(lines[pos]) >= 1
        m = int(lines[pos][0])
        if len(lines[pos]) == 2:
            if lines[pos][1] == "directional":
                G = nx.DiGraph()
            elif lines[pos][1] == "bidirectional":
                G = nx.Graph()
            else:
                assert False
        else:
            G = nx.Graph()
        pos += 1

        for i in range(m):
            assert len(lines[pos]) == 3
            a, b, c = lines[pos]
            c = float(c)
            G.add_edge(a,b,weight=c)
            pos+=1

        assert len(lines[pos])==2
        S = lines[pos][0]
        T = lines[pos][1]
        pos+=1

        forbidden = []
        n = len(lines[pos])
        for i in range(n):
            if '-' in lines[pos][i]:
                a, b = lines[pos][i].split('-')
                f = a, b
            else:
                f = lines[pos][i]
            forbidden.append(f)
        pos+=1

        forced = []
        n = len(lines[pos])
        for i in range(n):
            if '-' in lines[pos][i]:
                a, b = lines[pos][i].split('-')
                f = a, b
            else:
                f = lines[pos][i]
            forced.append(f)
        pos+=1
    except:
        assert False, "Incorrect file format on line " + str(pos+1)

    return G, S, T, forbidden, forced


