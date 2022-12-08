def main():
    file = open('input', 'r')
    lines = file.readlines()

    width = len(lines[0])
    height = len(lines)

    rows = [[] for y in range(height)]
    cols = [[] for x in range(width)]

    row_idx = 0
    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            continue
        rows[row_idx] = []
        col_idx = 0
        for height in line:
            height = int(height)
            rows[row_idx].append(height)
            cols[col_idx].append(height)
            col_idx += 1
        row_idx += 1

    matrix = [[False for x in range(len(rows[0]))] for y in range(len(cols[0]))]

    for [row_idx, row] in enumerate(rows):
        for [col_idx, height] in enumerate(row):
            is_edge = col_idx == 0 or col_idx == (len(row) - 1)
            visible = is_edge
            if not is_edge:
                before = row[col_idx + 1:]
                before.sort()
                after = row[0:col_idx]
                after.sort()
                visible = height > before[len(before)-1] or height > after[len(after)-1]
            matrix[row_idx][col_idx] = matrix[row_idx][col_idx] or visible

    for [col_idx, col] in enumerate(cols):
        for [row_idx, height] in enumerate(col):
            is_edge = row_idx == 0 or row_idx == (len(col) - 1)
            visible = is_edge
            if not is_edge:
                before = col[row_idx + 1:]
                before.sort()
                after = col[0:row_idx]
                after.sort()
                visible = height > before[len(before)-1] or height > after[len(after)-1]
            matrix[row_idx][col_idx] = matrix[row_idx][col_idx] or visible

    count = 0
    for row in matrix:
        for visible in row:
            if visible:
                count += 1

    print('Visible trees: {}'.format(count))


if __name__ == '__main__':
    main()
