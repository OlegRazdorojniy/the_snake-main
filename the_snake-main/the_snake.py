"""Calling Libraries"""
from random import randint
import pygame


# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
"""GameObject"""


class GameObject():
    """__init__"""

    def __init__(self, position=0, body_color=0):
        self.position = position
        self.body_color = body_color

    """draw"""

    def draw(self):
        """Pass"""
        pass


"""Apple"""


class Apple(GameObject):
    """__init__"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    """randomize_pozition"""

    def randomize_position(self):
        """Return"""
        return randint(0, SCREEN_WIDTH // 20) * 20, \
            randint(0, SCREEN_HEIGHT // 20) * 20

    """draw"""

    def draw(self, surface):
        """Realisation draw"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


"""Snake"""


class Snake(GameObject):
    """__init__"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 40 * 20, SCREEN_HEIGHT // 40 * 20)]
        self.direction = (1, 0)
        self.next_direction = None
        self.last = None

    """update_direction"""

    def update_direction(self):
        """Realisation update_direction"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    """move"""

    def move(self):
        """Realisation move"""
        if self.direction == UP:
            self.positions.insert(0, (self.positions[0][0],
                                      self.positions[0][1] - 20))
        elif self.direction == DOWN:
            self.positions.insert(0, (self.positions[0][0],
                                      self.positions[0][1] + 20))
        elif self.direction == LEFT:
            self.positions.insert(0, (self.positions[0][0] - 20,
                                      self.positions[0][1]))
        elif self.direction == RIGHT:
            self.positions.insert(0, (self.positions[0][0] + 20,
                                      self.positions[0][1]))
        self.last = self.positions[-1]
        self.positions.pop(-1)

    """draw"""

    def draw(self, surface):
        """Realisation draw"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    """get_head_position"""

    def get_head_position(self):
        """Return"""
        return self.positions[0]

    """reset"""

    def reset(self):
        """Realisation reset"""
        self.length = 1
        self.positions = [(320, 240)]
        self.directoin = (1, 0)
        self.next_direction = None
        self.body_color = (0, 255, 0)


"""hadle_keys"""


def handle_keys(game_object):
    """Realisation handle_keys"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


"""check_direction"""


def check_direction(position, direction):
    """Realisation check_direction"""
    if direction == UP:
        position += [(position[-1][0],
                      position[-1][1] + 20)]
    elif direction == DOWN:
        position += [(position[-1][0],
                      position[-1][1] - 20)]
    elif direction == LEFT:
        position += [(position[-1][0] + 20,
                      position[-1][1])]
    elif direction == RIGHT:
        position += [(position[-1][0] - 20,
                      position[-1][1] + 20)]


"""main"""


def main():
    """Realisation main"""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            check_direction(snake.positions, snake.direction)
            snake.length += 1
            apple.position = apple.randomize_position()
            if apple.position[0] >= SCREEN_WIDTH - 20\
                    or apple.position[0] <= 20:
                apple.position = apple.randomize_position()
            elif apple.position[1] >= SCREEN_HEIGHT - 20\
                    or apple.position[1] <= 20:
                apple.position = apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.positions[0] in snake.positions[1:]:
            for j in range(0, len(snake.positions)):
                last_rect = pygame.Rect(
                    (snake.positions[j][0], snake.positions[j][1]),
                    (GRID_SIZE, GRID_SIZE)
                )
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            snake.reset()

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()
