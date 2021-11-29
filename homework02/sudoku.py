import pathlib
import typing as tp

T = tp.TypeVar("T")
import random
from typing import Any

def read_sudoku(filename: Any) -> Any:
    """Прочитать Судоку из указанного файла

    Cделала программу read_sudoku and create_grid в одной"""
    
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid

def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
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
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    »> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    »> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """

    return [values[i : i + n] for i in range(0, len(values), n)]

    

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    i = pos[0] 
    return grid[i]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    i = pos[1]
    col = []
    for j in range(0, 9):
        list_in_list = grid[j]
        num = list_in_list[i] 
        col.append(num)
    return col 


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    row = pos[0] // 3
    row_start = row * 3
    row_end = row_start + 3

    col = pos[1] // 3
    col_start = col * 3
    col_end = col_start + 3

    result = []
    
    for i in range(row_start, row_end):
        for n in range(col_start, col_end):
            result.append(grid[i][n])

    return result    

def find_empty_positions(grid: list) -> tuple:
    """Найти первую свободную позицию в пазле
    »> find_empty_positions ([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    »> find_empty_positions ([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    »> find_empty_positions ([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == ".":
                return (i, j)
    return ()

def find_possible_values(grid: list, pos: tuple) -> set:
    """Вернуть множество возможных значения для указанной позиции
    »> grid = read_sudoku('puzzle1.txt')
    »> values = find_possible_values(grid, (0,2))
    »> values == {'1', '2', '4'}
    True
    »> values = find_possible_values(grid, (4,7))
    »> values == {'2', '5', '9'}
    True
    """
    
    gorisontal = get_row(grid, pos)
    #print(gorisontal)
    vertical = get_col(grid, pos)
    #print(vertical)
    block = get_block(grid, pos)
    #print(block)
    new_value_list = []
    list_val = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    list_same = []
    for j in list_val:
        for i in range(0, 9):
            if (gorisontal[i] == j):
                list_same.append(j)
            if (vertical[i] == j):
                list_same.append(j)
            if (block[i] == j):
               list_same.append(j)
    list_val, list_same = set(list_val), set(list_same)
    return list_val.difference(list_same)

def solve(grid: list) -> list:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
    1. Найти свободную позицию
    2. Найти все возможные значения,
    которые могут находиться на этой позиции
    3. Для каждого возможного значения:
    3.1. Поместить это значение на эту позицию
    3.2. Продолжить решать оставшуюся часть пазла
    »> grid = read_sudoku('puzzle1.txt')
    """
    
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
    return []

def check_solution(solution: list) -> bool:
    """Если решение solution верно,
    то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles
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
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
