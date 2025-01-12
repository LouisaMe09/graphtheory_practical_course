from its_iso_solver.helpers.utils import IsomorphismSolverTemplate, are_rcs_isomorphic

class IsomorphismSolver(IsomorphismSolverTemplate):
    def __init__(self, data: str, args: dict):
        print("wp02")
        super().__init__(data, args)

    def _calc_its_clustering(self):
        self.clustered_data = self._cluster_sort(data=self.data, cluster_function=are_rcs_isomorphic, pre_clustered=False)
