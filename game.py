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
apple.count = 21
apple.addToRoom(mainroom)

coin = Coin()
coin.count = 54
coin.addToRoom(secondroom)


if __name__ == "__main__":
    command_interpreter_loop(commands)