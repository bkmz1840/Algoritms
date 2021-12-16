from collections import deque


def parse_input(path):
    with open(path) as input_file:
        data = input_file.read().split("\n")
        data = data[1:]
    graph = []
    for row in data:
        cur_row = []
        for e in row.split():
            cur_row.append(int(e))
        graph.append(cur_row)
    return graph


def fill_empty_flow(n):
    result = []
    for i in range(n):
        result.append([0 for _ in range(n)])
    return result


def find_path(source, target, f, graph):
    queue = deque([source])
    link = {target: -1}
    flow = [0 for _ in range(len(graph))]
    flow[source] = -1
    while link[target] == -1 and len(queue) > 0:
        cur_vertex = queue.popleft()
        for i in range(len(graph)):
            if (graph[cur_vertex][i] - f[cur_vertex][i]) > 0 and flow[i] == 0:
                queue.append(i)
                link[i] = cur_vertex
                if (
                    (graph[cur_vertex][i] - f[cur_vertex][i]) <
                        flow[cur_vertex]
                ):
                    flow[i] = graph[cur_vertex][i]
                else:
                    if flow[cur_vertex] == -1:
                        flow[i] = graph[cur_vertex][i]
                    else:
                        flow[i] = flow[cur_vertex]

    if link[target] == -1:
        return 0

    cur_vertex = target
    while cur_vertex != source:
        f[link[cur_vertex]][cur_vertex] += flow[target]
        cur_vertex = link[cur_vertex]
    return flow[target]


def get_max_flow(source, target, graph):
    f = fill_empty_flow(len(graph))
    max_flow = 0
    while True:
        add_flow = find_path(source, target, f, graph)
        max_flow += add_flow
        if add_flow == 0:
            break
    return max_flow


def print_output(path, result):
    with open(path, "w+") as output_file:
        output_file.write(str(result))


def main():
    graph = parse_input("input.txt")
    source = 0
    target = len(graph) - 1
    max_trains = get_max_flow(source, target, graph)
    print_output("output.txt", max_trains)


if __name__ == "__main__":
    main()
