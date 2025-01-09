from helpers.utils import IsomorphismSolverTemplate, compute_wl_hash, prepare_graph, are_rcs_isomorphic
from collections import Counter
import networkx as nx

class IsomorphismSolver(IsomorphismSolverTemplate):

    iterations = 3
    depth = 0

    def __init__(self, graph_path: str, args: dict):
        print("wp04b")
        super().__init__(graph_path, args)


    def _calc_its_clustering(self):
        graphs = [graph['reaction_center'] for graph in self.data]
        self.initialize_weisfeiler_lehman(graphs)
        pre_clustered_graphs = self.cluster_graphs(graph_list=graphs, depth_threshold=self.depth)
        self.clustered_data = self._isomorphism_sort(data=pre_clustered_graphs, pre_clustered=True)


    def update_labels(self, graph):
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


    def initialize_weisfeiler_lehman(self, graphs):
        """
        Initialisiert die Knotenattribute 'compressed_label' und 'label' in einer Liste von Graphen.
        """
        for graph in graphs:
            # create combined label from charge and element strings
            prepare_graph(graph)
            # make the graph ready
            for node in graph.nodes():
                graph.nodes[node]["compressed_label"] = graph.nodes[node]["aggregated_attr"]
                graph.nodes[node]["hash_label"] = (None, None)


    def weisfeiler_lehman(self, graphs, num_iterations):
        """
        Führt die Weisfeiler-Lehmann-Iteration auf einer Liste von Graphen durch.
        """
        # Iterative Berechnung
        for _ in range(num_iterations):
            # Schritt 1: Aktualisiere die Labels basierend auf compressed_label
            for graph in graphs:
                self.update_labels(graph)

            # Schritt 2: Sammle alle Labels aus allen Graphen
            all_labels = set()
            for graph in graphs:
                for node in graph.nodes():
                    all_labels.add(graph.nodes[node]["hash_label"])

            # Schritt 3: Weisen jedem Label einen eindeutigen Integer-Wert zu
            label_to_int = {label: idx for idx, label in enumerate(sorted(all_labels), start=2)}

            # Schritt 4: Aktualisiere compressed_label basierend auf dem neuen Label
            for i, graph in enumerate(graphs):
                for node in graph.nodes():
                    current_label = graph.nodes[node]["hash_label"]
                    if current_label in label_to_int:
                        graph.nodes[node]["compressed_label"] = label_to_int[current_label]
                        histogram = self.get_histogram(graph)
                        graph.graph['histogram'] = histogram
                        #graphs[i] = graph
                    else:
                        print("Oh no")

        return graphs


    def get_histogram(self, graph):
        """
        Berechnet das Histogramm der compressed_labels für einen Graphen.
        """
        compressed_labels = [data["compressed_label"] for _, data in graph.nodes(data=True)]
        label_counts = Counter(compressed_labels)
        return label_counts


    def cluster_graphs(self, graph_list, depth_threshold=0, depth_count=0):
        cluster_sets = []

        graph_list = self.weisfeiler_lehman(graph_list, num_iterations=1)

        for graph in graph_list:

            found_cluster = False

            for i, cluster_set in enumerate(cluster_sets):
                # check if current graph hash is same as current cluster hash
                if graph.graph['histogram'] == cluster_set[0].graph['histogram']:
                    found_cluster = True
                    cluster_sets[i].append(graph)

            if not found_cluster:
                cluster_sets.append([graph])

        new_cluster_sets = []
        depth_count += 1
        if depth_count <= depth_threshold:
            for cluster in cluster_sets:
                if len(cluster) > 1:
                    # apply cluster algo recursively
                    new_cluster = self.cluster_graphs(cluster, depth_threshold, depth_count)
                    new_cluster_sets.extend(new_cluster)
                else:
                    new_cluster_sets.append(cluster)
        else:
            # max depth reached, return found clusters to previous recursion
            return cluster_sets

        return new_cluster_sets