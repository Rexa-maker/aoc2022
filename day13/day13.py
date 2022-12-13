def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()

class Packet:
    def __init__(self, line):
        self.parse_line(line)

    def parse_line(self, line):
        self.array = []
        line = line.replace('[', '').replace(']', '').rstrip().split(',')
        for d in line:
            print('{}'.format(d))
            self.array += [int(d)]

    def __lt__(self, other_packet):
        return self.array < other_packet.array

def solve(input):
    index = 1
    indices_sum = 0
    pair = [None, None]

    for line in input:
        line = line.rstrip()
        if len(line) == 0:
            pair = [None, None]
            continue

        if pair[0] is None:
            pair[0] = Packet(line)
        else:
            pair[1] = Packet(line)
            if pair[0] < pair[1]:
                indices_sum += index
            index += 1

    return index


def unit_test():
    example_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".splitlines()
    sum_of_correct_indices = solve(example_input)
    assert(sum_of_correct_indices == 13)
    print("unit tests passed")


if __name__ == '__main__':
    main()
