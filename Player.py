class Player:
    def __init__(self, name: str = "Explorer", health: int = 100):
        self.name = name
        self.health = health
        self.max_health = 100
        self.items = []       # e.g., ["flashlight"]
        self.keys = []        # e.g., ["library_key", "kitchen_key", "bedroom_key"]
        self.rooms_completed = []

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "health": self.health,
            "items": self.items,
            "keys": self.keys,
            "rooms_completed": self.rooms_completed
        }

    @classmethod
    def from_dict(cls, data: dict):
        player = cls(name=data.get("name", "Explorer"), health=data.get("health", 100))
        player.items = data.get("items", [])
        player.keys = data.get("keys", [])
        player.rooms_completed = data.get("rooms_completed", [])
        return player
