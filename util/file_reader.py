from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    # TODO: Use 'open' to open the file
    f = open(filename, "r").read().split()

    # TODO: Use the first line (G or D) to determine whether graph is directed
    # and create a graph object
    is_directed = True if f[0] == "D" else False
    graph_obj = Graph(is_directed=is_directed)

    # TODO: Use the second line to add the vertices to the graph
    graph_vertices = f[1].split(',')
    for vertice in graph_vertices:
        graph_obj.add_vertex(vertice)

    # TODO: Use the 3rd+ line to add the edges to the graph

    edges = f[2:]
    for edge in edges:
        # TODO: Issue might be here.
        edge1, edge2 = edge.string(')(').split(',')
        graph_obj.add_edge(edge1, edge2)

    return graph_obj


if __name__ == '__main__':
    graph = read_graph_from_file('test.txt')

    print(graph)
