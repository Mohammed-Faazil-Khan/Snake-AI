import torch
import random
import numpy as np
from collections import deque
from Snake_Game import SnakeGame
from model import LinearQNet, QTrainer
import matplotlib.pyplot as plt

def plot(scores, mean_scores, n_games):
    if n_games % 10 != 0:
        return

    plt.clf()
    plt.title("Snake AI Training Progress")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(scores, label="Score")
    plt.plot(mean_scores, label="Average Score")
    plt.legend()
    plt.ylim(ymin=0)
    plt.savefig("progress.png")  # saves as image!
    plt.close()  # closes immediately to free RAM!

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.game = SnakeGame()
        self.n_games = 0
        self.epsilon = 0      # randomness
        self.gamma = 0.9      # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # automatic max size!
        self.model = LinearQNet()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def is_danger(self, point):
        g = self.game
        x, y = point
        if x < 0 or x >= 640 or y < 0 or y >= 480:
            return True
        if point in g.snake:
            return True
        return False

    def get_state(self):
        g = self.game

        if g.dx == 20:
            point_straight = [g.x + 20, g.y]
            point_right = [g.x, g.y + 20]
            point_left = [g.x, g.y - 20]
        elif g.dy == 20:
            point_straight = [g.x, g.y + 20]
            point_right = [g.x - 20, g.y]
            point_left = [g.x + 20, g.y]
        elif g.dx == -20:
            point_straight = [g.x - 20, g.y]
            point_right = [g.x, g.y - 20]
            point_left = [g.x, g.y + 20]
        elif g.dy == -20:
            point_straight = [g.x, g.y - 20]
            point_right = [g.x + 20, g.y]
            point_left = [g.x - 20, g.y]

        state = [
            self.is_danger(point_straight),
            self.is_danger(point_right),
            self.is_danger(point_left),
            g.dx == 20,
            g.dx == -20,
            g.dy == -20,
            g.dy == 20,
            g.food_x < g.x,
            g.food_x > g.x,
            g.food_y < g.y,
            g.food_y > g.y
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = list(self.memory)

        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        action = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            idx = random.randint(0, 2)
            action[idx] = 1
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tensor)
            idx = torch.argmax(prediction).item()
            action[idx] = 1

        return action

    def train(self):
        scores = []
        mean_scores = []
        total_score = 0
        best_score = 0

        while True:
            state = self.get_state()
            action = self.get_action(state)
            reward, game_over, score = self.game.play_step(action)
            new_state = self.get_state()

            self.train_short_memory(state, action, reward, new_state, game_over)
            self.remember(state, action, reward, new_state, game_over)

            if game_over:
                self.game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > best_score:
                    best_score = score

                print(f"Game: {self.n_games} Score: {score} Best: {best_score}")

                scores.append(score)
                total_score += score
                mean_score = total_score / self.n_games
                mean_scores.append(mean_score)
                plot(scores, mean_scores, self.n_games)

if __name__ == "__main__":
    agent = Agent()
    agent.train()