// Kapishnan
def play_bedroom(player):
    
    print("\nYou push open the creaking door to the Ghost Bedroom. A cold mist fills the air, and a glowing specter blocks the path!")
    
    attempts_left = 3
    success = False
    
    while attempts_left > 0 and not success:
        print(f"\nThe ghost glares at you. You have {attempts_left} attempts left.")
        print("What do you want to do?")
        print("1. Talk to the ghost")
        print("2. Distract the ghost")
        print("3. Sneak past the ghost")
        print("4. Fight the ghost")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "2":
            print("You toss a loose coin across the room. The ghost chases the sound, leaving the key unguarded!")
            success = True
        elif choice == "1":
            print("You try to speak, but the ghost wails loudly, freezing you in fear.")
            attempts_left -= 1
        elif choice == "3":
            print("You try to creep past quietly, but the floorboard creeks. The ghost notices you!")
            attempts_left -= 1
        elif choice == "4":
            print("You swing blindly at the spirit—your hand passes right through it, chilling you to the bone.")
            attempts_left -= 1
        else:
            print("That's not a valid choice! Please enter a number between 1 and 4.")
            
    if success:
        print("You grab the key from the nightstand and slip out of the bedroom!")
        return True
    else:
        print("The ghost overpowers you with cold dread, forcing you to retreat.")
        return False
