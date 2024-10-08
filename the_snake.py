from random import randint

import pygame as pg


# Константы для аннотирования:
POSITION = tuple[int, int]
POSITIONS = list[tuple[int, int]]
COLOR = tuple[int, int, int]

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: POSITION = (0, -1)
DOWN: POSITION = (0, 1)
LEFT: POSITION = (-1, 0)
RIGHT: POSITION = (1, 0)

# Центральная точка экрана:
CENTRAL_CELL: POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Базовый цвет
DEFAULT_COLOR: COLOR = (255, 255, 255)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOR = (0, 255, 0)

# Цвеи камня
ROCK_COLOR: COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Родительский класс для игровых объектов.

    Аттрибуты:
    position: Содержит базовую позицию игрового объекта.
    body_color: Содержит базовый цвет игрового объекта.

    Методы:
    draw:
        Заготовка метода отрисовки игровых объектов для
        дальнейшего переопределения.
    """

    def __init__(self,
                 body_color=DEFAULT_COLOR,
                 position=CENTRAL_CELL) -> None:
        """Инициализирует объект."""
        self.position: POSITION = position
        self.body_color: COLOR = body_color

    def draw(self) -> None:
        """Заготовка метода для отрисовки объекта на игровом поле."""
        pass


class Apple(GameObject):
    """
    Класс яблока.

    Аттрибуты:
    body_color:
        Цвет яблока.

    Методы:
    randomize_position:
        Генерирует случайные координаты (x, y) для объекта.
    draw:
        Отрисовывает яблоко на игровом поле.
    """

    def __init__(self,
                 body_color: COLOR = APPLE_COLOR,
                 position: POSITION = CENTRAL_CELL,
                 unavailable_positions: POSITIONS = [CENTRAL_CELL]) -> None:
        """Инициализирует объект."""
        super().__init__(position=position, body_color=body_color)
        self.randomize_position(unavailable_positions)

    def draw(self) -> None:
        """Отрисовывает объект на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, unavailable_positions: POSITIONS):
        """Генерирует случайную позицию для яблока."""
        while self.position in unavailable_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


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

    def __init__(self,
                 body_color: COLOR = SNAKE_COLOR,
                 position=CENTRAL_CELL,
                 ) -> None:
        """Инициализирует объект."""
        super().__init__(position=position, body_color=body_color)
        self.positions: POSITIONS = [CENTRAL_CELL]
        self.direction: POSITION = RIGHT
        self.length: int = 1
        self.last = self.positions[-1]
        self.next_direction = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обноляет координаты головы змейки при движении."""
        point_1, point_2 = self.get_head_position()
        self.position = (
            (point_1 + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH,
            (point_2 + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает параметры змейки до заводских значений."""
        self.length = 1
        self.direction = RIGHT
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]

    def draw(self) -> None:
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш игрока."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        pg.display.update()


if __name__ == '__main__':
    main()
