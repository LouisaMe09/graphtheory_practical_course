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



# def update_labels(graph):
#     """Aktualisiert die Labels eines Graphen basierend auf compressed_label und den Nachbarn."""
#     for node in graph.nodes():
#         c_label = graph.nodes[node]["compressed_label"]
#         neighbor_labels = [
#             graph.nodes[neighbor]["compressed_label"] for neighbor in graph.neighbors(node)
#         ]
#         sorted_neighbor_labels = tuple(sorted(neighbor_labels))
#         graph.nodes[node]["label"] = (c_label, sorted_neighbor_labels)


# def initialize_weisfeiler_lehman(graph1, graph2):
#     """
#     Initialisiert die Knotenattribute 'compressed_label' und 'label' in einer Liste von Graphen.
#     """
#     for graph in graphs:
#         for node in graph.nodes():
#             graph.nodes[node]["compressed_label"] = 1
#             graph.nodes[node]["label"] = (None, None)

# def weisfeiler_lehman(graph1, graph2, num_iterations=1):
#     """
#     Führt die Weisfeiler-Lehmann-Iteration auf zwei Graphen durch.
#     """
#     # Iterative Berechnung
#     for _ in range(num_iterations):
#         # Schritt 1: Aktualisiere die Labels basierend auf compressed_label
#         for graph in [graph1, graph2]:
#             update_labels(graph)

#         # Schritt 2: Sammle alle Labels aus beiden Graphen
#         all_labels = set()
#         for graph in [graph1, graph2]:
#             for node in graph.nodes():
#                 all_labels.add(graph.nodes[node]["label"])

#         # Schritt 3: Weisen jedem Label einen eindeutigen Integer-Wert zu
#         label_to_int = {label: idx for idx, label in enumerate(sorted(all_labels), start=2)}

#         # Schritt 4: Aktualisiere compressed_label basierend auf dem neuen Label
#         for graph in [graph1, graph2]:
#             for node in graph.nodes():
#                 current_label = graph.nodes[node]["label"]
#                 if current_label in label_to_int:
#                     graph.nodes[node]["compressed_label"] = label_to_int[current_label]

#         # Schritt 5: Aktualisiere die Labels erneut basierend auf den neuen compressed_labels
#         for graph in [graph1, graph2]:
#             update_labels(graph)

#     # Ausgabe der finalen Labels und compressed_labels
#     for graph_id, graph in enumerate([graph1, graph2], start=1):
#         print(f"Graph {graph_id}:")
#         for node in graph.nodes():
#             print(
#                 f"Node {node}: "
#                 f"Label = {graph.nodes[node]['label']}, "
#                 f"Compressed Label = {graph.nodes[node]['compressed_label']}"
#             )
#         print("-" * 40)

# initialize_weisfeiler_lehman(graph1, graph2)
# weisfeiler_lehman(graph1, graph2, 1)

# def get_histogram(graph):
#     compressed_labels = [data["compressed_label"] for _, data in graph.nodes(data=True)]
#     label_counts = Counter(compressed_labels)
#     return(label_counts)

# print(get_histogram(graph1))
# print(get_histogram(graph2))


import networkx as nx
from collections import Counter

def update_labels(graph):
    """
    Aktualisiert die Labels eines Graphen basierend auf compressed_label und den Nachbarn.
    """
    for node in graph.nodes():
        c_label = graph.nodes[node]["compressed_label"]
        neighbor_labels = [
            graph.nodes[neighbor]["compressed_label"] for neighbor in graph.neighbors(node)
        ]
        sorted_neighbor_labels = tuple(sorted(neighbor_labels))
        graph.nodes[node]["label"] = (c_label, sorted_neighbor_labels)

def initialize_weisfeiler_lehman(graphs):
    """
    Initialisiert die Knotenattribute 'compressed_label' und 'label' in einer Liste von Graphen.
    """
    for graph in graphs:
        for node in graph.nodes():
            graph.nodes[node]["compressed_label"] = 1
            graph.nodes[node]["label"] = (None, None)

