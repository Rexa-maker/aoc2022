import numpy as np

def main():
    file = open('input', 'r')
    lines = file.readlines()

    for num_knots in (2, 10):
        knots = np.zeros([num_knots, 2], int)
        visited = set([(0, 0)])

        for line in lines:
            line = line.rstrip()
            if len(line) == 0:
                continue

            [direction, count] = line.split(" ")
            count = int(count)

            if direction == 'R':
                direction = [1, 0]
            elif direction == 'L':
                direction = [-1, 0]
            elif direction == 'U':
                direction = [0, 1]
            else:
                direction = [0, -1]

            for i in range(count):
                for idx, knot in enumerate(knots):
                    if idx == 0:
                        knot += direction
                    else:
                        distance = knots[idx - 1] - knots[idx]
                        if max(abs(distance)) > 1:
                            knots[idx] += np.sign(distance)
                visited.add(tuple(knots[-1]))

        print(len(visited))

if __name__ == '__main__':
    main()
