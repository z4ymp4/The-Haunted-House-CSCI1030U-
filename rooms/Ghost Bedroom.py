# Kapishnan 
# Member 4: Ghost Bedroom
# Demonstrates: Functions, Control Flow (if/elif/while), Collections (dict/list), Type Hints

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)


def play_bedroom(player: dict) -> bool:
    """
    Executes the Ghost Bedroom room interaction.
    """
    print_divider()
    print("👻 GHOST BEDROOM 👻")
    print("You push open the creaking door...")
    print("A cold mist fills the air, and a glowing specter blocks the exit!")
    print_divider()

    # Room choices dictionary
    choices: dict[str, str] = {
        "1": "Use the Flashlight",
        "2": "Distract the ghost with a coin",
        "3": "Sneak past the ghost",
        "4": "Fight the ghost"
    }

    attempts_left: int = 3
    cleared: bool = False

    while attempts_left > 0 and not cleared:
        print(f"\nHealth: {player.get('health', 3)} HP | Attempts left: {attempts_left}")
        print("What will you do?")
        
        # Display menu options cleanly
        for key, text in choices.items():
            print(f"  [{key}] {text}")

        user_choice: str = input("\nYour action (1-4): ").strip()

        # Option 1: Inventory check
        if user_choice == "1":
            if "Flashlight" in player.get("items", []):
                print("\n💥 FLASH! The bright light dazzles the ghost! It vanishes!")
                cleared = True
            else:
                print("\n❌ You don't have a Flashlight in your items!")
                print("The ghost attacks while you fumble in your pockets!")
                attempts_left -= 1

        # Option 2: Clever escape
        elif user_choice == "2":
            print("\n🪙 *CLINK!* You toss a coin to the far side of the room.")
            print("The ghost floats over to inspect it, letting you slip past!")
            cleared = True

        # Option 3: Sneak (fails)
        elif user_choice == "3":
            print("\n👟 *CREAK!* You step on a bad floorboard!")
            print("The ghost turns around and blasts you with icy wind!")
            player["health"] = player.get("health", 3) - 1
            attempts_left -= 1

        # Option 4: Direct fight (fails)
        elif user_choice == "4":
            print("\n🥊 You swing your fist, but it goes right through the ghost!")
            print("The ghost chills you to the bone!")
            player["health"] = player.get("health", 3) - 1
            attempts_left -= 1

        else:
            print("\n⚠️ Invalid choice! Enter 1, 2, 3, or 4.")

    # Room summary & reward handling
    print_divider()
    if cleared:
        print("🎉 SUCCESS: You grabbed the Bedroom Key and escaped!")
        
        # Safely update shared inventory lists
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
