# Kapishnan 

import random

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)

def play_bedroom(player: dict) -> bool:
    """
    Ghost Bedroom - Tactical Mode.
    Complex multi-step interactions with a balanced 3-attempt limit.
    """
    print_divider()
    print("👻 GHOST BEDROOM 👻")
    print("You step into the freezing room. A specter blocks the exit!")
    print_divider()

    attempts_left: int = 3
    cleared: bool = False
    
    # Track sub-game state items found inside the room
    has_mirror: bool = False

    while attempts_left > 0 and not cleared:
        current_health = player.get("health", 3)
        print(f"\n[ Health: {current_health} HP | Ghost Strikes Left: {attempts_left} ]")
        
        # Ghost changes stance each round
        ghost_state = random.choice(["watching", "charging", "wandering"])
        
        if ghost_state == "watching":
            print("👀 Ghost Stance: Floating in place, watching your every movement!")
        elif ghost_state == "charging":
            print("⚡ Ghost Stance: Gathering dark mist, getting ready to SURGE forward!")
        else:
            print("🌫️ Ghost Stance: Mindlessly drifting near the ceiling with its back turned.")

        print("\nPrimary Actions: [ search | distract | dodge | sneak | attack ]")
        action = input("Choose primary action: ").strip().lower()

        # -------------------------------------------------------------
        # 1. SEARCH (Has secondary locations to pick from)
        # -------------------------------------------------------------
        if action == "search":
            if ghost_state == "charging":
                print("\n❌ You searched while it was charging! You get slammed into the door!")
                player["health"] = max(0, current_health - 1)
                attempts_left -= 1
            else:
                print("\nWhere do you want to search?")
                target = input("Pick target [ drawer | bed | carpet ]: ").strip().lower()
                
                if target == "drawer":
                    if not has_mirror:
                        print("\n✨ You found a polished Silver Mirror inside the drawer!")
                        has_mirror = True
                    else:
                        print("\nDrawer is empty now.")
                elif target == "carpet":
                    print("\n🗝️ You peeked under the carpet and spotted the Bedroom Key!")
                    print("You snatch it before the ghost realizes!")
                    cleared = True
                elif target == "bed":
                    print("\n❌ Dust shoots out of the pillow! You cough loudly and alert the ghost!")
                    attempts_left -= 1
                else:
                    print("\n⚠️ You waste time searching nothing!")
                    attempts_left -= 1

        # -------------------------------------------------------------
        # 2. DISTRACT (Has sub-items to throw/use)
        # -------------------------------------------------------------
        elif action == "distract":
            opts = "coin | book" + (" | mirror" if has_mirror else "")
            print(f"\nWhat item do you use? [ {opts} ]")
            item_choice = input("Select item: ").strip().lower()

            if item_choice == "mirror" and has_mirror:
                print("\n💥 You reflect the ghost's image with the Silver Mirror!")
                print("It recoils in terror and vanishes into the walls!")
                cleared = True
            elif item_choice == "coin" and ghost_state == "watching":
                print("\n🪙 You flick a coin to the far left. The ghost floats over to inspect it!")
                print("This gives you enough time to rush the door!")
                cleared = True
            elif item_choice == "book" and ghost_state == "wandering":
                print("\n📚 The book lands quietly on the rug. The ghost ignores it completely.")
                attempts_left -= 1
            else:
                print("\n❌ Your distraction fails! The ghost turns and chills you!")
                player["health"] = max(0, current_health - 1)
                attempts_left -= 1

        # -------------------------------------------------------------
        # 3. DODGE (Has follow-up moves)
        # -------------------------------------------------------------
        elif action == "dodge":
            if ghost_state == "charging":
                print("\n⚡ You dive sideways just as the ghost charges! It slams into the wall!")
                follow_up = input("Quick! Follow-up move? [ counterattack | grabkey ]: ").strip().lower()
                
                if follow_up == "grabkey":
                    print("\n🎉 You snag the key floating off its belt while it's dazed and escape!")
                    cleared = True
                else:
                    print("\n🥊 You tried to punch it, but your fist passes through! It recovers!")
                    attempts_left -= 1
            else:
                print("\n❌ You dove for no reason! The ghost punishes your foolishness.")
                player["health"] = max(0, current_health - 1)
                attempts_left -= 1

        # -------------------------------------------------------------
        # 4. SNEAK (Simple condition based on wandering stance)
        # -------------------------------------------------------------
        elif action == "sneak":
            if ghost_state == "wandering":
                print("\n👟 You tiptoe along the edge of the rug, slip past the ghost, and unlock the door!")
                cleared = True
            else:
                print("\n❌ The ghost sees or hears you immediately!")
                player["health"] = max(0, current_health - 1)
                attempts_left -= 1

        # -------------------------------------------------------------
        # 5. ATTACK
        # -------------------------------------------------------------
        elif action == "attack":
            print("\n🥊 Physical attacks don't affect specters! You take cold damage!")
            player["health"] = max(0, current_health - 1)
            attempts_left -= 1

        else:
            print("\n⚠️ Invalid action! Type search, distract, dodge, sneak, or attack.")

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
