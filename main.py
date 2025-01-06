import networkx as nx

# Criar um grafo
grafo = nx.Graph()

# Adicionar cidades (nós)
grafo.add_node("Patrocínio")
grafo.add_node("Araxá")
grafo.add_node("Uberaba")

# Adicionar conexões (arestas) com pesos
grafo.add_edge("Patrocínio", "Araxá", distancia=100, custo=50, tempo=1.5)
grafo.add_edge("Araxá", "Uberaba", distancia=150, custo=75, tempo=2.0)
grafo.add_edge("Patrocínio", "Uberaba", distancia=200, custo=100, tempo=3.0)

# Exibir informações
print(grafo.edges(data=True))
