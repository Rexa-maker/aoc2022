import re

SMOLL_MAX_SIZE = 100000
CD_COMMAND_REGEXP   = re.compile(r"^\$ cd (.*)$")
LS_COMMAND_REGEXP   = re.compile(r"^\$ ls$")
DIR_LISTING_REGEXP  = re.compile(r"^dir (.*)$")
FILE_LISTING_REGEXP = re.compile(r"^(\d+) (.*)$")

def discover_file_system(lines):
    file_system = {
        'dirs'  : {},
        'files' : {},
        '..'    : None
    }
    current_dir = file_system

    for line in lines:
        line = line.rstrip()

        if len(line) == 0:
            continue

        print(line)

        m = CD_COMMAND_REGEXP.match(line)
        if m:
            goto_dir_name = m.group(1)

            if goto_dir_name == '/':
                current_dir = file_system
                continue

            if goto_dir_name == '..':
                current_dir = current_dir['..']
                assert(current_dir)  # Hopefully no `cd ..` on /
                continue

            assert(goto_dir_name in current_dir['dirs'])

            goto_dir = current_dir['dirs'][goto_dir_name]
            current_dir = goto_dir
            continue

        m = LS_COMMAND_REGEXP.match(line)
        if m:
            # Let's not bother with integrity here
            continue

        m = DIR_LISTING_REGEXP.match(line)
        if m:
            new_dir_name = m.group(1)

            if new_dir_name in current_dir['dirs']:
                raise Exception("User executed `ls` in the same dir again?!")

            current_dir['dirs'][new_dir_name] = {
                'dirs'  : {},
                'files' : {},
                '..'    : current_dir
            }
            continue

        m = FILE_LISTING_REGEXP.match(line)
        if m:
            new_file_size = int(m.group(1))
            new_file_name = m.group(2)

            if new_file_name in current_dir['files']:
                raise Exception("User executed `ls` in the same dir again?!")

            current_dir['files'][new_file_name] = new_file_size
            continue

        raise Exception("Unknown command {}".format(line))

    return file_system


def get_size_of_dir_and_smoll_tally(dir):
    size = sum(dir['files'].values())
    smoll_tally = 0

    for sub_dir in dir['dirs']:
        [sub_dir_size, sub_dir_smoll_tally] = get_size_of_dir_and_smoll_tally(dir['dirs'][sub_dir])
        size += sub_dir_size
        smoll_tally += sub_dir_smoll_tally

    if size <= SMOLL_MAX_SIZE:
        smoll_tally += size

    return [size, smoll_tally]


def main():
    file = open('input', 'r')
    lines = file.readlines()

    file_system = discover_file_system(lines)

    [_, sum_of_smolls] = get_size_of_dir_and_smoll_tally(file_system)

    print('sum of all dirs of size <= {}: {}'.format(str(SMOLL_MAX_SIZE), str(sum_of_smolls)))


if __name__ == '__main__':
    main()