import re


LINE_REGEXP = re.compile("^Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)$")


def main():
    unit_tests()

    file = open('input', 'r')
    lines = file.readlines()
    caves = Caves(lines)
    beaconless_on_row = caves.how_many_beaconless_on_row(2000000)
    print("# of beaconless spots on row 2000000: {}".format(beaconless_on_row))
    distress_beacon = Caves.Beacon(caves.find_distress_beacon(max_coordinate=4000000))
    print("Distress beacon's tuning frequency: {}".format(distress_beacon.tuning_frequency))


class Caves:
    class Sensor:
        def __init__(self, position, closest_beacon):
            self.position = position
            self.closest_beacon = closest_beacon

        def __str__(self):
            return str(self.position) + " sees " + str(self.closest_beacon)

        @property
        def scanned_distance(self):
            return abs(self.position[0] - self.closest_beacon[0]) + abs(self.position[1] - self.closest_beacon[1])

        @staticmethod
        def coordinates_within_bounds(candidate, bound_coordinates):
            return candidate[0] >= bound_coordinates[0] and \
                   candidate[0] <= bound_coordinates[1] and \
                   candidate[1] >= bound_coordinates[0] and \
                   candidate[1] <= bound_coordinates[1]

        def which_can_see_on_row(self, row, bound_coordinates=None):
            """ Return a set of the spots on a row that sensor can see (not counting any potentially found beacon there) """
            visible = set()
            vertical_distance = abs(row - self.position[1])
            vertical_spare = self.scanned_distance - vertical_distance
            if vertical_spare < 0:
                return visible
            for delta_x in range(vertical_spare + 1):  # Add the center twice I don't care
                for multiplier in [-1, 1]:
                    candidate = (self.position[0] + multiplier * delta_x, row)
                    if bound_coordinates is None or Caves.Sensor.coordinates_within_bounds(candidate, bound_coordinates):
                        visible.add(candidate)

            return visible

    class Beacon:
        def __init__(self, position):
            self.position = position

        @property
        def tuning_frequency(self):
            return self.position[0] * 4000000 + self.position[1]

    def __init__(self, input):
        self.sensors : list(Caves.Sensor) = []
        self.parse(input)

    def parse(self, input):
        for line in input:
            line = line.rstrip()
            if not line:
                continue
            m = LINE_REGEXP.match(line)
            assert(m)
            sensor_position = (int(m.group(1)), int(m.group(2)))
            closest_beacon = (int(m.group(3)), int(m.group(4)))
            sensor = Caves.Sensor(position=sensor_position, closest_beacon=closest_beacon)
            self.sensors += [sensor]

    def get_visible_on_row(self, row, bound_coordinates=None):
        visible_on_row = set()
        for sensor in self.sensors:
            visible_on_row = visible_on_row.union(sensor.which_can_see_on_row(row, bound_coordinates))
        return visible_on_row

    def how_many_beaconless_on_row(self, row):
        beacons_on_row = set()
        visible_on_row = self.get_visible_on_row(row)
        for sensor in self.sensors:
            if sensor.closest_beacon[1] == row:
                beacons_on_row.add(sensor.closest_beacon)
        beaconless_on_row = visible_on_row - beacons_on_row
        return len(beaconless_on_row)

    def find_distress_beacon(self, max_coordinate):
        """ both x and y are in [0, max_coordinate] """
        visible_on_row = set()
        beacon_row = 0
        bound_coordinates = (0, max_coordinate)
        for row in range(max_coordinate + 1):
            print("Considering row {}", str(row))
            visible_on_row = self.get_visible_on_row(row, bound_coordinates=bound_coordinates)
            if len(visible_on_row) < max_coordinate + 1:
                beacon_row = row
                break
        for x in range(0, max_coordinate + 1):
            candidate = (x, beacon_row)
            if candidate not in visible_on_row:
                return candidate

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
    beaconless_on_row = caves.how_many_beaconless_on_row(row=10)
    assert(beaconless_on_row == 26)
    distress_beacon = Caves.Beacon(caves.find_distress_beacon(max_coordinate=20))
    assert(distress_beacon.tuning_frequency == 56000011)
    print("Unit tests passed")

if __name__ == "__main__":
    main()