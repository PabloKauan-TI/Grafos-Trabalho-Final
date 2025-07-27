import sys
import ast
from collections import defaultdict
import networkx as nx

def read_graph(filename):
    """
    Lê um grafo a partir de um arquivo de texto no formato de matriz de adjacência.

    A primeira linha do arquivo deve conter o número de vértices (N),
    seguida por N linhas, cada uma representando uma linha da matriz.

    Args:
        filename (str): O caminho para o arquivo .txt contendo o grafo.

    Returns:
        tuple: Uma tupla contendo o número de vértices (int) e a matriz
               de adjacência (list of lists of float).
    """
    with open(filename, 'r') as f:
        # Lê a primeira linha para obter o número de vértices
        n = int(f.readline())
        matrix = []
        # Itera sobre as N linhas restantes para construir a matriz
        for _ in range(n):
            line = f.readline().strip()
            # Usa ast.literal_eval para converter a string da linha (ex: "[0.0, 1.0]") em uma lista Python
            row = ast.literal_eval(line)
            matrix.append(row)
    return n, matrix

def prim_mst(n, graph):
    """
    Encontra a Árvore Geradora Mínima (MST) de um grafo usando o algoritmo de Prim.

    Esta é uma implementação simples com complexidade O(N^2), adequada para grafos densos.

    Args:
        n (int): O número de vértices no grafo.
        graph (list of lists): A matriz de adjacência do grafo.

    Returns:
        tuple: Uma tupla contendo a lista de arestas da MST e o peso total da MST.
               Cada aresta é uma tupla (u, v, peso).
    """
    # 'selected' rastreia os vértices já incluídos na MST
    selected = [False] * n
    # Começa a MST a partir do primeiro vértice (vértice 0)
    selected[0] = True
    mst_edges = []
    total_weight = 0.0

    # A MST terá N-1 arestas
    for _ in range(n - 1):
        min_edge = (None, None, float('inf')) # Guarda a aresta de menor peso encontrada (u, v, peso)
        
        # Itera sobre todos os vértices para encontrar a aresta de menor peso
        # que conecta um vértice da MST a um vértice fora da MST
        for u in range(n):
            if selected[u]: # Se 'u' já está na MST
                for v in range(n):
                    # Se 'v' não está na MST e a aresta (u, v) tem peso menor que o mínimo atual
                    if not selected[v] and graph[u][v] < min_edge[2]:
                        min_edge = (u, v, graph[u][v])
        
        u, v, w = min_edge
        selected[v] = True  # Adiciona o novo vértice 'v' à MST
        mst_edges.append((u, v, w))
        total_weight += w
        
    return mst_edges, total_weight

def odd_degree_vertices(n, mst_edges):
    """
    Identifica os vértices de grau ímpar em uma árvore (neste caso, a MST).

    Args:
        n (int): O número de vértices.
        mst_edges (list of tuples): A lista de arestas da MST.

    Returns:
        list: Uma lista com os índices dos vértices que possuem grau ímpar.
    """
    degree = [0] * n
    # Calcula o grau de cada vértice
    for u, v, _ in mst_edges:
        degree[u] += 1
        degree[v] += 1
    
    # Retorna uma lista contendo apenas os vértices com grau ímpar
    return [i for i in range(n) if degree[i] % 2 == 1]

def induced_subgraph(odd_vertices, graph_matrix):
    """
    Cria um subgrafo induzido contendo apenas os vértices de grau ímpar.
    
    Este subgrafo será usado para encontrar o emparelhamento perfeito de custo mínimo.

    Args:
        odd_vertices (list): A lista de vértices de grau ímpar.
        graph_matrix (list of lists): A matriz de adjacência do grafo original completo.

    Returns:
        dict: Um dicionário representando o subgrafo, onde as chaves são os vértices
              e os valores são dicionários com os vizinhos e pesos das arestas.
    """
    subgraph = {}
    for u in odd_vertices:
        subgraph[u] = {}
        for v in odd_vertices:
            if u != v:
                subgraph[u][v] = graph_matrix[u][v]
    return subgraph

def min_weight_perfect_matching(subgraph):
    """
    Encontra o emparelhamento perfeito de custo mínimo (MWPM) em um subgrafo.

    Utiliza a biblioteca NetworkX, que possui uma implementação eficiente para este problema.

    Args:
        subgraph (dict): O subgrafo induzido pelos vértices de grau ímpar.

    Returns:
        list of tuples: Uma lista de arestas (u, v) que compõem o emparelhamento.
    """
    # Cria um objeto de grafo do NetworkX a partir do subgrafo
    G = nx.Graph()
    for u in subgraph:
        for v in subgraph[u]:
            if u < v: # Adiciona cada aresta apenas uma vez
                G.add_edge(u, v, weight=subgraph[u][v])
    
    # Executa o algoritmo de emparelhamento de custo mínimo do NetworkX
    matching = nx.algorithms.matching.min_weight_matching(G)
    
    return list(matching)

