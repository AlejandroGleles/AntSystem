import random
import networkx as nx
import googlemaps
from geopy.distance import geodesic
import folium
import webbrowser
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Definir os municípios do Alto Paranaíba e suas coordenadas (latitude e longitude)
municipios = {
    "Araxá, Minas Gerais, Brazil": {"latitude": -19.5934, "longitude": -46.9387},
    "Patrocínio, Minas Gerais, Brazil": {"latitude": -18.9386, "longitude": -46.5195},
    "Uberaba, Minas Gerais, Brazil": {"latitude": -19.7477, "longitude": -47.9305},
    "Uberlândia, Minas Gerais, Brazil": {"latitude": -18.9183, "longitude": -48.2751},
    "Ituiutaba, Minas Gerais, Brazil": {"latitude": -18.9734, "longitude": -49.4666},
    "Monte Carmelo, Minas Gerais, Brazil": {"latitude": -18.2432, "longitude": -46.9561},
    "Paracatu, Minas Gerais, Brazil": {"latitude": -17.2397, "longitude": -46.8694},
    "Coromandel, Minas Gerais, Brazil": {"latitude": -18.3719, "longitude": -47.3972},
    "Santa Vitória, Minas Gerais, Brazil": {"latitude": -19.1746, "longitude": -49.1528},
    "Estrela do Sul, Minas Gerais, Brazil": {"latitude": -19.0291, "longitude": -46.9092},
    "Perdizes, Minas Gerais, Brazil": {"latitude": -19.2628, "longitude": -47.2197},
    "Santa Juliana, Minas Gerais, Brazil": {"latitude": -19.3466, "longitude": -46.9194},
    "Pratinha, Minas Gerais, Brazil": {"latitude": -19.6432, "longitude": -46.8823}
}

# Definir a chave da API do Google Maps
gmaps = googlemaps.Client(key='AIzaSyCm2MrvTLqNAwsS9KDXhaISnUjO75iuReM')

# Funções auxiliares
def verifica_pedagio(origem, destino):
    """Verificar se a rota entre as cidades possui pedágios."""
    try:
        routes = gmaps.directions(origem, destino, mode="driving", alternatives=False)
        for route in routes:
            for leg in route['legs']:
                for step in leg['steps']:
                    if 'toll' in step and step['toll']:
                        return True
    except Exception as e:
        print(f"Erro ao verificar pedágio entre {origem} e {destino}: {e}")
    return False

def criar_grafo():
    """Cria o grafo com as cidades e suas rotas."""
    G = nx.Graph()

    # Adicionar nós (cidades) ao grafo
    for municipio, coords in municipios.items():
        G.add_node(municipio, latitude=coords["latitude"], longitude=coords["longitude"])

    # Adicionar arestas entre as cidades
    for cidade1, coords1 in municipios.items():
        for cidade2, coords2 in municipios.items():
            if cidade1 != cidade2 and not G.has_edge(cidade1, cidade2):
                distancia = geodesic((coords1["latitude"], coords1["longitude"]), (coords2["latitude"], coords2["longitude"])).km
                possui_pedagio = verifica_pedagio(cidade1, cidade2)
                custo_combustivel = distancia * 0.5
                tempo_estimado = distancia / 80
                custo_total = custo_combustivel + (20 if possui_pedagio else 0)
                G.add_edge(cidade1, cidade2, weight=distancia, custo=custo_total, tempo=tempo_estimado, pedagio=possui_pedagio)

    # Garantir conectividade do grafo
    if not nx.is_connected(G):
        conectar_cidades_desconectadas(G)

    return G, municipios

