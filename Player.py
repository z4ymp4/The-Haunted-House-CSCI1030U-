from typing import List, Optional


class Player:
    def __init__(
        self,
        name: str = "Explorer",
        health: int = 4,
        items: Optional[List[str]] = None,
        keys: Optional[List[str]] = None,
        rooms_completed: Optional[List[str]] = None,
        max_inventory_spots: int = 4,
    ):
        self.name = name
        self.health = max(0, health)
        self.max_health = 4
        self.items = list(items or [])
        self.keys = list(keys or [])
        self.rooms_completed = list(rooms_completed or [])
        self.max_inventory_spots = max(0, max_inventory_spots)

    def take_damage(self, amount: int = 1) -> None:
        self.health = max(0, self.health - max(0, amount))

    def heal(self, amount: int = 1) -> None:
        self.health = min(self.max_health, self.health + max(0, amount))

    def add_item(self, item: str) -> bool:
        if item in self.items:
            return True
        if len(self.items) >= self.max_inventory_spots:
            return False
        self.items.append(item)
        return True

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "items": self.items,
            "keys": self.keys,
            "rooms_completed": self.rooms_completed,
            "max_inventory_spots": self.max_inventory_spots,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        player = cls(
            name=data.get("name", "Explorer"),
            health=data.get("health", 4),
            items=data.get("items", []),
            keys=data.get("keys", []),
            rooms_completed=data.get("rooms_completed", []),
            max_inventory_spots=data.get("max_inventory_spots", 4),
        )
        player.max_health = data.get("max_health", 4)
        return player