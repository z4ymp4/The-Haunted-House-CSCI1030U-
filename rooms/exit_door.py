"""Room 5: The Exit Door (Member 5)."""
from rooms.base import Room

ALL_KEYS = ["hallway_key", "library_key", "kitchen_key", "bedroom_key"]


class ExitRoom(Room):
    room_id = "exit_door"
    title = "The Exit Room"

    def __init__(self, settings):
        super().__init__(settings)
        self.required_keys = settings["required_keys"]
        self.attempts_left = settings["attempts"]

    def play(self, ctx, player):
        ctx.say("You reach the heavy iron front door of the haunted house.")
        while self.attempts_left > 0:
            ctx.say("\n1. Inspect the door\n2. Try the door\n3. Look around for clues")
            choice = ctx.ask("Enter option (1-3): ").strip()
            if choice == "1":
                ctx.say(f"The door has {self.required_keys} heavy keyholes. It looks solid.")
            elif choice == "2":
                have = len(set(player.keys))
                ctx.say(f"You have {have} of {self.required_keys} keys needed.")
                if have >= self.required_keys:
                    ctx.say(f"Click! The door swings open! You escaped, {player.name}!")
                    return self.finish(player)
                self.attempts_left -= 1
                ctx.say(f"The lock won't budge! Attempts left: {self.attempts_left}")
            elif choice == "3":
                missing = [k for k in ALL_KEYS if k not in player.keys]
                if missing:
                    ctx.say("Faint engravings suggest keys you lack: " + ", ".join(missing))
                else:
                    ctx.say("You have every key. Try the door!")
            else:
                ctx.say("Invalid option. Please enter 1, 2, or 3.")
        ctx.say("\nA dark shadow envelops you before you can work out the lock...")
        return False

    def to_dict(self):
        return {"attempts_left": self.attempts_left}

    def from_dict(self, data):
        self.attempts_left = data.get("attempts_left", self.attempts_left)