def conectar_cidades_desconectadas(G):
    """Conecta componentes desconectados do grafo com arestas artificiais."""
    componentes = list(nx.connected_components(G))
    while len(componentes) > 1:
        comp1, comp2 = componentes[0], componentes[1]
        cidade1 = random.choice(list(comp1))
        cidade2 = random.choice(list(comp2))
        distancia = geodesic(
            (G.nodes[cidade1]['latitude'], G.nodes[cidade1]['longitude']),
            (G.nodes[cidade2]['latitude'], G.nodes[cidade2]['longitude'])
        ).km
        custo_combustivel = distancia * 0.5
        tempo_estimado = distancia / 80
        custo_total = custo_combustivel + 50  # Custo extra para penalizar conexões artificiais
        G.add_edge(cidade1, cidade2, weight=distancia, custo=custo_total, tempo=tempo_estimado, pedagio=False)
        componentes = list(nx.connected_components(G))

def escolher_3_melhores_rotas(rotas, custos):
    """Selecionar as 3 melhores rotas com base no custo total."""
    rotas_com_custos = sorted(zip(rotas, custos), key=lambda x: x[1])
    return rotas_com_custos[:3]

# Algoritmo de Colônia de Formigas
def otimizar_aco(grafo, evitar_pedagio=False):
    """Algoritmo de Colônia de Formigas (ACO) para otimização de rotas."""
    num_ants = 10
    num_iterations = 100
    evaporation_rate = 0.5
    pheromone_deposit = 1

    best_routes = []
    best_costs = []

    for iteration in range(num_iterations):
        all_routes = []
        all_costs = []

        for _ in range(num_ants):
            route = []
            current_city = random.choice(list(grafo.nodes))
            route.append(current_city)
            cost = 0

            while len(route) < len(grafo.nodes):
                next_city = escolher_proxima_cidade(grafo, current_city, route, evitar_pedagio)

                if next_city is None:
                    break

                route.append(next_city)
                cost += grafo[current_city][next_city]['custo']
                current_city = next_city

            if len(route) == len(grafo.nodes):
                route.append(route[0])  # Voltar para a cidade inicial
                cost += grafo[route[-2]][route[-1]]['custo']
                all_routes.append(route)
                all_costs.append(cost)

        evaporar_feromonio(grafo, evaporation_rate)
        depositar_feromônio(grafo, all_routes, pheromone_deposit)

        if all_routes:
            best_routes.extend(all_routes)
            best_costs.extend(all_costs)

    return escolher_3_melhores_rotas(best_routes, best_costs)

def escolher_proxima_cidade(grafo, current_city, visited, evitar_pedagio):
    neighbors = [city for city in grafo.neighbors(current_city) if city not in visited]

    if not neighbors:
        return None

    pheromone_values = []
    for neighbor in neighbors:
        pheromone = grafo[current_city][neighbor].get('weight', 1)
        if evitar_pedagio and grafo[current_city][neighbor].get('pedagio', False):
            pheromone = 0

        pheromone_values.append(pheromone)

    total_pheromone = sum(pheromone_values)
    if total_pheromone == 0:
        return random.choice(neighbors)

    probabilities = [pheromone / total_pheromone for pheromone in pheromone_values]
    return random.choices(neighbors, probabilities)[0]

def evaporar_feromonio(grafo, evaporation_rate):
    for u, v, data in grafo.edges(data=True):
        data['weight'] *= (1 - evaporation_rate)

def depositar_feromônio(grafo, all_routes, pheromone_deposit):
    for route in all_routes:
        for i in range(len(route) - 1):
            grafo[route[i]][route[i+1]]['weight'] += pheromone_deposit


def criar_mapa_inicial(grafo, municipios, arquivo_mapa):
    """Cria um mapa inicial mostrando todas as conexões do grafo."""
    mapa = folium.Map(location=[-19.0, -47.5], zoom_start=8)

    # Adicionar marcadores para as cidades
    for node in grafo.nodes:
        folium.Marker(
            location=[municipios[node]["latitude"], municipios[node]["longitude"]],
            popup=node,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mapa)

    # Adicionar conexões do grafo
    for u, v in grafo.edges:
        coords_u = municipios[u]
        coords_v = municipios[v]
        folium.PolyLine(
            locations=[(coords_u["latitude"], coords_u["longitude"]), (coords_v["latitude"], coords_v["longitude"])],
            color='blue', weight=2, opacity=0.5
        ).add_to(mapa)

    # Salvar o mapa inicial
    mapa.save(arquivo_mapa)


