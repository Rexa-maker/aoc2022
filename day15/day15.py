import re


LINE_REGEXP = re.compile("^Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)$")


def main():
    unit_tests()


class Caves:
    class Sensor:
        def __init__(self, position, closest_beacon):
            self.position = position
            self.closest_beacon = closest_beacon

        def __str__(self):
            return str(self.position) + " sees " + str(self.closest_beacon)

    def __init__(self, input):
        self.parse(input)

    def parse(self, input):
        self.sensors = []
        for line in input:
            line = line.rstrip()
            if not line:
                continue
            m = LINE_REGEXP.match(line)
            assert(m)
            sensor_position = [int(m.group(1)), int(m.group(2))]
            closest_beacon = [int(m.group(3)), int(m.group(4))]
            sensor = Caves.Sensor(position=sensor_position, closest_beacon=closest_beacon)
            self.sensors += [sensor]

    def __str__(self):
        res = ""
        for sensor in self.sensors:
            res += str(sensor) + "\n"
        return res



def unit_tests():
    example_input = \
"""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
    caves = Caves(example_input.splitlines())
    print(caves)

if __name__ == "__main__":
    main()