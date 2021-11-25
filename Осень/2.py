from collections import deque


def union_lists(lists):
    result = []
    for one_list in lists:
        result += [int(e) for e in one_list.split()]
    return result


def get_empty_graph(k, l):
    result = []
    for i in range(k):
        result.append([0 for v in range(l)])
    return result


def parse_input(path_to_file):
    with open(path_to_file) as input_file:
        data = input_file.read().split("\n")
        k, l = tuple(map(int, data.pop(0).split(" ")))
        data.pop(0)

    list_nodes = union_lists(data)
    end_nodes_indexes = list_nodes[0] - 2
    result = get_empty_graph(k, l)
    nodes_indexes = deque()

    for i in range(end_nodes_indexes):
        nodes_indexes.append(list_nodes[i])
    nodes_indexes.append(list_nodes[k])

    cur_node = 0
    while len(nodes_indexes) > 1:
        i = nodes_indexes.popleft() - 1

        while i < nodes_indexes[0] - 1:
            y = list_nodes[i] - 1
            if y == -1:
                i += 1
                continue
            result[cur_node][y] = 1
            i += 1

        cur_node += 1

    return result


def search_depth_first(
    x, px, py, visited, graph,
):
    if x in visited:
        return False

    visited.add(x)
    for y, is_edge_exists in enumerate(graph[x]):
        if not is_edge_exists:
            continue

        if py[y] == -1:
            py[y] = x
            px[x] = y
            return True

        if search_depth_first(
            py[y], px, py, visited, graph,
        ):
            py[y] = x
            px[x] = y
            return True
    return False


def get_max_matching(graph):
    px = [-1 for _ in range(len(graph[0]))]
    py = [-1 for _ in range(len(graph))]
    is_path = True

    while is_path:
        is_path = False
        visited = set()
        for x in range(len(graph)):
            if px[x] == -1:
                is_path = search_depth_first(
                    x, px, py, visited, graph
                )
    return px


def is_full_matching(matching_by_x):
    for x, y in enumerate(matching_by_x):
        if y == -1:
            return False, x
    return True, None


def print_result(path_to_out, result, failed_x, matching):
    if result:
        result_output = "Y\n"
        result_output += " ".join([str(y + 1) for y in matching])
    else:
        result_output = "N\n" + str(failed_x + 1)

    with open(path_to_out, "w+") as output_file:
        output_file.write(result_output)


def main():
    graph = parse_input("input.txt")
    max_matching = get_max_matching(graph)
    result, failed_x = is_full_matching(max_matching)
    print_result("output.txt", result, failed_x, max_matching)


if __name__ == "__main__":
    main()
