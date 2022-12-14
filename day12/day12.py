def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()

    hill_climbing = HillClimbing(lines)
    shortest_steps = hill_climbing.shortest_steps_from_start()
    print("Shortest steps from start: {}".format(str(shortest_steps)))
    shortest_steps = hill_climbing.shortest_steps_from_any_low()
    print("Shortest steps from any low: {}".format(str(shortest_steps)))


class HillClimbing:
    MIN_ELEVATION = ord('a') - ord('a')
    MAX_ELEVATION = ord('z') - ord('a')


    class Elevation:
        def __init__(self, x, y, altitude, hill_climbing):
            self.x = x
            self.y = y
            self.altitude = altitude
            self.hill_climbing = hill_climbing
            self.shortest_steps = None  # shortest steps to end

        def iter_neighbors(self):
            for x in [self.x - 1, self.x + 1]:
                if x < 0 or x >= self.hill_climbing.width:
                    continue
                yield (x, self.y)
            for y in [self.y - 1, self.y + 1]:
                if y < 0 or y >= self.hill_climbing.height:
                    continue
                yield (self.x, y)

        def update_neighbors_steps(self):
            """ Return a set of the neighbors to re-explore """
            assert(self.shortest_steps is not None)  # Do not call on an unexplored elevation
            neighbors_to_update = set()
            for neighbor in self.iter_neighbors():
                neighbor = self.hill_climbing.elevations[neighbor[1]][neighbor[0]]
                if self.altitude - neighbor.altitude <= 1:  # Can we climb (or fall) to self from neighbor
                    neighbor_visited = neighbor.shortest_steps is not None
                    if neighbor.shortest_steps is None or neighbor.shortest_steps > self.shortest_steps + 1:
                        neighbor.shortest_steps = self.shortest_steps + 1
                        # Re-explore update
                        neighbors_to_update.add(neighbor)
            return neighbors_to_update


    def __init__(self, input):
        self.parse_input(input)

    def parse_input(self, input):
        self.width = len(input[0].rstrip())
        self.height = len(input)
        # Access with [y][x] or [row_idx][col_idx]
        self.elevations = [[None for x in range(self.width)] for y in range(self.height)]
        row_idx = 0
        for line in input:
            line = line.rstrip()
            col_idx = 0
            for c in line:
                elevation = 0
                if c == 'S':
                    self.start = (col_idx, row_idx)
                elif c == 'E':
                    self.end = (col_idx, row_idx)
                    elevation = HillClimbing.MAX_ELEVATION
                else:
                    elevation = ord(c) - ord('a')
                self.elevations[row_idx][col_idx] = HillClimbing.Elevation(x=col_idx, y=row_idx, altitude=elevation, hill_climbing=self)
                col_idx += 1
            row_idx += 1

    def discover_all_shortest_steps(self):
        end = self.elevations[self.end[1]][self.end[0]]
        end.shortest_steps = 0
        neighbors_to_update = end.update_neighbors_steps()
        while True:
            if len(neighbors_to_update) == 0:
                break
            neighbor = neighbors_to_update.pop()
            neighbors_to_update = neighbors_to_update.union(neighbor.update_neighbors_steps())

    def shortest_steps_from_start(self):
        self.discover_all_shortest_steps()
        return self.elevations[self.start[1]][self.start[0]].shortest_steps

    def shortest_steps_from_any_low(self):
        self.discover_all_shortest_steps()
        shortest_steps = None
        for x in range(self.width):
            for y in range(self.height):
                elevation = self.elevations[y][x]
                if elevation.altitude == 0 and elevation.shortest_steps is not None and (shortest_steps is None or elevation.shortest_steps < shortest_steps):
                    shortest_steps = elevation.shortest_steps
        return shortest_steps


def unit_test():
    assert(HillClimbing.MIN_ELEVATION == 0)
    assert(HillClimbing.MAX_ELEVATION == 25)

    example_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".splitlines()
    hill_climbing = HillClimbing(example_input)
    assert(hill_climbing.width == 8)
    assert(hill_climbing.height == 5)
    shortest_steps = hill_climbing.shortest_steps_from_start()
    assert(shortest_steps == 31)
    shortest_steps = hill_climbing.shortest_steps_from_any_low()
    assert(shortest_steps == 29)
    print("unit tests passed")


if __name__ == '__main__':
    main()
