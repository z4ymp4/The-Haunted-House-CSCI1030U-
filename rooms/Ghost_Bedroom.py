# Kapishnan

import random
from rooms.base import Room

# -------------------------------------------------------------
# OOP REQUIREMENT: Ghost Helper Class
# -------------------------------------------------------------
class Ghost:
    def __init__(self):
        self.stance = "watching"
        self.health = 3

    def pick_random_stance(self):
        self.stance = random.choice(["watching", "charging", "wandering"])
        return self.stance

    def to_dict(self):
        return {"stance": self.stance, "health": self.health}

    def load_from_dict(self, data):
        self.stance = data.get("stance", "watching")
        self.health = data.get("health", 3)


# -------------------------------------------------------------
# OOP REQUIREMENT: Main Bedroom Room Class
# -------------------------------------------------------------
class BedroomRoom(Room):
    def __init__(self, difficulty="normal"):
        super().__init__(name="bedroom")
        self.ghost = Ghost()
        self.difficulty = difficulty
        
        if self.difficulty == "hard":
            self.attempts_left = 2
        elif self.difficulty == "easy":
            self.attempts_left = 4
        else:
            self.attempts_left = 3
            
        self.has_mirror = False
        self.searched_locations = []

    # -------------------------------------------------------------
    # RECURSION REQUIREMENT: Recursive Search Function
    # -------------------------------------------------------------
    def check_spot_recursively(self, spots_list, target_spot, index=0):
        if index >= len(spots_list):
            return False
        if spots_list[index] == target_spot:
            return True
        return self.check_spot_recursively(spots_list, target_spot, index + 1)

    # -------------------------------------------------------------
    # FILE I/O REQUIREMENT: Save & Load Dict Methods
    # -------------------------------------------------------------
    def to_dict(self):
        return {
            "name": self.name,
            "cleared": self.cleared,
            "difficulty": self.difficulty,
            "attempts_left": self.attempts_left,
            "has_mirror": self.has_mirror,
            "searched_locations": self.searched_locations,
            "ghost": self.ghost.to_dict()
        }

    def load_from_dict(self, data):
        self.cleared = data.get("cleared", False)
        self.attempts_left = data.get("attempts_left", 3)
        self.has_mirror = data.get("has_mirror", False)
        self.searched_locations = data.get("searched_locations", [])
        if "ghost" in data:
            self.ghost.load_from_dict(data["ghost"])

    # Helper method for player taking damage to avoid repeating code
    def damage_player(self, player):
        player.health = max(0, player.health - 1)
        self.attempts_left -= 1

    # -------------------------------------------------------------
    # MAIN GAMEPLAY LOOP
    # -------------------------------------------------------------
    def play(self, player):
        print("=" * 45)
        print("👻 GHOST BEDROOM 👻")
        print("You step into the freezing room. A specter blocks the exit!")
        print(f"Difficulty: {self.difficulty.upper()}")
        print("=" * 45)

        valid_spots = ["drawer", "bed", "carpet"]

        while self.attempts_left > 0 and not self.cleared:
            print(f"\n[ Health: {player.health} HP | Ghost Strikes Left: {self.attempts_left} ]")
            ghost_state = self.ghost.pick_random_stance()

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

            # --- 1. SEARCH ---
            if action == "1":
                print("\nWhere do you want to search?")
                print("  [1] Search Nightstand Drawer")
                print("  [2] Search Under Bed")
                print("  [3] Search Floor Carpet")
                target_choice = input("Pick location (1-3): ").strip()

                target_name = ""
                if target_choice == "1":
                    target_name = "drawer"
                elif target_choice == "2":
                    target_name = "bed"
                elif target_choice == "3":
                    target_name = "carpet"

                # Verify spot exists via recursion
                if self.check_spot_recursively(valid_spots, target_name):
                    if target_name in self.searched_locations:
                        if target_name == "drawer":
                            print("\n🔍 You search the drawer again... It's empty, but you notice a hidden passage switch!")
                            print("🗝️ You grab a spare bedroom_key inside the slot and escape through the wall!")
                            self.cleared = True
                        else:
                            print(f"\n🔍 You already checked the {target_name} area!")
                    else:
                        self.searched_locations.append(target_name)
                        if target_name == "drawer":
                            self.has_mirror = True
                            print("\n✨ You found a polished Silver Mirror inside the drawer!")
                        elif target_name == "bed":
                            print("\nDust flies into the air as you check the bed! The ghost turns toward you!")
                            print("  [1] Dive completely under the bed")
                            print("  [2] Throw a dusty pillow at the ghost")
                            bed_sub = input("Quick move (1-2): ").strip()
                            if bed_sub == "1" and ghost_state != "charging":
                                print("👟 You hide under the frame, snag the key from the post, and unlock the door!")
                                self.cleared = True
                            else:
                                print("❌ The ghost catches you completely off guard! You take heavy cold damage.")
                                self.damage_player(player)
                        elif target_name == "carpet":
                            if ghost_state == "wandering":
                                print("\n🗝️ You peek under the carpet, spot the bedroom_key, and unlock the door!")
                                self.cleared = True
                            else:
                                print("\n❌ You were spotted lifting the rug! The ghost strikes while you are exposed.")
                                self.damage_player(player)
                else:
                    print("\n⚠️ You hesitate and waste a turn!")
                    self.attempts_left -= 1

            # --- 2. DISTRACT ---
            elif action == "2":
                print("\nWhat item do you use?")
                print("  [1] Toss a heavy book")
                print("  [2] Flick a shiny coin")
                if self.has_mirror:
                    print("  [3] Reflect light with Silver Mirror")
                item_choice = input("Select item: ").strip()

                if item_choice == "3" and self.has_mirror:
                    print("\n💥 You reflect the ghost's image with the Silver Mirror!")
                    print("It recoils in terror, drops the bedroom_key, and vanishes into the walls!")
                    self.cleared = True
                elif item_choice == "2":
                    if ghost_state == "watching":
                        print("\n🪙 You flick a coin to the far left. The ghost floats over to inspect it!")
                        print("You grab the bedroom_key off the table and escape!")
                        self.cleared = True
                    else:
                        print("\nThe ghost ignores the small coin and locks onto you!")
                        print("  [1] Dash straight past the ghost")
                        print("  [2] Try to drop and hide")
                        coin_sub = input("Follow-up action (1-2): ").strip()
                        if coin_sub == "1" and ghost_state == "wandering":
                            print("🎉 You swipe the key and sprint past just in time!")
                            self.cleared = True
                        else:
                            print("❌ Bad timing! The ghost blasts you with dark mist.")
                            self.damage_player(player)
                elif item_choice == "1":
                    print("\n📚 You hurl the book across the room.")
                    print("  [1] Slip toward the exit while it looks")
                    print("  [2] Rush the ghost directly")
                    book_sub = input("Follow-up action (1-2): ").strip()
                    if book_sub == "1" and ghost_state != "watching":
                        print("👟 While the ghost is distracted, you grab the key and slip out!")
                        self.cleared = True
                    else:
                        print("❌ The ghost saw through your move and punished you!")
                        self.damage_player(player)
                else:
                    print("\n⚠️ Invalid item selection!")
                    self.attempts_left -= 1

            # --- 3. DODGE ---
            elif action == "3":
                print("\nHow do you maneuver?")
                print("  [1] Perform a low side-roll")
                print("  [2] Duck down underneath")
                dodge_sub = input("Select maneuver (1-2): ").strip()

                if dodge_sub == "1":
                    if ghost_state == "charging":
                        print("\n⚡ You roll sideways as the ghost surges! It crashes hard into the wall!")
                        print("You snatch the key while it's dazed and escape!")
                        self.cleared = True
                    else:
                        print("\n👟 You execute a clean roll, but the ghost is ready for you!")
                        print("  [1] Reach out to grab the key on the bedpost")
                        print("  [2] Hold your position")
                        roll_sub = input("Next move (1-2): ").strip()
                        if roll_sub == "1" and ghost_state == "wandering":
                            print("🎉 You snatch the key and unlock the exit!")
                            self.cleared = True
                        else:
                            print("❌ The ghost blasts you while recovering from the roll!")
                            self.damage_player(player)
                elif dodge_sub == "2":
                    if ghost_state == "charging":
                        print("\n💥 You duck under the charging specter! You snag the hanging key and exit!")
                        self.cleared = True
                    else:
                        print("\n❌ Ducking in place left you completely exposed to cold aura!")
                        self.damage_player(player)
                else:
                    print("\n⚠️ Invalid maneuver!")
                    self.attempts_left -= 1

            # --- 4. SNEAK ---
            elif action == "4":
                print("\nWhich route do you take?")
                print("  [1] Along the dark side walls")
                print("  [2] Straight through the center shadows")
                sneak_sub = input("Select route (1-2): ").strip()

                if sneak_sub == "2":
                    if ghost_state == "wandering":
                        print("\n👥 You stick to the center shadows, grab the key, and slip right past!")
                        self.cleared = True
                    else:
                        print("\n❌ The ghost catches your outline in the light! You take cold damage.")
                        self.damage_player(player)
                elif sneak_sub == "1":
                    if ghost_state == "wandering":
                        print("\n👟 You tiptoe along the wall quietly, grab the key, and unlock the door!")
                        self.cleared = True
                    else:
                        print("\nA floorboard creaks under your weight!")
                        print("  [1] Leap forward toward the key")
                        print("  [2] Freeze completely still")
                        recover = input("Quick recovery (1-2): ").strip()
                        if recover == "1" and ghost_state != "charging":
                            print("🎉 You leap forward onto the rug, snatch the key, and reach the exit!")
                            self.cleared = True
                        else:
                            print("❌ Hesitation cost you! The ghost turns around and hits you.")
                            self.damage_player(player)
                else:
                    print("\n⚠️ Invalid sneak route!")
                    self.attempts_left -= 1

            # --- 5. ATTACK ---
            elif action == "5":
                print("\nHow will you attack?")
                print("  [1] Wave a lit candle flame at it")
                print("  [2] Try to throw a physical punch")
                attack_sub = input("Choose tactic (1-2): ").strip()

                if attack_sub == "1":
                    if ghost_state != "charging":
                        print("\n🕯️ You wave the flame forward! The spirit recoils, drops the key, and retreats!")
                        self.cleared = True
                    else:
                        print("\n❌ The flame blew out as the ghost charged through it! Direct hit taken.")
                        self.damage_player(player)
                elif attack_sub == "2":
                    print("\n🥊 Your fist passes right through the ghost harmlessly!")
                    print("  [1] Kick a nightstand to knock over a lantern")
                    print("  [2] Back away slowly")
                    punch_sub = input("Follow-up (1-2): ").strip()
                    if punch_sub == "1":
                        print("🛋️ The lantern crashes and bursts into light! The key drops and the ghost retreats!")
                        self.cleared = True
                    else:
                        print("❌ Backing away slowly was too slow! Cold damage taken.")
                        self.damage_player(player)
                else:
                    print("\n⚠️ Invalid attack style!")
                    self.attempts_left -= 1

            else:
                print("\n⚠️ Invalid choice! Enter 1, 2, 3, 4, or 5.")

        # --- OUTCOME HANDLING ---
        print("=" * 45)
        if self.cleared:
            print("🎉 SUCCESS: You grabbed the bedroom_key and escaped!")
            player.keys.append("bedroom_key")
            player.rooms_completed.append("bedroom")
            print("=" * 45)
            return True
        else:
            print("💀 FAILED: You were driven out of the bedroom!")
            print("=" * 45)
            return False


# -------------------------------------------------------------
# DIRECT TEST BLOCK (For testing room directly in VS Code)
# -------------------------------------------------------------
if __name__ == "__main__":
    class SimplePlayer:
        def __init__(self):
            self.health = 3
            self.keys = []
            self.rooms_completed = []

    test_room = BedroomRoom(difficulty="normal")
    test_player = SimplePlayer()
    result = test_room.play(test_player)
    print(f"\n[TEST RESULT] Cleared: {result}")
