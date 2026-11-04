# Kapishnan 

import random

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)

def play_bedroom(player: dict) -> bool:
    """
    Ghost Bedroom - Interactive Sub-Action System.
    Every choice leads to sub-options with second chances to succeed!
    """
    print_divider()
    print("👻 GHOST BEDROOM 👻")
    print("You step into the freezing room. A specter blocks the exit!")
    print_divider()

    attempts_left: int = 30
    cleared: bool = False
    has_mirror: bool = False

    while attempts_left > 0 and not cleared:
        current_health = player.get("health", 3)
        print(f"\n[ Health: {current_health} HP | Ghost Strikes Left: {attempts_left} ]")
        
        # Ghost stance dictates the best conditions
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
        # 1. SEARCH (Sub-locations)
        # -------------------------------------------------------------
        if action == "search":
            print("\nWhere do you want to search?")
            target = input("Pick location [ drawer | bed | carpet ]: ").strip().lower()
            
            if target == "drawer":
                if not has_mirror:
                    print("\n✨ You found a polished Silver Mirror inside the drawer!")
                    has_mirror = True
                else:
                    print("\nDrawer is empty, but you notice a hidden passage switch!")
                    print("You hit the switch and escape through the wall!")
                    cleared = True

            elif target == "carpet":
                print("\n🗝️ You peek under the carpet and spot the Bedroom Key!")
                print("You snatch it up and unlock the door!")
                cleared = True

            elif target == "bed":
                print("\nDust flies into the air! The ghost rushes you!")
                bed_sub = input("Quick! [ dive under bed | throw pillow ]: ").strip().lower()
                if bed_sub == "dive under bed":
                    print("👟 You hide under the bed! The ghost misses you and you grab the key nearby!")
                    cleared = True
                else:
                    print("❌ The pillow passes straight through the ghost! It chills you.")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1
            else:
                print("\n⚠️ You hesitate and waste a turn!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 2. DISTRACT (Sub-items)
        # -------------------------------------------------------------
        elif action == "distract":
            opts = "coin | book" + (" | mirror" if has_mirror else "")
            print(f"\nWhat item do you use? [ {opts} ]")
            item_choice = input("Select item: ").strip().lower()

            if item_choice == "mirror" and has_mirror:
                print("\n💥 You reflect the ghost's image with the Silver Mirror!")
                print("It recoils in terror and vanishes into the walls!")
                cleared = True

            elif item_choice == "coin":
                if ghost_state == "watching":
                    print("\n🪙 You flick a coin to the far left. The ghost floats over to inspect it!")
                    print("You slip past and escape!")
                    cleared = True
                else:
                    print("\nThe ghost ignores the coin! It turns toward you!")
                    coin_sub = input("Quick follow-up! [ run past | hide ]: ").strip().lower()
                    if coin_sub == "run past":
                        print("🎉 You dash past the ghost just in time and make it out!")
                        cleared = True
                    else:
                        print("❌ You try to hide in the open, taking cold damage!")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1

            elif item_choice == "book":
                print("\n📚 You hurl the book across the room.")
                book_sub = input("Follow the sound or slip away? [ slip away | charge ]: ").strip().lower()
                if book_sub == "slip away":
                    print("👟 While the ghost turns to look, you slip through the door!")
                    cleared = True
                else:
                    print("❌ Charging didn't work! The ghost strikes you.")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1
            else:
                print("\n⚠️ Invalid item choice!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 3. DODGE (Sub-maneuvers)
        # -------------------------------------------------------------
        elif action == "dodge":
            print("\nHow do you maneuver?")
            dodge_sub = input("Choose maneuver [ roll | duck ]: ").strip().lower()

            if dodge_sub == "roll":
                if ghost_state == "charging":
                    print("\n⚡ You roll sideways as the ghost surges! It crashes into the wall!")
                    print("You snatch the floating key while it's dazed and escape!")
                    cleared = True
                else:
                    print("\n👟 You execute a clean tactical roll to safety across the room!")
                    roll_sub = input("What next? [ grab key | stand ground ]: ").strip().lower()
                    if roll_sub == "grab key":
                        print("🎉 You grab the key from the bed post and escape!")
                        cleared = True
                    else:
                        print("❌ Standing your ground gave the ghost a free hit!")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1

            elif dodge_sub == "duck":
                print("\n💥 You duck under the ghost's icy aura!")
                print("You see the door key hanging right above you!")
                cleared = True
            else:
                print("\n⚠️ Invalid dodge move!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 4. SNEAK (Sub-routes)
        # -------------------------------------------------------------
        elif action == "sneak":
            print("\nWhich path do you take?")
            sneak_sub = input("Pick route [ wall | shadows ]: ").strip().lower()

            if sneak_sub == "shadows":
                print("\n👥 You stick to the dark shadows near the curtains and slip right past!")
                cleared = True

            elif sneak_sub == "wall":
                if ghost_state == "wandering":
                    print("\n👟 You tiptoe along the wall quietly and unlock the door!")
                    cleared = True
                else:
                    print("\nThe floorboard creaks under your weight!")
                    recover = input("Quick recovery! [ jump | freeze ]: ").strip().lower()
                    if recover == "jump":
                        print("🎉 You leap forward onto the rug, avoiding the blast and reaching the exit!")
                        cleared = True
                    else:
                        print("❌ Freezing in place made you an easy target!")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1
            else:
                print("\n⚠️ Invalid sneak route!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 5. ATTACK (Sub-weapons)
        # -------------------------------------------------------------
        elif action == "attack":
            print("\nHow will you attack?")
            attack_sub = input("Choose tactic [ candle | punch ]: ").strip().lower()

            if attack_sub == "candle":
                print("\n🕯️ You grab a lit candle and wave the flame at the spirit!")
                print("The ghost fears the flame, backs away, and lets you pass!")
                cleared = True
            elif attack_sub == "punch":
                print("\n🥊 Your fist goes straight through the ghost!")
                punch_sub = input("Quick! Follow-up? [ kick furniture | back away ]: ").strip().lower()
                if punch_sub == "kick furniture":
                    print("🛋️ Kicking the nightstand knocks a lantern loose! The light scares the ghost away!")
                    cleared = True
                else:
                    print("❌ Backing away slowly wasn't fast enough. You take damage!")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1
            else:
                print("\n⚠️ Invalid attack style!")
                attempts_left -= 1

        else:
            print("\n⚠️ Invalid primary action! Choose search, distract, dodge, sneak, or attack.")

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
