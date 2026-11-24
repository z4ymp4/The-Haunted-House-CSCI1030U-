from rooms.base import Room

class ExitRoom(Room):
    def __init__(self, required_keys: int = 3):
        super().__init__("Exit Room", "The grand front doors of the mansion sit before you, heavy and locked.")
        self.required_keys = required_keys
        self.attempts_left = 3
        self.door_status = "locked"

    def play(self, player) -> bool:
        print(f"\n--- ROOM 5: THE EXIT DOOR ---")
        print(self.description)
        
        choices = [
            "1. Inspect the door", 
            "2. Try the door", 
            "3. Look around for clues"
        ]

        while self.attempts_left > 0:
            print(f"\nYou have {len(player.keys)} key(s). Attempts left: {self.attempts_left}")
            print("\nWhat would you like to do?")
            for choice in choices:
                print(choice)
                
            action = input("> ").strip()

            if action == "1" or "inspect" in action.lower():
                print("\nYou examine the door closely. It features a massive iron lock with three keyholes.")
            elif action == "2" or "try" in action.lower():
                if len(player.keys) >= self.required_keys:
                    print("\n🔑 You insert your keys into the three locks... Click, click, click! The front door swings open!")
                    self.completed = True
                    return True
                else:
                    print(f"\n The lock clicks stubbornly. You need {self.required_keys} keys, but you only have {len(player.keys)}!")
                    self.attempts_left -= 1
            elif action == "3" or "clues" in action.lower():
                print("\nYou search the dark hallway surrounding the door. Scrawled on the wall in fading paint: 'Only those who gather all keys may leave.'")
            else:
                print("\nInvalid choice. Try again.")

        print("\nThe mansion walls close in on you... You ran out of attempts and failed to escape.")
        return False

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "attempts_left": self.attempts_left,
            "door_status": self.door_status
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        room = cls()
        room.completed = data.get("completed", False)
        room.attempts_left = data.get("attempts_left", 3)
        room.door_status = data.get("door_status", "locked")
        return room
