from enum import Enum
import numpy as np


WIDTH = 200  # from a glance a the input
HEIGHT = 200
W_OFFSET = 400  # value to be removed from all x coordinate from input
SAND_START = [500 - W_OFFSET, 0]


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    t = Topology(lines)
    sand_units = t.drop_sand()
    print("Sand units: {}".format(sand_units))


class Topology:
    class Material(Enum):
        AIR = 0,
        ROCK = 1
        SAND = 2

    def __init__(self, input):
        self.topology = [[Topology.Material.AIR for x in range(WIDTH)] for y in range(HEIGHT)]
        self.parse(input)

    def parse(self, input):
        for line in input:
            line = line.rstrip().split(" -> ")
            prev_pair = None
            for pair in line:
                next_pair = list(map(lambda i: int(i), pair.split(",")))
                next_pair[0] -= W_OFFSET
                if prev_pair is None:
                    prev_pair = next_pair
                    continue
                x_diff = next_pair[0] - prev_pair[0]
                y_diff = next_pair[1] - prev_pair[1]
                if x_diff != 0:
                    sign = np.sign(x_diff)
                    for x in range(prev_pair[0], next_pair[0] + sign, sign):
                        self.topology[next_pair[1]][x] = Topology.Material.ROCK
                else:
                    sign = np.sign(y_diff)
                    for y in range(prev_pair[1], next_pair[1] + sign, sign):
                        self.topology[y][next_pair[0]] = Topology.Material.ROCK
                prev_pair = next_pair

    def get_material(self, coordinates):
        return self.topology[coordinates[1]][coordinates[0]]

    def _drop_one_sand(self):
        sand = SAND_START
        moved = True
        while sand[1] < HEIGHT - 1 and moved:
            moved = False
            for x_delta in [0, -1, +1]:  # under, under-left, under-right
                moved = False
                under = [sand[0] + x_delta, sand[1] + 1]
                if self.get_material(under) == Topology.Material.AIR:
                    sand = under
                    moved = True
                    break
        if not moved:
            self.topology[sand[1]][sand[0]] = Topology.Material.SAND
        return sand[1] >= HEIGHT - 1

    def drop_sand(self):
        count = 0
        while True:
            fell_out = self._drop_one_sand()
            if fell_out:
                break
            count += 1

        return count


    def __str__(self):
        s = ""
        for row_idx, row in enumerate(self.topology):
            s += "|"
            for col_idx, col in enumerate(row):
                if col_idx == SAND_START[0] and row_idx == SAND_START[1]:
                    s += "+"
                elif col == Topology.Material.AIR:
                    s += "."
                elif col == Topology.Material.ROCK:
                    s += "#"
                else:
                    s+= "o"
            s += "|\n"
        return s



def unit_test():
    example_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".splitlines()
    t = Topology(example_input)
    sand_units = t.drop_sand()
    assert(sand_units == 24)
    print("unit tests passed")


if __name__ == '__main__':
    main()
