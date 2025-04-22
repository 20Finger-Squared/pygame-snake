from numpy import array
import pygame

from collections import deque  # for the snake
from random import randint  # for the random position of the snake


def random_position(numpyArray) -> tuple[int, ...]:
    shape: tuple[int, int] = numpyArray.shape
    return tuple(randint(0, shape[i] - 1) for i in range(len(shape)))


def calc_positions(
    interableOne: tuple | list, interableTwo: tuple | list, add: bool
        ) -> tuple[int, int]:

            if len(interableOne) != len(interableTwo):
                raise ValueError("interables need to be same length")

            if add:
                return tuple(
                    interableOne[i] + interableTwo[i] for i in range(len(interableTwo))
                )
            else:
                return tuple(
                    interableOne[i] * interableTwo[i] for i in range(len(interableTwo))
                )


class GUIBoard:
    def display_board(
        self, border_width, snake_color, board_color, apple_color
    ) -> None:
        global board
        columns = board.shape[1]


        rows = board.shape[0]
        screen_with_borders = SCREEN_SIZE[0] + border_width

        cell_size = screen_with_borders // columns

        for row in range( rows ):
            for col in range( columns ):
                x = col * cell_size
                y = row * cell_size

                rect = pygame.Rect(x+border_width, y+border_width, cell_size - border_width, cell_size - border_width)

                value = board[row, col]
                color = (
                    snake_color
                    if value == SNAKE_ID
                    else apple_color if value == APPLE_ID else board_color
                )

                pygame.draw.rect(screen, color, rect)

        pygame.display.flip()


class Snake:
    def __init__(self) -> None:
        self.snake = deque([random_position(board)] * 3)
        self.SNAKE_HEAD = -1
        self.direction = (0, 0)
        board[self.snake[self.SNAKE_HEAD]] = 1

    def die(self) -> None:
        global running
        print(f"You lost. Score {len(self.snake)-1}")
        running = False

    def move_snake(self) -> None:
        global board
        global apple

        new_position: tuple[int, ...] = tuple(
            map(
                lambda x, y: (x + y) % BOARD_WIDTH,
                self.snake[self.SNAKE_HEAD],
                self.direction,
            )
        )

        if new_position in self.snake and not self.direction == (0, 0):
            self.die()

        self.snake.append(new_position)
        board[*new_position] = 1

        if not new_position == apple:
            if not self.direction == (0, 0):
                old = self.snake.popleft()
                board[old] = BOARD_ID
            else:
                old = self.snake.popleft()
        else:
            while True:
                apple = random_position(board)
                if not apple in self.snake:
                    break

            board[apple] = APPLE_ID

    def get_direction(self) -> None:
        UP = (-1, 0)
        DOWN = (1, 0)
        RIGHT = (0, 1)
        LEFT = (0, -1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not self.direction == RIGHT:
            self.direction = LEFT
        if keys[pygame.K_RIGHT] and not self.direction == LEFT:
            self.direction = RIGHT
        if keys[pygame.K_DOWN] and not self.direction == UP:
            self.direction = DOWN
        if keys[pygame.K_UP] and not self.direction == DOWN:
            self.direction = UP


add_positions = lambda x, y: calc_positions(x, y, True)
multiply = lambda x, y: calc_positions(x, y, False)


# constants
APPLE_ID = 2
BOARD_ID = 0
SNAKE_ID = 1
SCREEN_SIZE: tuple = (500, 500)
BOARD_WIDTH: int = 14

if (SCREEN_SIZE[0] // BOARD_WIDTH) == 0:
    print(BOARD_WIDTH)
    raise ValueError("The Boardwidth musn't be greater than the screen size")


board = array([[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_WIDTH)])


GuiBoard = GUIBoard()
snake = Snake()

# the apple is basically just a
# position to render and check for so nothing unique is needed
apple = random_position(board)
board[apple] = APPLE_ID

# pygame variables
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running: bool = True

while running:
    GuiBoard.display_board(1, "blue", "green", "red")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    snake.move_snake()
    snake.get_direction()
    clock.tick(10)


pygame.quit()
