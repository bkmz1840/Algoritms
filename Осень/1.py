from collections import deque

_ = float("inf")


def union_lists(lists):
    result = []
    for one_list in lists:
        result += [int(e) for e in one_list.split()]
    return result


def get_empty_graph(count_nodes):
    result = []
    for i in range(count_nodes):
        result.append([_ for v in range(count_nodes)])
    return result


def parse_input(path_to_file):
    with open(path_to_file) as input_file:
        data = input_file.read().split("\n")
        data.pop(0)

    list_nodes = union_lists(data)
    end_nodes_indexes = list_nodes[0] - 2
    result = get_empty_graph(end_nodes_indexes)
    nodes_indexes = deque()

    for i in range(end_nodes_indexes):
        nodes_indexes.append(list_nodes[i])

    cur_node = 0
    while len(nodes_indexes) > 0:
        i = nodes_indexes.popleft() - 1

        while (
            len(nodes_indexes) > 0 and
            i < nodes_indexes[0] - 1 or
            len(nodes_indexes) == 0 and
            i < len(list_nodes) - 1
        ):
            result[cur_node][list_nodes[i] - 1] = list_nodes[i + 1]
            i += 2

        cur_node += 1

    return result


def get_min_ostov(graph):
    nodes_count = len(graph)
    free_vertex = deque(range(nodes_count))
    tied = [free_vertex.popleft()]
    road_length = 0
    result = []
    while free_vertex:
        min_link = None
        overall_min_path = _

        for cur_vertex in tied:
            weights = graph[cur_vertex]
            min_path = _
            free_vertex_min = cur_vertex

            for v in range(nodes_count):
                path = weights[v]

                if path == _:
                    continue

                if v in free_vertex and path < min_path:
                    free_vertex_min = v
                    min_path = path

            if free_vertex_min != cur_vertex:
                if overall_min_path > min_path:
                    min_link = (cur_vertex, free_vertex_min)
                    overall_min_path = min_path

        try:
            path_length = graph[min_link[0]][min_link[1]]
        except TypeError:
            print("Unable to find path")
            return

        road_length += path_length
        free_vertex.remove(min_link[1])
        tied.append(min_link[1])
        result.append(min_link)

    return result, road_length


def find_into_tuples_list(first_item, tuples_list):
    for e in tuples_list:
        if e[0] == first_item:
            return e
    return None


def add_back_edges(edges):
    return edges + [(e[1], e[0]) for e in edges]


def print_output(result, weight, count_vortexes, path_to_file):
    sorted_result = sorted(add_back_edges(result), key=lambda e: e[0])
    out = ""
    for vortex_number in range(count_vortexes):
        paths = deque(sorted_result)

        out += f"{vortex_number}: {vortex_number} -> "
        cur_vortex = vortex_number
        visited_nodes = {cur_vortex}
        while len(paths) > 0:
            edge = find_into_tuples_list(cur_vortex, paths)
            if not edge:
                break

            if edge[1] in visited_nodes:
                paths.remove(edge)
                continue

            cur_vortex = edge[1]
            out += f"{edge[1]} -> "
            paths.remove(edge)
            visited_nodes.add(edge[1])

        out += "n\n"

    out += str(weight)
    with open(path_to_file, "w+") as output_file:
        output_file.write(out)


def main():
    graph = parse_input("input.txt")
    result, weight = get_min_ostov(graph)
    count_nodes = len(graph)
    print_output(result, weight, count_nodes, "output.txt")


if __name__ == "__main__":
    main()
