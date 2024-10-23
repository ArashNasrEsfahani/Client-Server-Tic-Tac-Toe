# Client-Server-Tic-Tac-Toe


A scalable implementation of Tic-Tac-Toe featuring client-server architecture, customizable grid sizes, and real-time multiplayer gameplay using socket programming.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Tkinter](https://img.shields.io/badge/tkinter-included-blue.svg)
![Socket](https://img.shields.io/badge/socket-programming-blue.svg)

## 📝 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Usage](#-usage)
- [Technical Implementation](#-technical-implementation)
- [Project Structure](#-project-structure)

  
## ✨ Features

- Multiplayer support through client-server architecture
- Customizable grid sizes (3x3, 4x4, 5x5)
- Real-time game state updates
- Interactive GUI using Tkinter
- Automatic turn management
- Win detection for varying board sizes
- Game state persistence and synchronization

## 🔧 Prerequisites

- Python 3.6+
- Tkinter (usually comes with Python)
- Socket library (built-in)
- Pickle library (built-in)


## 💻 Usage

1. Start the server:
```bash
python server.py
```

2. Launch the client(s):
```bash
python client.py
```

3. Select the grid size when prompted (3x3, 4x4, or 5x5)
4. Play the game by clicking on the desired cell when it's your turn

## 🔨 Technical Implementation

### Server Features
- Socket-based communication handling
- Multi-threaded client connections
- Game state management
- Move validation
- Win condition checking
- Board state synchronization

### Client Features
- GUI implementation using Tkinter
- Real-time board updates
- Move transmission
- Game state reception
- User input validation
- Dynamic grid size support

## 📁 Project Structure

```
multiplayer-tictactoe/
├── server.py        # Server implementation
├── client.py        # Client implementation with GUI
├── README.md        # Project documentation
```
