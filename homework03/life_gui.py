import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.height, self.width = self.life.rows * cell_size, self.life.cols * self.cell_size
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.speed = speed

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for y in range(self.height):
            for x in range(self.width):
                if self.life.curr_generation[y][x] != 1:
                    colour = "white"
                else:
                    colour = "green"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(colour),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                )

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.life.curr_generation = self.life.create_grid(randomize=True)

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
            self.life.curr_generation = self.life.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
