from collections import deque


class FigureCoordinates:
    def __init__(self, horizontal, vertical):
        self.horizontal = int(horizontal)
        if isinstance(vertical, str):
            vertical = FigureCoordinates.get_int_by_str_vertical(vertical)
        self.vertical = vertical

    def __eq__(self, other):
        return self.horizontal == other.horizontal \
               and self.vertical == other.vertical

    def __str__(self):
        return FigureCoordinates \
                   .get_str_vertical_by_int(self.vertical) + \
                   str(self.horizontal)

    @staticmethod
    def get_int_by_str_vertical(str_vertical):
        pairs = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8
        }
        return pairs[str_vertical]

    @staticmethod
    def get_str_vertical_by_int(int_vertical):
        pairs = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h",
        }
        return pairs[int_vertical]


class SingleLinkedList:
    def __init__(self, value, prev):
        self.value = value
        self.prev = prev

    def __str__(self):
        result = []
        current_point = self
        while current_point.prev is not None:
            result.append(str(current_point.value))
            current_point = current_point.prev
        result_str = ""
        for step in reversed(result):
            result_str += step + "\n"
        return result_str


def init_figures(path):
    with open(path) as file:
        inputData = file.read().split("\n")
    if len(inputData) < 2:
        raise SyntaxError("Invalid input")
    str_coords_horse = inputData[0].strip()
    horse = FigureCoordinates(str_coords_horse[1], str_coords_horse[0])
    str_coords_pawn = inputData[1].strip()
    if str_coords_pawn[1] == "1" or str_coords_pawn[1] == "8":
        raise SyntaxError("Invalid pawn horizontal")
    pawn = FigureCoordinates(str_coords_pawn[1], str_coords_pawn[0])
    return horse, pawn


def get_death_points_for_horse(pawn):
    first_point = FigureCoordinates(pawn.horizontal - 1, pawn.vertical - 1)
    second_point = FigureCoordinates(pawn.horizontal - 1, pawn.vertical + 1)
    return first_point, second_point


def take_step_horse(stack: deque, position: SingleLinkedList):
    position_coords = position.value
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal + 1, position_coords.vertical - 2),
        position))
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal - 1, position_coords.vertical - 2),
        position))
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal - 2, position_coords.vertical - 1),
        position))
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal - 2, position_coords.vertical + 1),
        position))
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal - 1, position_coords.vertical + 2),
        position))
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal + 1, position_coords.vertical + 2),
        position))
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal + 2, position_coords.vertical + 1),
        position))
    stack.append(SingleLinkedList(FigureCoordinates(
        position_coords.horizontal + 2, position_coords.vertical - 1),
        position))


def find_path(horse: FigureCoordinates, pawn: FigureCoordinates):
    stack = deque()
    death_horse_points = get_death_points_for_horse(pawn)
    visited_points = set()
    stack.append(SingleLinkedList(horse, None))
    while len(stack) != 0:
        current_point = stack.pop()
        point_coords = current_point.value
        if 1 > point_coords.horizontal or point_coords.horizontal > 8 \
                or 1 > point_coords.vertical or point_coords.vertical > 8:
            continue
        if point_coords == death_horse_points[0] \
                or point_coords == death_horse_points[1] \
                or str(point_coords) in visited_points:
            continue
        visited_points.add(str(point_coords))
        if point_coords == pawn:
            return current_point
        take_step_horse(stack, current_point)


def write_result(path_to_file, result_path):
    with open(path_to_file, "w") as file:
        file.write(result_path)


def main():
    horse, pawn = init_figures("./input.txt")
    path_horse_to_pawn = find_path(horse, pawn)
    str_result_path = str(horse) + "\n" + str(path_horse_to_pawn)
    write_result("./output.txt", str_result_path)


if __name__ == '__main__':
    main()
