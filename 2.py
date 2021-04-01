from collections import deque


class Edge:
    def __init__(self, left, right):
        self.left_node = left
        self.right_node = right


class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, other_node):
        self.edges.append(Edge(self, other_node))

    def __str__(self):
        return self.name


class Graph:
    def __init__(self):
        self.nodes = []

    def add_nodes(self, count):
        for i in range(1, count + 1):
            self.nodes.append(Node(str(i)))

    def add_edge_to_node(self, name_node, name_adjacent_node):
        self.nodes[name_node - 1]\
            .add_edge(self.nodes[name_adjacent_node - 1])

    def get_node_by_name(self, name):
        return self.nodes[name - 1]


def init_graph(path):
    with open(path) as file:
        data = file.read().split('\n')
    graph = Graph()
    count_nodes = int(data[0])
    graph.add_nodes(count_nodes)
    for i in range(1, count_nodes + 1):
        for name_adjacent_node in data[i].split():
            if name_adjacent_node == "0":
                continue
            graph.add_edge_to_node(i, int(name_adjacent_node))
    return graph


def check_is_adjacent_nodes_visited(node, visited_node):
    for edge in node.edges:
        if str(edge.right_node) not in visited_node:
            return False
    return True


def get_node_in_next_connectivity_component(visited_nodes, graph):
    for i in range(1, len(graph.nodes) + 1):
        if str(i) not in visited_nodes:
            return graph.get_node_by_name(i)
    return None


def add_adjacent_nodes(node, queue, visited_node):
    for edge in node.edges:
        adjacent_node = edge.right_node
        if str(adjacent_node) in visited_node:
            continue
        queue.append(edge.right_node)


def get_count_connectivity_components(graph):
    queue = deque()
    visited_nodes = set()
    queue.append(graph.get_node_by_name(1))
    current_connectivity_component = []
    result = []
    while len(queue) != 0:
        current_node = queue.popleft()
        if str(current_node) in visited_nodes:
            if len(queue) == 0:
                result.append(current_connectivity_component)
                return result
            continue
        visited_nodes.add(str(current_node))
        current_connectivity_component.append(current_node)
        if len(queue) == 0 and check_is_adjacent_nodes_visited(
                current_node, visited_nodes):
            result.append(current_connectivity_component)
            current_connectivity_component = []
            next_node = get_node_in_next_connectivity_component(
                visited_nodes, graph)
            if next_node is None:
                return result
            queue.append(next_node)
        else:
            add_adjacent_nodes(current_node, queue, visited_nodes)


def format_result(result):
    formatted_result = str(len(result)) + "\n"
    for connectivity_component in result:
        connectivity_component.sort(key=lambda node: int(node.name))
        formatted_result += " ".join(map(str, connectivity_component)) + " 0\n"
    return formatted_result


def write_result(path_to_file, result):
    with open(path_to_file, "w") as file:
        file.write(format_result(result))


def main():
    graph = init_graph("./input.txt")
    result = get_count_connectivity_components(graph)
    write_result("./output.txt", result)


if __name__ == "__main__":
    main()
