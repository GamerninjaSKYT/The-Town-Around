from Core.room import *
from Core.inventory import *

class Entity:
    def __init__(self, name: str, 
                 description: str,
                 hp: float,):
        self.name = name
        self.speciesname = "Entity"
        self.description = description
        self.hp = hp
        self.maxhp = hp
        self.currentroom:Room = None
        self.player = False
        self.inv = None
        self.index = "entity"
    
    def addToRoom(self, target:Room): #Moves the creature from its current room to the target room
        if self.currentroom != target:
            self.remove()
            self.currentroom = target
            self.currentroom.entities.append(self)
    def removeFromCurrentroom(self): #Removes the creature from its current room
        if self.currentroom:
            self.currentroom.entities.remove(self)
            self.currentroom = None
    def removeFromRoom(self, target:Room): #Removes the creature from the room if it´s in it
        if target == self.currentroom:
            self.removeFromCurrentroom()

    def damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()
    
    def heal(self, heal):
        if self.hp < self.maxhp:
            self.hp = min(self.maxhp, self.hp + heal)
            return True
        else:
            return False
    
    def die(self):
        self.hp = 0
        self.remove()
    
    def remove(self): #Removes this entity from the world
        self.removeFromCurrentroom()
    
    def __str__(self):
        return f"[{self.hp}/{self.maxhp}HP] {self.getNameAndSpecies()}: {self.description}"

    def getNameAndSpecies(self):
        return f"{self.name} [{self.speciesname}]"

class Alive(Entity): #Entities that eat, drink and sleep should go here
    def __init__(self, name, description, hp):
        super().__init__(name, description, hp)
        self.speciesname = "Alive"
        self.index = "alive"

class Human(Alive):
    def __init__(self, name, description):
        super().__init__(name, description, 100)
        self.speciesname = "Human"
        self.inv = Inventory(self.name + "'s inventory",15)
        self.index = "human"