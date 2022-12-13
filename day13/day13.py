import json
import functools


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    sum_of_correct_indices = get_indices_sum(lines)
    print("Sum of correct indices: {}".format(str(sum_of_correct_indices)))
    decoder_key = get_decoder_key(lines)
    print("Decoder key: {}".format(str(decoder_key)))


class Packet:
    def __init__(self, input):
        if isinstance(input, str):
            self.parse_line(input)
        else:
            assert(isinstance(input, list))
            self.array = input

    def parse_line(self, line):
        self.array = json.loads(line)

    def compare(self, other_packet: "Packet"):  # return 1 if "bigger" (wrong), 0 if "same", -1 if "smaller" (right)
        if len(self.array) == 0:
            if len(other_packet.array) == 0:
                # both empty, we have equality!
                return 0
            # if left runs out of item before right, the order's correct
            return -1

        if len(other_packet.array) == 0:
            # if right runs out before left, the order's wrong
            return 1

        left = self.array[0]
        left_rest = self.array[1:]
        right = other_packet.array[0]
        right_rest = other_packet.array[1:]
        if isinstance(left, list):
            if isinstance(right, list):
                # both are lists
                first_compare = Packet(left).compare(Packet(right))
                if first_compare != 0:
                    return first_compare
                return Packet(left_rest).compare(Packet(right_rest))
            # left is list, right is integer
            first_compare = Packet(left).compare(Packet([right]))
            if first_compare != 0:
                return first_compare
            return Packet(left_rest).compare(Packet(right_rest))
        else:
            if isinstance(other_packet.array[0], list):
                # left is integer, right is list
                first_compare = Packet([left]).compare(Packet(right))
                if first_compare != 0:
                    return first_compare
                return Packet(left_rest).compare(Packet(right_rest))
            # both are integer
            if left < right:
                return -1
            if left > right:
                return 1
            return Packet(left_rest).compare(Packet(right_rest))

def remove_empty_lines(packets):
    return [packet for packet in packets if packet != ""]

def sort_packets(packets):
    return sorted(packets, key=functools.cmp_to_key(lambda packet1, packet2: Packet(packet1).compare(Packet(packet2))))

def add_divider_packets(packets):
    return packets + [[[2]], [[6]]]

def get_decoder_key(packets):
    packets = [packet.rstrip() for packet in packets]
    packets = remove_empty_lines(packets)
    packets = add_divider_packets(packets)
    packets = sort_packets(packets)
    idx = 1
    key = 1
    for packet in packets:
        if packet == [[2]] or packet == [[6]]:
            key *= idx
        idx += 1
    return key

def get_indices_sum(input):
    index = 1
    indices_sum = 0
    pair = [None, None]

    for line in input:
        line = line.rstrip()
        if len(line) == 0:
            continue

        if pair[0] is None:
            pair[0] = Packet(line)
        else:
            pair[1] = Packet(line)
            if pair[0].compare(pair[1]) <= 0:
                indices_sum += index
            pair = [None, None]
            index += 1

    return indices_sum

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
    sum_of_correct_indices = get_indices_sum(example_input)
    assert(sum_of_correct_indices == 13)
    decoder_key = get_decoder_key(example_input)
    assert(decoder_key == 140)
    print("unit tests passed")


if __name__ == '__main__':
    main()
