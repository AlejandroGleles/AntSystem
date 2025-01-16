# Otimização de Rotas - Alto Paranaíba

Este projeto visa otimizar rotas entre municípios do Alto Paranaíba, em Minas Gerais, utilizando o **Algoritmo de Colônia de Formigas (ACO)**. O sistema calcula rotas de transporte entre cidades, levando em consideração fatores como distância, custo de combustível, tempo estimado e a presença de pedágios.

## Funcionalidades

- **Criação de Grafo**: Representação dos municípios e suas conexões como um grafo, onde os nós são as cidades e as arestas representam as rotas entre elas.
- **Verificação de Pedágios**: O sistema verifica se a rota entre duas cidades possui pedágios.
- **Otimização de Rotas**: Uso do Algoritmo de Colônia de Formigas (ACO) para otimizar rotas com base no custo total (distância e pedágio).
- **Visualização de Mapas**: Geração de mapas interativos com as cidades e rotas otimizadas usando o **Folium**.
- **Interface Gráfica**: Interface simples com **Tkinter** para visualização e interação com o sistema.

## Requisitos

- **Python 3.x**
- Bibliotecas necessárias:
  - `networkx`
  - `googlemaps`
  - `geopy`
  - `folium`
  - `tkinter`
  - `matplotlib`
  
Instale as dependências com o seguinte comando:

pip install networkx googlemaps geopy folium matplotlib
Como Usar
1. Rodando o Script
Execute o script para gerar a otimização das rotas e visualizar os mapas.

Copiar
Editar
python otimizar_rotas.py 2. Interface Gráfica
A interface gráfica gerada pelo Tkinter permite ao usuário:

Visualizar o mapa inicial com todas as conexões entre as cidades.
Selecionar se deseja evitar pedágios.
Rodar a otimização das rotas usando o algoritmo de colônia de formigas.
Visualizar o resultado da otimização com as melhores rotas, incluindo custos.
3. Visualização dos Mapas
O mapa inicial com todas as conexões entre as cidades será salvo como grafo_alto_paranaiba_inicial.html.
O mapa otimizado, mostrando as melhores rotas, será salvo como grafo_alto_paranaiba_otimizado.html.
Abra os arquivos .html em um navegador para visualizar os mapas interativos.

Algoritmo de Colônia de Formigas (ACO)
O ACO é utilizado para encontrar as melhores rotas entre os municípios, levando em consideração o custo (distância + pedágio) e o tempo estimado de viagem. O algoritmo simula o comportamento de formigas para explorar diferentes rotas e depositar feromônios nas melhores, otimizando o processo ao longo das iterações.

Estrutura do Código
Funções Principais:

criar_grafo(): Cria o grafo com as cidades e suas rotas.
verifica_pedagio(): Verifica se a rota entre duas cidades possui pedágio.
otimizar_aco(): Implementa o Algoritmo de Colônia de Formigas para otimização das rotas.
criar_mapa_inicial(): Cria o mapa com as conexões do grafo.
Interface: Classe responsável pela interface gráfica.
Módulos Externos Utilizados:

Google Maps API: Para calcular rotas e verificar pedágios entre cidades.
NetworkX: Para criar e manipular o grafo.
Geopy: Para calcular distâncias geográficas entre as cidades.
Folium: Para gerar mapas interativos.
Tkinter: Para criar a interface gráfica.
Repositório
Você pode acessar o código fonte completo do projeto no GitHub:

https://github.com/AlejandroGleles/AntSystem.git

Vídeo de Demonstração
Assista a uma demonstração do funcionamento do sistema no YouTube:

https://youtu.be/H2J9vSUL_ew
