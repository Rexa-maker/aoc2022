import numpy as np

def main():
    file = open('input', 'r')
    lines = file.readlines()

    head = np.array([0, 0])
    tail = np.array([0, 0])
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
            head += direction
            distance = head - tail
            if max(abs(distance)) > 1:
                tail += np.sign(distance)
            visited.add(tuple(tail))

    print(len(visited))

if __name__ == '__main__':
    main()
