#region Init
from Core import *
import shlex
import sys
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
apple.count = 23
apple.addToRoom(mainroom)

coin = Coin()
coin.count = 54
coin.addToRoom(secondroom)

def update(): #Runs everytime the player executes a gameplay-impacting command
    for entity in player.currentroom.entities:
        entity.update()
    for item in player.currentroom.items:
        item.update()

#region CommandFuncs
def exit_program(args):
    print(">>Exiting<<")
    sys.exit()

def help_command(args):
    seen_functions = set()
    unique_commands = []
    
    if not args:
        for cmd, var in commands.items():
            if var[0] not in seen_functions:
                seen_functions.add(var[0])
                unique_commands.append(cmd)
        print("Available commands:\n", "\n ".join(unique_commands))
    else:
        targetname = args[0]
        for cmd, var in commands.items():
            if cmd == targetname and len(var) > 1:
                print(var[1])
            elif cmd == targetname:
                print("This command has no help text.")
            if cmd == targetname:
                aliases = []
                for cmd2, var2 in commands.items():
                    if var2[0] == var[0] and cmd2 != cmd:
                        aliases.append(cmd2)
                if len(aliases) > 0:
                    print("Aliases:\n", "\n ".join(aliases))
                return
        print("There's no command like that.")

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
        print(multi_word_name_notice("items or objects"))
        return
    targetname = args[0]
    target = None
    if player.inv.content:
        for i in player.inv.content:
            if targetname == i.name.lower():
                target = i
                break
    if player.currentroom.items and target == None:
        for i in player.currentroom.items:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        numOfItems = 1
        if len(args) > 1:
            if args[1].isnumeric():
                numOfItems = int(args[1])
                maxItems = 1000
                if numOfItems > maxItems:
                    print(f"{numOfItems} is above {maxItems}.")
                    return
            else:
                print(f"{args[1]} is not a valid number.")
                return
        for x in range(numOfItems):
            if target.use(player):
                update()
    else:
        print("There's nothing like that here.")

def take(args):
    if not args:
        print("You must specify an item to take.")
        print(multi_word_name_notice("items"))
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
        update()
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
        print(multi_word_name_notice("items"))
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
        update()
        target.addToRoom(player.currentroom, numOfItems)
        print(f"You drop {target.name}.")
    else:
        print("You have nothing like that.")

def dropall(args):
    dropped = 0
    if player.inv.content:
        dropped = player.inv.dropContents(player.currentroom)
    if dropped:
        update()
        print(f"You dropped {dropped} item(s).")
    else:
        print("You have nothing to drop.")

def go(args):
    if not args:
        print("You must specify a room to go to.")
        print(multi_word_name_notice("rooms"))
        return
    targetname = args[0]
    target = None
    if player.currentroom.exits:
        for i in player.currentroom.exits:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        update()
        player.addToRoom(target)
        print(f"You go to {target.name}.")
        print(target)
    else:
        print("You see no such room.")

def equip(args):
    if not args:
        print("You must specify an item to equip.")
        print(multi_word_name_notice("items"))
        return
    targetname = args[0]
    target = None
    if player.inv.content:
        for i in player.inv.content:
            if targetname == i.name.lower():
                target = i
                break
    if target:
        update()
        if target.equipTo(player):
            print(f"You equip {target.name}.")
        else:
            print(f"You already equipped {target.name}.")
    else:
        print("You have nothing like that.")

def unequip(args):
    if not player.equiped:
        print("You have nothing equipped to unequip.")
        return
    update()
    print(f"You unequip {player.equiped.name}")
    player.equiped.unequip()

#endregion
#region CommandList
exit_help = "Exits the game."
help_help = "Prints all the commands and prints the details of a command when its name is given as an argument."
look_help = "Prints info about the current room and prints info about items and entities when their name is given as an argument."
me_help = "Prints info about the player."
use_help = "Uses an item or object when its name is given as an argument, giving a second argument specifies how many times to use it."
inv_help = "Prints the player's inventory."
take_help = "Picks up an item from the current room when its name is given as an argument."
drop_help = "Drops an item from the inventory when its name is given as an argument."
dropall_help = "Drops all items from the inventory."
go_help = "Goes to a room when its name is given as an argument."
equip_help = "Equips an item when its name is given as an argument."
unequip_help = "Unequips an item when its name is given as an argument."

commands = { #COMMAND NAMES MUST BE LOWERCASE AND ALIASES NEVER GO FIRST
    "exit": [exit_program, exit_help],
    "quit": [exit_program, exit_help],

    "help": [help_command, help_help],

    "look": [look, look_help],
    "l" : [look, look_help],

    "me": [lookself, me_help],
    "self": [lookself, me_help],
    "lookme" : [lookself, me_help],
    "lookself" : [lookself, me_help],

    "use": [use, use_help],
    "u" : [use, use_help],

    "inv": [inv, inv_help],
    "i": [inv, inv_help],
    "inventory": [inv, inv_help],

    "take": [take, take_help],
    "t" : [take, take_help],
    "grab": [take, take_help],

    "drop": [drop, drop_help],
    "d" : [drop, drop_help],

    "dropall" : [dropall, dropall_help],
    "dropa": [dropall, dropall_help],

    "go" : [go, go_help],
    "g" : [go, go_help],

    "equip": [equip, equip_help],
    "e" : [equip, equip_help],

    "unequip" : [unequip, unequip_help],
    "une" : [unequip, unequip_help],
}
#endregion


def command_interpreter_loop(cmds):
    while True:
        try:
            user_input = shlex.split(input("$ ").lower().strip())
            if not user_input:
                continue
            command, *args = user_input
            if command in cmds:
                cmds[command][0](args)
            else:
                unknown_command(args)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    command_interpreter_loop(commands) # type: ignore