import os
import pickle
import networkx as nx
import argparse
from collections import Counter

# file_path = os.path.join('data', 'ITS_graphs.pkl.gz')

# parser = argparse.ArgumentParser()
# parser.add_argument("-g", "--graphs", help="Specifies the graphs to be used.", required=True, default=file_path)
# args = parser.parse_args()

# graph_path = args.graphs
graph_path = r"C:\Users\Louisa\Documents\Graphentheorie\graphtheory_practical_course\data\ITS_graphs.pkl.gz"


# Lade die ITS-Graphen-Daten aus der Pickle-Datei
with open(graph_path, 'rb') as f:  # Absoluter Pfad zu deiner Datei
    data = pickle.load(f)

# Using SynUtils
from synutility.SynIO.data_type import load_from_pickle #hier data_type statt datatype


# ITS-Graphen-Daten mit SynUtils laden
data = load_from_pickle(graph_path)  # Absoluter Pfad

# Extracting reaction center and plotting using SynUtils
from synutility.SynAAM.misc import get_rc
#from src.rcextract import get_rc
reaction_center = get_rc(data[0]['ITS'])  # Reaktionszentrum extrahieren


nx.set_node_attributes(reaction_center, 1, name="compressed_label")
nx.set_node_attributes(reaction_center, (None, None), name="label")


for node in reaction_center.nodes():
    c_label= reaction_center.nodes[node]["compressed_label"]
    neighbor_labels = [reaction_center.nodes[neighbor]["compressed_label"] for neighbor in reaction_center.neighbors(node)]
    sorted_neighbor_labels = sorted(neighbor_labels)  # Sortiere die Liste

    reaction_center.nodes[node]["label"] = (c_label, sorted_neighbor_labels)


print(reaction_center.nodes(data=True))  # Zeigt alle Knoten und ihre Eigenschaften

compressed_labels = [data["compressed_label"] for _, data in reaction_center.nodes(data=True)]

# Zähle die Häufigkeiten der Werte
label_counts = Counter(compressed_labels)
b=Counter({1: 4})
if b==label_counts:
    print("yes")
# Ausgabe
print(label_counts) 

