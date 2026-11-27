# The Haunted House

Welcome to **Escape the Haunted House** — a multiplayer networked text adventure built in Python.

You wake up inside a haunted house. Complete the rooms, collect keys, survive ghost encounters, and race other players to the exit! There are 5 rooms:
1. **Room 1: The Dark Hallway** (Stack navigation & backtracking maze)
2. **Room 2: The Riddle Library** (Riddle queue, edit-distance fuzzy matching & timer thread)
3. **Room 3: The Locked Kitchen** (Iterative stack search, 0/1 knapsack loot & item locks)
4. **Room 4: The Ghost Bedroom** (Attack queue, greedy weakest-player targeting & ghost-tick thread)
5. **Room 5: The Exit Room** (BST leaderboard, merge-sort rankings & locked score updates)

---

## How to Run

### 1. Multiplayer Network Mode (Milestone 3)
Start the server in one terminal:
```bash
python server.py --host 127.0.0.1 --port 5555
