#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'game.json'
item_file = 'items.json'
inventory = []

# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        with open(os.path.join(__location__, item_file)) as json_file: items = json.load(json_file)
        return (game,items)
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)


def check_inventory(item):
    for i in inventory:
        if i == item:
            return True
    return False


def render(game,items,current):
    c = game[current]
    print("\n\nYou are currently in " + c["name"])
    print(c["desc"])

    #display any items
    if "items" in c:
        for item in c["items"]:
            if not check_inventory(items["item"]):
                print(item["desc"])

    #display item information
    for i in inventory:
        if i in items:
            if current in items[i]["exits"]:
                print(items[i]["exits"][current])


    print("\nAvalible exits: ")
    for e in c["exits"]:
        if "condition" in e:
            if e["condition"] in inventory:
                print(e["exit"].lower())
        else:
            print(e["exit"].lower())



def get_input():
    response = input("\nWhat do you want to do now? ")
    response = response.upper().strip()
    return response

def update(game,items,current,response):
    if response == "INVENTORY":
        print("\nYou currently have: ")
        if len(inventory) == 0:
            print("nothing")
        else:
            for i in inventory:
                print(i.lower())
        return current

    c = game[current]
    for e in c["exits"]:
        if "condition" in e:
            if e["condition"] in inventory and response == e["exit"]:
                return e["target"]
        elif response == e["exit"]:
            return e["target"]

    for i in c["items"]:
        if response == "GET " + i["item"] and not check_inventory(i["item"]):
            print(i["take"])
            inventory.append(i["item"])
            return current

    for i in inventory:
        if i in items:
            for action in items[i]["actions"]:
                if response == action + " " + i:
                    print(i[i]["actions"][action])
                    return current

    if response[0:3] == "GET":
        print("You can't take that.")
    elif response in ("NORTH","WEST","SOUTH","SW","SE","NW","NE"):
        print("You can't go there.")
    else:
        print("I don't understand what you want to do.")
    return current
    










# The main function for the game
def main():
    current = 'BEDCH'  # The starting location
    end_game = ['BEDHEAL','BEDHEALFAV']  # Any of the end-game locations

    (game,items) = load_files()

    while True:
        render(game,items,current)
        response = get_input()

        if response == "QUIT":
            break

        current = update(game,items,current,response)


    print("Thanks for playing!!!")




# run the main function
if __name__ == '__main__':
	main()