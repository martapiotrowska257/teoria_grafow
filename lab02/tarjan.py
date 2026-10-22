import sys

file = sys.argv[1]
with open(file) as f:
    lines = f.read().splitlines()

type = lines[0].strip()  # 'U' (undirected) lub 'D' (directed)
graph = {}

for line in lines[1:]:
    line = line.replace(":", "")
    parts = line.split()
    if not parts:
        continue
    u = parts[0]    # root
    neighbours = parts[1:]  # roots neighbours
    graph[u] = neighbours

# zmienne globalne potrzebne dla algorytmu Tarjana
disc = {}   # discovery - czas odkrycia
low = {}    # najmniejszy numer disc, do jakiego da się uciec z danego wierzchołka
time = 0

# 1 - graf nieskierowany (przeguby i mosty)
if type == "U":
    cut_vertices = set()
    bridges = []

    def dfs_undirected(v, parent):
        global time
        time += 1
        disc[v] = low[v] = time
        children = 0

        for neighbour in graph[v]:     # każdy z sąsiadów z listy sąsiadów wierzchołka v
            if neighbour not in disc:  # sasiad nie był odwiedzony (krawędź drzewa dfs)
                u = neighbour
                children += 1
                dfs_undirected(u, v)
                low[v] = min(low[v], low[u])

                # warunek na przegub (gdy v nie jest korzeniem)
                if parent is not None and low[u] >= disc[v]:
                    cut_vertices.add(v)

                # warunek na most
                if low[u] > disc[v]:
                    bridges.append((v, u))

            elif neighbour != parent:  # sasiad był odwiedzony i nie jest rodzicem (krawędź wsteczna)
                w = neighbour
                low[v] = min(low[v], disc[w])

        # osobny warunek na przegub dla korzenia
        if parent is None and children >= 2:
            cut_vertices.add(v)

    # pętla po wszystkich wierzchołkach (gdyby graf był niespójny)
    for vertex in graph:
        if vertex not in disc:
            dfs_undirected(vertex, None)

    print("disc:", disc)
    print("low: ", low)
    print("cut_vertices:", list(cut_vertices))
    print("bridges:   ", bridges)

# 2 - graf skierowany (składowe silnej spójności - SCC)
elif type == "D":
    stack = []
    scc_list = []

    def dfs_directed(v):
        global time
        time += 1
        disc[v] = low[v] = time
        stack.append(v)

        for neighbour in graph[v]:
            if neighbour not in disc:  # sasiad nie był odwiedzony
                u = neighbour
                dfs_directed(u)
                low[v] = min(low[v], low[u])
            elif neighbour in stack:  # sasiad był odwiedzony i NADAL jest na stosie
                w = neighbour
                low[v] = min(low[v], disc[w])

        # jeśli v jest korzeniem składowej SCC, zdejmujemy ze stosu
        if low[v] == disc[v]:
            component = []
            while True:
                element = stack.pop()
                component.append(element)
                if element == v:
                    break
            scc_list.append(component)

    # pętla po wszystkich wierzchołkach (gdyby graph był niespójny)
    for vertex in graph:
        if vertex not in disc:
            dfs_directed(vertex)

    print("disc:", disc)
    print("low: ", low)
    print("Składowe silnej spójności (SCC):", scc_list)