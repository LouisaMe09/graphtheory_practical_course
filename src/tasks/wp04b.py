from helpers.utils import IsomorphismSolverTemplate, are_rcs_isomorphic
from collections import Counter

class IsomorphismSolver(IsomorphismSolverTemplate):

    iterations = 3
    depth = 0

    def __init__(self, graph_path: str, args: dict):
        print("wp04b")
        super().__init__(graph_path, args)


    def _calc_its_clustering(self):
        graphs = [graph['reaction_center'] for graph in self.data]
        self._initialize_weisfeiler_lehman(graphs)

        pre_clustered_graphs = self._cluster_sort(data=self.data, cluster_function=self._weisfeiler_lehman_compare, max_depth=self.depth)
        self.clustered_data = self._cluster_sort(data=pre_clustered_graphs, cluster_function=are_rcs_isomorphic, pre_clustered=True)


    def _weisfeiler_lehman_compare(self, rc1, rc2):
        # rc1 = first member of cluster, rc2 = compare graph
        rc1_depth = rc1.graph['depth']
        rc2_depth = rc2.graph['depth']
        
        if rc1_depth == -1 or rc1_depth == rc2_depth:
            self._weisfeiler_lehman(rc1)
        
        self._weisfeiler_lehman(rc2)
        
        return rc1.graph['histogram'] == rc2.graph['histogram']


    def _initialize_weisfeiler_lehman(self, graphs):
        """
        Initialisiert die Knotenattribute 'compressed_label' und 'label' in einer Liste von Graphen.
        """
        for graph in graphs:
            # make the graph ready
            for node in graph.nodes():
                graph.nodes[node]["compressed_label"] = graph.nodes[node]["aggregated_attr"]
                graph.nodes[node]["hash_label"] = (None, None)
                graph.graph['depth'] = -1


    def _update_labels(self, graph):
        """
        Aktualisiert die Labels eines Graphen basierend auf compressed_label und den Nachbarn.
        """
        for node in graph.nodes():
            c_label = graph.nodes[node]["compressed_label"]
            neighbor_labels = [
                graph.nodes[neighbor]["compressed_label"] for neighbor in graph.neighbors(node)
            ]
            sorted_neighbor_labels = tuple(sorted(neighbor_labels))
            graph.nodes[node]["hash_label"] = hash((c_label, sorted_neighbor_labels))
            #graph.nodes[node]["hash_label"] = hash(sorted_neighbor_labels)


    def get_histogram(self, graph):
        """
        Berechnet das Histogramm der compressed_labels für einen Graphen.
        """
        compressed_labels = [data["compressed_label"] for _, data in graph.nodes(data=True)]
        label_counts = Counter(compressed_labels)
        return label_counts


    def _weisfeiler_lehman(self, graph):
        """
        Führt die Weisfeiler-Lehmann-Iteration auf einer Liste von Graphen durch.
        """
        # Iterative Berechnung
        for _ in range(self.iterations):
            # Schritt 1: Aktualisiere die Labels basierend auf compressed_label
            self._update_labels(graph)

        histogram = self.get_histogram(graph)
        graph.graph['histogram'] = histogram
        graph.graph['depth'] += 1
