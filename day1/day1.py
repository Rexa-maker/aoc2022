def main():
    most_calories = 0
    current_tally = 0
    file = open('input', 'r')
    lines = file.readlines()
    for line in lines:
        line = line.rstrip()
        if line == '':
            print('new elf, prev tally was ' + str(current_tally))
            if most_calories < current_tally:
                most_calories = current_tally
            current_tally = 0
        else:
            current_tally += int(line)
    print('Largest calories count: ' + str(most_calories))

if __name__ == '__main__':
    main()