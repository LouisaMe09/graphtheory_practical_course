# Using only pickle
import pickle
import networkx as nx
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--graphs", help="Specifies the graphs to be used.", required=True)
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
data = load_from_pickle(graph_path)  # Absoluter Pfad

from networkx.algorithms.isomorphism import GraphMatcher
#isomorphism check

def are_rcs_isomorphic(rc_1, rc_2):
    """
    Prüft, ob zwei Graphen G1 und G2 isomorph sind, 
    unter Berücksichtigung von Knoten- und Kantenattributen.

    Parameter:
    - rc_1: Der erste NetworkX-Graph.
    - rc_2: Der zweite NetworkX-Graph.

    Rückgabe:
    - True, wenn die Graphen isomorph sind, andernfalls False.
    """

    # Definiere die Knotenvergleichsfunktion
    def node_match(n1, n2):
        return (
            n1.get('charge') == n2.get('charge') and
            n1.get('element') == n2.get('element')
        )

    # Definiere die Kantenvergleichsfunktion
    def edge_match(e1, e2):
        return e1.get('order') == e2.get('order')

    # Erstelle den GraphMatcher mit den Vergleichsfunktionen
    GM = GraphMatcher(rc_1, rc_2, node_match=node_match, edge_match=edge_match)
    
    # Rückgabe, ob die Graphen isomorph sind
    return GM.is_isomorphic()



# # Extracting reaction center and plotting using SynUtils
from synutility.SynAAM.misc import get_rc
#rc_1 = get_rc(data[0]['ITS'])
#rc_2 = get_rc(data[2]['ITS'])


#print(are_rcs_isomorphic(rc_1, rc_2))

def cluster_alg(rc_1, rc_2, alg):
    if alg == "vertex_count":
        return rc_1.number_of_nodes() == rc_2.number_of_nodes()
    if alg == "edge_count":
        return rc_1.number_of_edges() == rc_2.number_of_edges()
    if alg == "vertex_degrees":
        return sorted(dict(rc_1.degree()).values()) == sorted(dict(rc_2.degree()).values())
    if alg == "algebraic_connectivity":
        return nx.algebraic_connectivity(rc_1, method="tracemin_lu") == nx.algebraic_connectivity(rc_2, method="tracemin_lu")
    if alg == "rank":
        adj_matrix_1 = nx.adjacency_matrix(rc_1).toarray()
        adj_matrix_2 = nx.adjacency_matrix(rc_2).toarray()

        rank_1 = np.linalg.matrix_rank(adj_matrix_1)
        rank_2 = np.linalg.matrix_rank(adj_matrix_2)

        return rank_1 == rank_2



graph_counter = 0
cluster_sets = []
#cluster_num = []
data_length = len(data)

for d in data:
    print("Graphs: " + str(graph_counter) + "/" + str(data_length))

    rc = get_rc(data[graph_counter]['ITS'])

    found_cluster = False
    cluster_counter = 0

    for cluster_set in cluster_sets:
        if cluster_alg(cluster_set[0][1], rc, clustering_algorithm):
            found_cluster = True
            cluster_sets[cluster_counter].append((graph_counter, rc, d['R-id']))
            #cluster_num[iso_counter].append(d['R-id'])

        cluster_counter += 1


    if not found_cluster:
        cluster_sets.append([(graph_counter, rc, d['R-id'])])
        #cluster_num.append([d['R-id']])

    graph_counter += 1

iso_cluster_sets = []
iso_cluster_num = []
iso_num = []

iso_cluster_counter = 0

cluster_length = len(cluster_sets)

for cluster in cluster_sets:
    print("Cluster: " + str(iso_cluster_counter) + "/" + str(cluster_length))

    iso_cluster_sets.append([])
    iso_cluster_num.append([])
    for graph in cluster:
        rc = graph[1]
        graph_id = graph[2]
        found_iso = False
        iso_set_counter = 0
        for iso_set in iso_cluster_sets[iso_cluster_counter]:
            if are_rcs_isomorphic(iso_set[0], rc):
                found_iso = True
                iso_cluster_sets[iso_cluster_counter][iso_set_counter].append(rc)
                iso_cluster_num[iso_cluster_counter][iso_set_counter].append(graph_id)
                break
            iso_set_counter += 1

        if not found_iso:
            iso_cluster_sets[iso_cluster_counter].append([rc])
            iso_cluster_num[iso_cluster_counter].append([graph_id])
    
    for iso_set in iso_cluster_num[iso_cluster_counter]:
        iso_num.append(iso_set)

    iso_cluster_counter += 1

print(iso_num)
print(len(iso_num))