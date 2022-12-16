def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def is_invisible_on_left(tree_grid, row_index, column_index):
    tree_height = tree_grid[row_index][column_index]
    for side_tree_height in tree_grid[row_index][0:column_index]:
        if int(side_tree_height) >= int(tree_height):
            return True
    return False


def is_invisible_on_right(tree_grid, row_index, column_index):
    tree_height = tree_grid[row_index][column_index]
    for side_tree_height in tree_grid[row_index][column_index + 1:]:
        if int(side_tree_height) >= int(tree_height):
            return True
    return False


def is_invisible_on_top(tree_grid, row_index, column_index):
    tree_height = tree_grid[row_index][column_index]
    for side_tree_height_row in tree_grid[0:row_index]:
        side_tree_height = side_tree_height_row[column_index]
        if int(side_tree_height) >= int(tree_height):
            return True
    return False


def is_invisible_on_bottom(tree_grid, row_index, column_index):
    tree_height = tree_grid[row_index][column_index]
    for side_tree_height_row in tree_grid[row_index + 1:]:
        side_tree_height = side_tree_height_row[column_index]
        if int(side_tree_height) >= int(tree_height):
            return True
    return False


def is_invisible(tree_grid, row_index, column_index):
    invisible_on_left = is_invisible_on_left(tree_grid, row_index, column_index)
    invisible_on_right = is_invisible_on_right(tree_grid, row_index, column_index)
    invisible_on_top = is_invisible_on_top(tree_grid, row_index, column_index)
    invisible_on_bottom = is_invisible_on_bottom(tree_grid, row_index, column_index)

    # invisible_on_right and invisible_on_left
    return invisible_on_right and invisible_on_left and invisible_on_top and invisible_on_bottom


def part_one(tree_grid):
    invisible_trees = 0
    for row_index, tree_row in enumerate(tree_grid):
        for column_index, tree_height in enumerate(list(tree_row)):
            if is_invisible(tree_grid, row_index, column_index):
                invisible_trees += 1
    total_trees = len(tree_grid) * len(tree_grid[0])
    return total_trees - invisible_trees


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "30373",
        "25412",
        "65332",
        "33549",
        "35390"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 21)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day08-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 1477771
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 3579501
