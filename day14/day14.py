from enum import Enum
import numpy as np


WIDTH = 400  # from a glance a the input
HEIGHT = 200
W_OFFSET = int(500 - WIDTH / 2)  # value to be removed from all x coordinate from input
SAND_START = [500 - W_OFFSET, 0]


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    t = Topology(lines)
    sand_units = t.drop_sand()
    print("Sand units: {}".format(sand_units))
    t = Topology(lines, floor=True)
    sand_units = t.drop_sand()
    print("Sand units with floor: {}".format(sand_units))


class Topology:
    class Material(Enum):
        AIR = 0,
        ROCK = 1
        SAND = 2

    def __init__(self, input, floor=False):
        self.haz_floor = False
        self.topology = [[Topology.Material.AIR for x in range(WIDTH)] for y in range(HEIGHT)]
        self.parse(input)
        if floor:
            self._insert_floor()

    def parse(self, input):
        self.deepest_rock_y = 0
        for line in input:
            line = line.rstrip().split(" -> ")
            prev_pair = None
            for pair in line:
                next_pair = list(map(lambda i: int(i), pair.split(",")))
                if next_pair[1] > self.deepest_rock_y:
                    self.deepest_rock_y = next_pair[1]
                next_pair[0] -= W_OFFSET
                if prev_pair is None:
                    prev_pair = next_pair
                    continue
                x_diff = next_pair[0] - prev_pair[0]
                y_diff = next_pair[1] - prev_pair[1]
                if x_diff != 0:
                    sign = np.sign(x_diff)
                    for x in range(prev_pair[0], next_pair[0] + sign, sign):
                        self.set_material([x, next_pair[1]], Topology.Material.ROCK)
                else:
                    sign = np.sign(y_diff)
                    for y in range(prev_pair[1], next_pair[1] + sign, sign):
                        self.set_material([next_pair[0], y], Topology.Material.ROCK)
                prev_pair = next_pair

    def _insert_floor(self):
        for x in range(WIDTH):
            self.set_material([x, self.deepest_rock_y + 2], Topology.Material.ROCK)
        self.haz_floor = True

    def get_material(self, coordinates):
        return self.topology[coordinates[1]][coordinates[0]]

    def set_material(self, coordinates, material):
         self.topology[coordinates[1]][coordinates[0]] = material

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
            self.set_material(sand, Topology.Material.SAND)
        if not self.haz_floor:
            return sand[1] >= HEIGHT - 1
        else:
            return sand == SAND_START

    def drop_sand(self):
        count = 0
        while True:
            if not self.haz_floor:
                fell_out = self._drop_one_sand()
                if fell_out:
                    break
                count += 1
            else:
                count += 1
                filled_up = self._drop_one_sand()
                if filled_up:
                    break

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
    t = Topology(example_input, floor=True)
    sand_units = t.drop_sand()
    assert(sand_units == 93)
    print("unit tests passed")


if __name__ == '__main__':
    main()
