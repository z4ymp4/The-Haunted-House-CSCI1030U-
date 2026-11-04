# Kapishnan 

import random

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)

def play_bedroom(player: dict) -> bool:
    """
    Ghost Bedroom - Extreme Mode.
    No numbered menus! Players must type action verbs based on ghost behavior.
    """
    print_divider()
    print("👻 GHOST BEDROOM (NIGHTMARE MODE) 👻")
    print("You push open the creaking door...")
    print("An angry specter floats before you, blocking the exit!")
    print_divider()

    attempts_left: int = 3
    cleared: bool = False

    while attempts_left > 0 and not cleared:
        current_health = player.get("health", 3)
        print(f"\n[Health: {current_health} HP | Attempts Left: {attempts_left}]")
        
        # Ghost changes state every turn—player must react to this!
        ghost_state = random.choice(["watching", "charging", "wandering"])
        
        if ghost_state == "watching":
            print("👀 The ghost's glowing red eyes are LOCKED onto you!")
        elif ghost_state == "charging":
            print("⚡ The ghost is preparing to surge straight toward you!")
        else:
            print("🌫️ The ghost is aimlessly drifting near the ceiling.")

        print("\nCommands: [ search | sneak | dodge | attack | distract ]")
        action = input("Type your move: ").strip().lower()

        # -------------------------------------------------------------
        # DODGE (Crucial when ghost is charging)
        # -------------------------------------------------------------
        if action == "dodge":
            if ghost_state == "charging":
                print("\n💥 You dive to the floor just as the ghost swoops over you!")
                print("It crashes into the wall, dazing itself!")
                # Small 40% chance to grab the key while dazed
                if random.randint(1, 10) <= 4:
                    print("You snag the Bedroom Key off the floor and bolt out!")
                    cleared = True
                else:
                    print("You dodged the attack, but the ghost quickly recovers!")
            else:
                print("\n❌ You roll across the floor for no reason. The ghost punishes your foolishness!")
                player["health"] = current_health - 1
                attempts_left -= 1

        # -------------------------------------------------------------
        # SNEAK (Only works when ghost is wandering + low success rate)
        # -------------------------------------------------------------
        elif action == "sneak":
            if ghost_state == "watching":
                print("\n❌ The ghost was watching you directly! It blasts you with icy wind!")
                player["health"] = current_health - 1
                attempts_left -= 1
            elif ghost_state == "wandering" and random.randint(1, 10) <= 3: # 30% chance
                print("\n👟 You creep silently along the wall, grab the key, and escape!")
                cleared = True
            else:
                print("\n👟 *CREAK!* A floorboard snaps! The ghost turns and chills you!")
                player["health"] = current_health - 1
                attempts_left -= 1

        # -------------------------------------------------------------
        # SEARCH (Risky gamble to find a light relic)
        # -------------------------------------------------------------
        elif action == "search":
            if ghost_state == "charging":
                print("\n❌ You opened a drawer while being charged! Heavy damage taken!")
                player["health"] = current_health - 2
                attempts_left -= 1
            else:
                search_roll = random.randint(1, 10)
                if search_roll == 10: # Only 10% chance to find relic
                    print("\n✨ You found a blessed Silver Mirror! It reflects the ghost's curse!")
                    cleared = True
                else:
                    print("\n❌ You find nothing but dust. The ghost strikes while you search!")
                    player["health"] = current_health - 1
                    attempts_left -= 1

        # -------------------------------------------------------------
        # DISTRACT (Only useful when watching)
        # -------------------------------------------------------------
        elif action == "distract":
            if ghost_state == "watching" and random.choice([True, False]): # 50% chance
                print("\n🪙 You hurl a piece of trash to the corner. The ghost floats over to inspect!")
                print("You slip past and escape!")
                cleared = True
            else:
                print("\n❌ The ghost ignores your distraction completely!")
                player["health"] = current_health - 1
                attempts_left -= 1

        # -------------------------------------------------------------
        # ATTACK (Almost guaranteed failure)
        # -------------------------------------------------------------
        elif action == "attack":
            if random.randint(1, 20) == 20: # 5% critical miracle
                print("\n🥊 CRITICAL HIT! You somehow punch a ghost into another dimension!")
                cleared = True
            else:
                print("\n🥊 Your fist passes right through it! The ghost freezes your soul!")
                player["health"] = current_health - 2
                attempts_left -= 1

        # -------------------------------------------------------------
        # INVALID COMMAND
        # -------------------------------------------------------------
        else:
            print("\n⚠️ Hesitation is fatal! Type a valid command: search, sneak, dodge, attack, or distract.")
            attempts_left -= 1

    # Outcome handling
    print_divider()
    if cleared:
        print("🎉 SUCCESS: You escaped the Ghost Bedroom!")
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
