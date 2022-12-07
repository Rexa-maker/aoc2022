import re

FILE_SYSTEM_SIZE = 70000000
UPDATE_SIZE      = 30000000
SMOLL_MAX_SIZE   = 100000
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


def get_size_of_dir_n_smoll_tally(dir):
    size = sum(dir['files'].values())
    smoll_tally = 0

    for sub_dir in dir['dirs']:
        [sub_dir_size, sub_dir_smoll_tally] = get_size_of_dir_n_smoll_tally(dir['dirs'][sub_dir])
        size += sub_dir_size
        smoll_tally += sub_dir_smoll_tally

    if size <= SMOLL_MAX_SIZE:
        smoll_tally += size

    return [size, smoll_tally]


def get_smollest4update(dir, needed_freed_size):
    size = sum(dir['files'].values())
    sub_dirs_smollest_smollest4update = None

    for sub_dir in dir['dirs']:
        [sub_dir_size, smollest4update] = get_smollest4update(dir['dirs'][sub_dir], needed_freed_size)
        size += sub_dir_size
        if smollest4update and (not sub_dirs_smollest_smollest4update or smollest4update < sub_dirs_smollest_smollest4update):
            sub_dirs_smollest_smollest4update = smollest4update

    if size >= needed_freed_size and (not sub_dirs_smollest_smollest4update or size < sub_dirs_smollest_smollest4update):
        sub_dirs_smollest_smollest4update = size

    return [size, sub_dirs_smollest_smollest4update]


def main():
    file = open('input', 'r')
    lines = file.readlines()

    file_system = discover_file_system(lines)

    [sizeof_root, sum_of_smolls] = get_size_of_dir_n_smoll_tally(file_system)

    free_size = FILE_SYSTEM_SIZE - sizeof_root
    needed_freed_size = UPDATE_SIZE - free_size
    [_, smollest4update] = get_smollest4update(file_system, needed_freed_size)

    print('size of /: {}'.format(str(sizeof_root)))
    print('sum of all dirs of size <= {}: {}'.format(str(SMOLL_MAX_SIZE), str(sum_of_smolls)))
    print('smollest dir size for update {}'.format(smollest4update))


if __name__ == '__main__':
    main()