import pathlib
import random
import typing as tp
from typing import Any

T = tp.TypeVar("T")


def read_sudoku(filename: Any) -> Any:

    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(values: Any) -> Any:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: list, n: int) -> list:

    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(values: list, pos: tuple) -> Any:

    i = pos[0]
    return values[i]


def get_col(values: list, pos: tuple) -> list:

    return [values[i][pos[1]] for i in range(len(values))]


def get_block(values: list, pos: tuple) -> list:

    row = pos[0] // 3
    row_start = row * 3
    row_end = row_start + 3

    col = pos[1] // 3
    col_start = col * 3
    col_end = col_start + 3

    result = []

    for i in range(row_start, row_end):
        for n in range(col_start, col_end):
            result.append(values[i][n])

    return result


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Tuple[int, int]:

    for i in grid:
        if "." in i:
            empty_pos = (grid.index(i), i.index("."))
            return empty_pos
        else:
            empty_pos = (-1, -1)
    return empty_pos


def find_possible_values(grid: list, pos: tuple) -> set:
    pos_val = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    return (
        set(pos_val)
        - set(str(get_block(grid, pos)))
        - set(str(get_col(grid, pos)))
        - set(str(get_row(grid, pos)))
    )


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:

    position = find_empty_positions(grid)
    if not position:
        return grid
    row, col = position
    for value in find_possible_values(grid, position):
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
    grid[row][col] = "."
    return None


def check_solution(solution: list) -> bool:

    for row in range(len(solution)):
        values = set(get_row(solution, (row, 0)))
        if values != set("123456789"):
            return False

    for col in range(len(solution)):
        values = set(get_col(solution, (0, col)))
        if values != set("123456789"):
            return False

    for row in (0, 3, 6):
        for col in (0, 3, 6):
            values = set(get_block(solution, (row, col)))
            if values != set("123456789"):
                return False

    return True


def generate_sudoku(N: int) -> list:

    grid = solve([["."] * 9 for _ in range(9)])
    N = 81 - min(81, N)

    while N:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != ".":
            grid[row][col] = "."
            N -= 1
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        try:
            grid = read_sudoku(fname)
            display(grid)
            solution = solve(grid)
            if not solution:
                print(f"Puzzle {fname} can't be solved")
            else:
                display(solution)
        except:
            print(f"Puzzle {fname} can't be solved")
            pass
