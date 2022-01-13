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
    cord_i, cord_j = coord
    path_ = randint(0, 1)
    lenn_grid = len(grid[0]) - 2
    if path_ != 0:
        if cord_j == lenn_grid:
            if cord_i != 1:
                grid[cord_i - 1][cord_j] = " "
        else:
            grid[cord_i][cord_j + 1] = " "
    else:
        if cord_i == 0:
            if cord_j != lenn_grid:
                grid[cord_i][cord_j + 1] = " "
        else:
            grid[cord_i - 1][cord_j] = " " 
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

    for row in range(len(grid) - 1):
        for col in range(len(grid[row]) - 1):
            if grid[row][col] == k:
                if grid[row + 1][col] == 0:
                    grid[row + 1][col] = k + 1
                if grid[row - 1][col] == 0:
                    grid[row - 1][col] = k + 1
                if grid[row][col + 1] == 0:
                    grid[row][col + 1] = k + 1
                if grid[row][col - 1] == 0:
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
    x, y = exit_coord
    exits_lists = [exit_coord]
    num = int(grid[x][y]) + 1
    k = num
    n = num
    row = len(grid)
    col = len(grid[0])
    while num != 1:
        k -= 1
        if x - 1 >= 0 and grid[x - 1][y] == k:
            exits_lists.append((x - 1, y))
            exit_coord = (x - 1, y)
            x, y = exit_coord
            num = int(grid[x][y])
        if x + 1 <= row and grid[x + 1][y] == k:
            exits_lists.append((x + 1, y))
            exit_coord = (x + 1, y)
            x, y = exit_coord
            num = int(grid[x][y])
        if y - 1 >= 0 and grid[x][y - 1] == k:
            exits_lists.append((x, y - 1))
            exit_coord = (x, y - 1)
            x, y = exit_coord
            num = int(grid[x][y])
        if y + 1 < col and grid[x][y + 1] == k:
            exits_lists.append((x, y + 1))
            exit_coord = (x, y + 1)
            x, y = exit_coord
            num = int(grid[x][y])
    if len(exits_lists) != n:
        grid[exits_lists[-1][0]][exits_lists[-1][1]] = " "
        exits_lists.pop(len(exits_lists) - 1)
        shortest_path(grid, exit_coord)
    return exits_lists


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord

    if (
        coord != (0, 0)
        and coord != (0, len(grid) - 1)
        and coord != (len(grid) - 1, 0)
        and coord != (len(grid[0]) - 1, len(grid) - 1)
    ):
        if x == 0:
            if grid[x + 1][y] == "■":
                return True
        if x == len(grid) - 1:
            if grid[x - 1][y] == "■":
                return True
        if y == 0:
            if grid[x][y + 1] == "■":
                return True
        if y == len(grid[0]) - 1:
            if grid[x][y - 1] == "■":
                return True
        return False
    return True


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
    if not encircled_exit(grid, start) and not encircled_exit(grid, fin):
        grid[start[0]][start[1]] = 1
        grid[fin[0]][fin[1]] = 0
        k = 1 
        for row in range(len(grid) - 1):
            for col in range(len(grid[row]) - 1):
                if grid[row][col] == " ":
                    grid[row][col] = 0    
        while grid[fin[0]][fin[1]] == 0:
            grid = make_step(grid, k)
            k += 1
        return grid, shortest_path(grid, fin)
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
    #print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    #print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    #print(pd.DataFrame(MAZE))
