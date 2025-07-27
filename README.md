# 🚚 Trabalho Final - Grafos: Aproximação para o TSP

Este projeto implementa uma **solução heurística para o Problema do Caixeiro Viajante (TSP)** usando a técnica de aproximação de **Christofides**, que garante uma solução com custo no máximo 1.5 vezes o ótimo para grafos métricos.

A implementação é realizada em Python, com leitura de grafos em formato de matriz de adjacência e aplicação de algoritmos clássicos de Teoria dos Grafos.

---

## 🧠 Algoritmos Utilizados

O projeto segue os seguintes passos:

1. **Leitura da matriz de adjacência** de um grafo não direcionado com pesos.
2. **Construção da Árvore Geradora Mínima (MST)** utilizando o algoritmo de Prim.
3. **Identificação dos vértices de grau ímpar** na MST.
4. **Criação de um subgrafo induzido** com os vértices ímpares.
5. **Emparelhamento perfeito de peso mínimo** com NetworkX.
6. **Combinação da MST com o emparelhamento** para formar um **multigrafo euleriano**.
7. **Geração de um circuito euleriano**.
8. **Atalhamento do circuito** para obter um caminho hamiltoniano (solução aproximada do TSP).

---

## 📁 Estrutura da Pasta

```
📂 Grafos - Trabalho Final/
├── 📂 Documentação/
│   └── Relatório.pdf           # Tudo referente ao trabalho
|
├── 📂 Código e Exemplos/
│   ├── grafo_29v.txt           # Matriz de adjacência para grafo com 29 vértices
│   ├── saida_grafo_29v.txt     # Saída correspondente para o grafo de 29 vértices
│   ├── grafo_175v.txt          # Matriz de adjacência para grafo com 175 vértices
│   ├── saida_grafo_175v.txt    # Saída correspondente para o grafo de 175 vértices
│   └── codigo.py               # Implementação do algoritmo de Christofides
```

---

## ▶️ Como Executar

### 1. Instale o Python (recomendado: 3.8+)

### 2. Instale a dependência

Este projeto utiliza a biblioteca `networkx`:

```bash
pip install networkx
```

### 3. Execute o código

Entre na pasta `Código e Exemplos` e execute:

```bash
python codigo.py [caminho/nome_arquivo_do_grafo].txt
```

Por padrão, o script lê um dos arquivos `grafo_29v.txt` ou `grafo_175v.txt`, que devem conter:

- A primeira linha: número de vértices `n`
- As `n` linhas seguintes: listas de `n` números (pesos), representando a matriz de adjacência

---

## 🧪 Funções Principais do Código

- `read_graph(filename)`: lê a matriz de adjacência de um arquivo `.txt`
- `prim_mst(n, graph)`: gera a árvore geradora mínima
- `odd_degree_vertices(n, mst_edges)`: encontra vértices de grau ímpar
- `induced_subgraph(odd_vertices, graph_matrix)`: cria subgrafo induzido
- `min_weight_perfect_matching(subgraph)`: emparelhamento com menor custo usando NetworkX
- `build_multigraph(...)`: monta o grafo euleriano
- `find_eulerian_tour(graph)`: encontra tour de Euler
- `shortcut_eulerian_tour(tour)`: converte para caminho Hamiltoniano (solução TSP)

---

## 📦 Dependências

- Python 3.8+
- [`networkx`](https://networkx.org/) (para emparelhamento perfeito)

---

## 📝 Notas

- O grafo de entrada deve ser **simétrico e completo**, com `graph[i][j] == graph[j][i]`, e não deve haver laços (`graph[i][i] = 0`).
- O algoritmo de Christofides não garante o caminho ótimo, mas fornece uma **aproximação eficiente** para instâncias grandes do TSP.
