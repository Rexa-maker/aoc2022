from enum import Enum


class Janken(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


def battle_score(opponent, me):
    """ return score based on who plays what """
    if opponent == me:
        return 3
    if opponent == Janken.Rock:
        if me == Janken.Scissors:
            return 0
        return 6  # me == Paper
    if opponent == Janken.Paper:
        if me == Janken.Rock:
            return 0
        return 6  # me == Scissors
    if me == Janken.Paper:  # opponent == Scissors
        return 0
    return 6  # me == Rock


def opponent2play(opponent):
    if opponent == "A":
        return Janken.Rock
    if opponent == "B":
        return Janken.Paper
    if opponent == "C":
        return Janken.Scissors
    raise Exception(opponent)


def me2play(me):
    if me == "X":
        return Janken.Rock
    if me == "Y":
        return Janken.Paper
    if me == "Z":
        return Janken.Scissors
    raise Exception(me)


def gimme_me(opponent, strategy):
    if strategy == "Y":  # draw
        return opponent
    if strategy == "X":  # lose
        if opponent == Janken.Rock:
            return Janken.Scissors
        if opponent == Janken.Paper:
            return Janken.Rock
        return Janken.Paper
    # Z = win
    if opponent == Janken.Rock:
        return Janken.Paper
    if opponent == Janken.Paper:
        return Janken.Scissors
    return Janken.Rock


def main():
    file = open('input', 'r')
    lines = file.readlines()
    score = 0
    for line in lines:
        line = line.rstrip()
        if line == '':
            break
        [opponent, strategy] = line.split(" ")
        opponent = opponent2play(opponent)
        me = gimme_me(opponent, strategy)
        score += battle_score(opponent, me) + me.value
    print('my score would be: ' + str(score))


if __name__ == '__main__':
    main()