import pygame
import random
import vidmaker
import atexit


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 25)

        # 1. Initialize the lightweight video maker frame recorder
        self.video = vidmaker.Video(path="snake_ai_demo.mp4", fps=30, resolution=(640, 480))

        # 2. Register an exit handler to save the video even if you force-quit (Ctrl+C)
        atexit.register(self.close_video)

        self.reset()

    def close_video(self):
        """Safely flushes memory and saves the video on program exit."""
        print("\n[System] Compiling and saving your portfolio video... Please wait.")
        try:
            self.video.export()
            print("[System] Success! Video saved safely as 'snake_ai_demo.mp4'")
        except Exception as e:
            print(f"[System] Video export failed: {e}")

    def reset(self):
        self.x = 320
        self.y = 240
        self.dx = 20
        self.dy = 0
        self.snake = []
        self.snake_length = 1
        self.score = 0
        self.food_x = random.randrange(0, 640, 20)
        self.food_y = random.randrange(0, 480, 20)

    def play_step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        clock_wise = [(20, 0), (0, 20), (-20, 0), (0, -20)]
        current_dir = clock_wise.index((self.dx, self.dy))
        if action == [1, 0, 0]:
            new_dir = current_dir
        elif action == [0, 1, 0]:
            new_dir = (current_dir + 1) % 4
        elif action == [0, 0, 1]:
            new_dir = (current_dir - 1) % 4
        self.dx, self.dy = clock_wise[new_dir]

        self.x += self.dx
        self.y += self.dy

        game_over = False
        if self.x < 0 or self.x >= 640 or self.y < 0 or self.y >= 480:
            return -10, True, self.score

        for block in self.snake[:-1]:
            if block == [self.x, self.y]:
                return -10, True, self.score

        reward = 0
        if self.x == self.food_x and self.y == self.food_y:
            self.food_x = random.randrange(0, 640, 20)
            self.food_y = random.randrange(0, 480, 20)
            self.snake_length += 1
            self.score += 1
            reward = 10

        self.snake.append([self.x, self.y])
        if len(self.snake) > self.snake_length:
            del self.snake[0]

        self.screen.fill((0, 0, 0))
        score_text = self.font.render(f"Score:{self.score}", True, "white")
        self.screen.blit(score_text, [10, 10])
        for block in self.snake:
            pygame.draw.rect(self.screen, "green", [block[0], block[1], 20, 20])
        pygame.draw.rect(self.screen, "red", [self.food_x, self.food_y, 20, 20])
        pygame.display.update()

        # 3. Capture the frame directly from Pygame's pixel buffer array
        self.video.update(pygame.surfarray.pixels3d(self.screen).swapaxes(0, 1), inverted=False)

        self.clock.tick(60)

        return reward, False, self.score