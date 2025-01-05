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
rc_1 = get_rc(data[0]['ITS'])
rc_2 = get_rc(data[2]['ITS'])


print(are_rcs_isomorphic(rc_1, rc_2)) 