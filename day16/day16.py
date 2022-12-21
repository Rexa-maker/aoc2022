import re


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    tunnels = Tunnels(lines)
    best_solution = tunnels.prune_early(start_time=Tunnels.ALONE_STARTING_TIME, num_parallels=1)
    print("Best solution {} tallies pressure {}".format(str(best_solution), int(best_solution)))
    best_solution = tunnels.prune_early(start_time=Tunnels.ELEPHANT_STARTING_TIME, num_parallels=2)
    print("Best solution {} tallies pressure {}".format(str(best_solution), int(best_solution)))


class Tunnels:
    class Valve:
        REGEXP = re.compile(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")

        def __init__(self, tunnels: "Tunnels", input):
            self.tunnels = tunnels
            self.input = input

            m = Tunnels.Valve.REGEXP.match(input)
            assert(m)
            self.name = m.group(1)
            self.flow = int(m.group(2))
            self.others_names = m.group(3).split(", ")

            self.distances = {}

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
        def __init__(self, other : "Tunnels", num_parallels=None, start_time=None):
            if isinstance(other, Tunnels):
                assert(num_parallels is not None and start_time is not None)
                self.valves = [[]] * num_parallels
                self.tunnels = other
                self.remaining_time = [start_time] * num_parallels
                self.total_pressure = 0
            elif isinstance(other, Tunnels.Solution):
                self.valves = [other.valves[i].copy() for i in range(len(other.valves))]
                self.tunnels = other.tunnels
                self.remaining_time = other.remaining_time.copy()
                self.total_pressure = other.total_pressure
            else:
                assert(False)

        def add_valve(self, valve : "Tunnels.Valve", parralel_index):
            """ Return true iff there is enough time to go and open the added valve and thus the valve was added to the solution"""
            last_valve = self.tunnels.valves[Tunnels.START_VALVE] if self.valves[parralel_index] == [] else self.valves[parralel_index][-1]

            time_cost = last_valve.distances[valve.name] + 1
            if time_cost > self.remaining_time[parralel_index]:
                return False

            self.valves[parralel_index].append(valve)
            self.remaining_time[parralel_index] -= time_cost
            self.total_pressure += self.remaining_time[parralel_index] * valve.flow
            return True

        def __iter__(self):
            """ Iterate over all the valves in the solution """
            for valve in self.valves:
                yield valve

        def __int__(self):
            """ Casting a solution to int returns its total pressure """
            return self.total_pressure

        def __str__(self):
            if len(self.valves) == 1:
                return " -> ".join([valve.name for valve in self.valves[0]])
            return ", ".join([" -> ".join([valve.name for valve in self.valves[i]]) for i in range(len(self.valves))])

    ALONE_STARTING_TIME = 30
    ELEPHANT_STARTING_TIME = 26
    START_VALVE = "AA"

    def __init__(self, input):
        self.valves = {}
        for line in [line.rstrip() for line in input]:
            if len(line) == 0:
                continue
            valve = Tunnels.Valve(self, line)
            self.valves[valve.name] = valve
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

    def get_useful_valves(self):
        """ return a list of the useful valves """
        useful_valves = []
        for valve in self:
            if int(valve) != 0:
                useful_valves.append(valve)
        return useful_valves

    def yield_solutions_for_remaining_valves(self, solution_so_far, remaining_valves, num_parallels):
        extended_solution = False
        for parralel_index in range(num_parallels):
            for idx, valve in enumerate(remaining_valves):
                solution = Tunnels.Solution(solution_so_far)  # Clone solution
                if solution.add_valve(valve, parralel_index=parralel_index):
                    extended_solution = True
                    remaining_valves_without_added = remaining_valves[0:idx] + remaining_valves[idx+1:]
                    yield from self.yield_solutions_for_remaining_valves(solution_so_far=solution,
                                                                         remaining_valves=remaining_valves_without_added,
                                                                         num_parallels=num_parallels)

        if not extended_solution:
            yield solution_so_far

    def prune_early(self, start_time, num_parallels):
        useful_valves = self.get_useful_valves()
        print("{} useful valves found".format(len(useful_valves)))

        best_solution = None
        idx = 0
        # More lines = safer job
        initial_solution = Tunnels.Solution(self,
                                            start_time=start_time,
                                            num_parallels=num_parallels)
        for solution in self.yield_solutions_for_remaining_valves(solution_so_far=initial_solution,
                                                                  remaining_valves=useful_valves,
                                                                  num_parallels=num_parallels):
            print("Found solution {}: {} {}".format(idx, int(solution), str(solution)))
            if best_solution is None or int(best_solution) < int(solution):
                best_solution = solution
            idx += 1
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
    best_solution = tunnels.prune_early(start_time=Tunnels.ALONE_STARTING_TIME, num_parallels=1)
    assert(str(best_solution) == "DD -> BB -> JJ -> HH -> EE -> CC")
    assert(int(best_solution) == 1651)
    best_solution = tunnels.prune_early(start_time=Tunnels.ELEPHANT_STARTING_TIME, num_parallels=2)
    assert(str(best_solution) == "DD -> HH -> EE, JJ -> BB -> CC")
    assert(int(best_solution) == 1707)
    print("unit tests passed")


if __name__ == '__main__':
    main()
