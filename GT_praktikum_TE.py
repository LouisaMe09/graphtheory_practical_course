# Using only pickle
import pickle
import networkx as nx

# Lade die ITS-Graphen-Daten aus der Pickle-Datei
with open(r"C:\Users\Louisa\Downloads\ITS_graphs.pkl.gz", 'rb') as f:  # Absoluter Pfad zu deiner Datei
    data = pickle.load(f)

# Using SynUtils
from synutility.SynIO.data_type import load_from_pickle #hier data_type statt datatype


# ITS-Graphen-Daten mit SynUtils laden
data = load_from_pickle(r"C:\Users\Louisa\Downloads\ITS_graphs.pkl.gz")  # Absoluter Pfad

# Extracting reaction center and plotting using SynUtils
from synutility.SynAAM.misc import get_rc
#from src.rcextract import get_rc
reaction_center = get_rc(data[0]['ITS'])  # Reaktionszentrum extrahieren

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
