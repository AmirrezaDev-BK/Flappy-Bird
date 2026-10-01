# 🐦 Flappy Bird — Python Edition

A modern remake of the classic **Flappy Bird** game, built with **Python** and **Pygame**.  
Features difficulty levels, a built-in music player, pause system, and full mouse/touch support.

> 🎮 Tap to fly. Don't crash.

---

## ✨ Features

- 🎮 **Classic gameplay** — tap / click / press `Space` to flap
- 🎯 **3 difficulty levels** — Easy, Medium, Hard
- 🎵 **Built-in music player** — add your own songs from anywhere
- ⏸ **Pause system** — pause the game and switch tracks
- 🖱 **Full mouse & touch support** — every button is clickable
- 🪟 **Resizable window** — plus `F` for fullscreen toggle
- 🎨 **Modern UI** — gradient sky, rounded buttons, smooth animations
- 📊 **Clickable progress bar** — seek to any position in the current track
- 🏆 **In-memory high score** — tracked per session

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/AmirrezaDev-BK/Flappy-Bird.git
cd Flappy-Bird
```

### 2. Install dependencies

```bash
pip install pygame-ce
```

> ⚠️ Make sure you have **Python 3.10+** installed.

### 3. Run the game

```bash
python main.py
```

---

## 🎯 Controls

### 🏠 Main Menu

| Key | Action |
|-----|--------|
| `Space` | Start Game |
| `H` | How to Play |
| `M` | Music |
| `D` | Change Difficulty |
| `Esc` | Quit |

### 🎮 In-Game

| Key | Action |
|-----|--------|
| `Space` / Click | Flap |
| `P` | Pause |
| `F` | Toggle Fullscreen |
| `S` | Stop Music |
| `←` / `→` | Previous / Next Track |

### 🎵 Music Screen

| Key | Action |
|-----|--------|
| `Space` | Play / Stop |
| `S` | Stop |
| `←` / `→` | Previous / Next Track |
| `L` | Toggle Loop |
| `A` | Add Music |
| `Esc` | Back |

---

## 📁 Project Structure

```
Flappy-Bird/
│
├── main.py          # Entry point
├── config.py        # Global settings & constants
├── game.py          # Core game logic & state machine
├── ui.py            # UI screens, buttons, progress bar
├── bird.py          # Bird class
├── pipe.py          # Pipe class & manager
├── music.py         # Music player (singleton)
│
├── assets/
│   └── bird.png     # Bird sprite
│
├── bird.ico         # App icon
└── README.md
```

---

## 🛠 Built With

- 🐍 **Python 3.14**
- 🎮 **Pygame-CE 2.5.8**
- 🖼 **Tkinter** (for the file dialog)

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**AMIRREZA** — *AmirrezaDev-BK*

- 🐙 GitHub: [@AmirrezaDev-BK](https://github.com/AmirrezaDev-BK)
- 📸 Instagram: [@amirreza.bk.py](https://instagram.com/amirreza.bk.py)

> 💻 Programmer · 🌐 Web Designer · ♟️ Chess Enthusiast · 🐍 Python & Tkinter  
> 🌱 Open source · Always learning

---

<p align="center">
  Made with ❤️ in Iran 🇮🇷
</p>
