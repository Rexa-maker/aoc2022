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

class Range:
    def __init__(self, range):
        self.range = range

    def fully_contains(self, other):
        return self.range[0] <= other.range[0] and other.range[1] <= self.range[1]

    def overlaps(self, other):
        return not (self.range[1] < other.range[0] or other.range[1] < self.range[0])

    def immediately_follows(self, other):
        return self.range[0] == other.range[1] + 1

    def after(self, other):
        return self.range[0] > other.range[1]

    def merge_if_possible(self, other: "Range"):
        """ Return a range if 2 ranges can become one, or None """
        if self.fully_contains(other):
            return self
        if other.fully_contains(self):
            return other
        if self.immediately_follows(other):
            return Range((other.range[0], self.range[1]))
        if other.immediately_follows(self):
            return Range((self.range[0], other.range[1]))
        if self.overlaps(other):
            return Range((min(self.range[0], other.range[0]), max(self.range[1], other.range[1])))
        return None

    def __int__(self):
        return self.range[1] - self.range[0] + 1

    def __str__(self):
        return str(self.range)


class Ranges:
    """ Maintain a sorted list of non-overlapping integer ranges """
    def __init__(self):
        self.ranges = []

    def add(self, new_range : Range):
        if new_range is None:
            return
        if len(self.ranges) == 0:
            self.ranges = [new_range]
            return
        for idx, range in enumerate(self.ranges):
            merged = new_range.merge_if_possible(range)
            if merged is None:
                continue

            remaining_ranges = self.ranges[idx + 1:]
            self.ranges = self.ranges[:idx]

            idx = 0
            while idx < len(remaining_ranges):
                new_merged = merged.merge_if_possible(remaining_ranges[idx])
                if new_merged is None:
                    self.ranges += [merged] + remaining_ranges[idx:]
                    return
                merged = new_merged
                idx += 1

            # We merged everything until the end
            self.ranges += [merged]
            return

        # No merge: just add and sort
        self.ranges = sorted(self.ranges + [new_range], key=lambda x: x.range)

    def __str__(self):
        return ", ".join(str(range) for range in self.ranges)

    def __int__(self):
        return sum(int(range) for range in self.ranges)


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

        def visible_range_for_row(self, row, bound_coordinates=None):
            """ Instead of a set, return a Range of visibility """
            vertical_distance = abs(row - self.position[1])
            vertical_spare = self.scanned_distance - vertical_distance
            if vertical_spare < 0:
                return None
            if bound_coordinates is not None:
                return Range((max(self.position[0] - vertical_spare, bound_coordinates[0]), min(self.position[0] + vertical_spare, bound_coordinates[1])))
            else:
                return Range((self.position[0] - vertical_spare, self.position[0] + vertical_spare))


    class Beacon:
        def __init__(self, position):
            self.position = position

        @property
        def tuning_frequency(self):
            return self.position[0] * 4000000 + self.position[1]

        def __str__(self):
            return "Beacon " + str(self.position)

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

    def get_visible_ranges_on_row(self, row, bound_coordinates=None):
        ranges = Ranges()
        for sensor in self.sensors:
            ranges.add(sensor.visible_range_for_row(row, bound_coordinates))
        return ranges

    def find_distress_beacon(self, max_coordinate):
        """ both x and y are in [0, max_coordinate] """
        bound_coordinates = (0, max_coordinate)
        for row in range(max_coordinate + 1):
            # print("Considering row {}".format(str(row)))  # back in the 9s per row days, this was vital
            ranges = self.get_visible_ranges_on_row(row, bound_coordinates=bound_coordinates)
            if len(ranges.ranges) > 1:
                return (ranges.ranges[0].range[1] + 1, row)
            if ranges.ranges[0].range[0] > 0:
                return (0, row)
            if ranges.ranges[0].range[1] < max_coordinate:
                return (max_coordinate, row)

    def how_many_beaconless_on_row(self, row):
        beacons_on_row = set()
        visible_ranges_on_row = self.get_visible_ranges_on_row(row)
        for sensor in self.sensors:
            if sensor.closest_beacon[1] == row:
                beacons_on_row.add(sensor.closest_beacon)
        return int(visible_ranges_on_row) - len(beacons_on_row)

    def __str__(self):
        res = ""
        for sensor in self.sensors:
            res += str(sensor) + "\n"
        return res


def unit_tests():
    ranges = Ranges()
    ranges.add(Range((1, 1)))
    ranges.add(Range((2, 2)))
    assert(ranges.ranges[0].range == (1, 2))

    ranges.add(Range((4, 5)))
    ranges.add(Range((-1, 0)))
    assert(ranges.ranges[0].range == (-1, 2) and ranges.ranges[1].range == (4, 5))

    ranges.add(Range((-10, -5)))
    ranges.add(Range((-15, -1)))
    assert(ranges.ranges[0].range == (-15, 2) and ranges.ranges[1].range == (4, 5))

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