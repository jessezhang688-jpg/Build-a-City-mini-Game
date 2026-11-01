#  Tile-Based City Builder (Pygame)

A tile-based city builder simulation built from scratch in Python using Pygame. Design your city layout, manage your budget, watch citizens commute along road networks, and balance your economy through dynamic zoning and taxation!

---

##  Key Features

* **Organic World Generation**: Procedurally generated natural lakes and winding rivers on every new game.
* **Drag-to-Paint Brush System**: Smoothly click and drag your mouse across the grid to build roads, zone areas, or bulldoze structures instantly.
* **Dynamic Calendar & Time System**: Tracks in-game Months and Years in real-time, driving growth and seasonal tax collection.
* **Realistic Economy & Taxation**: 
  * Starts you off with a realistic **$500 budget**.
  * Taxes are collected **monthly**, but only from citizens who are successfully employed and commuting to active commercial or industrial zones.
* **Advanced Citizen Commuter System**:
  * **Housing & Population**: Houses start with 2 residents and naturally grow up to a cap of **5 people**.
  * **Road Pathfinding**: Citizens use Breadth-First Search (BFS) pathfinding to walk exclusively along connected road networks (`1`) from their homes to workplaces.
  * **Workplace Capacity**: Commercial and industrial zones support up to **5 workers** each.
  * **Visual Feedback**: White dots represent citizens inside your houses. When a citizen goes to work, their dot temporarily disappears from the house, travels along the roads to work, stays there for a shift, and walks back home!
* **Save & Load System**: Instantly serialize your entire city state (grid, buildings, calendar time, and house populations) into a Base64 code via the terminal to save or share with friends.

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