class Interface:
    def __init__(self, root, grafo, municipios):
        self.root = root
        self.grafo = grafo
        self.municipios = municipios
        self.root.title("Otimização de Rotas - Alto Paranaíba")
        self.root.geometry("800x600")
        self.mapa_inicial_path = "grafo_alto_paranaiba_inicial.html"
        self.mapa_otimizado_path = "grafo_alto_paranaiba_otimizado.html"

        # Criar o mapa inicial
        criar_mapa_inicial(self.grafo, self.municipios, self.mapa_inicial_path)

        self.frame_mapa = tk.Frame(self.root)
        self.frame_mapa.pack(pady=20)
        self.btn_visualizar_mapa_inicial = tk.Button(self.frame_mapa, text="Visualizar Mapa Inicial", command=self.visualizar_mapa_inicial)
        self.btn_visualizar_mapa_inicial.pack(pady=10)

        self.frame_configuracao = tk.Frame(self.root)
        self.frame_configuracao.pack(pady=20)

        self.var_pedagio = tk.BooleanVar()
        self.chk_pedagio = tk.Checkbutton(self.frame_configuracao, text="Evitar Pedágios", variable=self.var_pedagio)
        self.chk_pedagio.grid(row=0, column=0, padx=10, pady=10)

        self.btn_otimizar = tk.Button(self.frame_configuracao, text="Rodar Otimização de Rota", command=self.otimizar_rota)
        self.btn_otimizar.grid(row=1, column=0, padx=10, pady=10)

        self.label_resultado = tk.Label(self.root, text="Resultado da Otimização: Nenhuma rota otimizada ainda.", wraplength=600)
        self.label_resultado.pack(pady=20)

    def visualizar_mapa_inicial(self):
        if os.path.exists(self.mapa_inicial_path):
            webbrowser.open(self.mapa_inicial_path)
        else:
            messagebox.showerror("Erro", "Mapa inicial não encontrado!")

    def otimizar_rota(self):
        if not nx.is_connected(self.grafo):
            messagebox.showerror("Erro", "O grafo não está completamente conectado. Verifique as conexões.")
            return

        evitar_pedagio = self.var_pedagio.get()
        melhores_rotas = otimizar_aco(self.grafo, evitar_pedagio)
        resultado_texto = "\n".join([f"Rota: {rota} - Custo: {custo:.2f} R$" for rota, custo in melhores_rotas])
        self.label_resultado.config(text=f"Resultado da Otimização:\n{resultado_texto}")
        self.desenhar_rotas_no_mapa(melhores_rotas)

    def desenhar_rotas_no_mapa(self, melhores_rotas):
        """Desenha as rotas otimizadas no mapa."""
        mapa = folium.Map(location=[-19.0, -47.5], zoom_start=8)

        for node in self.grafo.nodes:
            folium.Marker(
                location=[self.municipios[node]["latitude"], self.municipios[node]["longitude"]],
                popup=node,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)

        cores = ['red', 'green', 'blue']
        for (rota, custo), cor in zip(melhores_rotas, cores):
            layer = folium.FeatureGroup(name=f"Rota ({cor.capitalize()}) - Custo: R${custo:.2f}")
            for i in range(len(rota) - 1):
                cidade1 = rota[i]
                cidade2 = rota[i + 1]
                coords1 = self.municipios[cidade1]
                coords2 = self.municipios[cidade2]
                folium.PolyLine(
                    locations=[(coords1["latitude"], coords1["longitude"]), (coords2["latitude"], coords2["longitude"])],
                    color=cor, weight=4, opacity=1
                ).add_to(layer)
            mapa.add_child(layer)

        folium.LayerControl().add_to(mapa)
        mapa.save(self.mapa_otimizado_path)
        webbrowser.open(self.mapa_otimizado_path)


def main():
    G, municipios = criar_grafo()
    root = tk.Tk()
    interface = Interface(root, G, municipios)
    root.mainloop()


if __name__ == "__main__":
    main()
