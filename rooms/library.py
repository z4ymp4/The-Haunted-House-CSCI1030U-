def play_library(player):
    riddle = {
        "question": "What has keys but cannot open locks?",
        "answer": "piano",
        "reward": "library_key"
    }

    attempts = 3

    print("\nRoom 2: The Riddle Library")
    print("A mysterious voice gives you a riddle.")

    while attempts > 0:
        print("\n" + riddle["question"])
        answer = input("Your answer: ").lower()

        if answer == riddle["answer"]:
            print("Correct! You found the library key.")
            player["keys"].append(riddle["reward"])
            return True
        else:
            attempts -= 1
            print("Wrong answer.")
            print("Attempts left:", attempts)

        print("You failed the riddle and continue without the key.")
        return False
