import os
import pickle
import networkx as nx
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--graphs", help="Specifies the graphs to be used.", required=True)
args = parser.parse_args()

graph_path = args.graphs

<<<<<<< HEAD
# Relativer Pfad zur Pickle-Datei
file_path = os.path.join('data', 'ITS_graphs.pkl.gz')

# Lade die ITS-Graphen-Daten
with open(file_path, 'rb') as f:
    data = pickle.load(f)

=======
# Lade die ITS-Graphen-Daten aus der Pickle-Datei
with open(graph_path, 'rb') as f:  # Absoluter Pfad zu deiner Datei
    data = pickle.load(f)

# Using SynUtils
from synutility.SynIO.data_type import load_from_pickle #hier data_type statt datatype


# ITS-Graphen-Daten mit SynUtils laden
data = load_from_pickle(graph_path)  # Absoluter Pfad

>>>>>>> 5c09f676bd873b367d042b69803209fa3421a843
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
