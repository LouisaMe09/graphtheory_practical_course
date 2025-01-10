from helpers.utils import IsomorphismSolverTemplate, are_rcs_isomorphic
from networkx import weisfeiler_lehman_graph_hash

class IsomorphismSolver(IsomorphismSolverTemplate):

    iterations = 3

    def __init__(self, graph_path: str, args: dict):
        print("wp04a")
        super().__init__(graph_path, args)

    def _calc_its_clustering(self): 
        function = self._weisfeiler_lehman
        pre_clustered_data = self._cluster_sort(data=self.data, cluster_function=function)
        self.clustered_data = self._cluster_sort(data=pre_clustered_data, cluster_function=are_rcs_isomorphic, pre_clustered=True)

    def _weisfeiler_lehman(self, rc_1, rc_2):
        return self._compute_wl_hash(rc_1, self.iterations) == self._compute_wl_hash(rc_2, self.iterations)

    # can be substituted into _weisfeiler_lehman
    def _compute_wl_hash(self, graph, iterations, node_attr='aggregated_attr', edge_attr='order'):
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