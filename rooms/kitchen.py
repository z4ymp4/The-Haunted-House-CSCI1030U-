def play_kitchen_room(player):
    print("Welcome to room 3")
    print("You entered kitchen. Find the key to unlock the exit door")

    locations = ["table", "fridge", "closet", "drawer"]
    searched = []
    found_key = False

    while not found_key and player["health"] > 0:
        print(f"\nHealth: {player['health']} | Keys: {player['keys']}")
        print("Please select location:", locations)
        choice = input("Where would you like to search? ").strip().lower()

        if choice not in locations:
            print("Choose from the options.")
            continue

        if choice in searched:
            print("You have been there, time is running!")
            continue

        searched.append(choice)

        if choice == "drawer":
            print(">> Found the Kitchen Key!")
            player["keys"].append("kitchen_key")
            found_key = True
        elif choice == "fridge":
            print("Found fresh water! (+1 Health)")
            player["health"] += 1
        elif choice == "table":
            print("A rat bit you! (-1 Health)")
            player["health"] -= 1
        elif choice == "closet":
            print("Spiders living in webs.")

    if player["health"] <= 0:
        print("\nYou lost in the kitchen.")
        return False

    player["rooms_completed"].append("Kitchen")
    print("Go to room 4")
    return True