
from Player import Player


class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_dict(self) -> dict:
        return {"name": self.name, "description": self.description}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data.get("name", "kitchen_key"), data.get("description", "A small brass key."))


class KitchenRoom:
    def __init__(self, max_inventory_spots: int = 4):
        self.name = "Locked Kitchen"
        self.is_cleared = False
        self.max_inventory_spots = max_inventory_spots
        self.found_key = False
        self.key_item = Item("kitchen_key", "A small brass key.")
        
        # Track searched locations for save/load state
        self.searched_locations = []
        
        # 3-Level Deep Nested Data for Recursion (table -> wooden_box -> velvet_pouch -> key)
        self.nested_box = {
            "name": "wooden_box",
            "searched": False,
            "contents": {
                "name": "velvet_pouch",
                "searched": False,
                "has_key": True
            }
        }

    
    # RECURSION 
    def search_nested_container(self, container: dict, target_name: str, depth: int = 0) -> bool:

        indent = "  " * depth

        if container["name"] == target_name:
            container["searched"] = True
            print(f"{indent}--> You opened the {container['name']}!")

            if container.get("has_key"):
                print(f"{indent}>> Found the Kitchen Key!")
                self.found_key = True
                return True

            if "contents" in container:
                nested = container["contents"]
                print(f"{indent}Inside the {container['name']}, you spot a {nested['name']}.")

            return True

        
        if "contents" in container and not container["contents"]["searched"]:
            return self.search_nested_container(container["contents"], target_name, depth + 1)

        return False

    
    # GAME LOOP (INTERFACE)
    
    def play(self, player: Player) -> bool:
        if self.is_cleared:
            return True

        self.max_inventory_spots = player.max_inventory_spots
        print("\nWelcome to room 3")
        print("You entered kitchen. Find the key to unlock the exit door")

        locations = ["table", "fridge", "closet", "drawer"]

        while not self.found_key and player.health > 0:
            print(f"\nHealth: {player.health} | Keys: {player.keys}")
            print(f"Please select location: {locations}")
            
            choice = input("Where would you like to search? ").strip().lower()

            if choice not in locations and choice not in ["wooden_box", "velvet_pouch"]:
                print("Choose from the options.")
                continue

            if choice in self.searched_locations:
                print("You have been there, time is running!")
                continue

            self.searched_locations.append(choice)

            # Location Logic matching your original room 3
            if choice == "table":
                print("A rat bit you! (-1 Health)")
                player.take_damage(1)
                print("Under the table, you spot a hidden 'wooden_box'!")

            elif choice == "fridge":
                print("Found fresh water! (+1 Health)")
                player.heal(1)

            elif choice == "closet":
                print("Spiders living in webs.")

            elif choice == "drawer":
                print("Just empty silver spoons.")

            # Trigger Recursive Search for hidden container items
            elif choice in ["wooden_box", "velvet_pouch"]:
                self.search_nested_container(self.nested_box, choice)

            # Check for Key Discovery
            if self.found_key:
                if "kitchen_key" not in player.keys:
                    player.keys.append(self.key_item.name)
                if "kitchen" not in player.rooms_completed:
                    player.rooms_completed.append("kitchen")
                self.is_cleared = True
                print("Go to room 4")
                return True

        if player.health <= 0:
            print("\nYou lost in the kitchen.")
            return False

        return self.is_cleared

    
    # FILE I/O SERIALIZATION
    
    def to_dict(self) -> dict:
        """Saves kitchen state for JSON file persistence."""
        return {
            "name": self.name,
            "is_cleared": self.is_cleared,
            "found_key": self.found_key,
            "key_item": self.key_item.to_dict(),
            "max_inventory_spots": self.max_inventory_spots,
            "searched_locations": self.searched_locations,
            "nested_box": self.nested_box
        }

    def from_dict(self, data: dict) -> None:
        """Restores kitchen state from JSON save files."""
        self.is_cleared = data.get("is_cleared", False)
        self.found_key = data.get("found_key", False)
        if isinstance(data.get("key_item"), dict):
            self.key_item = Item.from_dict(data["key_item"])
        self.max_inventory_spots = data.get("max_inventory_spots", 4)
        self.searched_locations = data.get("searched_locations", [])
        if "nested_box" in data:
            self.nested_box = data["nested_box"]