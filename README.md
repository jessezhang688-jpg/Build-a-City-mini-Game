#  Tile-Based City Builder (Pygame)

A tile-based city builder simulation built from scratch in Python using Pygame.

---

##  Key Features

* **World Generation**: Generates the world randomly, and you can save the save code to save your progress in the terminal
* **Drag-to-Paint Brush**: drag your mouse over the tiles to build stuff
* **Calendar & Time**: Tracks time passed in the game (not that relistic tho)
* **Taxation**: 
  * Starts you off with a **$500 budget**.
  * Taxes are collected **monthly**, but only from citizens who are commuting to active commercial or industrial zones.
* **Citizen Commuter**:
  * **Housing & Population**: Houses start with 2 residents can grow up to a cap of **5 people**.
  * **Road Pathfinding**: Citizens use Breadth-First Search (BFS) pathfinding to walk along connected road tiles from their homes to workplaces.
  * **Workplace Capacity**: Each commercial and industrial tile support up to **5 workers** each.
  * **Visual**: White dots represent citizens inside your houses. When a citizen goes to work, their dot will walk from their house to their workplace!
* **Save code gen**: Instantly generates your whole game progress into a Base64 code via the terminal to save or share with friends.

---

##  Controls & Shortcuts

| Key / Action | Description |
| :--- | :--- |
| **Mouse Click + Drag** | Paint/Build selected tool continuously across the grid |
| **`1`** | Select **Road Tool** ($10) |
| **`2`** | Select **House Tool** ($50, max 5 residents) |
| **`3`** | Select **Commercial Zone** ($75) |
| **`4`** | Select **Industrial Zone** ($100, max 5 workers) |
| **`5`** | Select **Bulldozer** (Free, refunds $5) |
| **`R`** | Generate a **New World** |
| **`S`** | **Save Game** (Outputs base64 save code to your terminal) |
| **`L`** | **Load Game** (Opens text prompt to paste a save code) |

---

##  Getting Started

### Prerequisites
Make sure you have Python and Pygame installed on your system:
```bash
pip install pygame
```

<img width="1293" height="281" alt="image" src="https://github.com/user-attachments/assets/90a03208-1993-4852-a5a5-3a7cc1c62faf" />

<img width="1917" height="1140" alt="image" src="https://github.com/user-attachments/assets/e5420f66-c99e-47c1-84f9-df5737fc4886" />


