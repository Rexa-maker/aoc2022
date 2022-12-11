from functools import reduce


def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    keep_away = KeepAway.parse_input(lines)
    print(keep_away.monkey_business_after_X_rounds(20))


class Monkey:
    def __init__(self, items, operation, test):
        self.inspections = 0
        self.items = items
        self.operation = operation
        self.test = test

    def receive_item(self, item):
        self.items += [item]

    def __iter__(self):
        items = self.items[:]
        for item in items:
            self.items = self.items[1:]
            yield item

    def inspect_item(self, item):
        print("item before: " + str(item))
        print("item after op before /3: " + str(self.operation(item)))
        item = int(self.operation(item) / 3)
        destination_monkey = self.test(item)
        self.inspections += 1
        print("item after: " + str(item) + " over to " + str(destination_monkey))
        return destination_monkey, item

    def __str__(self):
        return ", ".join([str(item) for item in self.items]) if self.items else ""

    # I tried using lambdas but it got weird


class KeepAway:
    FOCUS_MONKEYS_COUNT = 2

    @staticmethod
    def parse_input(lines):
        monkeys = []

        for line in lines:
            line = line.rstrip()
            if "Monkey" in line:
                pass
            elif "Starting items:" in line:
                line = line[line.index(":") + 2:]
                items = [int(l) for l in line.split(", ")]
            elif "Operation: new = old" in line:
                line = line[line.index("d") + 2:]
                operator, other = line.split(" ")
                # print("op {} other {}".format(operator, other))
                fun = (lambda x, y : x * y) if operator == "*" else (lambda x, y : x + y)
                # print("fun(79) = {}".format(str(fun(79, int(other)))))
                try:
                    other = int(other)
                    operation = (lambda x : x * other) if operator == "*" else (lambda x : x + other)
                except:
                    # Assume operation is between x and x if cannot parse int
                    operation = lambda x : (lambda x : x * x) if operator == "*" else (lambda x : x + x)
                # print("operation(79) = {}".format(str(operation(79))))
            elif "Test: divisible by" in line:
                divisible_by = int(line[line.index('y') + 1:])
                test_fun = lambda x : x % divisible_by == 0
            elif "If true: throw to monkey" in line:
                target_true = int(line[line.index("y") + 1:])
            elif "If false: throw to monkey" in line:
                target_false = int(line[line.index("y") + 1:])
                test = lambda x : target_true if test_fun(x) else target_false
            else:
                # Can't parse, generate monkey
                monkeys += [Monkey(items=items, operation=operation, test=test)]
                print("mokey[0].operation(79) = {}".format(int(monkeys[0].operation(79))))

        return KeepAway(monkeys=monkeys)


    def __init__(self, monkeys):
        self.monkeys = monkeys

    def round(self):
        for monkey in self.monkeys:
            for item in monkey:
                destination_monkey, item = monkey.inspect_item(item)
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
        return "\n".join(["Monkey {}: {}".format(str(idx), monkey) for idx, monkey in enumerate(self.monkeys)])


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

"""
    keep_away = KeepAway.parse_input(example_input.splitlines())
    print(keep_away)
    keep_away.round()
    print(keep_away)
    assert(keep_away.monkey_business_after_X_rounds(20) == 10605)


if __name__ == '__main__':
    main()
