def fully_contains(range1, range2):
    return ((range1[0] <= range2[0] and range1[1] >= range2[1]) or 
            (range2[0] <= range1[0] and range2[1] >= range1[1]))


def main():
    contained_count = 0

    file = open('input', 'r')
    lines = file.readlines()
    for line in lines:
        line = line.rstrip()
        if line == '':
            break

        [range1, range2] = line.split(',')
        range1 = list(map(lambda a: int(a), range1.split('-')))
        range2 = list(map(lambda a: int(a), range2.split('-')))

        if fully_contains(range1, range2):
            contained_count += 1

    print('fully contained pairs: ' + str(contained_count))


if __name__ == '__main__':
    main()