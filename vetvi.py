import numpy as np
import networkx as nx
import math


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
    # print(coords)
    for i in range(len(ids)):
        # расстояние будем искать для всех последующих вершин
        for j in range(i + 1, len(ids)):
            G.add_edge(ids[i], ids[j], weight=distance(coords[ids[i]], coords[ids[j]]))
    return G


def printMatrix(matrix, prevText):
    print()
    print("#############")
    print(f"{prevText}:")
    for i in matrix:
        for j in i:
            print("{:<5}".format(j), end=" ")
        print()
    print("#############")
    print()

def mainPart(G):

    # create a matrix
    matrixLen = len(G.nodes)
    matrix = np.ones(matrixLen**2).reshape(matrixLen, matrixLen)
    for i in G.nodes:
        for j in G.nodes:
            if i == j:
                matrix[i-1][j-1] = math.inf
            else:
                matrix[i-1][j-1] = G[i][j]['weight']

    # Test log created matrix
    printMatrix(matrix, "StartMatrix")

    # find minimum element in each string
    minStringElements = [min(i) for i in matrix]

    # Test log finded element
    print("minStringElement = ", minStringElements)

    # subtraction min element from each element in string
    for i in range(len(matrix)):
        for n in range(len(matrix[i])):
            matrix[i][n] -= minStringElements[i]

    # Test log matrix
    printMatrix(matrix, "Matrix After Sub String")

    # Find minimum element in each colone
    minColomnElements = [min(matrix[:, i]) for i in range(len(matrix))]
    print(minColomnElements)

    # subtraction min element from each element in colomn
    for i in range(len(matrix)):
        for n in range(len(matrix[i])):
            matrix[n][i] -= minColomnElements[i]

    # Test log matrix
    printMatrix(matrix, "Matrix After Sub Colon")

    # Estimate each null
    maxNullElement = {"value": -1, "string": 0, "column": 0}
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                minElementInString = np.concatenate((matrix[i, :j], matrix[i, j+1:])).min()
                minElementInColomn = np.concatenate((matrix[:i, j], matrix[i+1:, j])).min()
                value = minElementInColomn + minElementInString
                print("value", value)
                if value > maxNullElement["value"]:
                    maxNullElement["value"] = value
                    maxNullElement["string"] = i
                    maxNullElement["column"] = j

    print("maxNullElement: ", maxNullElement)

    # Eraser colomn and string from maxNullElement
    matrix = np.concatenate((matrix[:maxNullElement["string"]], matrix[maxNullElement["string"]+1:]))
    matrix =



if __name__ == '__main__':
    print(f"start algorithm of BAE!")
    G = ReadPointGraph("graph/test.tsp.txt")
    # print(G.edges)

    mainPart(G)

