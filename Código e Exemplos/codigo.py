import sys
import ast
from collections import defaultdict
import networkx as nx

def read_graph(filename):
    with open(filename, 'r') as f:
        n = int(f.readline())
        matrix = []
        for _ in range(n):
            line = f.readline().strip()
            row = ast.literal_eval(line)
            matrix.append(row)
    return n, matrix

def prim_mst(n, graph):
    selected = [False] * n
    selected[0] = True
    mst_edges = []
    total_weight = 0.0

    for _ in range(n - 1):
        min_edge = (None, None, float('inf'))
        for u in range(n):
            if selected[u]:
                for v in range(n):
                    if not selected[v] and graph[u][v] < min_edge[2]:
                        min_edge = (u, v, graph[u][v])
        u, v, w = min_edge
        selected[v] = True
        mst_edges.append((u, v, w))
        total_weight += w
    return mst_edges, total_weight

def odd_degree_vertices(n, mst_edges):
    degree = [0] * n
    for u, v, _ in mst_edges:
        degree[u] += 1
        degree[v] += 1
    return [i for i in range(n) if degree[i] % 2 == 1]

def induced_subgraph(odd_vertices, graph_matrix):
    subgraph = {}
    for u in odd_vertices:
        subgraph[u] = {}
        for v in odd_vertices:
            if u != v:
                subgraph[u][v] = graph_matrix[u][v]
    return subgraph

def min_weight_perfect_matching(subgraph):
    G = nx.Graph()
    for u in subgraph:
        for v in subgraph[u]:
            if u < v:
                G.add_edge(u, v, weight=subgraph[u][v])
    matching = nx.algorithms.matching.min_weight_matching(G)
    return list(matching)

def build_multigraph(n, mst_edges, matching_edges, graph_matrix):
    graph = defaultdict(list)
    for u, v, w in mst_edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    for u, v in matching_edges:
        w = graph_matrix[u][v]
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph

def find_eulerian_tour(graph):
    graph_copy = {u: list(edges) for u, edges in graph.items()}
    circuit = []
    stack = [next(iter(graph_copy))]

    while stack:
        u = stack[-1]
        if graph_copy[u]:
            v, w = graph_copy[u].pop()
            for i, (x, wx) in enumerate(graph_copy[v]):
                if x == u:
                    del graph_copy[v][i]
                    break
            stack.append(v)
        else:
            circuit.append(stack.pop())
    return circuit[::-1]

def shortcutting(eulerian_cycle):
    visited = set()
    path = []
    for v in eulerian_cycle:
        if v not in visited:
            path.append(v)
            visited.add(v)
    path.append(path[0])
    return path

def cycle_cost(cycle, graph_matrix):
    cost = 0.0
    for i in range(len(cycle) - 1):
        cost += graph_matrix[cycle[i]][cycle[i + 1]]
    return cost

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python christofides.py arquivo.txt")
        sys.exit(1)

    filename = sys.argv[1]
    n, graph_matrix = read_graph(filename)

    mst_edges, mst_weight = prim_mst(n, graph_matrix)
    print("\nÁrvore Geradora Mínima:")
    for u, v, w in mst_edges:
        print(f"({u}, {v}, peso={w})")
    print(f"Peso total da MST: {mst_weight:.2f}\n")

    odd_vertices = odd_degree_vertices(n, mst_edges)

    subgraph = induced_subgraph(odd_vertices, graph_matrix)
    matching_edges = min_weight_perfect_matching(subgraph)

    multigraph = build_multigraph(n, mst_edges, matching_edges, graph_matrix)

    eulerian_cycle = find_eulerian_tour(multigraph)
    eulerian_cost = cycle_cost(eulerian_cycle, graph_matrix)
    print(f"Ciclo Euleriano: {eulerian_cycle}")
    print(f"Custo do ciclo Euleriano: {eulerian_cost:.2f}\n")

    hamiltonian_cycle = shortcutting(eulerian_cycle)
    hamiltonian_cost = cycle_cost(hamiltonian_cycle, graph_matrix)

    print("Ciclo Hamiltoniano (solução de Christofides):")
    print(f"[{' -> '.join(map(str, hamiltonian_cycle))}]")
    print(f"Custo total do ciclo Hamiltoniano: {hamiltonian_cost:.2f}")
