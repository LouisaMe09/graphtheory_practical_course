from helpers.utils import IsomorphismSolverTemplate, compute_wl_hash

class IsomorphismSolver(IsomorphismSolverTemplate):

    iterations = 3

    def __init__(self, graph_path: str, args: dict):
        print("wp04a")
        super().__init__(graph_path, args)

    def _calc_its_clustering(self): 
        function = self._weisfeiler_lehman
        self.clustered_data = self._cluster_sort(data=self.data, cluster_function=function)
        # self.clustered_data = self._isomorphism_sort(data=pre_clustered_data, pre_clustered=True)

    def _weisfeiler_lehman(self, rc_1, rc_2):
        return compute_wl_hash(rc_1, self.iterations) == compute_wl_hash(rc_2, self.iterations)
