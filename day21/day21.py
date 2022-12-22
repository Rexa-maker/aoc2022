def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    troop = Troop(lines)
    root_number = troop.root_number()
    print("Root's yelled number is {}".format(root_number))


class Troop:
    class Monkey:
        def __init__(self, troop, name, number, others=None, operation=None):
            self.troop = troop
            self.name = name
            if number is not None:
                self.number = number
                self.others = self.operation = None
            else:
                self.others = others
                self.operation = operation
                self.number = None

        def yelled_number(self):
            if self.number is not None:
                return self.number
            other_numbers = [self.troop.monkeys[self.others[i]].yelled_number() for i in range(2)]
            return self.operation(other_numbers[0], other_numbers[1])

    def __init__(self, input):
        self.monkeys = {}
        for line in input:
            line = line.rstrip().split(": ")
            name = line[0]
            try:
                number = int(line[1])
                self.monkeys[name] = Troop.Monkey(troop=self, name=name, number=number)
            except ValueError:
                other1, operand, other2 = line[1].split(" ")
                if operand == "+":
                    operation = lambda x, y: x + y
                elif operand == "-":
                    operation = lambda x, y: x - y
                elif operand == "/":
                    operation = lambda x, y: x / y
                elif operand == "*":
                    operation = lambda x, y: x * y
                else:
                    raise Exception("Unknown operand " + operand)
                self.monkeys[name] = Troop.Monkey(troop=self, name=name, number=None, others=[other1, other2], operation=operation)

    def root_number(self):
        return self.monkeys["root"].yelled_number()


def unit_test():
    example_input = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".splitlines()
    troop = Troop(example_input)
    root_number = troop.root_number()
    assert(root_number == 152)
    print("unit tests passed")


if __name__ == '__main__':
    main()
