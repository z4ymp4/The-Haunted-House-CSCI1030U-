def kitchen-room(player)

print("Welcome to room 3")
print("You entered kitchen .Find the key to unlock the exit door")

locations=["table","fridge","closet","drawer"]

searched=[]
found_key=False

while not found_key and player["health"]>0:
    print(f"\nHealth: {player['health']} \n| Keys: {player['keys']}")
        print("Please select location ", locations)
        choice = input("Where would you like to search? ")

        if choice not in locations:
            print(" Choose from the options.")
            continue

        if choice in searched:
            print("You have been there,Time running ")
            continue

        searched.append(choice)

        if choice=="drawer":
            print(">> Found the Kitchen Key!")
            player["keys"].append("kitchen_key")
            found_key = True
        elif choice == "fridge":
            print(" Found fresh water! (+1 Health)")
            player["health"] += 1
        elif choice == "table":
            print(" A rat bit you ")
            player["health"] -= 1
        elif choice == "closet":
            print(" spiders living in webs.")

    if player["health"] <= 0:
        print("\nYou lost in the kitchen.")
        return False

player["rooms_completed"].append("Kitchen")
print("go to room 4 ")
return True
            
