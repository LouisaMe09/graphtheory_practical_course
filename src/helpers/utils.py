from networkx import weisfeiler_lehman_graph_hash, is_isomorphic, edge_subgraph, Graph


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
    
    return graph

    # Ensure edges have proper attributes (if needed, handle missing attributes)
    #for u, v, data in graph.edges(data=True):
    #    if 'order' not in data:
    #        data['order'] = 1  # Assign default weight


def compute_wl_hash(graph, iterations, node_attr='aggregated_attr', edge_attr='order'):
    """
    Compute the Weisfeiler-Lehman graph hash for the given graph.

    Parameters:
        - graph: The input graph (prepared with aggregated attributes).
        - iterations: Number of WL refinement steps.
        - node_attr: Node attribute to consider for hashing (default: 'aggregated_attr').
        - edge_attr: Edge attribute to consider (default: 'order').

    Returns:
        - A string representing the WL graph hash.
    """
    return weisfeiler_lehman_graph_hash(
        graph, edge_attr=edge_attr, node_attr=node_attr, iterations=iterations
    )


def cluster_graphs_wl(graphs, iterations=2, node_attr='aggregated_attr', edge_attr='order'):
    """
    Perform hierarchical clustering based on WL graph hash.

    Parameters:
        - graphs: List of graphs to cluster.
        - iterations: Number of WL refinement steps.
        - node_attr: Node attribute for hashing.
        - edge_attr: Edge attribute for hashing.

    Returns:
        - A dictionary where keys are hash values and values are lists of graph indices.
    """
    clusters = {}

    for i, graph in enumerate(graphs):
        prepare_graph(graph)
        graph_hash = compute_wl_hash(graph, iterations, node_attr, edge_attr)

        if graph_hash not in clusters:
            clusters[graph_hash] = []
        clusters[graph_hash].append(i)

    return clusters


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

    # only used in wp04b
    def _isomorphism_sort(self, data: list, pre_clustered: bool):

        iso_sets = []

        if not pre_clustered:
            for graph in data:

                # rc = graph['reaction_center']
                rc = graph

                found_iso = False

                for iso_set in iso_sets:
                    if are_rcs_isomorphic(iso_set[0], rc):
                        found_iso = True
                        iso_set.append(graph)
                        break

                if not found_iso:
                    iso_sets.append([graph])

        else:
            for cluster in data:
                iso_sets.extend(self._isomorphism_sort(data=cluster, pre_clustered=False))
        
        return iso_sets
    
    # cluster + isomorphism functionality combined
    def _cluster_sort(self, data: list, cluster_function: Callable[[Graph, Graph], bool], max_depth=0, current_depth=0, is_isomorphism_function=False, pre_clustered=False):

        if len(data) <= 1:
            return [[data]]

        cluster_sets = []

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
            if is_isomorphism_function:
                return cluster_sets

            else:
                iso_cluster_sets = []

                for cluster in cluster_sets:
                    iso_cluster_sets.extend(
                        self._cluster_sort(
                            data=cluster,
                            cluster_function=are_rcs_isomorphic,
                            is_isomorphism_function=True
                        )
                    )

                return iso_cluster_sets
