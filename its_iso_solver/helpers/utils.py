from networkx import is_isomorphic, edge_subgraph, Graph


def prepare_graph(graph):
    """
    Prepare the graph by combining node attributes ('charge' and 'element') into a single string
    and ensuring edge attributes are well-defined.
    """
    for node, data in graph.nodes(data=True):
        # Combine 'charge' and 'element' into a single string attribute
        charge = str(data.get('charge', ''))
        element = str(data.get('element', ''))
        data['aggregated_attr'] = f"{charge}_{element}"


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

    return is_isomorphic(rc_1, rc_2, node_match=node_match, edge_match=edge_match)


from synutility.SynIO.data_type import load_from_pickle #hier data_type statt datatype
from abc import abstractmethod
from collections.abc import Callable


class IsomorphismSolverTemplate():
    
    clustered_data = []

    def __init__(self, graph_path: str, args: dict):
        # Lade die ITS-Graphen-Daten aus der Pickle-Datei
        self.data = load_from_pickle(graph_path)  # Absoluter Pfad
        
        for graph in self.data:
            graph['reaction_center'] = edge_subgraph(graph['ITS'], [(e[0], e[1]) for e in graph['ITS'].edges(data=True) if e[2]["standard_order"] != 0])
            prepare_graph(graph['reaction_center'])

        for key, value in args.items():
            setattr(self, key, value)


    @abstractmethod
    def _calc_its_clustering(self):
        pass


    def its_clustering(self):
        self._calc_its_clustering()
        return self

    def get_clustered_data(self):
        return self.clustered_data
    

    # cluster + isomorphism functionality combined
    def _cluster_sort(self, data: list, cluster_function: Callable[[Graph, Graph], bool], max_depth=0, current_depth=0, pre_clustered=False):

        if len(data) <= 1:
            return [[data]]

        cluster_sets = []

        if not pre_clustered:
            for graph in data:

                rc = graph['reaction_center']

                found_cluster = False

                for cluster_set in cluster_sets:
                    if cluster_function(cluster_set[0]['reaction_center'], rc):
                        found_cluster = True
                        cluster_set.append(graph)
                        break
                
                if not found_cluster:
                    cluster_sets.append([graph])
        else:
            for cluster in data:
                cluster_sets.extend(self._cluster_sort(data=cluster, cluster_function=cluster_function, pre_clustered=False))

        if max_depth > current_depth:
            improved_cluster_sets = []

            for cluster in cluster_sets:
                improved_cluster_sets.extend(
                    self._cluster_sort(
                        data=cluster,
                        cluster_function=cluster_function,
                        max_depth=max_depth,
                        current_depth=current_depth+1
                    )
                )

            return improved_cluster_sets

        else:
            return cluster_sets
