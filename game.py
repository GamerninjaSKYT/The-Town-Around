#region Init
import sys
import shlex
from Core import *
#endregion

mainroom = Room("Main Room","It's the main room!")
secondroom = Room("Second Room","It's newer and seconder!")
mainroom.addTwoWay(secondroom)

#Initialize player
player = Human("Player","Just some random person")
player.player = True
player.inv.name = "Your inventory"
player.addToRoom(mainroom)

apple = Apple()
apple.count = 21
apple.addToRoom(mainroom)

#region CommandList
def exit_program(args):
    print(">>Exiting<<")
    sys.exit()

def help_command(args):
    seen_functions = set()
    unique_commands = []
    
    for cmd, func in commands.items():
        if func not in seen_functions:
            seen_functions.add(func)
            unique_commands.append(cmd)

    print("Available commands:\n", "\n ".join(unique_commands))

def unknown_command(args):
    print("Unknown command. Type 'help' for a list of commands.")

def look(args):
    if not args:
        print(player.currentroom)
        return
    targetname = args[0]
    target = None
    if player.currentroom.items:
        for i in player.currentroom.items:
            if targetname == i.name.lower():
                target = i
                break
    if player.currentroom.entities and target == None:
        for i in player.currentroom.entities:
            if targetname == i.name.lower():
                target = i
                break
    if player.inv.content and target == None:
        for i in player.inv.content:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        print(target)
    else:
        print("There's nothing like that here.")

def lookself(args):
    print(player)

def inv(args):
    print(player.inv)

def use(args):
    if not args:
        print("You must specify an item or object to use.")
        print('Names of items longer than 1 word need to be in "" marks')
        return
    targetname = args[0]
    target = None
    if player.currentroom.items:
        for i in player.currentroom.items:
            if targetname == i.name.lower():
                target = i
                break
    if player.inv.content and target == None:
        for i in player.inv.content:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        target.use(player)
    else:
        print("There's nothing like that here.")

def take(args):
    if not args:
        print("You must specify an item to take.")
        print('Names of items longer than 1 word need to be in "" marks')
        return
    targetname = args[0]
    target = None
    if player.currentroom.items:
        for i in player.currentroom.items:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        numOfItems = target.count
        if len(args) > 1:
            if args[1].isnumeric():
                numOfItems = int(args[1])
            else:
                print(f"{args[1]} is not a valid number.")
                return
        if target.addToInv(player.inv, numOfItems):
            print(f"You take {target.name}.")
        elif target.cantake == False:
            print(f"You cannot take {target.name}")
        elif player.inv.totalsize < player.inv.maxsize:
            print(f"{target.name} is too big to fit in {player.inv.name}.")
        else:
            print(f"{player.inv.name} is full.")
    else:
        print("There's nothing like that here.")

def drop(args):
    if not args:
        print("You must specify an item to drop.")
        print('Names of items longer than 1 word need to be in "" marks')
        return
    targetname = args[0]
    target = None
    if player.inv.content:
        for i in player.inv.content:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        numOfItems = target.count
        if len(args) > 1:
            if args[1].isnumeric():
                numOfItems = int(args[1])
            else:
                print(f"{args[1]} is not a valid number.")
                return
        target.addToRoom(player.currentroom, numOfItems)
        print(f"You drop {target.name}.")
    else:
        print("You have nothing like that.")

def dropall(args):
    dropped = 0
    if player.inv.content:
        dropped = player.inv.dropContents(player.currentroom)
    if dropped:
        print(f"You dropped {dropped} item(s).")
    else:
        print("You have nothing to drop.")

def go(args):
    if not args:
        print("You must specify a room to go to.")
        print('Names of rooms longer than 1 word need to be in "" marks')
        return
    targetname = args[0]
    target = None
    if player.currentroom.exits:
        for i in player.currentroom.exits:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        player.addToRoom(target)
        print(f"You go to {target.name}.")
    else:
        print("You see no such room.")

#endregion
commands = { #COMMAND NAMES MUST BE LOWERCASE
    "exit": exit_program,
    "quit": exit_program,

    "help": help_command,

    "look": look,
    "l" : look,

    "me": lookself,
    "self": lookself,
    "lookme" : lookself,
    "lookself" : lookself,

    "use": use,
    "u" : use,

    "inv": inv,
    "i": inv,
    "inventory": inv,

    "take": take,
    "grab": take,

    "drop": drop,

    "dropall" : dropall,
    "dropa": dropall,

    "go" : go,
    "g" : go,
}

def command_interpreter_loop(cmds):
    while True:
        try:
            user_input = shlex.split(input("$ ").lower().strip())
            if not user_input:
                continue
            command, *args = user_input
            cmds.get(command, unknown_command)(args)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    command_interpreter_loop(commands)