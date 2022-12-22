def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    troop = Troop(lines)
    root_number = troop.root_number()
    print("Root's yelled number is {}".format(root_number))
    humn_goal = troop.humn_must_yell()
    print("Humn must yell {}".format(humn_goal))


class Troop:
    class Monkey:
        def __init__(self, troop, name, number, others=None, operations=None):
            self.troop = troop
            self.name = name
            if number is not None:
                self.number = number
                self.others = self.operations = None
            else:
                self.others = others
                self.operations = operations
                self.number = None

        def yelled_number(self):
            if self.number is not None:
                return self.number
            other_numbers = [self.troop.monkeys[self.others[i]].yelled_number() for i in range(2)]
            return self.operations[0](other_numbers[0], other_numbers[1])

        def needs_humn(self):
            """ Return true iff its output depends on humn"""
            if self.name == "humn":
                return True
            if self.number is not None:
                return False
            return self.troop.monkeys[self.others[0]].needs_humn() or self.troop.monkeys[self.others[1]].needs_humn()

        def humn_goal(self, goal):
            if self.name == "humn":
                return goal
            if self.number is not None:
                raise Exception("Cannot create goal from number!")
            if self.troop.monkeys[self.others[0]].needs_humn():
                right_number = self.troop.monkeys[self.others[1]].yelled_number()
                left_goal = self.operations[2](right_number, goal)
                return self.troop.monkeys[self.others[0]].humn_goal(left_goal)
            else:
                left_number = self.troop.monkeys[self.others[0]].yelled_number()
                right_goal = self.operations[1](left_number, goal)
                return self.troop.monkeys[self.others[1]].humn_goal(right_goal)


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
                    # g = x + y; x = g - y; y = g - x
                    operation = lambda left, right: left + right
                    reverse_operation_from_left = lambda left, goal: goal - left
                    reverse_operation_from_right = lambda right, goal: goal - right
                elif operand == "-":
                    # g = x - y; x = g + y; y = x - g
                    operation = lambda left, right: left - right
                    reverse_operation_from_left = lambda left, goal: left - goal
                    reverse_operation_from_right = lambda right, goal: goal + right
                elif operand == "/":
                    # g = x / y; x = g * y; y = x / g
                    operation = lambda left, right: left / right
                    reverse_operation_from_left = lambda left, goal: left / goal
                    reverse_operation_from_right = lambda right, goal: goal * right
                elif operand == "*":
                    # g = x * y; x = g / y; y = g / x
                    operation = lambda left, right: left * right
                    reverse_operation_from_left = lambda left, goal: goal / left
                    reverse_operation_from_right = lambda right, goal: goal / right
                else:
                    raise Exception("Unknown operand " + operand)
                operations = [operation, reverse_operation_from_left, reverse_operation_from_right]
                self.monkeys[name] = Troop.Monkey(troop=self, name=name, number=None, others=[other1, other2], operations=operations)

    def root_number(self):
        return self.monkeys["root"].yelled_number()

    def humn_must_yell(self):
        root_actors = self.monkeys["root"].others
        if self.monkeys[root_actors[0]].needs_humn():
            goal = self.monkeys[root_actors[1]].yelled_number()
            humn_goal = self.monkeys[root_actors[0]].humn_goal(goal)
        else:
            goal = self.monkeys[root_actors[0]].yelled_number()
            humn_goal = self.monkeys[root_actors[1]].humn_goal(goal)
        return humn_goal


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
    humn_goal = troop.humn_must_yell()
    print(humn_goal)
    assert(humn_goal == 301)
    print("unit tests passed")


if __name__ == '__main__':
    main()
