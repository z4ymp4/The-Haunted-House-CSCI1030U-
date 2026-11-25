# Kapishnan

import time
import threading
from rooms.base import Room


class Ghost:
    def __init__(self):
        self.stance = "watching"
        self.health = 3
        self.attacks = ["Chill Touch", "Shadow Swipe", "Poltergeist Slam"]

    def next_attack(self):
        attack = self.attacks.pop(0)
        self.attacks.append(attack)
        return attack

    def pick_weakest_player(self, players):
        weakest = players[0]
        for player in players:
            if player.health < weakest.health:
                weakest = player
        return weakest

    def to_dict(self):
        return {
            "stance": self.stance,
            "health": self.health,
            "attacks": self.attacks,
        }

    def from_dict(self, data):
        self.stance = data["stance"]
        self.health = data["health"]
        self.attacks = data["attacks"]


class BedroomRoom(Room):
    def __init__(self, difficulty="normal"):
        super().__init__(name="bedroom")
        self.ghost = Ghost()
        self.difficulty = difficulty
        self.has_mirror = False
        self.ghost_active = False

        if difficulty == "hard":
            self.attempts_left = 2
        elif difficulty == "easy":
            self.attempts_left = 4
        else:
            self.attempts_left = 3

    def search_spot(self, spot):
        if type(spot) == str:
            return spot == "mirror"

        for item in spot.values():
            if self.search_spot(item):
                return True
        return False

    def ghost_attack_loop(self, io, shared_state):
        while self.ghost_active and self.ghost.health > 0:
            time.sleep(8) 

            if self.ghost_active and len(shared_state["players"]) > 0:
                with shared_state["lock"]:
                    target = self.ghost.pick_weakest_player(shared_state["players"])
                    if target.health > 0:
                        attack = self.ghost.next_attack()
                        target.take_damage(1)
                        io.broadcast(f"[GHOST] {attack} hit {target.name} (weakest player)! HP left: {target.health}")

    def play(self, player, io, shared_state):
        io.send(f"\n--- Ghost Bedroom (Difficulty: {self.difficulty}) ---")
        io.broadcast(f"{player.name} entered the Ghost Bedroom!")

        self.ghost_active = True
        thread = threading.Thread(target=self.ghost_attack_loop, args=(io, shared_state))
        thread.start()

        hiding_spots = {
            "wardrobe": {"winter_coat": {"inner_pocket": "mirror"}},
            "desk": {"top_drawer": {"false_bottom": "bedroom_key"}},
        }

        while self.ghost.health > 0 and player.health > 0:
            io.send(f"\nYour HP: {player.health} | Ghost HP: {self.ghost.health}")
            io.send("[1] Search wardrobe  [2] Search desk  [3] Attack Ghost with mirror")
            choice = io.ask("Choose 1, 2, or 3: ")

            if choice == "1":
                if self.search_spot(hiding_spots["wardrobe"]):
                    self.has_mirror = True
                    io.send("You found a Silver Mirror deep inside the wardrobe!")

            elif choice == "2":
                if "bedroom_key" not in player.keys:
                    player.keys.append("bedroom_key")
                    io.send("You found the bedroom_key inside the desk!")
                else:
                    io.send("The desk is empty.")

            elif choice == "3":
                if self.has_mirror:
                    self.ghost.health -= 2
                    io.send("You shine the Silver Mirror! Ghost loses 2 HP!")
                else:
                    io.send("You have no mirror! The Ghost hits you!")
                    with shared_state["lock"]:
                        player.take_damage(1)
            else:
                io.send("Invalid choice. Enter 1, 2, or 3.")

        self.ghost_active = False

        if player.health <= 0:
            io.send("You ran out of health!")
            return False

        io.broadcast(f"{player.name} beat the Ghost and escaped the Bedroom!")
        return True

    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "attempts_left": self.attempts_left,
            "has_mirror": self.has_mirror,
            "ghost": self.ghost.to_dict(),
        }

    def from_dict(self, data):
        self.difficulty = data["difficulty"]
        self.attempts_left = data["attempts_left"]
        self.has_mirror = data["has_mirror"]
        self.ghost.from_dict(data["ghost"])
