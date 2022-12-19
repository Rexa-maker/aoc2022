import re
from itertools import permutations


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    tunnels = Tunnels(lines)
    best_solution = tunnels.brute_force()
    print("Best solution {} tallies pressure {}".format(str(best_solution), int(best_solution)))


class Tunnels:
    class Valve:
        REGEXP = re.compile(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")

        def __init__(self, tunnels: "Tunnels", input):
            self.tunnels = tunnels
            self.input = input
            self.open = False

            m = Tunnels.Valve.REGEXP.match(input)
            assert(m)
            self.name = m.group(1)
            self.flow = int(m.group(2))
            self.others_names = m.group(3).split(", ")

            self.distances = {}

        def reset(self):
            self.open = False

        def update_distance_to_valve(self, valve: "Tunnels.Valve", distance):
            if valve.name not in self.distances or self.distances[valve.name] > distance:
                self.distances[valve.name] = distance
                for neighbor in self:
                    neighbor.update_distance_to_valve(valve, distance + 1)

        def __iter__(self):
            """ Iterate on neighbors """
            for other in self.others_names:
                yield self.tunnels.get_valve(other)

        def __int__(self):
            return self.flow

        def __str__(self):
            return self.input

    class Solution:
        def __init__(self, tunnels : "Tunnels"):
            self.valves = []
            self.tunnels = tunnels

        @property
        def time_cost(self):
            time = 0
            valve = self.tunnels.valves[Tunnels.START_VALVE]
            for next_valve in self:
                time += valve.distances[next_valve.name] + 1  # go there, open the valve
                valve = next_valve
            return time

        def add_valve(self, valve):
            """ Return true iff there is enough time to go and open the added valve and thus the valve was added to the solution"""
            remaining_time = Tunnels.STARTING_TIME - self.time_cost
            if len(self.valves) > 0 and valve.distances[self.valves[-1].name] + 1 > remaining_time:
                return False
            self.valves.append(valve)
            return True

        def __iter__(self):
            """ Iterate over all the valves in the solution """
            for valve in self.valves:
                yield valve

        def __int__(self):
            """ Casting a solution to int returns its total pressure """
            pressure = 0
            remaining_time = Tunnels.STARTING_TIME
            valve = self.tunnels.valves[Tunnels.START_VALVE]
            for next_valve in self:
                remaining_time -= valve.distances[next_valve.name] + 1
                pressure += int(next_valve) * remaining_time
                valve = next_valve
            assert(remaining_time >= 0)
            return pressure

        def __str__(self):
            return " -> ".join([valve.name for valve in self.valves])

    STARTING_TIME = 30
    START_VALVE = "AA"

    def __init__(self, input):
        self.valves = {}
        for line in [line.rstrip() for line in input]:
            if len(line) == 0:
                continue
            valve = Tunnels.Valve(self, line)
            self.valves[valve.name] = valve
        self.reset_puzzle()
        self.find_all_distances()

    def __str__(self):
        return "\n".join([str(valve) for valve in self])

    def __iter__(self):
        for valve in self.valves.values():
            yield valve

    def find_all_distances(self):
        for valve in self:
            valve.update_distance_to_valve(valve, 0)

    def get_valve(self, name):
        return self.valves[name]

    def reset_puzzle(self):
        self.current_valve = None
        for valve in self:
            valve.reset()
            if valve.name == Tunnels.START_VALVE:
                self.current_valve = valve
        assert(self.current_valve is not None)
        self.remaining_time = Tunnels.STARTING_TIME

    def get_useful_valves(self):
        """ return a list of the useful valves """
        useful_valves = []
        for valve in self:
            if int(valve) != 0:
                useful_valves.append(valve)
        return useful_valves

    def brute_force(self):
        best_pressure = 0
        best_solution = None

        useful_valves = self.get_useful_valves()
        print("{} useful valves found".format(len(useful_valves)))
        possible_orders = set()
        for permutation in permutations(useful_valves, len(useful_valves)):
            possible_orders.add(tuple(permutation))
        print("Found {} possible solutions".format(len(possible_orders)))
        for idx, possible_order in enumerate(possible_orders):
            solution = Tunnels.Solution(self)
            for valve in possible_order:
                if not solution.add_valve(valve):
                    break
            solution_pressure = int(solution)
            print("Solution #{} {} total pressure: {}".format(idx, solution, solution_pressure))
            if solution_pressure > best_pressure:
                best_pressure = solution_pressure
                best_solution = solution

        return best_solution

def unit_test():
    example_input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".splitlines()
    tunnels = Tunnels(example_input)
    best_solution = tunnels.brute_force()
    assert(str(best_solution) == "DD -> BB -> JJ -> HH -> EE -> CC")
    assert(int(best_solution) == 1651)
    print("unit tests passed")


if __name__ == '__main__':
    main()
