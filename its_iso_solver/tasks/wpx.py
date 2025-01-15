from helpers.utils import are_rcs_isomorphic
from tasks.wp03 import IsomorphismSolver as WP03
from tasks.wp04a import IsomorphismSolver as WP04A
from tasks.wp04b import IsomorphismSolver as WP04B
import time

class IsomorphismSolver(WP03, WP04A, WP04B):

    algorithm = "vertex_count"

    def __init__(self, data: str, args: dict):
        print("wpx")
        super().__init__(data, args)

    def _calc_its_clustering(self):
        start = time.time()
        if "weisfeiler_lehman" in self.algorithms:
            graphs = [graph['reaction_center'] for graph in self.data]
            self._initialize_weisfeiler_lehman(graphs)

        functions = self.__multi_select(alg_list=self.algorithms)
        pre_clustered_data = self.data
        for i, f in enumerate(functions):
            pre_clustered_data = self._cluster_sort(data=pre_clustered_data, cluster_function=f, pre_clustered=(lambda i: i != 0)(i))
        self.clustered_data = self._cluster_sort(data=pre_clustered_data, cluster_function=are_rcs_isomorphic, pre_clustered=True)
        end = time.time()
        print(f"Time: {end - start}")

    def __multi_select(self, alg_list):
        algorithms = []
        for alg in alg_list:
            algorithms.append(self.__select_cluster_function(alg))
        return algorithms

    def __select_cluster_function(self, algorithm):
        match algorithm:
            case "vertex_count": return self._vertex_count
            case "edge_count": return self._edge_count
            case "vertex_degrees": return self._vertex_degrees
            case "algebraic_connectivity": return self._algebraic_connectivity
            case "rank": return self._rank
            case "weisfeiler_lehman_nx": return self._weisfeiler_lehman_nx
            case "weisfeiler_lehman": return self._weisfeiler_lehman_compare
            case _:
                print("Algorithm does not exist.")
                raise LookupError
