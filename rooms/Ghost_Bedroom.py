# Kapishnan 

import random

def print_divider() -> None:
    """Helper function to keep output clean and readable."""
    print("=" * 45)

def play_bedroom(player: dict) -> bool:
    """
    Ghost Bedroom - Numbered Dynamic Choice System.
    Uses numbered sub-choices with real risk/reward and stance checks.
    """
    print_divider()
    print("👻 GHOST BEDROOM 👻")
    print("You step into the freezing room. A specter blocks the exit!")
    print_divider()

    attempts_left: int = 30
    cleared: bool = False
    
    # State tracking
    has_mirror: bool = False
    searched_drawer: bool = False
    searched_carpet: bool = False
    searched_bed: bool = False

    while attempts_left > 0 and not cleared:
        current_health = player.get("health", 3)
        print(f"\n[ Health: {current_health} HP | Ghost Strikes Left: {attempts_left} ]")
        
        # Ghost stance dictates which tactics are dangerous
        ghost_state = random.choice(["watching", "charging", "wandering"])
        
        if ghost_state == "watching":
            print("👀 Ghost Stance: Floating in place, watching your every movement!")
        elif ghost_state == "charging":
            print("⚡ Ghost Stance: Gathering dark mist, getting ready to SURGE forward!")
        else:
            print("🌫️ Ghost Stance: Mindlessly drifting near the ceiling with its back turned.")

        print("\nPrimary Actions:")
        print("  [1] Search the room")
        print("  [2] Distract the ghost")
        print("  [3] Dodge / Maneuver")
        print("  [4] Sneak around")
        print("  [5] Attack directly")
        
        action = input("\nChoose action (1-5): ").strip()

        # -------------------------------------------------------------
        # 1. SEARCH
        # -------------------------------------------------------------
        if action == "1":
            print("\nWhere do you want to search?")
            print("  [1] Search Nightstand Drawer")
            print("  [2] Search Under Bed")
            print("  [3] Search Floor Carpet")
            target = input("Pick location (1-3): ").strip()
            
            if target == "1":
                if not searched_drawer:
                    searched_drawer = True
                    has_mirror = True
                    print("\n✨ You found a polished Silver Mirror inside the drawer!")
                else:
                    print("\n🔍 You search the drawer again... It's empty, but you notice a hidden passage switch!")
                    print("🗝️ You grab a spare Bedroom Key inside the slot and escape through the wall!")
                    cleared = True

            elif target == "2":
                if not searched_bed:
                    searched_bed = True
                    print("\nDust flies into the air as you check the bed! The ghost turns toward you!")
                    print("  [1] Dive completely under the bed")
                    print("  [2] Throw a dusty pillow at the ghost")
                    bed_sub = input("Quick move (1-2): ").strip()
                    
                    if bed_sub == "1" and ghost_state != "charging":
                        print("👟 You hide under the frame, snag the key from the post, and unlock the door!")
                        cleared = True
                    else:
                        print("❌ The ghost catches you completely off guard! You take heavy cold damage.")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1
                else:
                    print("\n🔍 You already checked the bed area!")

            elif target == "3":
                if not searched_carpet:
                    searched_carpet = True
                    if ghost_state == "wandering":
                        print("\n🗝️ You peek under the carpet, spot the Bedroom Key, and unlock the door!")
                        cleared = True
                    else:
                        print("\n❌ You were spotted lifting the rug! The ghost strikes while you are exposed.")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1
                else:
                    print("\n🔍 You already checked under the carpet.")

            else:
                print("\n⚠️ You hesitate and waste a turn!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 2. DISTRACT
        # -------------------------------------------------------------
        elif action == "2":
            print("\nWhat item do you use?")
            print("  [1] Toss a heavy book")
            print("  [2] Flick a shiny coin")
            if has_mirror:
                print("  [3] Reflect light with Silver Mirror")
            
            item_choice = input("Select item: ").strip()

            if item_choice == "3" and has_mirror:
                print("\n💥 You reflect the ghost's image with the Silver Mirror!")
                print("It recoils in terror, drops the Bedroom Key, and vanishes into the walls!")
                cleared = True

            elif item_choice == "2":
                if ghost_state == "watching":
                    print("\n🪙 You flick a coin to the far left. The ghost floats over to inspect it!")
                    print("You grab the Bedroom Key off the table and escape!")
                    cleared = True
                else:
                    print("\nThe ghost ignores the small coin and locks onto you!")
                    print("  [1] Dash straight past the ghost")
                    print("  [2] Try to drop and hide")
                    coin_sub = input("Follow-up action (1-2): ").strip()
                    
                    if coin_sub == "1" and ghost_state == "wandering":
                        print("🎉 You swipe the key and sprint past just in time!")
                        cleared = True
                    else:
                        print("❌ Bad timing! The ghost blasts you with dark mist.")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1

            elif item_choice == "1":
                print("\n📚 You hurl the book across the room.")
                print("  [1] Slip toward the exit while it looks")
                print("  [2] Rush the ghost directly")
                book_sub = input("Follow-up action (1-2): ").strip()
                
                if book_sub == "1" and ghost_state != "watching":
                    print("👟 While the ghost is distracted, you grab the key and slip out!")
                    cleared = True
                else:
                    print("❌ The ghost saw through your move and punished you!")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1
            else:
                print("\n⚠️ Invalid item selection!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 3. DODGE
        # -------------------------------------------------------------
        elif action == "3":
            print("\nHow do you maneuver?")
            print("  [1] Perform a low side-roll")
            print("  [2] Duck down underneath")
            dodge_sub = input("Select maneuver (1-2): ").strip()

            if dodge_sub == "1":
                if ghost_state == "charging":
                    print("\n⚡ You roll sideways as the ghost surges! It crashes hard into the wall!")
                    print("You snatch the key while it's dazed and escape!")
                    cleared = True
                else:
                    print("\n👟 You execute a clean roll, but the ghost is ready for you!")
                    print("  [1] Reach out to grab the key on the bedpost")
                    print("  [2] Hold your position")
                    roll_sub = input("Next move (1-2): ").strip()
                    
                    if roll_sub == "1" and ghost_state == "wandering":
                        print("🎉 You snatch the key and unlock the exit!")
                        cleared = True
                    else:
                        print("❌ The ghost blasts you while you recovery from the roll!")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1

            elif dodge_sub == "2":
                if ghost_state == "charging":
                    print("\n💥 You duck under the charging specter! You snag the hanging key and exit!")
                    cleared = True
                else:
                    print("\n❌ Ducking in place left you completely exposed to cold aura!")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1
            else:
                print("\n⚠️ Invalid maneuver!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 4. SNEAK
        # -------------------------------------------------------------
        elif action == "4":
            print("\nWhich route do you take?")
            print("  [1] Along the dark side walls")
            print("  [2] Straight through the center shadows")
            sneak_sub = input("Select route (1-2): ").strip()

            if sneak_sub == "2":
                if ghost_state == "wandering":
                    print("\n👥 You stick to the center shadows, grab the key, and slip right past!")
                    cleared = True
                else:
                    print("\n❌ The ghost catches your outline in the light! You take cold damage.")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1

            elif sneak_sub == "1":
                if ghost_state == "wandering":
                    print("\n👟 You tiptoe along the wall quietly, grab the key, and unlock the door!")
                    cleared = True
                else:
                    print("\nA floorboard creaks under your weight!")
                    print("  [1] Leap forward toward the key")
                    print("  [2] Freeze completely still")
                    recover = input("Quick recovery (1-2): ").strip()
                    
                    if recover == "1" and ghost_state != "charging":
                        print("🎉 You leap forward onto the rug, snatch the key, and reach the exit!")
                        cleared = True
                    else:
                        print("❌ Hesitation cost you! The ghost turns around and hits you.")
                        player["health"] = max(0, current_health - 1)
                        attempts_left -= 1
            else:
                print("\n⚠️ Invalid sneak route!")
                attempts_left -= 1

        # -------------------------------------------------------------
        # 5. ATTACK
        # -------------------------------------------------------------
        elif action == "5":
            print("\nHow will you attack?")
            print("  [1] Wave a lit candle flame at it")
            print("  [2] Try to throw a physical punch")
            attack_sub = input("Choose tactic (1-2): ").strip()

            if attack_sub == "1":
                if ghost_state != "charging":
                    print("\n🕯️ You wave the flame forward! The spirit recoils, drops the key, and retreats!")
                    cleared = True
                else:
                    print("\n❌ The flame blew out as the ghost charged through it! Direct hit taken.")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1

            elif attack_sub == "2":
                print("\n🥊 Your fist passes right through the ghost harmlessly!")
                print("  [1] Kick a nightstand to knock over a lantern")
                print("  [2] Back away slowly")
                punch_sub = input("Follow-up (1-2): ").strip()
                
                if punch_sub == "1":
                    print("🛋️ The lantern crashes and bursts into light! The key drops and the ghost retreats!")
                    cleared = True
                else:
                    print("❌ Backing away slowly was too slow! Cold damage taken.")
                    player["health"] = max(0, current_health - 1)
                    attempts_left -= 1
            else:
                print("\n⚠️ Invalid attack style!")
                attempts_left -= 1

        else:
            print("\n⚠️ Invalid choice! Enter 1, 2, 3, 4, or 5.")

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
