def main():
    file = open('input', 'r')
    lines = file.readlines()

    matrix_width = len(lines[0].rstrip())
    matrix_height = len(lines)

    rows = [[] for y in range(matrix_height)]
    cols = [[] for x in range(matrix_width)]

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

    matrix_visible = [[False for x in range(len(rows[0]))] for y in range(len(cols[0]))]
    matrix_scenic = [[1 for x in range(len(rows[0]))] for y in range(len(cols[0]))]

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
            matrix_visible[row_idx][col_idx] = matrix_visible[row_idx][col_idx] or visible

            if is_edge:
                matrix_scenic[row_idx][col_idx] = 0
            else:
                visible_before = 0
                for idx in range(col_idx-1, -1, -1):
                    visible_before += 1
                    if row[idx] >= height:
                        break

                visible_after = 0
                for idx in range(col_idx+1, matrix_width):
                    visible_after += 1
                    if row[idx] >= height:
                        break
                matrix_scenic[row_idx][col_idx] *= visible_before * visible_after


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
            matrix_visible[row_idx][col_idx] = matrix_visible[row_idx][col_idx] or visible

            if is_edge:
                matrix_scenic[row_idx][col_idx] = 0
            else:
                visible_before = 0
                for idx in range(row_idx-1, -1, -1):
                    visible_before += 1
                    if col[idx] >= height:
                        break

                visible_after = 0
                for idx in range(row_idx+1, matrix_height):
                    visible_after += 1
                    if col[idx] >= height:
                        break
                matrix_scenic[row_idx][col_idx] *= visible_before * visible_after

    count = 0
    for row in matrix_visible:
        for visible in row:
            if visible:
                count += 1

    biggest_score = 0
    for row in matrix_scenic:
        for score in row:
            if score > biggest_score:
                biggest_score = score

    print('Visible trees: {}'.format(count))
    print('Biggest score: {}'.format(biggest_score))


if __name__ == '__main__':
    main()
