from random import choice, randint

import pygame

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color = None

    def __init__(self, position, body_color) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    body_color = APPLE_COLOR

    @staticmethod
    def randomize_position():
        return (randint(0, SCREEN_HEIGHT) * GRID_SIZE,
                randint(0, SCREEN_WIDTH) * GRID_SIZE)

    def __init__(self):
        self.position = self.randomize_position()

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    length = 1
    positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)

    def __init__(self,
                 position,
                 body_color,
                 lenght,
                 direction):
        super().__init__(position)
        self.direction = direction
        self.body_color = body_color
        self.length = lenght

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_position = self.get_head_position()
        if self.direction == RIGHT:
            if head_position[0] == 640:
                self.positions.insert(0, (0,
                                          head_position[1]))
            else:
                self.positions.insert(0, (head_position[0] + GRID_SIZE,
                                          head_position[1]))
        elif self.direction == LEFT:
            if head_position[0] == 0:
                self.positions.insert(0, (SCREEN_WIDTH,
                                          head_position[1]))
            else:
                self.positions.insert(0, (head_position[0] - GRID_SIZE,
                                          head_position[1]))
        elif self.direction == UP:
            if head_position[1] == 480:
                self.positions.insert(0, (head_position[0],
                                          0))
            else:
                self.positions.insert(0, (head_position[0],
                                          head_position[1] + GRID_SIZE))
        elif self.direction == DOWN:
            if head_position[1] == 0:
                self.positions.insert(0, (head_position[0],
                                          SCREEN_HEIGHT))
            else:
                self.positions.insert(0, (head_position[0],
                                          head_position[1] - GRID_SIZE))

    def get_head_position(self):
        head_position = self.positions[0]
        return head_position

    def reset(self):
        pass

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @staticmethod
    def handle_keys(game_object):
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


def main():
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        snake.handle_keys

    # Тут опишите основную логику игры.
    # ...


if __name__ == '__main__':
    main()


# Метод draw класса Apple


# # Метод draw класса Snake

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя


# Метод обновления направления после нажатия на кнопку
