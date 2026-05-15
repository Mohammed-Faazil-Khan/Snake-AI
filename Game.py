import pygame
import random

pygame.init()

clock = pygame.time.Clock()

s_width = 640
s_height = 480
dx = 0
dy = 0
x = s_width//2
y = s_height//2
food_x = random.randrange(0, s_width, 20)
food_y = random.randrange(0, s_height, 20)
game_over = False
snake = []
snake_length = 1
score = 0
font = pygame.font.SysFont("arial",25)

screen = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption("Snake game learnt by AI")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -20
                dy = 0
            elif event.key == pygame.K_RIGHT:
                dx = 20
                dy = 0
            elif event.key == pygame.K_DOWN:
                dy = 20
                dx = 0
            elif event.key == pygame.K_UP:
                dy = -20
                dx = 0
    x += dx
    y += dy

    if x < 0 or x >= s_width or y < 0 or y >= s_height:
        running = False

    if x == food_x and y == food_y:
        food_x = random.randrange(0, s_width, 20)
        food_y = random.randrange(0, s_height, 20)
        snake_length += 1
        score += 1
    for block in snake[:-1]:
        if block == [x,y]:
            running = False

    screen.fill((0,0,0))

    score_text = font.render(f"Score:{score}", True, "white")
    screen.blit(score_text, [10, 10])

    pygame.draw.rect(screen,"green",[x,y,20,20])
    pygame.draw.rect(screen, "red", [food_x, food_y, 20, 20])

    snake.append([x,y])
    if len(snake) > snake_length:
        del snake[0]
    for block in snake:
        pygame.draw.rect(screen,"green",[block[0],block[1],20,20])

    pygame.display.update()
    clock.tick(10)

pygame.quit()
