#region Init
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
apple.count = 23
apple.addToRoom(mainroom)

coin = Coin()
coin.count = 54
coin.addToRoom(secondroom)

def update():
    for entity in player.currentroom.entities:
        entity.update()
    for item in player.currentroom.items:
        item.update()

if __name__ == "__main__":
    command_interpreter_loop(commands) # type: ignore