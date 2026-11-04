# Kapishnan 

import random

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)

def play_bedroom(player: dict) -> bool:
    """
    Ghost Bedroom - Dynamic Sub-Action System with State Memory.
    Prevents repeated searches and guarantees key collection before escaping!
    """
    print_divider()
    print("👻 GHOST BEDROOM 👻")
    print("You step into the freezing room. A specter blocks the exit!")
    print_divider()

    attempts_left: int = 30
    cleared: bool = False
    
    # State flags to prevent repetitive searches
    has_mirror: bool = False
    searched_drawer: bool = False
    searched_carpet: bool = False
    searched_bed: bool = False

    while attempts_left > 0 and not cleared:
        current_health = player.get("health", 3)
        print(f"\n[ Health: {current_health} HP | Ghost Strikes Left: {attempts_left} ]")
        
        # Ghost stance dictates the safest strategy
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
        # 1. SEARCH (Sub-locations with repetition prevention)
        # -------------------------------------------------------------
        if action == "search":
            print("\nWhere do you want to search?")
            target = input("Pick location [ drawer | bed | carpet ]: ").strip().lower()
            
            if target == "drawer":
                if not searched_drawer:
                    searched_drawer = True
                    has_mirror = True
                    print("\n✨ You found a polished Silver Mirror inside the drawer!")
                else:
                    print("\n🔍 You search the drawer again... It's empty, but you notice a hidden passage switch!")
                    print("🗝️ You grab a spare Bedroom Key hidden inside the switch slot and escape through the wall!")
                    cleared = True

            elif target == "carpet":
                if not searched_carpet:
                    searched_carpet = True
                    print("\n🗝️ You peek under the carpet and spot the Bedroom Key!")
                    print("You snatch it up and unlock the door!")
                    cleared = True
                else:
                    print("\n🔍 You already checked under the carpet. Nothing else here.")

            elif target == "bed":
                if not searched_bed:
                    searched_bed = True
                    print("\nDust flies into the air! The ghost rushes you!")
                    bed_sub = input("Quick! [ dive under bed | throw pillow ]: ").strip().lower()
                    if bed_sub == "dive under bed":
                        print("👟 You hide under the bed, snag the key off the nightstand frame, and unlock the door!")
                        cleared = True
                    else:
                        print("❌ The pillow passes straight through the ghost! It chills you.")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1
                else:
                    print("\n🔍 You already checked the bed area!")
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
                print("It recoils in terror, drops the Bedroom Key, and vanishes into the walls!")
                cleared = True

            elif item_choice == "coin":
                if ghost_state == "watching":
                    print("\n🪙 You flick a coin to the far left. The ghost floats over to inspect it!")
                    print("You grab the Bedroom Key off the table and escape!")
                    cleared = True
                else:
                    print("\nThe ghost ignores the coin! It turns toward you!")
                    coin_sub = input("Quick follow-up! [ run past | hide ]: ").strip().lower()
                    if coin_sub == "run past":
                        print("🎉 You swipe the key, dash past the ghost just in time, and make it out!")
                        cleared = True
                    else:
                        print("❌ You try to hide in the open, taking cold damage!")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1

            elif item_choice == "book":
                print("\n📚 You hurl the book across the room.")
                book_sub = input("Follow the sound or slip away? [ slip away | charge ]: ").strip().lower()
                if book_sub == "slip away":
                    print("👟 While the ghost turns to look, you grab the key and slip through the door!")
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
                        print("🎉 You grab the Bedroom Key from the bedpost and escape!")
                        cleared = True
                    else:
                        print("❌ Standing your ground gave the ghost a free hit!")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1

            elif dodge_sub == "duck":
                print("\n💥 You duck under the ghost's icy aura!")
                print("You snatch the Bedroom Key hanging right above you and unlock the door!")
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
                print("\n👥 You stick to the dark shadows, grab the key from the nightstand, and slip right past!")
                cleared = True

            elif sneak_sub == "wall":
                if ghost_state == "wandering":
                    print("\n👟 You tiptoe along the wall quietly, grab the key, and unlock the door!")
                    cleared = True
                else:
                    print("\nThe floorboard creaks under your weight!")
                    recover = input("Quick recovery! [ jump | freeze ]: ").strip().lower()
                    if recover == "jump":
                        print("🎉 You leap forward onto the rug, snatch the key, and reach the exit!")
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
                print("The ghost fears the flame, drops the key, and backs away so you can pass!")
                cleared = True
            elif attack_sub == "punch":
                print("\n🥊 Your fist goes straight through the ghost!")
                punch_sub = input("Quick! Follow-up? [ kick furniture | back away ]: ").strip().lower()
                if punch_sub == "kick furniture":
                    print("🛋️ Kicking the nightstand knocks a lantern loose! The key tumbles out and light scares the ghost away!")
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
