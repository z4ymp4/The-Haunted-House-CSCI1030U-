# Kapishnan 

import random

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)

def play_bedroom(player: dict) -> bool:
    """
    Executes the Ghost Bedroom room interaction.
    Challenging mode: lower win probabilities and higher risk!
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
        
        # Ghost stance dictates the safest strategy for that turn
        ghost_stance = random.choice(["alert", "distracted", "enraged"])
        if ghost_stance == "alert":
            print("👀 The ghost is watching the room intensely!")
        elif ghost_stance == "distracted":
            print("🌫️ The ghost seems unfocused, staring into the dark corner.")
        else:
            print("🔥 The ghost is glowing red with rage!")

        print("\nWhat will you do?")
        print("  [1] Search the nightstand for a relic (Risky search)")
        print("  [2] Throw a heavy book across the room (Distraction)")
        print("  [3] Sneak past the ghost (Stealth check)")
        print("  [4] Charge through the ghost (Desperation move)")

        user_choice: str = input("\nYour action (1-4): ").strip()

        # Option 1: Low-chance search (20% chance to win)
        if user_choice == "1":
            luck = random.randint(1, 10)
            if luck >= 9:  # Only 9 or 10 succeeds
                print("\n✨ You found a Holy Candle on the nightstand and light it!")
                print("The ghost shrieks in agony and dissolves into thin air!")
                cleared = True
            else:
                print("\n❌ You frantically search the drawer, but find only dust!")
                print("The ghost turns around and blasts you with icy wind!")
                player["health"] = current_health - 1
                attempts_left -= 1

        # Option 2: Distraction (Only works if ghost is distracted + 50% luck)
        elif user_choice == "2":
            if ghost_stance == "distracted" and random.choice([True, False]):
                print("\n🪙 *THUD!* You throw a book. The distracted ghost floats over!")
                print("You grab the key from the bed post and slip past!")
                cleared = True
            else:
                print("\n❌ The ghost ignores the sound and strikes you!")
                player["health"] = current_health - 1
                attempts_left -= 1

        # Option 3: Sneak (30% chance to succeed)
        elif user_choice == "3":
            sneak_roll = random.randint(1, 10)
            if sneak_roll <= 3:  # 30% success rate
                print("\n👟 You tread silently on the carpet and slip right past!")
                cleared = True
            else:
                print("\n👟 *CREAK!* A loud floorboard betrays you!")
                print("The ghost chills you to the bone!")
                player["health"] = current_health - 1
                attempts_left -= 1

        # Option 4: Direct Charge (10% chance to succeed)
        elif user_choice == "4":
            if random.randint(1, 10) == 10:  # 10% chance
                print("\n🥊 Miraculously, your force knocks the spirit off balance! You burst through!")
                cleared = True
            else:
                print("\n🥊 You pass straight through the ice-cold phantom! Heavy damage taken!")
                player["health"] = current_health - 2
                attempts_left -= 1

        else:
            print("\n⚠️ Invalid choice! Enter 1, 2, 3, or 4.")

    # Outcome handling
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
