from networkx import weisfeiler_lehman_graph_hash, is_isomorphic


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

    # Ensure edges have proper attributes (if needed, handle missing attributes)
    #for u, v, data in graph.edges(data=True):
    #    if 'order' not in data:
    #        data['order'] = 1  # Assign default weight


def compute_wl_hash(graph, iterations, node_attr='aggregated_attr', edge_attr='order'):
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


def cluster_graphs_wl(graphs, iterations=2, node_attr='aggregated_attr', edge_attr='order'):
    """
    Perform hierarchical clustering based on WL graph hash.

    Parameters:
        - graphs: List of graphs to cluster.
        - iterations: Number of WL refinement steps.
        - node_attr: Node attribute for hashing.
        - edge_attr: Edge attribute for hashing.

    Returns:
        - A dictionary where keys are hash values and values are lists of graph indices.
    """
    clusters = {}

    for i, graph in enumerate(graphs):
        prepare_graph(graph)
        graph_hash = compute_wl_hash(graph, iterations, node_attr, edge_attr)

        if graph_hash not in clusters:
            clusters[graph_hash] = []
        clusters[graph_hash].append(i)

    return clusters


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