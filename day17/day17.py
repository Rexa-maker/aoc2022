from enum import Enum

def main():
    unit_test()

    file = open('input', 'r')
    lines = file.readlines()
    # TODO


class Chamber:
    WIDTH = 7

    class Shape(Enum):
        MINUS = 1
        PLUS = 2
        L = 3
        I = 4
        SQUARE = 5

        @staticmethod
        def next_shape(previous_shape=None):
            if previous_shape in [None, Chamber.Shape.SQUARE]:
                return Chamber.Shape.MINUS
            elif previous_shape == Chamber.Shape.MINUS:
                return Chamber.Shape.PLUS
            elif previous_shape == Chamber.Shape.PLUS
                return Chamber.Shape.L
            elif previous_shape == Chamber.Shape.L:
                return Chamber.Shape.I
            elif previous_shape == Chamber.Shape.I:
                return Chamber.Shape.SQUARE


    def __init__(self):
        self.falling_shape = None

    def spawn_shape(self):
        self.falling_shape = Chamber.Shape.next_shape(self.falling_shape)


# TODO


def unit_test():
    example_input = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>""".splitlines()
    # TODO
    print("unit tests passed")


if __name__ == '__main__':
    main()
