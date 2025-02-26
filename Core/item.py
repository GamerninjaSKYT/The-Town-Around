from Core.room import *
from Core.entity import *
import math as m
import copy

class Item:
    def __init__(self, name: str, 
                 description: str,
                 size: float,
                 cantake: bool = True,
                 stackable: bool = False,):
        self.name = name
        self.description = description
        self.currentroom:Room = None
        self.currentinv:Inventory = None
        self.currentequip:Entity = None #Which entity (if any) has this item currently equipped
        self.size = size
        self.cantake = cantake
        self.stackable = stackable
        self.count = 1
        self.index = "item"
    
    def canStack(self, other:"Item"):
        return (self.index == other.index and 
                self.name == other.name)

    def addToRoom(self, target:Room, numOfItems = 0): #Moves the item from its current room to the target room
        if self.currentroom == target:
            return
        if numOfItems == 0 or numOfItems > self.count:
            numOfItems = self.count
        if self.stackable == False:
            self.remove()
            self.currentroom = target
            self.currentroom.items.append(self)
            return
        else:
            for i in target.items:
                if self.canStack(i):
                    i.count += numOfItems
                    self.count -= numOfItems
                    if self.currentinv:
                        self.currentinv.totalsize -= numOfItems*self.size
                    numOfItems = 0
                    if self.count < 1:
                        self.remove()
                        return
                    break
            if numOfItems:
                stackcopy = copy.deepcopy(self)
                stackcopy.clear_location_vars() #The copy is not in any inventory but it copied currentinv so it thinks it is
                stackcopy.currentroom = target
                target.items.append(stackcopy)
                stackcopy.count = numOfItems
                self.count -= numOfItems
                if self.currentinv:
                        self.currentinv.totalsize -= numOfItems*self.size
                if self.count < 1:
                    self.remove()
                return

    def removeFromCurrentroom(self): #Removes the item from its current room
        if self.currentroom:
            self.currentroom.items.remove(self)
            self.currentroom = None
    def removeFromRoom(self, target:Room): #Removes the item from the room if it´s in it
        if target == self.currentroom:
            self.removeFromCurrentroom()
    def addToInv(self, target:Inventory, numOfItems = 0):
        if self.cantake == False:
            return False
        if self.currentinv == target:
            return True
        if numOfItems == 0 or numOfItems > self.count:
            numOfItems = self.count
        if self.stackable == False:
            if target.totalsize + self.size > target.maxsize:
                return False
            self.remove()
            self.currentinv = target
            self.currentinv.content.append(self)
            self.currentinv.totalsize += self.size
            return True
        else:
            if self.size > 0:
                canAdd = min(m.floor((target.maxsize-target.totalsize)/self.size), numOfItems)
            else:
                canAdd = numOfItems
            if canAdd < 1:
                return False
            for i in target.content:
                if self.canStack(i):
                    i.count += canAdd
                    target.totalsize += canAdd*self.size
                    self.count -= canAdd
                    if self.currentinv:
                        self.currentinv.totalsize -= canAdd*self.size
                    canAdd = 0
                    if self.count < 1:
                        self.remove()
                        return True
                    break
            if canAdd:
                stackcopy = copy.deepcopy(self)
                stackcopy.clear_location_vars() #The copy is not in any room but it copied currentroom so it thinks it is
                stackcopy.currentinv = target
                target.content.append(stackcopy)
                stackcopy.count = canAdd
                target.totalsize += canAdd*self.size
                self.count -= canAdd
                if self.currentinv:
                        self.currentinv.totalsize -= canAdd*self.size
                if self.count < 1:
                    self.remove()
                return True
            else:
                return False

    def equipTo(self, target:Entity):
        if target.equiped:
            target.equiped.unequip()
        target.equiped = self
        self.currentequip = target
    def unequip(self):
        if self.currentequip == None:
            return
        self.currentequip.equiped = None
        self.currentequip = None

    def removeFromCurrentinv(self):
        if self.currentinv:
            self.currentinv.content.remove(self)
            self.currentinv.totalsize -= self.size*self.count
            self.currentinv = None
    def removeFromInv(self, target:Inventory):
        if target == self.currentinv:
            self.removeFromCurrentinv()

    def remove(self): #Removes this item from the world
        self.removeFromCurrentroom()
        self.removeFromCurrentinv()
        self.unequip()
    def clear_location_vars(self): #Sets currentinv/currentroom to None but doesnt affect the room/inv itself
        self.currentinv = None
        self.currentroom = None
        self.currentequip = None

    def use(self, user: Entity):
        if user.player:
            print(f"{self.name} has no use.")
    
    def __str__(self):
        output = f"{self.getItemHeader()}: {self.description}"
        return output
    
    def getItemHeader(self):
        countstr = ""
        if self.canStack:
            countstr = f"({self.count})"
        return f"{self.name}{countstr} [Weight : {self.size * self.count}]"

class Food(Item):
    def __init__(self, name, description, size, heal, stackable):
        super().__init__(name, description, size, True, stackable)
        self.index = "food"
        self.heal = heal
        self.consumeverb = "eat"
    
    def use(self, user):
        if not isinstance(user, Alive): #Only entities inherited from the Alive class need to eat
            if user.player:
                print(f"You don't seem to have the need to {self.consumeverb}")
            return
        start_hp = user.hp
        if user.heal(self.heal):
            if user.player:
                print(f"You {self.consumeverb} {self.name} and heal {user.hp - start_hp}HP")
            self.count -= 1
            if self.count < 1:
                self.remove()
        elif user.player:
            print("You already have full health")
    
    def __str__(self):
        return super().__str__()+f"\nHeals {self.heal}HP."

class Apple(Food):
    def __init__(self):
        super().__init__("Apple", "A juicy apple", 1, 5, True)
        self.index = "apple"

class Coin(Item):
    def __init__(self):
        super().__init__("Coin", "A small golden coin", 0, True, True)
        self.currency = 1
    
    def __str__(self):
        return super().__str__()+f"\nWorth {self.currency} currency."