def weisfeiler_lehman(graphs, num_iterations=1):
    """
    Führt die Weisfeiler-Lehmann-Iteration auf einer Liste von Graphen durch.
    """
    # Iterative Berechnung
    for _ in range(num_iterations):
        # Schritt 1: Aktualisiere die Labels basierend auf compressed_label
        for graph in graphs:
            update_labels(graph)

        # Schritt 2: Sammle alle Labels aus allen Graphen
        all_labels = set()
        for graph in graphs:
            for node in graph.nodes():
                all_labels.add(graph.nodes[node]["label"])

        # Schritt 3: Weisen jedem Label einen eindeutigen Integer-Wert zu
        label_to_int = {label: idx for idx, label in enumerate(sorted(all_labels), start=2)}

        # Schritt 4: Aktualisiere compressed_label basierend auf dem neuen Label
        for graph in graphs:
            for node in graph.nodes():
                current_label = graph.nodes[node]["label"]
                if current_label in label_to_int:
                    graph.nodes[node]["compressed_label"] = label_to_int[current_label]

    # # Ausgabe der finalen Labels und compressed_labels für alle Graphen
    # for graph_id, graph in enumerate(graphs, start=1):
    #     print(f"Graph {graph_id}:")
    #     for node in graph.nodes():
    #         print(
    #             f"Node {node}: "
    #             f"Label = {graph.nodes[node]['label']}, "
    #             f"Compressed Label = {graph.nodes[node]['compressed_label']}"
    #         )
    #     print("-" * 40)
    

def get_histogram(graph):
    """
    Berechnet das Histogramm der compressed_labels für einen Graphen.
    """
    compressed_labels = [data["compressed_label"] for _, data in graph.nodes(data=True)]
    label_counts = Counter(compressed_labels)
    return label_counts

# Beispielgraphen
graph1 = get_rc(data[116]['ITS'])
graph2 = get_rc(data[34]['ITS'])
graph3 = get_rc(data[12]['ITS'])


# Initialisierung der Graphen
graphs = [graph1, graph2, graph3]
initialize_weisfeiler_lehman(graphs)

# Weisfeiler-Lehmann-Iteration starten
weisfeiler_lehman(graphs, num_iterations=1)

# Histogramme berechnen und ausgeben
for graph_id, graph in enumerate(graphs, start=1):
    print(f"Histogram for Graph {graph_id}: {get_histogram(graph)}")








# from synutility.SynVis.graph_visualizer import GraphVisualizer  #auch hier hat n unterstrich gefehlt
# import matplotlib.pyplot as plt

# # Visualisierung vorbereiten
# fig, ax = plt.subplots(2, 1, figsize=(15, 10))
# vis = GraphVisualizer()

# # ITS-Graph plotten
# vis.plot_its(graph1, ax[0], use_edge_color=True)

# # Reaktionszentrum plotten
# vis.plot_its(graph2, ax[1], use_edge_color=True)

# # Plot anzeigen
# plt.show()

################################################################
# def cluster_alg(rc_1, rc_2, alg):
#     if alg == "histogram":
#         return get_histogram(graph1) == get_histogram(graph2)
    

# graph_counter = 0
# cluster_sets = []
# #cluster_num = []
# data_length = len(data)

# for d in data:
#     print("Graphs: " + str(graph_counter) + "/" + str(data_length))

#     rc = get_rc(data[graph_counter]['ITS'])

#     found_cluster = False
#     cluster_counter = 0

#     for cluster_set in cluster_sets:
#         if cluster_alg(cluster_set[0][1], rc, clustering_algorithm):
#             found_cluster = True
#             cluster_sets[cluster_counter].append((graph_counter, rc, d['R-id']))
#             #cluster_num[iso_counter].append(d['R-id'])

#         cluster_counter += 1


#     if not found_cluster:
#         cluster_sets.append([(graph_counter, rc, d['R-id'])])
#         #cluster_num.append([d['R-id']])

#     graph_counter += 1

# iso_cluster_sets = []
# iso_cluster_num = []
# iso_num = []

# iso_cluster_counter = 0

# cluster_length = len(cluster_sets)

# for cluster in cluster_sets:
#     print("Cluster: " + str(iso_cluster_counter) + "/" + str(cluster_length))

#     iso_cluster_sets.append([])
#     iso_cluster_num.append([])
#     for graph in cluster:
#         rc = graph[1]
#         graph_id = graph[2]
#         found_iso = False
#         iso_set_counter = 0
#         for iso_set in iso_cluster_sets[iso_cluster_counter]:  #iteriert über alle listen von rcs in dem cluster
#             if are_rcs_isomorphic(iso_set[0], rc):
#                 found_iso = True
#                 iso_cluster_sets[iso_cluster_counter][iso_set_counter].append(rc)
#                 iso_cluster_num[iso_cluster_counter][iso_set_counter].append(graph_id)
#                 break
#             iso_set_counter += 1

#         if not found_iso:
#             iso_cluster_sets[iso_cluster_counter].append([rc])
#             iso_cluster_num[iso_cluster_counter].append([graph_id])
    
#     for iso_set in iso_cluster_num[iso_cluster_counter]:
#         iso_num.append(iso_set)

#     iso_cluster_counter += 1

# print(iso_num)
# print(len(iso_num))