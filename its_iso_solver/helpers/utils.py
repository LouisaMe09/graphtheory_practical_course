from networkx import is_isomorphic, edge_subgraph, Graph
from tqdm import tqdm

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


from abc import abstractmethod
from collections.abc import Callable


class IsomorphismSolverTemplate():
    
    clustered_data = []
    l_neighborhood = 0

    def __init__(self, data: list, args: dict):
        # Lade die ITS-Graphen-Daten aus der Pickle-Datei
        self.data = data

        for key, value in args.items():
            setattr(self, key, value)

        for graph in self.data:
            # graph['reaction_center'] = edge_subgraph(graph['ITS'], [(e[0], e[1]) for e in graph['ITS'].edges(data=True) if e[2]["standard_order"] != 0])
            graph['reaction_center'] = self._get_subgraph(graph['ITS'], self.l_neighborhood)
            prepare_graph(graph['reaction_center'])


    def _get_subgraph(self, graph, L):
        if L == 0:
            return edge_subgraph(graph, [(e[0], e[1]) for e in graph.edges(data=True) if e[2]["standard_order"] != 0])
        else:
            subgraph = self._get_subgraph(graph, L-1)
            edge_set = set()

            for node in subgraph.nodes():
                edge_set.update({(e[0], e[1]) for e in graph.edges(data=True) if e[0] == node or e[1] == node})
            
            edge_list = list(edge_set)
            return edge_subgraph(graph, edge_list)


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

        if len(data) <= 1 and not pre_clustered:
            return [data]

        cluster_sets = []

        if not pre_clustered:
            with tqdm(total=len(data), desc=f"cluster_function={cluster_function.__name__}, current_depth={str(current_depth)}, max_depth={str(max_depth)}, pre_clustered={pre_clustered}") as progress_bar:

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

                    progress_bar.update(1)
        else:
            for cluster in data:
                cluster_sets.extend(
                    self._cluster_sort(
                        data=cluster,
                        max_depth=max_depth,
                        current_depth=current_depth,
                        cluster_function=cluster_function,
                        pre_clustered=False
                    )
                )
        if max_depth > current_depth:
            return self._cluster_sort(
                        data=cluster_sets,
                        cluster_function=cluster_function,
                        max_depth=max_depth,
                        current_depth=current_depth+1,
                        pre_clustered=True
                    )
        else:
            return cluster_sets
