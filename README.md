# CHESS  
*Data Structures and Algorithms Final Project*

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Data Structures](#data-structures)
- [Algorithms](#algorithms)
- [Results](#results)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## Overview
This is a feature-rich chess application developed as part of our **Data Structures and Algorithms (DSA) final project**. The game not only incorporates standard chess rules but is entirely implemented using core DSA principles, making it computationally optimized and ideal for both learning and gaming experiences.

## Features
- **AI Integration**: Play against a challenging AI opponent.
- **Multiple Game Modes**: Choose from rapid, classic, and professional modes.
- **Undo Functionality**: Undo your moves (not available in professional mode).
- **Captured Piece Display**: Visual tracking of captured pieces during the game.
- **Dynamic Chessboard Rendering**: Built using **Pygame** for interactive and engaging visuals.
- **Advanced Rules**: En passant, castling, and pawn promotion are supported.
- **BFS-based Move Generation**: Ensures accurate and optimized move calculations.

---

## Technologies Used
- **Programming Language**: Python
- **Graphics**: Pygame library
- **Algorithms**: Breadth-First Search (BFS) for move generation, heuristic evaluation for AI.
- **Data Structures**: Dictionary, Stack, and custom node-based logic.

---

## Installation
Follow these steps to set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/chess-dsa.git
2. Navigate to the project directory:  
   ```bash
   cd chess-dsa
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the application:
   ```bash
   python main.py

## How to Play
1. Launch the game using the main.py script.
2. Choose your desired game mode from the menu using up and down keys.
3. Use the mouse to select and move pieces on the board.
4. The game will highlight valid moves for the selected piece. (Except proffessional Mode)
5. Enjoy playing against the AI or with another player!

# Data Structures/Algorithms  

| **Data Structure/Algorithm** | **Use**                                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------|
| **Graph Representation**     | Efficiently represents the chessboard and tracks piece positions.                      |
| **Stack**                    | Tracks moves for undo functionality.                                                   |
| **BFS/DFS**                  | Calculates valid moves, checks for game states like checks and mates.                  |
| **Dictionary**               | Tracks piece positions, identifies empty/occupied squares.                             |
| **Minimax Algorithm**        | Powers the AI, enabling optimal move calculation.                                      |
| **Alpha-Beta Pruning**       | Optimizes the Minimax algorithm by pruning branches to improve efficiency.             |
| **Tuple**                    | Used to capture and store the state of a move with multiple elements that should not change. |
| **List**                     | Tracks and manages collections of elements like valid moves, captured pieces, or move history. |
| **Tree**                     | Utilized in the Minimax algorithm to represent possible game states and moves.          |
| **Queue**                    | Used in BFS to keep track of the nodes.                                                |

---

# Algorithms  

### **Breadth-First Search (BFS)**  
- Used for move generation of sliding pieces (Rook, Bishop, Queen).  
- Ensures valid traversal of the chessboard within boundaries and without obstacles.  

### **Heuristic Evaluation**  
- AI uses board evaluation functions to determine the best possible move.  
- Factors include piece value, positional advantage, and board control.  

### **Game State Validation**  
- Ensures moves do not place the player's king in check.  
- Validates checkmate, stalemate, and other game-ending conditions.  

### **Special Rules Implementation**  
- Implements castling, en passant, and pawn promotion logic.  
- Move history is utilized for rules like en passant.  

---

# Results  

- **AI Efficiency**: The AI makes intelligent decisions based on heuristic evaluation.  
- **Optimized Move Calculation**: BFS ensures moves are calculated accurately and quickly.  
- **User Experience**: The Pygame interface provides an engaging and interactive gaming experience.  

---

# Future Enhancements  

- Add online multiplayer functionality.  
- Improve AI difficulty levels with more advanced heuristics.  
- Include a tutorial mode for beginners.  
- Add timer-based gameplay for competitive modes.  

---

# Contributors  

- **Khadija Saeed     (2023-CS-74)** 
- **Hira Sohail     (2023-CS-76)**   
- **Ufaq Hafeez     (2023-CS-75)**
- **Ayesha Wasim     (2023-CS-66)** 
 
