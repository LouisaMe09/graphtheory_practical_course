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

graph1 = get_rc(data[113]['ITS'])
graph2 = get_rc(data[34]['ITS'])

def update_labels(graph):
    """Aktualisiert die Labels eines Graphen basierend auf compressed_label und den Nachbarn."""
    for node in graph.nodes():
        c_label = graph.nodes[node]["compressed_label"]
        neighbor_labels = [
            graph.nodes[neighbor]["compressed_label"] for neighbor in graph.neighbors(node)
        ]
        sorted_neighbor_labels = tuple(sorted(neighbor_labels))
        graph.nodes[node]["label"] = (c_label, sorted_neighbor_labels)

def weisfeiler_lehman(graph1, graph2, num_iterations=1):
    # Initialisierung: Setze compressed_label und label
    for graph in [graph1, graph2]:
        for node in graph.nodes():
            graph.nodes[node]["compressed_label"] = 1
            graph.nodes[node]["label"] = (None, None)

    # Iterative Berechnung
    for _ in range(num_iterations):
        # Schritt 1: Aktualisiere die Labels basierend auf compressed_label
        for graph in [graph1, graph2]:
            update_labels(graph)

        # Schritt 2: Sammle alle Labels aus beiden Graphen
        all_labels = set()
        for graph in [graph1, graph2]:
            for node in graph.nodes():
                all_labels.add(graph.nodes[node]["label"])

        # Schritt 3: Weisen jedem Label einen eindeutigen Integer-Wert zu
        label_to_int = {label: idx for idx, label in enumerate(sorted(all_labels), start=2)}

        # Schritt 4: Aktualisiere compressed_label basierend auf dem neuen Label
        for graph in [graph1, graph2]:
            for node in graph.nodes():
                current_label = graph.nodes[node]["label"]
                if current_label in label_to_int:
                    graph.nodes[node]["compressed_label"] = label_to_int[current_label]

        # Schritt 5: Aktualisiere die Labels erneut basierend auf den neuen compressed_labels
        for graph in [graph1, graph2]:
            update_labels(graph)

    # Ausgabe der finalen Labels und compressed_labels
    for graph_id, graph in enumerate([graph1, graph2], start=1):
        print(f"Graph {graph_id}:")
        for node in graph.nodes():
            print(
                f"Node {node}: "
                f"Label = {graph.nodes[node]['label']}, "
                f"Compressed Label = {graph.nodes[node]['compressed_label']}"
            )
        print("-" * 40)

weisfeiler_lehman(graph1, graph2, 1)

def get_histogram(graph):
    compressed_labels = [data["compressed_label"] for _, data in graph.nodes(data=True)]
    label_counts = Counter(compressed_labels)
    return(label_counts)

print(get_histogram(graph1))
print(get_histogram(graph2))

