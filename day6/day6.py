
def main():
    four = []
    count = 0
    file = open('input', 'r')
    characters = file.read()
    for character in characters:
        four.append(character)
        count += 1
        all_different = True
        for i in range(len(four)-1):
            if character == four[i]:
                all_different = False
                four = four[i+1:]
                break
        if all_different and len(four) == 14:
            print("Got signal at count {}".format(count))
            return


if __name__ == '__main__':
    main()