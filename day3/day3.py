def priority_of(letter):
    letter_ord = ord(letter)
    if letter_ord < ord('a'):
        return 27 + letter_ord - ord('A')
    return 1 + letter_ord - ord('a')


def find_dup_item(bag):
    half = int(len(bag) / 2)
    bag1 = bag[0 : half]
    bag2 = bag[half :]
    for item in bag1:
        if item in bag2:
            return item


def find_common_item(lines):
    for item in lines[0]:
        if item in lines[1] and item in lines[2]:
            return item


def main():
    badges_tally = 0

    file = open('input', 'r')
    lines = file.readlines()
    priority_tally = 0
    trio = []
    for line in lines:
        line = line.rstrip()
        if line == '':
            break

        trio.append(line)
        if (len(trio) == 3):
            badges_tally += priority_of(find_common_item(trio))
            trio = []

    print('badges tally: ' + str(badges_tally))


if __name__ == '__main__':
    main()