def main():
    most_calories = [0, 0, 0]
    current_tally = 0
    file = open('input', 'r')
    lines = file.readlines()
    for line in lines:
        line = line.rstrip()
        if line == '':
            print('new elf, prev tally was ' + str(current_tally))
            most_calories.append(current_tally)
            most_calories.sort(reverse=True)
            most_calories = most_calories[0:-1]
            current_tally = 0
        else:
            current_tally += int(line)
    print('Largest calories count: ' + str(most_calories))
    print('3 largest = {}+{}+{}={}'.format(most_calories[0], most_calories[1], most_calories[2], sum(most_calories)))

if __name__ == '__main__':
    main()