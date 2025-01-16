from helpers.utils import are_rcs_isomorphic
from tasks.wp03 import IsomorphismSolver as WP03
from tasks.wp04a import IsomorphismSolver as WP04A
from tasks.wp04b import IsomorphismSolver as WP04B
import time

class IsomorphismSolver(WP03, WP04A, WP04B):

    algorithm = "vertex_count"

    def __init__(self, data: str, args: dict):
        print("wpx")
        self.__class__.__mro__[4].__init__(self, data, args)

    def _calc_its_clustering(self):
        start = time.time()
        if "weisfeiler_lehman" in self.algorithms:
            graphs = [graph['reaction_center'] for graph in self.data]
            self._initialize_weisfeiler_lehman(graphs)

        functions = self.__multi_select(alg_list=self.algorithms)
        pre_clustered_data = self.data
        for i, f in enumerate(functions):
            pre_clustered_data = self._cluster_sort(data=pre_clustered_data, cluster_function=f[0], pre_clustered=(lambda i: i != 0)(i), max_depth=f[1])
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
            case "vertex_count": return (self._vertex_count, 0)
            case "edge_count": return (self._edge_count, 0)
            case "vertex_degrees": return (self._vertex_degrees, 0)
            case "algebraic_connectivity": return (self._algebraic_connectivity, 0)
            case "rank": return (self._rank, 0)
            case "weisfeiler_lehman_nx": return (self._weisfeiler_lehman_nx, self.depth)
            case "weisfeiler_lehman": return (self._weisfeiler_lehman_compare, self.depth)
            case _:
                print("Algorithm does not exist.")
                raise LookupError
