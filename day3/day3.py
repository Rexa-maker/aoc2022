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


def main():
    file = open('input', 'r')
    lines = file.readlines()
    priority_tally = 0
    for line in lines:
        line = line.rstrip()
        if line == '':
            break
        dup_item = find_dup_item(line)
        priority_tally += priority_of(dup_item)
    print('priority tally: ' + str(priority_tally))


if __name__ == '__main__':
    main()