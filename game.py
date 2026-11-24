"""Game class: runs the rooms, saves and loads (Member 6)."""
import json
import os

from player import Player
from scoreboard import ScoreBoard
from rooms.dark_hallway import DarkHallway, HOUSE_MAP, count_reachable
from rooms.library import LibraryRoom
from rooms.kitchen import KitchenRoom
from rooms.bedroom import BedroomRoom
from rooms.exit_door import ExitRoom

ROOM_CLASSES = [DarkHallway, LibraryRoom, KitchenRoom, BedroomRoom, ExitRoom]
ROOM_IDS = [cls.room_id for cls in ROOM_CLASSES]

DIFFICULTY = {
    "easy":   {"health": 5, "attempts": 4, "ghost_damage": 1},
    "normal": {"health": 4, "attempts": 3, "ghost_damage": 1},
    "hard":   {"health": 3, "attempts": 2, "ghost_damage": 2},
}

# Expected shape of a save file; used by validate().
SAVE_TEMPLATE = {
    "difficulty": str,
    "current_room": int,
    "player": {"name": str, "health": int, "items": list,
               "keys": list, "rooms_completed": list},
    "rooms": dict,
}


def build_settings(difficulty, riddles_file, inventory_size):
    settings = dict(DIFFICULTY[difficulty])
    settings.update(difficulty=difficulty, riddles_file=riddles_file,
                    inventory_size=inventory_size, required_keys=3)
    return settings


def validate(data, template, where="save"):
    """Recursively check that nested save data matches the template."""
    if isinstance(template, dict):
        if not isinstance(data, dict):
            raise ValueError(f"{where} should be an object")
        for key, sub in template.items():
            if key not in data:
                raise ValueError(f"{where} is missing '{key}'")
            validate(data[key], sub, f"{where}.{key}")
    elif not isinstance(data, template):
        raise ValueError(f"{where} should be {template.__name__}")


class Game:
    def __init__(self, settings, player, scoreboard, save_path):
        self.settings = settings
        self.player = player
        self.scoreboard = scoreboard
        self.save_path = save_path
        self.rooms = [cls(settings) for cls in ROOM_CLASSES]
        self.current = 0

    def skip_to(self, room_id):
        """Practice mode: start at a later room with earlier rewards granted."""
        index = ROOM_IDS.index(room_id)
        for room in self.rooms[:index]:
            room.give_rewards(self.player)
            self.player.rooms_completed.append(room.room_id)
        self.current = index

    def to_dict(self):
        return {
            "difficulty": self.settings["difficulty"],
            "current_room": self.current,
            "player": self.player.to_dict(),
            "rooms": {room.room_id: room.to_dict() for room in self.rooms},
        }

    def save(self):
        folder = os.path.dirname(self.save_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.save_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"Game saved to {self.save_path}.")

    @classmethod
    def load(cls, save_path, scoreboard, riddles_file, inventory_size):
        with open(save_path) as f:
            data = json.load(f)
        validate(data, SAVE_TEMPLATE)
        if not 0 <= data["current_room"] < len(ROOM_CLASSES):
            raise ValueError("save has an invalid current_room")
        settings = build_settings(data["difficulty"], riddles_file, inventory_size)
        game = cls(settings, Player.from_dict(data["player"]), scoreboard, save_path)
        game.current = data["current_room"]
        for room in game.rooms:
            room.from_dict(data["rooms"].get(room.room_id, {}))
        return game

    def run(self):
        """Play from the current room. Returns 'won', 'lost' or 'saved'."""
        while self.current < len(self.rooms):
            room = self.rooms[self.current]
            ahead = count_reachable(HOUSE_MAP, room.room_id) - 1
            print(f"\n>>> {room.title}  ({ahead} more room(s) after this one)")
            print(f"Health: {self.player.health} | Keys: {len(self.player.keys)}")
            choice = input("[Enter] go in, [s] save and quit: ").lower().strip()
            if choice == "s":
                self.save()
                return "saved"
            if not room.play(self.player):
                print("\nGAME OVER!")
                return "lost"
            self.current += 1
        score = (ScoreBoard.tally(self.player.rooms_completed)
                 + self.player.health * 5)
        print(f"\nCONGRATULATIONS {self.player.name}! You escaped! Score: {score}")
        self.scoreboard.add(self.player.name, score, self.settings["difficulty"])
        return "won"
