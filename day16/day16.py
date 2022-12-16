import re
from itertools import combinations


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    # TODO


# TODO
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
            self.others = m.group(3).split(", ")

        def reset(self):
            self.open = False

        def __iter__(self):
            """ Iterate on neighbors """
            for other in self.others:
                yield self.tunnels.get_valve(other)

        def __int__(self):
            return self.flow

        def __str__(self):
            return self.input

    class Solution:
        def __init__(self, tunnels : "Tunnels"):
            # list of names of traversed valves, repeated name for an opening action
            # the idea is to get a "unique solution string" that can be hashed and placed in a set
            self.valves_names = ""
            self.tunnels = tunnels

        @property
        def time_cost(self):
            return len([valve for valve in self])

        def add_valve(self, valve):
            name = valve.name if isinstance(valve, Tunnels.Valve) else valve
            self.valves_names += " {}".format(name)
            assert(self.time_cost <= Tunnels.STARTING_TIME)

        def __iter__(self):
            """ Iterate over all the valves in the solution """
            for name in self.valves_names.split(" "):
                yield self.tunnels.get_valve(name)

        def __int__(self):
            """ Casting a solution to int returns its total pressure """
            pressure = 0
            remaining_time = Tunnels.STARTING_TIME
            current_valve_name = Tunnels.START_VALVE
            for name in self.valves_names.split(" "):
                valve = self.tunnels.get_valve(name)
                if name == current_valve_name:
                    pressure += int(valve) * remaining_time
                else:
                    current_valve_name = name
                remaining_time -= 1
                assert(remaining_time >= 0)
            return pressure

        def __str__(self):
            return self.valves_names

    STARTING_TIME = 30
    START_VALVE = "AA"

    def __init__(self, input):
        self.valves = {}
        for line in [line.rstrip() for line in input]:
            if len(line) == 0:
                continue
            valve = Tunnels.Valve(self, line)
            self.valves[valve.name] = valve
        for valve in self:
            pass  # TODO
        self.reset_puzzle()

    def __str__(self):
        return "\n".join([str(valve) for valve in self])

    def __iter__(self):
        for valve in self.valves.values():
            yield valve

    def all_open(self):
        """ All the valves worth opening are open """
        for valve in self:
            if int(valve) != 0 and not valve.open:
                return False
        return True

    def get_valve(self, name):
        return self.valves[name]

    def reset_puzzle(self):
        self.current_valve = None
        for valve in self:
            valve.reset()
            print(valve)
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
        tested_solutions = set()

        useful_valves = self.get_useful_valves()
        possible_orders = list()
        for n in range(len(useful_valves), 0, -1):
            possible_orders += list(combinations(useful_valves, n))
        print("\n".join(" ".join(valve.name for valve in order) for order in possible_orders))
        for possible_order in possible_orders:
            pass  # TODO





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
    tunnels.brute_force()
    # TODO
    print("unit tests passed")


if __name__ == '__main__':
    main()
