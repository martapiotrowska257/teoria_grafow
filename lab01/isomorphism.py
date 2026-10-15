from pynauty import Graph, isomorphic, canon_label

# DANE: dla każdego podpunktu (n, krawędzie G, krawędzie H)
CASES = {
    "a": (6,
          [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)],
          [(0, 3), (0, 4), (1, 4), (1, 5), (2, 5), (2, 3), (1, 3)]),
    "b": (4,
          [(0, 1), (1, 2), (2, 3)],            # ścieżka
          [(0, 1), (0, 2), (0, 3)]),           # gwiazda
    "c": (6,
          [(0, 1), (0, 2), (0, 3), (1, 4), (2, 5)],
          [(0, 1), (0, 2), (0, 3), (1, 4), (4, 5)]),
}


def isomorphism(case):
    n, edges_G, edges_H = CASES[case]
    print("=== podpunkt", case, "===")

    # zamiana listy krawędzi na słownik sąsiedztwa - format grafu przyjmowany przez pynauty
    adj_G = {v: [] for v in range(n)}
    for u, v in edges_G:
        adj_G[u].append(v)
    print(adj_G)

    adj_H = {v: [] for v in range(n)}
    for u, v in edges_H:
        adj_H[u].append(v)
    print(adj_H)

    # zbudowanie grafów w pynauty
    G = Graph(n, directed=False, adjacency_dict=adj_G)
    H = Graph(n, directed=False, adjacency_dict=adj_H)

    # sekwencje stopni
    deg_G = [sum(v in e for e in edges_G) for v in range(n)]
    deg_H = [sum(v in e for e in edges_H) for v in range(n)]
    print("stopnie G:", sorted(deg_G, reverse=True))
    print("stopnie H:", sorted(deg_H, reverse=True))

    # sprawdzenie izomorfizmu
    result = isomorphic(G, H)
    print("Czy grafy G i H są izomorficzne?", result)

    if not result:
        print("Brak izomorfizmu.")
        return
    print("Sprawdzamy, który wierzchołek G odpowiada któremu wierzchołkowi H.")

    # szukanie izomorfizmu f (kanonizacja grafów za pomocą funkcj canon_label z pynauty)
    lab_G = canon_label(G)
    lab_H = canon_label(H)
    print("canon_label G:", lab_G)
    print("canon_label H:", lab_H)

    f = {}
    for i in range(n):
        f[lab_G[i]] = lab_H[i]
    print("Izomorfizm f:", dict(sorted(f.items())))

    # sprawdzenie resultu
    edges_H_set = {tuple(sorted(e)) for e in edges_H}
    ok = True
    for u, v in edges_G:
        representation = tuple(sorted((f[u], f[v])))
        print(f"krawędź ({u},{v}) w G -> {representation} w H, czy istnieje w H:", representation in edges_H_set)
        if obraz not in edges_H_set:
            ok = False
    print("Wszystkie krawędzie się zgadzają:", ok)


isomorphism("c")