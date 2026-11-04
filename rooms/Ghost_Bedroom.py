# Kapishnan 

import random

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)

def play_bedroom(player: dict) -> bool:
    """
    Executes the Ghost Bedroom room interaction.
    Self-contained: relies only on room choices, strategy, and luck!
    """
    print_divider()
    print("👻 GHOST BEDROOM 👻")
    print("You push open the creaking door...")
    print("A terrifying specter floats in the middle of the dark room!")
    print_divider()

    attempts_left: int = 3
    cleared: bool = False

    while attempts_left > 0 and not cleared:

        current_health = player.get("health", 3)
        print(f"\nHealth: {current_health} HP | Attempts left: {attempts_left}")
        
        ghost_stance = random.choice(["alert", "distracted"])
        if ghost_stance == "alert":
            print("👀 The ghost is watching the room intensely!")
        else:
            print("🌫️ The ghost seems unfocused, staring into the dark corner.")

        print("\nWhat will you do?")
        print("  [1] Search the nightstand for a relic")
        print("  [2] Throw a heavy book across the room")
        print("  [3] Sneak past the ghost")
        print("  [4] Charge through the ghost")

        user_choice: str = input("\nYour action (1-4): ").strip()

        if user_choice == "1":
            luck = random.randint(1, 10)
            if luck > 4:
                print("\n✨ You found a Holy Candle on the nightstand and light it!")
                print("The ghost shrieks in agony and dissolves into thin air!")
                cleared = True
            else:
                print("\n❌ You search the drawer, but it's empty! The ghost spots you!")
                player["health"] = current_health - 1
                attempts_left -= 1

        elif user_choice == "2":
            if ghost_stance == "distracted":
                print("\n🪙 *THUD!* You throw a book. The distracted ghost floats away!")
                print("You grab the key from the bed post and slip past!")
                cleared = True
            else:
                print("\n❌ The ghost was too alert! It ignores the noise and blasts you with cold air!")
                player["health"] = current_health - 1
                attempts_left -= 1

        elif user_choice == "3":
            if random.choice([True, False]):
                print("\n👟 You tread lightly on the carpet and slip right past the ghost!")
                cleared = True
            else:
                print("\n👟 *CREAK!* A floorboard betrays you! The ghost chills you to the bone!")
                player["health"] = current_health - 1
                attempts_left -= 1

        elif user_choice == "4":
            if random.randint(1, 10) == 10:  # 10% chance to succeed
                print("\n🥊 Miraculously, your force knocks the spirit off balance! You burst through!")
                cleared = True
            else:
                print("\n🥊 You pass straight through the ice-cold phantom! Massive damage taken!")
                player["health"] = current_health - 2
                attempts_left -= 1

        else:
            print("\n⚠️ Invalid choice! Enter 1, 2, 3, or 4.")

    print_divider()
    if cleared:
        print("🎉 SUCCESS: You grabbed the Bedroom Key and escaped!")
        
        if "keys" in player:
            player["keys"].append("bedroom_key")
        if "rooms_completed" in player:
            player["rooms_completed"].append("Ghost Bedroom")
            
        print_divider()
        return True
    else:
        print("💀 FAILED: You were driven out of the bedroom!")
        print_divider()
        return False
