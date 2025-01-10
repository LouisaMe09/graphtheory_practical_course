from helpers.utils import IsomorphismSolverTemplate, are_rcs_isomorphic

class IsomorphismSolver(IsomorphismSolverTemplate):
    def __init__(self, graph_path: str, args: dict):
        print("wp02")
        super().__init__(graph_path, args)

    def _calc_its_clustering(self):
        # self.clustered_data = self._isomorphism_sort(data=self.data, pre_clustered=False)
        self.clustered_data = self._cluster_sort(data=self.data, pre_clustered=False, is_isomorphism_function=are_rcs_isomorphic, is_isomorphism_function=True)
