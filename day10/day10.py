import numpy as np


WIDTH = 40
HEIGHT = 6


def print_screen(screen):
    for screen_line in screen:
        line = ""
        for pixel in screen_line:
            line += "#" if pixel else "."
        print(line)


def update_screen(screen, X, cycle):
    cycles_of_interest = [20, 60, 100, 140, 180, 220]
    increment = X * cycle if cycle in cycles_of_interest else 0

    # cycle-th is 1-indexed, the screen is 0-indexed
    x = (cycle-1) % WIDTH
    y = int((cycle-1) / WIDTH)

    if x in range(X-1, X+2):
        screen[y][x] = True

    return increment


def main():
    file = open('input', 'r')
    lines = file.readlines()

    X = 1
    cycle = 1
    sum = 0

    screen = np.zeros((HEIGHT, WIDTH), dtype=bool)
    update_screen(screen, X, cycle)

    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            continue

        if "noop" in line:
            cycle += 1

        else:
            op, count = line.split(" ")
            count = int(count)

            cycle += 1
            sum += update_screen(screen, X, cycle)
            cycle += 1
            X += count

        sum += update_screen(screen, X, cycle)

    print(sum)
    print_screen(screen)


if __name__ == '__main__':
    main()
