import random
import typing as tp
import zoneinfo
from random import choice
from typing import List, Type

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:

        if randomize:
            field = [
                [choice([0, 1]) for x in range(self.cell_width)] for y in range(self.cell_height)
            ]
        else:
            field = [[0 for x in range(self.cell_width)] for y in range(self.cell_height)]

        return field

    def draw_grid(self) -> None:

        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] != 1:
                    colour = "white"
                else:
                    colour = "green"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(colour),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                )

    def get_neighbours(self, cell: Cell):

        nei_list = []
        y, x = cell[0], cell[1]
        if 0 < y:
            nei_list.append(self.grid[y - 1][x])
        if y < self.cell_height - 1:
            nei_list.append(self.grid[y + 1][x])
        if x > 0:
            nei_list.append(self.grid[y][x - 1])
        if x < self.cell_width - 1:
            nei_list.append(self.grid[y][x + 1])
        if y > 0 and x > 0:
            nei_list.append(self.grid[y - 1][x - 1])
        if y > 0 and x < self.cell_width - 1:
            nei_list.append(self.grid[y - 1][x + 1])
        if y < self.cell_height - 1 and x > 0:
            nei_list.append(self.grid[y + 1][x - 1])
        if y < self.cell_height - 1 and x < self.cell_width - 1:
            nei_list.append(self.grid[y + 1][x + 1])
        return nei_list

    def get_next_generation(self) -> Grid:
        buffer = self.create_grid(randomize=False)
        field = self.grid
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                c = field[y][x]
                cc = (y, x)
                nei = self.get_neighbours(cc)
                nei_len = nei.count(1)
                if c == 0:
                    buffer[y][x] = 1 if nei_len == 3 else 0
                else:
                    buffer[y][x] = 1 if nei_len in (2, 3) else 0
        field = buffer
        # assert isinstance(field, object)
        return field


if __name__ == "__main__":
    game = GameOfLife(640, 480, 10, 1)
    game.run()
