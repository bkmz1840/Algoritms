from collections import deque
import os


class Edge:
    def __init__(self, left, right, weight):
        self.left_node = left
        self.right_node = right
        self.weight = weight

    def __str__(self):
        return f"{self.left_node} -> {self.right_node} ({self.weight})"


class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, other_node, weight):
        self.edges.append(Edge(self, other_node, weight))

    def __str__(self):
        return str(self.name)


class Graph:
    def __init__(self):
        self.nodes = []

    def add_nodes(self, count):
        for i in range(1, count + 1):
            self.nodes.append(Node(i))

    def add_edge_to_node(self, name_node, name_adjacent_node,
                         weight):
        self.nodes[name_node - 1]\
            .add_edge(self.nodes[name_adjacent_node - 1], weight)

    def get_node_by_name(self, name):
        return self.nodes[name - 1]


def init_graph(path):
    with open(path) as file:
        data = file.read().split('\n')
    count_nodes = int(data[0])
    result = Graph()
    result.add_nodes(count_nodes)
    for i in range(1, len(data) - 2):
        row = list(map(int, data[i].split()))
        for j in range(0, len(row)):
            if row[j] == -32768:
                continue
            result.add_edge_to_node(i, j + 1, row[j])
    start_node = int(data[-2])
    finish_node = int(data[-1])
    return result, start_node, finish_node


def make_search_in_deep(node, nodes):
    stack = deque()
    stack.append(node)
    visited_nodes = set()
    while len(stack) > 0:
        current_node = stack.pop()
        if current_node.name in visited_nodes \
                or current_node.name in nodes["grey"] \
                or current_node.name in nodes["black"]:
            continue
        nodes["white"].remove(current_node.name)
        nodes["grey"].add(current_node.name)
        visited_nodes.add(current_node.name)
        for edge in current_node.edges:
            stack.append(edge.right_node)


def top_sort(graph: Graph, start):
    nodes = {
        "white": set(),
        "grey": set(),
        "black": set()
    }
    for node in graph.nodes:
        nodes["white"].add(node.name)
    k = len(graph.nodes)
    numbers_nodes = {}
    while len(nodes["white"]) > 0:
        if len(nodes["white"]) == len(graph.nodes):
            current_white_node_name = start
            nodes["white"].remove(start)
        else:
            current_white_node_name = nodes["white"].pop()
        current_white_node = graph.get_node_by_name(
            current_white_node_name)
        nodes["white"].add(current_white_node_name)
        make_search_in_deep(current_white_node, nodes)
        while len(nodes["grey"]) > 0:
            node_name = nodes["grey"].pop()
            node = graph.get_node_by_name(int(node_name))
            if is_node_black(node, nodes):
                nodes["black"].add(node.name)
                numbers_nodes[node_name] = k
                k -= 1
    return numbers_nodes


def rename_nodes(graph: Graph, names):
    old_names = {}
    for node in graph.nodes:
        new_name = names[node.name]
        old_names[new_name] = node.name
        node.name = new_name
    graph.nodes.sort(key=lambda n: n.name)
    return old_names


def is_node_black(node, nodes):
    if len(node.edges) == 0:
        return True
    for edge in node.edges:
        right_node_name = edge.right_node.name
        if right_node_name not in nodes["grey"] \
                and right_node_name not in nodes["black"]:
            return False
    return True


def search_max_path(graph, start_node, finish_node):
    d = [0]
    prev = [0]
    count_nodes = len(graph.nodes)
    for k in range(1, count_nodes):
        d.append(-1)
        prev.append(-1)
    for k in range(0, count_nodes - 1):
        for edge in graph.nodes[k].edges:
            v = edge.right_node.name - 1
            if d[k] + edge.weight > d[v]:
                d[v] = d[k] + edge.weight
                prev[v] = k
    path = []
    cur_node = finish_node - 1
    sum_weights = d[cur_node]
    while True:
        if cur_node == -1:
            return None, 0
        path.append(cur_node + 1)
        if cur_node == start_node - 1:
            return path, sum_weights
        cur_node = prev[cur_node]


def rename_nodes_in_path(path, names):
    result = []
    for node in path:
        result.append(names[node])
    return result[::-1]


def main():
    graph, start_node, finish_node = init_graph("./input.txt")
    new_nodes_names = top_sort(graph, finish_node)
    old_names = rename_nodes(graph, new_nodes_names)
    start_node = new_nodes_names[start_node]
    finish_node = new_nodes_names[finish_node]
    path, sum_weights = search_max_path(graph, start_node, finish_node)
    if path is None:
        print("N")
    else:
        print(rename_nodes_in_path(path, old_names))
        print(sum_weights)


if __name__ == '__main__':
    print(os.environ.get("DJANGO_PLACE_REMEMBER_TOKEN"))
