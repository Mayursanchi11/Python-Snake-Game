import pygame
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
SNAKE_SPEED = 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

class Snake:
    def __init__(self):
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = (1, 0)

    def update(self, food):
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0] * GRID_SIZE, head_y + self.direction[1] * GRID_SIZE)
        self.positions.insert(0, new_head) # type: ignore

        if new_head == food.position:
            food.randomize()
        else:
            self.positions.pop()

    def change_direction(self, direction):
        if (direction[0], direction[1]) != (-self.direction[0], -self.direction[1]):
            self.direction = direction

    def check_collision(self):
        head = self.positions[0]
        return (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in self.positions[1:]
        )

    def draw(self, surface):
        for segment in self.positions:
            pygame.draw.rect(surface, GREEN, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

snake = Snake()
food = Food()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1, 0))

    snake.update(food)
    
    if snake.check_collision():
        running = False

    screen.fill(WHITE)
    snake.draw(screen)
    food.draw(screen)
    pygame.display.flip()

    clock.tick(SNAKE_SPEED)

pygame.quit()
