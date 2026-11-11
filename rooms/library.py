import json
import os

# Recursive hint function (satisfies the recursion requirement)
def get_recursive_hint(hints, index=0):
    if index >= len(hints):
        print("-> No more hints available!")
        return
    print(f"-> HINT {index + 1}: {hints[index]}")
    choice = input("Would you like an even deeper hint? (y/n): ").strip().lower()
    if choice == 'y':
        get_recursive_hint(hints, index + 1)

class LibraryRoom:
    def __init__(self, riddles_path="data/riddles.json"):
        self.riddles_path = riddles_path
        self.riddle = self.load_riddles()

    def load_riddles(self):
        # File I/O requirement (loading from JSON)
        if os.path.exists(self.riddles_path):
            with open(self.riddles_path, "r") as f:
                return json.load(f)
        return {
            "question": "What has keys but cannot open locks?",
            "answer": "piano",
            "reward": "library_key",
            "hints": ["It makes music.", "It has black and white keys."]
        }

    def play(self, player):
        print("\n--- ROOM 2: THE RIDDLE LIBRARY ---")
        print("Dusty bookshelves line the walls. A glowing ledger rests on a pedestal.")

        attempts = 3
        while attempts > 0:
            print(f"\nRiddle: {self.riddle['question']}")
            user_input = input("Your answer (or type 'hint'): ").strip().lower()

            if user_input == "hint":
                get_recursive_hint(self.riddle["hints"])
                continue

            if user_input == self.riddle["answer"]:
                print("Correct! The ledger glows green, and a key drops out.")
                player.keys.append(self.riddle["reward"])
                player.rooms_completed.append("library")
                return True
            else:
                attempts -= 1
                print(f"Wrong answer! Attempts left: {attempts}")

        print("You failed the riddle and continue without the key.")
        player.rooms_completed.append("library_failed")
        return False

    def to_dict(self):
        return {"riddles_path": self.riddles_path}

    @classmethod
    def from_dict(cls, data):
        return cls(riddles_path=data.get("riddles_path", "data/riddles.json"))

if __name__ == "__main__":
    # Simple mock player class for testing
    class MockPlayer:
        def __init__(self):
            self.keys = []
            self.rooms_completed = []
    player = MockPlayer()
    library = LibraryRoom()
    library.play(player)
    print("Test finished! Player keys:", player.keys)
