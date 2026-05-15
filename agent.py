import torch
import random
import numpy as np
from collections import deque
from Snake_Game import SnakeGame
from model import LinearQNet, QTrainer

# Constants
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
            point_right =    [g.x, g.y + 20]
            point_left =     [g.x, g.y - 20]
        elif g.dy == 20:
            point_straight = [g.x, g.y + 20]
            point_right =    [g.x - 20, g.y]
            point_left =     [g.x + 20, g.y]
        elif g.dx == -20:
            point_straight = [g.x - 20, g.y]
            point_right =    [g.x, g.y - 20]
            point_left =     [g.x, g.y + 20]
        elif g.dy == -20:
            point_straight = [g.x, g.y - 20]
            point_right =    [g.x + 20, g.y]
            point_left =     [g.x - 20, g.y]

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
        # store one experience in memory
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        # train on a batch of past experiences
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = list(self.memory)

        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        # train on just this one experience
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # start random, get smarter over time
        self.epsilon = 80 - self.n_games
        action = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            # random move (exploration)
            idx = random.randint(0, 2)
            action[idx] = 1
        else:
            # model's best move (exploitation)
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tensor)
            idx = torch.argmax(prediction).item()
            action[idx] = 1

        return action

    def train(self):
        best_score = 0
        while True:
            # get current state
            state = self.get_state()

            # get action
            action = self.get_action(state)

            # perform action
            reward, game_over, score = self.game.play_step(action)

            # get new state
            new_state = self.get_state()

            # train short memory
            self.train_short_memory(state, action, reward, new_state, game_over)

            # remember
            self.remember(state, action, reward, new_state, game_over)

            if game_over:
                # train long memory
                self.game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > best_score:
                    best_score = score

                print(f"Game: {self.n_games} Score: {score} Best: {best_score}")

if __name__ == "__main__":
    agent = Agent()
    agent.train()