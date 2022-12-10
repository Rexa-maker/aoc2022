def main():
    file = open('input', 'r')
    lines = file.readlines()

    X = 1
    cycle = 1
    sum = 0

    cycles_of_interest = [20, 60, 100, 140, 180, 220]

    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            continue

        if "noop" not in line:
            op, count = line.split(" ")
            count = int(count)

            cycle += 1
            if cycle in cycles_of_interest:
                sum += X * cycle
            cycle += 1
            X += count
        else:
            cycle += 1

        if cycle in cycles_of_interest:
            sum += X * cycle

    print(sum)


if __name__ == '__main__':
    main()
