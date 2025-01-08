from collections import Counter
import networkx as nx

from utils import prepare_graph, are_rcs_isomorphic


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
        #graph.nodes[node]["hash_label"] = hash((c_label, sorted_neighbor_labels))
        graph.nodes[node]["hash_label"] = hash(sorted_neighbor_labels)


def initialize_weisfeiler_lehman(graphs):
    """
    Initialisiert die Knotenattribute 'compressed_label' und 'label' in einer Liste von Graphen.
    """
    for graph in graphs:
        # create combined label from charge and element strings
        prepare_graph(graph)
        # make the graph ready
        for node in graph.nodes():
            graph.nodes[node]["compressed_label"] = graph.nodes[node]["aggregated_attr"]
            graph.nodes[node]["hash_label"] = (None, None)


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
                all_labels.add(graph.nodes[node]["hash_label"])

        # Schritt 3: Weisen jedem Label einen eindeutigen Integer-Wert zu
        label_to_int = {label: idx for idx, label in enumerate(sorted(all_labels), start=2)}

        # Schritt 4: Aktualisiere compressed_label basierend auf dem neuen Label
        for i, graph in enumerate(graphs):
            for node in graph.nodes():
                current_label = graph.nodes[node]["hash_label"]
                if current_label in label_to_int:
                    graph.nodes[node]["compressed_label"] = label_to_int[current_label]
                    histogram = get_histogram(graph)
                    graph.graph['histogram'] = histogram
                    #graphs[i] = graph
                else:
                    print("Oh no")

        return graphs

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


def cluster_graphs(graph_list, depth_threshold=3, depth_count=0):
    cluster_sets = []

    graph_list = weisfeiler_lehman(graph_list, num_iterations=1)

    for graph in graph_list:

        found_cluster = False

        for i, cluster_set in enumerate(cluster_sets):
            # check if current graph hash is same as current cluster hash
            if graph.graph['histogram'] == cluster_set[0].graph['histogram']:
                found_cluster = True
                cluster_sets[i].append(graph)

        if not found_cluster:
            cluster_sets.append([graph])

    new_cluster_sets = []
    depth_count += 1
    if depth_count <= depth_threshold:
        for cluster in cluster_sets:
            if len(cluster) > 1:
                # apply cluster algo recursively
                new_cluster = cluster_graphs(cluster, depth_threshold, depth_count)
                new_cluster_sets.extend(new_cluster)
            else:
                new_cluster_sets.append(cluster)
    else:
        # max depth reached, return found clusters to previous recursion
        return cluster_sets

    return new_cluster_sets


from synutility.SynAAM.misc import get_rc
import argparse
import pickle
import os

file_path = os.path.join('data', 'ITS_graphs.pkl.gz')

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--graphs", help="Specifies the graphs to be used.", required=False, default=file_path)
parser.add_argument("-a", "--algorithm", help="Specifies the clustering algorithm to be used.", required=False, default="vertex_count")
args = parser.parse_args()

clustering_algorithm = args.algorithm
graph_path = args.graphs

# Lade die ITS-Graphen-Daten aus der Pickle-Datei
with open(graph_path, 'rb') as f:  # Absoluter Pfad zu deiner Datei
    data = pickle.load(f)

# Using SynUtils
from synutility.SynIO.data_type import load_from_pickle #hier data_type statt datatype


# ITS-Graphen-Daten mit SynUtils laden
data = load_from_pickle(graph_path)

graphs = []
for i in range(len(data)):
    g = data[i]['ITS']
    graphs.append(nx.edge_subgraph(g, [(e[0], e[1]) for e in g.edges(data=True) if e[2]["standard_order"] != 0]))
    # graphs.append(get_rc(data[i]['ITS']))

# Initialisierung der Graphen
initialize_weisfeiler_lehman(graphs)

clusters = cluster_graphs(graphs)
# print(clusters)

iso_cluster_sets = []
iso_sets = []
#iso_cluster_num = []
#iso_num = []

iso_cluster_counter = 0

cluster_length = len(clusters)

for cluster in clusters:
    print("Cluster: " + str(iso_cluster_counter + 1) + "/" + str(cluster_length))

    iso_cluster_sets.append([])
    #iso_cluster_num.append([])
    for graph in cluster:
        rc = graph
        #graph_id = graph[2]
        found_iso = False
        iso_set_counter = 0
        for iso_set in iso_cluster_sets[iso_cluster_counter]:
            if are_rcs_isomorphic(iso_set[0], rc):
                found_iso = True
                iso_cluster_sets[iso_cluster_counter][iso_set_counter].append(rc)
                #iso_cluster_num[iso_cluster_counter][iso_set_counter].append(graph_id)
                break
            iso_set_counter += 1

        if not found_iso:
            iso_cluster_sets[iso_cluster_counter].append([rc])
            #iso_cluster_num[iso_cluster_counter].append([graph_id])

    #for iso_set in iso_cluster_num[iso_cluster_counter]:
    #    iso_num.append(iso_set)
    for iso_set in iso_cluster_sets[iso_cluster_counter]:
        iso_sets.append(iso_set)

    iso_cluster_counter += 1

#print(iso_sets)
print("Iso: " + str(len(iso_sets)))
