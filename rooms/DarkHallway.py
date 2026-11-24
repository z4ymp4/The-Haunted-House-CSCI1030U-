def play_hallway(player): #kavin 
    choices = ["left", "right", "forward"]
    print("welcome to the Dark Hallway\n")
    print("You entered the Dark Hallway. You can go left, right, or forward. Choose wisely.")

    while True:
        choice = input("which way?").lower().strip()
        
        if choice not in choices:
            print("invalid choice. Enter left, right, or forward.")
            
        elif choice == "left":
            print(" you have found a flashlight!")
            player["items"].append("flashlight")
            print("You can now see in the dark hallway.")
            break
        elif choice =="right":
            print("You have fallen into a trap! (-1 Health)")
            player["health"] -= 1
            if player["health"] <= 0:
                print("You have died in the Dark Hallway.")
    
        else:
            print("you walk forward nd find a key!")
            player["keys"].append("hallway_key")
            break
                
       
                
        
     
