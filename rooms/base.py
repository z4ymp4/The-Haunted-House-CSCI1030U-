from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.completed = False

    @abstractmethod
    def play(self, player) -> bool:
        """Executes room logic. Returns True if room passed/cleared, False if failed/game over."""
        pass

    def to_dict(self) -> dict:
        """Serializes room state to a dict for JSON saving."""
        return {
            "name": self.name,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Reconstructs room instance from dict."""
        room = cls()
        room.completed = data.get("completed", False)
        return room