def build_multigraph(n, mst_edges, matching_edges, graph_matrix):
    """
    Cria um multigrafo Euleriano unindo as arestas da MST e do emparelhamento.

    O grafo resultante terá todos os vértices com grau par.

    Args:
        n (int): Número de vértices.
        mst_edges (list of tuples): Arestas da MST.
        matching_edges (list of tuples): Arestas do emparelhamento.
        graph_matrix (list of lists): Matriz de adjacência original.

    Returns:
        defaultdict: Um dicionário representando o multigrafo.
    """
    graph = defaultdict(list)
    # Adiciona arestas da MST ao multigrafo
    for u, v, w in mst_edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
        
    # Adiciona arestas do emparelhamento ao multigrafo
    for u, v in matching_edges:
        w = graph_matrix[u][v]
        graph[u].append((v, w))
        graph[v].append((u, w))
        
    return graph

def find_eulerian_tour(graph):
    """
    Encontra um ciclo Euleriano no multigrafo usando o algoritmo de Hierholzer.

    Args:
        graph (defaultdict): O multigrafo onde todos os vértices têm grau par.

    Returns:
        list: Uma lista de vértices que formam o ciclo Euleriano.
    """
    # Faz uma cópia do grafo para poder remover arestas durante o percurso
    graph_copy = {u: list(edges) for u, edges in graph.items()}
    circuit = []
    stack = [next(iter(graph_copy))] # Começa a partir de um vértice qualquer

    while stack:
        u = stack[-1]
        # Se o vértice atual ainda tem arestas não visitadas
        if graph_copy[u]:
            v, w = graph_copy[u].pop()
            
            # Remove a aresta oposta (v, u) para não percorrê-la no sentido contrário
            for i, (x, wx) in enumerate(graph_copy[v]):
                if x == u:
                    del graph_copy[v][i]
                    break
            stack.append(v)
        else:
            # Se o vértice não tem mais arestas, adiciona-o ao circuito
            circuit.append(stack.pop())
            
    # O circuito é construído de trás para frente, então é preciso invertê-lo
    return circuit[::-1]

def shortcutting(eulerian_cycle):
    """
    Converte um ciclo Euleriano em um ciclo Hamiltoniano removendo vértices repetidos.

    Args:
        eulerian_cycle (list): O ciclo Euleriano.

    Returns:
        list: O ciclo Hamiltoniano resultante.
    """
    visited = set()
    path = []
    for v in eulerian_cycle:
        if v not in visited:
            path.append(v)
            visited.add(v)
    
    # Adiciona o primeiro vértice ao final para fechar o ciclo
    path.append(path[0])
    return path

def cycle_cost(cycle, graph_matrix):
    """
    Calcula o custo total de um ciclo (Euleriano ou Hamiltoniano).

    Args:
        cycle (list): A lista de vértices no ciclo.
        graph_matrix (list of lists): A matriz de adjacência do grafo original.

    Returns:
        float: O custo total do ciclo.
    """
    cost = 0.0
    # Soma os pesos das arestas consecutivas no ciclo
    for i in range(len(cycle) - 1):
        cost += graph_matrix[cycle[i]][cycle[i + 1]]
    return cost

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    # Verifica se o nome do arquivo foi passado como argumento na linha de comando
    if len(sys.argv) != 2:
        print("Uso: python christofides.py arquivo.txt")
        sys.exit(1)

    filename = sys.argv[1]
    
    # Passo 1: Ler o grafo do arquivo
    n, graph_matrix = read_graph(filename)

    # Passo 2: Calcular a Árvore Geradora Mínima (MST)
    mst_edges, mst_weight = prim_mst(n, graph_matrix)
    print("\nÁrvore Geradora Mínima (MST) encontrada.")
    # for u, v, w in mst_edges:
    #     print(f"({u}, {v}, peso={w})")
    print(f"Peso total da MST: {mst_weight:.2f}\n")

    # Passo 3: Identificar vértices de grau ímpar na MST
    odd_vertices = odd_degree_vertices(n, mst_edges)

    # Passo 4: Encontrar o emparelhamento perfeito de custo mínimo (MWPM)
    subgraph = induced_subgraph(odd_vertices, graph_matrix)
    matching_edges = min_weight_perfect_matching(subgraph)

    # Passo 5: Construir o multigrafo Euleriano
    multigraph = build_multigraph(n, mst_edges, matching_edges, graph_matrix)

    # Passo 6: Encontrar o ciclo Euleriano
    eulerian_cycle = find_eulerian_tour(multigraph)
    # OBS: O cálculo de custo aqui pode ser impreciso se a função cycle_cost for usada,
    # pois ela não considera as arestas duplicadas do multigrafo.
    # O custo correto seria a soma do peso da MST com o peso do emparelhamento.
    print(f"Ciclo Euleriano encontrado com {len(eulerian_cycle)} vértices (incluindo repetições).\n")


    # Passo 7: Aplicar o "shortcutting" para obter o ciclo Hamiltoniano
    hamiltonian_cycle = shortcutting(eulerian_cycle)
    
    # Passo 8: Calcular o custo do ciclo Hamiltoniano final
    hamiltonian_cost = cycle_cost(hamiltonian_cycle, graph_matrix)

    print("--- Solução Aproximada (Christofides) ---")
    print("Ciclo Hamiltoniano:")
    # Formata a saída para ser mais legível, ex: "[0 -> 1 -> 2 -> 0]"
    print(f"[{' -> '.join(map(str, hamiltonian_cycle))}]")
    print(f"\nCusto total do ciclo Hamiltoniano: {hamiltonian_cost:.2f}")