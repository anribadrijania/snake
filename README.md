# 🐍 Snake vs AI Snake

**Snake vs AI Snake** is a head-to-head competitive Snake game where you (the player) go up against an AI snake on a parallel grid. Race to eat apples, grow your snake, and avoid crashing — may the best snake win!

## 🎮 Features

- Classic snake gameplay with smooth controls
- Competing AI with two difficulty modes: `easy` and `hard`
- Simultaneous two-grid display: one for the player and one for the AI
- Sound effects for eating, crashing, winning, and losing
- Optional time-limited gameplay
- Hamiltonian path strategy for hard AI mode

## 🛠 Requirements

- Python 3.8+
- `pygame` library

Install dependencies:
```bash
pip install pygame
```

## 🚀 How to Play

1. **Clone the repository or download the game files.**

2. **Run the game** using Python:
   ```bash
   python game.py
   ```
   Or by running **SnakeGame.exe** 
3. Control your snake using the arrow keys:
   * ↑ Up
   * ↓ Down
   * ← Left
   * → Right


4. Objective:
    * Eat apples to grow your snake.
    * Avoid crashing into your own body.
    * Outlast or outscore the AI opponent.


5. Winning conditions:
    * The AI crashes and you survive.
    * You score more than the AI before time runs out.
    * You fill your entire grid before the AI does.

## ⚙️ Configuration
You can customize gameplay by passing a config object to run_game(config):
* grid_size: Tuple like (rows, cols)
* difficulty: "easy" or "hard"
* seed: Integer for deterministic food placement
* time_limit: Tuple like (minutes, seconds), or None for unlimited time

## 🔊 Sounds
Make sure the following files are in a sounds/ directory:
* biting.wav
* crashing.wav
* win.wav
* lose.wav

Without them, the game may still run but sound playback will fail.

## 📁 File Structure
```bash
├── game.py                 # Main game loop and rendering
├── snake.py                # Snake mechanics (movement, growth, collision)
├── ai.py                   # AI logic (easy/hard modes)
├── utils.py                # Helper functions (e.g., food generation)
├── sounds/
│   ├── biting.wav
│   ├── crashing.wav
│   ├── win.wav
│   └── lose.wav
└── README.md               # This file
```

## 🧠 AI Strategy
* Easy: Greedy or basic logic to reach the food
* Hard: Follows a Hamiltonian cycle to avoid collisions and eventually reach the apple

## Enjoy The Game :)