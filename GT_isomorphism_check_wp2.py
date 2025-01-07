# Using only pickle
import pickle
import networkx as nx
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--graphs", help="Specifies the graphs to be used.", required=True)
args = parser.parse_args()

graph_path = args.graphs

# Lade die ITS-Graphen-Daten aus der Pickle-Datei
with open(graph_path, 'rb') as f:  # Absoluter Pfad zu deiner Datei
    data = pickle.load(f)

# Using SynUtils
from synutility.SynIO.data_type import load_from_pickle #hier data_type statt datatype


# ITS-Graphen-Daten mit SynUtils laden
data = load_from_pickle(graph_path)  # Absoluter Pfad

#from networkx.algorithms.isomorphism import GraphMatcher
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
    #GM = GraphMatcher(rc_1, rc_2, node_match=node_match, edge_match=edge_match)
    
    # Rückgabe, ob die Graphen isomorph sind
    # return GM.is_isomorphic()
    return nx.is_isomorphic(rc_1, rc_2, node_match=node_match, edge_match=edge_match)


# # Extracting reaction center and plotting using SynUtils
from synutility.SynAAM.misc import get_rc
#rc_1 = get_rc(data[0]['ITS'])
#rc_2 = get_rc(data[2]['ITS'])


#print(are_rcs_isomorphic(rc_1, rc_2))

graph_counter = 0
iso_sets = []
iso_num = []
data_length = len(data)

for d in data:
    print("Graphs: " + str(graph_counter) + "/" + str(data_length))

    #rc = get_rc(data[graph_counter]['ITS'])
    g = data[graph_counter]['ITS']
    rc = nx.edge_subgraph(g, [(e[0], e[1]) for e in g.edges(data=True) if e[2]["standard_order"] != 0])

    found_iso = False
    iso_counter = 0

    for iso_set in iso_sets:
        if are_rcs_isomorphic(iso_set[0][1], rc):
            found_iso = True
            iso_set.append((graph_counter, rc))
            iso_num[iso_counter].append(d['R-id'])
            break

        iso_counter += 1


    if not found_iso:
        iso_sets.append([(graph_counter, rc)])
        iso_num.append([d['R-id']])

    graph_counter += 1

print(iso_num)
print(len(iso_num))