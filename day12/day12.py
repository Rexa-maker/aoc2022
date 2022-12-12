def main():
    unit_test()

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
            print("exploring x {} y {} shortest steps {} altitude {}".format(str(self.x), str(self.y), str(self.shortest_steps), str(self.altitude)))
            assert(self.shortest_steps is not None)  # Do not call on an unexplored elevation
            for neighbor in self.iter_neighbors():
                neighbor = self.hill_climbing.elevations[neighbor[1]][neighbor[0]]
                print("considering neighbor x {} y {} altitude {}".format(str(neighbor.x), str(neighbor.y), str(neighbor.altitude)))
                if self.altitude - neighbor.altitude <= 1:  # Can we climb to self from neighbor
                    neighbor_visited = neighbor.shortest_steps is not None
                    if not neighbor.shortest_steps or neighbor.shortest_steps > self.shortest_steps + 1:
                        neighbor.shortest_steps = self.shortest_steps + 1
                        # Re-update neighbor's
                        neighbor.update_neighbors_steps()

        def __str__(self):
            return str(self.altitude)

    def __init__(self, input):
        self.parse_input(input)

    def parse_input(self, input):
        self.width = len(input[0].rstrip())
        self.height = len(input)
        print("{}x{}".format(str(self.width), str(self.height)))
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

    def shortest_steps(self):
        end = self.elevations[self.end[1]][self.end[0]]
        end.shortest_steps = 0
        end.update_neighbors_steps()
        return self.elevations[self.start[1]][self.start[1]].shortest_steps

    def __str__(self):
        lines = [[str(self.elevations[y][x]) for x in range(self.width)] for y in range(self.height)]
        res = ""
        for line in lines:
            res += str(line) + "\n"
        return res

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
    print(hill_climbing)
    shortest_steps = hill_climbing.shortest_steps()
    print("shortest from start {}".format(str(shortest_steps)))
    assert(shortest_steps == 31)
    print("unit tests passed")


if __name__ == '__main__':
    main()
