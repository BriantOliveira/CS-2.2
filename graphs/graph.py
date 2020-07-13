from collections import deque
from random import choice


class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {}  # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        self.__neighbors_dict[vertex_obj.__id] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id


class Graph:

    """ Graph Class
    Represents a directed or undirected graph.
    """

    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {}  # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        self.__vertex_dict[vertex_id] = Vertex(vertex_id)
        return self.__vertex_dict[vertex_id]

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        vertex_2 = self.get_vertex(vertex_id2)
        self.__vertex_dict[vertex_id1].add_neighbor(vertex_2)
        if not self.__is_directed:
            self.__vertex_dict[vertex_id2].add_neighbor(
                self.__vertex_dict[vertex_id1])

    def get_vertices(self):
        """
        Return all vertices in the graph.

        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.pop()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return  # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id]  # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque()
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.popleft()  # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            if (current_vertex_id == target_id):
                return vertex_id_to_path[target_id]

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)
                    # print(vertex_id_to_path)

        if target_id not in vertex_id_to_path:  # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.

        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        vertice_distance = {start_id: 0}

        results = []
        seen = set()
        seen.add(start_id)

        queue = deque()
        queue.append(self.get_vertex(start_id))

        pause = False

        while queue:
            vertex = queue.popleft()
            vertex_id = vertex.get_id()

            neighbors = vertex.get_neighbors()

            if vertice_distance[vertex_id] == target_distance + 1:
                pause = True
                break

            for n in neighbors:
                neighbor_id = n.get_id()
                if neighbor_id not in seen:
                    if neighbor_id not in vertice_distance:
                        vertice_distance[neighbor_id] = vertice_distance[vertex_id]
                    vertice_distance[neighbor_id] += 1
                    if vertice_distance[neighbor_id] == target_distance:
                        results.append(neighbor_id)
                    seen.add(neighbor_id)
                    queue.append(n)
        return results

    def is_bipartite(self):
        """
        Return True if the graph is bipartite, and False otherwise.
        """

        start_id = choice(list(self.__vertex_dict.keys()))

        queue = deque()
        queue.append(self.get_vertex(start_id))

        all_colors = {
            start_id: "red"
        }

        while queue:
            vertex_object = queue.pop()
            vertex_id = vertex_object.get_id()

            neighbors = vertex_object.get_neighbors()

            for n in neighbors:
                n_id = n.get_id()
                if n_id not in all_colors:
                    all_colors[n_id] = "blue" if all_colors[vertex_id] == "red" else "red"
                    queue.appendleft(n)
                else:
                    if all_colors[n_id] == all_colors[vertex_id]:
                        return False
        return True

    def get_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """
        start_id = choice(list(self.__vertex_dict.keys()))

        # must be a list, can't be a set because random.choice does not it
        ids_left = list(self.__vertex_dict.keys())
        ids_left.remove(start_id)

        seen = set()
        seen.add(start_id)

        queue = deque()
        queue.append(self.get_vertex(start_id))

        components = []
        com = []
        while queue:
            vertex_oject = queue.pop()
            vertex_id = vertex_oject.get_id()
            com.append(vertex_id)

            neighbors = vertex_oject.get_neighbors()

            for n in neighbors:
                n_id = n.get_id()
                if n_id not in seen:
                    seen.add(n_id)
                    queue.appendleft(n)
                    ids_left.remove(n_id)

            # if there is no vertex left in the queue
            if len(queue) == 0:
                components.append(com)
                # if there are no more components left to traverse through
                if len(ids_left) == 0:
                    break
                com = []
                new_start = choice(ids_left)
                seen.add(new_start)
                queue.appendleft(self.get_vertex(new_start))
                ids_left.remove(new_start)

        return components

    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        paths = {
            start_id: [start_id]
        }

        stack = deque()
        stack.append(self.get_vertex(start_id))

        while stack:
            vertex_object = stack.pop()
            vertex_id = vertex_object.get_id()

            neighbors = vertex_object.get_neighbors()

            for n in neighbors:
                n_id = n.get_id()
                if n_id not in paths:
                    current_path = paths[vertex_id]
                    next_path = current_path + [n_id]
                    if n_id == target_id:
                        return next_path
                    paths[n_id] = next_path
                    stack.append(n)
        return paths

    def dfs_traversal(self, start_id):
        """Visit each vertex, starting with start_id, in DFS order."""

        visited = set()  # set of vertices we've visited so far

        def dfs_traversal_recursive(start_vertex):
            print(f'Visiting vertex {start_vertex.get_id()}')

            # recurse for each vertex in neighbors
            for neighbor in start_vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    visited.add(neighbor.get_id())
                    dfs_traversal_recursive(neighbor)
            return

        visited.add(start_id)
        start_vertex = self.get_vertex(start_id)
        dfs_traversal_recursive(start_vertex)

    def contains_cycle(self):
        """
        Return True if the directed graph contains a cycle, False otherwise.
        """
        def dfs_cycle(vertex, visited, recursion_stack):
            vertex_id = vertex.get_id()
            visited.append(vertex_id)
            neighbors = vertex.get_neighbors()
            for n in neighbors:
                n_id = n.get_id()
                if n_id in visited:
                    recursion_stack.append(True)
                    return
                else:
                    recursion_stack.append(False)
                    dfs_cycle(n, visited, recursion_stack)
            return recursion_stack[-1]

        start_id = list(self.__vertex_dict.keys())[0]
        start_obj = self.get_vertex(start_id)
        visited, recursion_stack = [start_id], []
        is_cycle = dfs_cycle(start_obj, visited, recursion_stack)
        return is_cycle

    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.

        """
        # TODO: Create a stack to hold the vertex ordering.
        # TODO: For each unvisited vertex, execute a DFS from that vertex.
        # TODO: On the way back up the recursion tree (that is, after visiting a
        # vertex's neighbors), add the vertex to the stack.
        # TODO: Reverse the contents of the stack and return it as a valid ordering.

        vertexes = self.get_vertices()
        indegree_dict = {}
        for vert in vertexes:
            if vert.get_id() not in indegree_dict:
                indegree_dict[vert.get_id()] = 0
            for neighbor in vert.get_neighbors():
                neighbor_id = neighbor.get_id()
                if neighbor_id in indegree_dict:
                    indegree_dict[neighbor_id] += 1
                else:
                    indegree_dict[neighbor_id] = 1

        indeg0 = []
        for vertex_id, indegree in indegree_dict.items():
            if indegree == 0:
                indeg0.append(vertex_id)

        sorted_list = []

        while len(indeg0) > 0:
            current_id = indeg0.pop()
            sorted_list.append(current_id)
            current_vertex = self.get_vertex(current_id)
            for neighbor in current_vertex.get_neighbors():
                neighbor_id = neighbor.get_id()
                indegree_dict[neighbor_id] -= 1
                if indegree_dict[neighbor_id] == 0:
                    indeg0.append(neighbor_id)
        return sorted_list

    def find_connected_components(self):
        all_ids = set(self.__vertex_dict.keys())

        components = []

        while len(all_ids) > 0:
            start_id = list(all_ids).pop()
            all_ids.remove(start_id)
            start_vertex = self.get_vertex(start_id)
            seen = set()
            quene = [start_id]
            seen.add(start_id)
            while len(quene) > 0:
                current_id = quene.pop(0)
                current_vertex = self.get_vertex(current_id)
                for neighbor in current_vertex.get_neighbors():
                    neighbor_id = neighbor.get_id()
                    if neighbor_id in all_ids:
                        all_ids.remove(neighbor_id)
                    if neighbor_id not in seen:
                        quene.append(neighbor_id)
                        seen.add(neighbor_id)
            components.append(list(seen))
        return(components)

    def greedy_coloring(self):
        """Return a dictionary of vertex id -> color."""
        vertex_id_color = {}

        # TODO: Fill in the dictionary by visiting each vertex and checking the
        # colors of its neighbors, then assigning the “smallest” color which has
        # not yet been assigned.

        return vertex_id_color


if __name__ == "__main__":
    graph = Graph(is_directed=True)
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    # graph.add_vertex('D')
    # graph.add_vertex('E')
    # graph.add_vertex('F')
    # graph.add_vertex('G')
    # graph.add_vertex('H')
    # graph.add_vertex('Y')
    # graph.add_vertex('Z')

    graph.add_edge('A', 'B')
    # graph.add_edge('A', 'D')
    graph.add_edge('B', 'C')
    # graph.add_edge('C', 'D')
    graph.add_edge('C', 'A')

    # graph.add_edge('A', 'B')
    # graph.add_edge('A', 'E')
    # graph.add_edge('B', 'C')
    # graph.add_edge('C', 'D')
    # graph.add_edge('B', 'D')
    # graph.add_edge('E', 'F')
    # graph.add_edge('G', 'D')

    # graph.add_edge('A', 'B')
    # graph.add_edge('A', 'C')
    # graph.add_edge('B', 'C')
    # graph.add_edge('C', 'Z')
    # graph.add_edge('D', 'E')
    # graph.add_edge('E', 'F')
    # graph.add_edge('F', 'Y')
    # graph.add_edge('G', 'H')

    # print(graph.is_bipartite())
    # print(graph.get_connected_components())
    # print(graph.bfs_traversal('A'))
    # print(graph.find_path_dfs_iter('A', 'F'))
    # print(graph.topological_sort())
    print(graph.contains_cycle())
