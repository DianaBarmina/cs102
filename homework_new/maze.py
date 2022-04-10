from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    y, x = coord
    cols = len(grid[0])
    direction = randint(0, 1)
    if direction == 0:
        if y == 1:
            if x != cols - 2:
                grid[y][x + 1] = " "
        else:
            grid[y - 1][x] = " "
    else:
        if x != cols - 2:
            grid[y][x + 1] = " "
        else:
            if y != 1:
                grid[y - 1][x] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for _, cell in enumerate(empty_cells):
        grid = remove_wall(grid, cell)
    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits_list = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "X":
                exits_list.append((i, j))
    return exits_list


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == k:
                if row != len(grid) - 1 and grid[row + 1][col] == 0:
                    grid[row + 1][col] = k + 1
                if row != 0 and grid[row - 1][col] == 0:
                    grid[row - 1][col] = k + 1
                if col != len(grid[0]) - 1 and grid[row][col + 1] == 0:
                    grid[row][col + 1] = k + 1
                if col != 0 and grid[row][col - 1] == 0:
                    grid[row][col - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    short_path = []
    short_path.append(exit_coord)
    x, y = exit_coord
    cur_short = grid[x][y]
    sh_num = int(cur_short)
    while sh_num > 1:
        if x != len(grid) - 1 and grid[x + 1][y] == sh_num - 1:
            x += 1
            short_path.append((x, y))
        elif x != 0 and grid[x - 1][y] == sh_num - 1:
            x -= 1
            short_path.append((x, y))
        elif y != len(grid[0]) - 1 and grid[x][y + 1] == sh_num - 1:
            y += 1
            short_path.append((x, y))
        elif y != 0 and grid[x][y - 1] == sh_num - 1:
            y -= 1
            short_path.append((x, y))
        sh_num -= 1
    return short_path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    i, j = coord
    if i == 0:
        if grid[i + 1][j] == "■":
            return True
    elif i == len(grid) - 1:
        if grid[i - 1][j] == "■":
            return True
    elif j == 0:
        if grid[i][j + 1] == "■":
            return True
    elif j == len(grid[0]) - 1:
        if grid[i][j - 1] == "■":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) != 1:
        start, fin = exits
    else:
        return grid, exits
    work = deepcopy(grid)
    if not encircled_exit(grid, start) and not encircled_exit(grid, fin):
        grid[start[0]][start[1]] = 1
        grid[fin[0]][fin[1]] = 0
        k = 1
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == " ":
                    grid[row][col] = 0
        while grid[fin[0]][fin[1]] == 0:
            grid = make_step(grid, k)
            k += 1
        final_path = shortest_path(grid, fin)
        return work, final_path
    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
