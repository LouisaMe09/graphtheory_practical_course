from helpers.utils import IsomorphismSolverTemplate, are_rcs_isomorphic
import networkx as nx
import numpy as np

class IsomorphismSolver(IsomorphismSolverTemplate):

    algorithm = "vertex_count"

    def __init__(self, graph_path: str, args: dict):
        print("wp03")
        super().__init__(graph_path, args)

    def _calc_its_clustering(self):
        function = self.__select_cluster_function(algorithm=self.algorithm)
        pre_clustered_data = self._cluster_sort(data=self.data, cluster_function=function)
        self.clustered_data = self._cluster_sort(data=pre_clustered_data, cluster_function=are_rcs_isomorphic, pre_clustered=True)

    def __select_cluster_function(self, algorithm):
        match algorithm:
            case "vertex_count": return self._vertex_count
            case "edge_count": return self._edge_count
            case "vertex_degrees": return self._vertex_degrees
            case "algebraic_connectivity": return self._algebraic_connectivity
            case "rank": return self._rank
            case _:
                print("Algorithm does not exist.")
                raise LookupError

    def _vertex_count(self, rc_1, rc_2):
        return rc_1.number_of_nodes() == rc_2.number_of_nodes()
    
    def _edge_count(self, rc_1, rc_2):
        return rc_1.number_of_edges() == rc_2.number_of_edges()

    def _vertex_degrees(self, rc_1, rc_2):
        return sorted(dict(rc_1.degree()).values()) == sorted(dict(rc_2.degree()).values())

    def _algebraic_connectivity(self, rc_1, rc_2):
        return nx.algebraic_connectivity(rc_1, method="tracemin_lu") == nx.algebraic_connectivity(rc_2, method="tracemin_lu")

    def _rank(self, rc_1, rc_2):
        adj_matrix_1 = nx.adjacency_matrix(rc_1).toarray()
        adj_matrix_2 = nx.adjacency_matrix(rc_2).toarray()

        rank_1 = np.linalg.matrix_rank(adj_matrix_1)
        rank_2 = np.linalg.matrix_rank(adj_matrix_2)

        return rank_1 == rank_2