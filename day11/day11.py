from functools import reduce


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    Monkey.WORRIED_HOOMAN = False
    keep_away = KeepAway.parse_input(lines)
    print("Monkey business after 20 rounds: " + str(keep_away.monkey_business_after_X_rounds(20)))
    Monkey.WORRIED_HOOMAN = True
    keep_away = KeepAway.parse_input(lines)
    print("Monkey business after 10000 rounds: " + str(keep_away.monkey_business_after_X_rounds(10000)))


class Monkey:
    WORRIED_HOOMAN = False

    def __init__(self, items, operation, destination_monkeys, divisible_by):
        self.inspections = 0
        self.items = items
        self.operation = operation
        self.destination_monkeys = destination_monkeys
        self.divisible_by = divisible_by

    def receive_item(self, item):
        self.items += [item]

    def __iter__(self):
        items = self.items[:]
        for item in items:
            self.items = self.items[1:]
            yield item

    def inspect_item(self, item):
        item = self.operation(item)
        if not Monkey.WORRIED_HOOMAN:
            item = int(item / 3)
        destination_monkey = self.destination_monkeys[0] if item % self.divisible_by == 0 else self.destination_monkeys[1]
        self.inspections += 1
        return destination_monkey, item

    def __str__(self):
        return ", ".join([str(item) for item in self.items]) if self.items else ""

    @staticmethod
    def parse_input(lines):
        for line in lines:
            if "Monkey" in line:
                pass
            elif "Starting items:" in line:
                line = line[line.index(":") + 2:]
                items = [int(l) for l in line.split(", ")]
            elif "Operation: new = old" in line:
                line = line[line.index("d") + 2:]
                operator, other = line.split(" ")
                fun = (lambda x, y : x * y) if operator == "*" else (lambda x, y : x + y)
                try:
                    other = int(other)
                    operation = lambda x : fun(x, other)
                except:
                    # Assume operation is between x and x if cannot parse int
                    operation = lambda x : fun(x, x)
            elif "Test: divisible by" in line:
                divisible_by = int(line[line.index('y') + 1:])
                test_fun = lambda x : x % divisible_by == 0
            elif "If true: throw to monkey" in line:
                target_true = int(line[line.index("y") + 1:])
            elif "If false: throw to monkey" in line:
                target_false = int(line[line.index("y") + 1:])
                test = lambda x : target_true if test_fun(x) else target_false
        return Monkey(items=items, operation=operation, destination_monkeys=[target_true, target_false], divisible_by=divisible_by)


class KeepAway:
    FOCUS_MONKEYS_COUNT = 2

    @staticmethod
    def parse_input(lines):
        monkeys = []
        monkey_lines = []

        for line in lines:
            line = line.rstrip()
            if len(line) == 0:
                monkeys += [Monkey.parse_input(monkey_lines)]
                monkey_lines = []
            else:
                monkey_lines += [line]

        return KeepAway(monkeys=monkeys)


    def __init__(self, monkeys):
        self.monkeys = monkeys
        self.all_divisible_by = reduce(lambda x, y: x * y, [monkey.divisible_by for monkey in monkeys])

    def round(self):
        for monkey in self.monkeys:
            for item in monkey:
                destination_monkey, item = monkey.inspect_item(item)
                item = item % self.all_divisible_by
                self.monkeys[destination_monkey].receive_item(item)

    @property
    def monkey_business(self):
        """ Monkey business is multiplication of inspections of 2 most active monkeys """
        inspections_list = [monkey.inspections for monkey in self.monkeys]
        inspections_list.sort(reverse=True)
        inspections_list = inspections_list[:self.FOCUS_MONKEYS_COUNT]
        return reduce((lambda x, y : x * y), inspections_list)

    def monkey_business_after_X_rounds(self, rounds):
        for i in range(rounds):
            self.round()
        return self.monkey_business

    def __str__(self):
        return "\n".join(["Monkey {} inpected {} times: {}".format(str(idx), str(monkey.inspections), monkey) for idx, monkey in enumerate(self.monkeys)])


def unit_test():
    example_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1

""".splitlines()
    keep_away = KeepAway.parse_input(example_input)
    assert(keep_away.monkey_business_after_X_rounds(20) == 10605)

    Monkey.WORRIED_HOOMAN = True
    keep_away = KeepAway.parse_input(example_input)
    assert(keep_away.monkey_business_after_X_rounds(10000) == 2713310158)
    print("unit tests passed")


if __name__ == '__main__':
    main()
