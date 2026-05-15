# 🐍 Snake AI — Deep Reinforcement Learning

An AI agent that learns to play Snake entirely by itself using 
Deep Q-Learning (DQN) — with zero human guidance, 
only rewards and punishments!

Built by a Class 12 graduate as a self-taught AI/ML project.

---

## 📈 Learning Progress

| Game | Best Score |
|------|-----------|
| 1    | 0 (random)|
| 45   | 6         |
| 79   | 29        |
| 93   | 49        |
| 104  | 54        |
| 126  | 62        |

The agent went from **scoring 0 to scoring 62** in just 
126 games — entirely on its own! 🤯

---

## 🧠 How It Works
State (11 values) → Neural Network → Action (3 values)
↑
Learns from rewards

### The AI sees 11 things:
- Is there danger straight ahead?
- Is there danger to the right?
- Is there danger to the left?
- Which direction is the snake moving?
- Where is the food relative to the snake?

### The AI decides:
- Go straight
- Turn right
- Turn left

### The AI learns:
- Ate food → reward +10 ✅
- Hit wall or itself → reward -10 ❌
- Repeat 100+ games → gets smarter!

---

## 🏗️ Architecture
Input Layer  → 11 neurons (game state)
Hidden Layer → 256 neurons (pattern recognition)
Output Layer → 3 neurons (possible actions)

Uses **Deep Q-Learning (DQN)** with:
- Experience replay memory (100,000 moves)
- Epsilon-greedy exploration
- Gamma = 0.9 (values future rewards)

---

## 🛠️ Tech Stack

- **Python** — core language
- **Pygame** — game engine
- **PyTorch** — neural network
- **NumPy** — state representation

---

## 🚀 How to Run

### Install dependencies
```bash
pip install pygame torch numpy
```

### Run the AI
```bash
python agent.py
```

Watch the AI learn in real time! Scores improve 
noticeably after game 80! 🔥

---

## 📁 Project Structure
Snake-AI/
├── Snake_Game.py  # Game environment
├── agent.py       # AI brain + training loop
└── model.py       # Neural network + Q-Trainer

---

## 💡 Key Concepts Learned

- Reinforcement Learning
- Deep Q-Networks (DQN)
- Neural Networks with PyTorch
- Experience Replay
- Epsilon-Greedy Exploration
- Object Oriented Programming

---

## 👨‍💻 About

Built by **Mohammed Faazil Khan**
Aspiring AI/ML Engineer | Mumbai, India

- 🎓 Class 12 CBSE — 89% | Physics Section Topper
- 🐍 Self taught Python + ML
- 🎯 Targeting BTech AI/ML

⭐ Star this repo if you found it interesting!
