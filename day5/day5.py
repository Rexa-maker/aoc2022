import re 


def parse_crates(lines):
    crates = [None] * 9
    for line in lines:
        line = line.rstrip()
        if not '[' in line:
            return crates
        for i in range(9):
            crate = line[1]
            if crate != ' ':
                if crates[i] is None:
                    crates[i] = [crate]
                else:
                    crates[i].append(crate)
            if len(line) > 3:
                line = line[4:]
            else:
                break


def move_crates(crates, steps):
    p = re.compile('move (\d+) from (\d) to (\d)')
    for step in steps:
        m = p.match(step)
        if not m:
            continue
        how_many = int(m.group(1))
        where_from = int(m.group(2)) - 1
        where_to = int(m.group(3)) - 1
        while how_many > 0:
            how_many -= 1
            crate = crates[where_from][0]
            crates[where_from] = crates[where_from][1:]
            crates[where_to] = [crate] + crates[where_to]


def main():
    file = open('input_crates', 'r')
    lines = file.readlines()
    crates = parse_crates(lines)

    file = open('input_steps', 'r')
    steps = file.readlines()
    move_crates(crates, steps)

    top_crates = ''
    for pile in crates:
        top_crates += pile[0]

    print('top crates: ' + str(top_crates))


if __name__ == '__main__':
    main()