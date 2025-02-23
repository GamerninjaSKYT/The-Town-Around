from Core.room import *
from Core.entity import *

class Item:
    def __init__(self, name: str, 
                 description: str,
                 size: float,
                 cantake: bool = True,):
        self.name = name
        self.description = description
        self.currentroom:Room = None
        self.currentinv:Inventory = None
        self.size = size
        self.cantake = cantake
        self.index = "item"
    
    def addToRoom(self, target:Room): #Moves the item from its current room to the target room
        if self.currentroom != target:
            self.remove()
            self.currentroom = target
            self.currentroom.items.append(self)
    def removeFromCurrentroom(self): #Removes the item from its current room
        if self.currentroom:
            self.currentroom.items.remove(self)
            self.currentroom = None
    def removeFromRoom(self, target:Room): #Removes the item from the room if it´s in it
        if target == self.currentroom:
            self.removeFromCurrentroom()
    def addToInv(self, target:Inventory):
        if self.currentinv == target:
            return True
        if target.totalsize + self.size > target.maxsize or self.cantake == False:
            return False
        self.remove()
        self.currentinv = target
        self.currentinv.content.append(self)
        self.currentinv.totalsize += self.size
        return True
    def removeFromCurrentinv(self):
        if self.currentinv:
            self.currentinv.content.remove(self)
            self.currentinv.totalsize -= self.size
            self.currentinv = None
    def removeFromInv(self, target:Inventory):
        if target == self.currentinv:
            self.removeFromCurrentinv()

    def remove(self): #Removes this item from the world
        self.removeFromCurrentroom()
        self.removeFromCurrentinv()

    def use(self, user: Entity):
        if user.player:
            print(f"{self.name} has no use.")
    
    def __str__(self):
        return f"{self.name}: {self.description}"

class Food(Item):
    def __init__(self, name, description, size, heal):
        super().__init__(name, description, size, True)
        self.index = "food"
        self.heal = heal
    
    def use(self, user):
        start_hp = user.hp
        if user.heal(self.heal):
            if user.player:
                print(f"You eat {self.name} and heal by {user.hp - start_hp}HP")
            self.remove()
        elif user.player:
            print("You already have full health")
    
    def __str__(self):
        return super().__str__()+f"\nHeals {self.heal}HP"

class Apple(Food):
    def __init__(self):
        super().__init__("Apple", "A juicy apple", 1, 5)
        self.index = "apple"