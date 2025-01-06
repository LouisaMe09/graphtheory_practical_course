import os
import pickle
import networkx as nx

# Relativer Pfad zur Pickle-Datei
file_path = os.path.join('data', 'ITS_graphs.pkl.gz')

# Lade die ITS-Graphen-Daten
with open(file_path, 'rb') as f:
    data = pickle.load(f)

# Extracting reaction center and plotting using SynUtils
from synutility.SynAAM.misc import get_rc
#from src.rcextract import get_rc
reaction_center = get_rc(data[0]['ITS'])  # Reaktionszentrum extrahieren
vertex_degrees = dict(reaction_center.degree())
print(vertex_degrees)


from synutility.SynVis.graph_visualizer import GraphVisualizer  #auch hier hat n unterstrich gefehlt
import matplotlib.pyplot as plt

# Visualisierung vorbereiten
fig, ax = plt.subplots(2, 1, figsize=(15, 10))
vis = GraphVisualizer()

# ITS-Graph plotten
vis.plot_its(data[0]['ITS'], ax[0], use_edge_color=True)

# Reaktionszentrum plotten
vis.plot_its(reaction_center, ax[1], use_edge_color=True)

# Plot anzeigen
plt.show()

###########################################################################
print(data[0].keys())
# USPTO-Datenbank-ID
print(data[0]['R-id'])  # Gibt die ID des ersten Reaktionsdatensatzes zurück

# Klasse des Reaktionsdatensatzes
print(data[0]['class'])  # Gibt die Klassifikation zurück

# ITS-Graph
print(data[0]['ITS'])  # Zeigt die NetworkX-Darstellung des ITS-Graphen

its_graph = data[0]['ITS']  # Der ITS-Graph des ersten Reaktionsdatensatzes

print(its_graph.nodes(data=True))  # Zeigt alle Knoten und ihre Eigenschaften
