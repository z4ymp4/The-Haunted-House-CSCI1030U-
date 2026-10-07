def play_exit(player):
    """
    Room 5: The Exit Door
    The player must inspect and try the final exit door using collected keys.
    """
    # Dictionary storing room info & requirements
    exit_info = {
        "required_keys": 3,
        "attempts_left": 3,
        "door_status": "locked",
        "choices": ["1. Inspect the door", "2. Try the door", "3. Look around for clues"]
    }

    print("\n--- ROOM 5: THE EXIT DOOR ---")
    print("You reach the heavy iron front door of the haunted house.")

    # while Loop allowing the player to make decisions, locking them in the loop tiil either they escape or run out of attempts
    while exit_info["attempts_left"] > 0:
        print("\nWhat would you like to do?")
        for choice in exit_info["choices"]:
            print(choice)

        user_choice = input("Enter option (1-3): ").strip()

        # if elsee conditions for player choice
        if user_choice == "1":
            print(f"The door has {exit_info['required_keys']} heavy keyholes. It looks solid.")
            
        elif user_choice == "2":
            # Check player's keys list from shared player dictionary
            keys_found = len(player["keys"])
            print(f"You have {keys_found} out of {exit_info['required_keys']} keys needed.")

            if keys_found >= exit_info["required_keys"]:
                exit_info["door_status"] = "unlocked"
                print("\nYou insert all your keys into the door... Click! The heavy door swings open!")
                print(f"Congratulations {player['name']}! You escaped the haunted house!")
                
                # Update player tracking collection
                player["rooms_completed"].append("exit_door")
                return True
            else:
                exit_info["attempts_left"] -= 1
                print("The lock won't budge! You don't have enough keys yet.")
                print(f"Attempts left: {exit_info['attempts_left']}")

        elif user_choice == "3":
            print("Dust settles on the cold floor. The only way out is through that front door.")

        else:
            print("Invalid option. Please enter 1, 2, or 3.")

    # Outcome if player runs out of attempts/time at the door
    print("\nA dark shadow envelops you before you can figure out the lock...")
    print("GAME OVER - You failed to escape in time.")
    return False
