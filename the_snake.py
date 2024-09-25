from random import randint
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
    """
    Родительский класс для игровых объектов.

    Аттрибуты:
    position: Содержит базовую позицию игрового объекта.
    body_color: Содержит базовый цвет игрового объекта.

    Методы:
    __init__:
        Инициализирует игровой объект.
    draw:
        Заготовка метода отрисовки игровых объектов для
        дальнейшего переопределения.
    """

    position: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    body_color: tuple[int, int, int] = (0, 0, 0)

    def __init__(self) -> None:
        """Инициализирует объект."""
        self.position = self.position
        self.body_color = self.body_color

    def draw(self) -> None:
        """Заготовка метода для отрисовки объекта на игровом поле."""
        pass


def randomize_position() -> tuple[int, int]:
    """Генерирует случайные координаты."""
    return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Apple(GameObject):
    """
    Класс яблока.

    Аттрибуты:
    body_color:
        Цвет яблока.

    Методы:
    __init__:
        Инициализирует объект.
    randomize_position:
        Генерирует случайные координаты (x, y) для объекта.
    draw:
        Отрисовывает яблоко на игровом поле.
    """

    body_color = (255, 0, 0)

    def __init__(self) -> None:
        """Инициализирует объект."""
        self.position = randomize_position()
        self.body_color = Apple.body_color

    def draw(self) -> None:
        """Отрисовывает объект на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс змейки.

    Аттрибуты:
    length:
        Числовое значение длины змейки.
    positions:
        Список кортежей, содержащих координаты сегментов змейки.
    direction:
        Направление движения змейки.
    next_direction:
        Следующее направление движения змейки.
    body_color:
        Цвет змейки.
    last:
        Координаты последнего сегмента змейки.

    Методы:
    __init__:
        Инициализирует объект.
    update_direction:
        Обновляет направление движения змейки.
    move:
        Обновляет координаты головы змейки при её движении.
    get_head_position:
        Возвращает координаты головы змейки.
    reset:
        Начинает игру сначала при столкновении змейки с самой собой.
    draw:
        Отрисовывает змейку на игровом поле.
    """

    length: int = 1
    positions: list[tuple[int, int]] = [
        ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    direction: tuple[int, int] = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR
    last = positions[-1]

    def __init__(self) -> None:
        """Инициализирует объект."""
        super().__init__()
        self.positions = Snake.positions
        self.direction = Snake.direction
        self.body_color = Snake.body_color
        self.length = Snake.length
        self.last = Snake.last

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обноляет координаты головы змейки при движении."""
        head_position = self.get_head_position()
        if self.direction == RIGHT:
            if head_position[0] == 620:
                self.positions.insert(0, (0,
                                          head_position[1]))
            else:
                self.positions.insert(0, (head_position[0] + GRID_SIZE,
                                          head_position[1]))
        elif self.direction == LEFT:
            if head_position[0] == 0:
                self.positions.insert(0, (620,
                                          head_position[1]))
            else:
                self.positions.insert(0, (head_position[0] - GRID_SIZE,
                                          head_position[1]))
        elif self.direction == DOWN:
            if head_position[1] == 460:
                self.positions.insert(0, (head_position[0],
                                          0))
            else:
                self.positions.insert(0, (head_position[0],
                                          head_position[1] + GRID_SIZE))
        elif self.direction == UP:
            if head_position[1] == 0:
                self.positions.insert(0, (head_position[0],
                                          460))
            else:
                self.positions.insert(0, (head_position[0],
                                          head_position[1] - GRID_SIZE))

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        head_position: tuple[int, int] = self.positions[0]
        return head_position

    def reset(self) -> None:
        """Сбрасывает параметры змейки до заводских значений."""
        head_position = self.get_head_position()
        if self.positions.count(head_position) > 1:
            self.length = 1
            self.direction = Snake.direction
            self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
            screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self) -> None:
        """Отрисовывает змейку на игровом поле."""
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


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш, обновляя аттрибут next_direction."""
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
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    status = True
    print(apple.position)

    while status:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = randomize_position()
            while apple.position in snake.positions:
                apple.position = randomize_position()
        else:
            snake.last = snake.positions.pop(-1)
        snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
