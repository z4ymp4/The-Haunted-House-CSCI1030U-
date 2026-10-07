#intro to comp sci project
#add your room libary here that you created. 
from rooms.kitchen import play_kitchen_room, play_bedroom

def main():
    player = {"health": 4, "keys": [], "rooms_completed": []}

    # everyone pls add your room function here
    rooms = [
        ("Kitchen", play_kitchen_room),
        ("Ghost Bedroom", play_bedroom),
    ]

    for name, room_func in rooms:
        if not room_func(player):
            print("\nGAME OVER!")
            return

    print("\nCONGRATULATIONS! You escaped!")

if __name__ == "__main__":
    main()
