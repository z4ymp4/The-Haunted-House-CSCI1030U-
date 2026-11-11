"""Haunted House - Milestone 2. Run: python main.py [options]"""
import argparse
import os

from game import DIFFICULTY, ROOM_IDS, Game, build_settings
from player import Player
from scoreboard import ScoreBoard

BASE = os.path.dirname(os.path.abspath(__file__))


def parse_args():
    p = argparse.ArgumentParser(description="Escape the haunted house!")
    p.add_argument("--difficulty", choices=DIFFICULTY, default="normal",
                   help="sets starting health, attempts and ghost damage")
    p.add_argument("--name", help="player name (skips the name prompt)")
    p.add_argument("--save-file", default=os.path.join(BASE, "data", "savegame.json"),
                   help="where to save/load the game")
    p.add_argument("--scores-file", default=os.path.join(BASE, "data", "scores.json"),
                   help="where high scores are stored")
    p.add_argument("--riddles", default=os.path.join(BASE, "data", "riddles.json"),
                   help="JSON file of riddles for the library")
    p.add_argument("--inventory-size", type=int, default=5,
                   help="maximum number of items the player can carry")
    p.add_argument("--start-room", choices=ROOM_IDS,
                   help="practice mode: start at this room with earlier rewards granted")
    return p.parse_args()


HOW_TO_PLAY = """
HOW TO PLAY
Escape through five rooms: Dark Hallway, Riddle Library, Locked Kitchen,
Ghost Bedroom and the Exit Room. Collect keys along the way (you need 3).
Items matter: the flashlight or a coin can get you past the ghost.
Before each room you can save and quit, then load the game later.
"""


def new_game(args, scoreboard):
    name = args.name or input("What is your name? ").strip() or "Player"
    settings = build_settings(args.difficulty, args.riddles, args.inventory_size)
    game = Game(settings, Player(name, settings["health"]), scoreboard, args.save_file)
    if args.start_room:
        game.skip_to(args.start_room)
    game.run()


def load_game(args, scoreboard):
    try:
        game = Game.load(args.save_file, scoreboard, args.riddles, args.inventory_size)
    except FileNotFoundError:
        print("No saved game found.")
        return
    except (ValueError, KeyError) as err:
        print(f"That save file is not usable ({err}).")
        return
    print(f"Welcome back, {game.player.name}!")
    game.run()


def main():
    args = parse_args()
    scoreboard = ScoreBoard(args.scores_file)
    while True:
        print("\n=== HAUNTED HOUSE ===")
        print("1. New game\n2. Load game\n3. High scores\n4. How to play\n5. Quit")
        choice = input("> ").strip()
        if choice == "1":
            new_game(args, scoreboard)
        elif choice == "2":
            load_game(args, scoreboard)
        elif choice == "3":
            scoreboard.display()
        elif choice == "4":
            print(HOW_TO_PLAY)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
