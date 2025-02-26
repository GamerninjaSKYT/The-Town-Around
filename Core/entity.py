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
        self.equiped = None #An item from self.inv
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
        output = f"[{self.hp}/{self.maxhp}HP] {self.getNameAndSpecies()}: {self.description}"
        if self.equiped:
            output += f"\n{self.getPronoun(3,False)} holding {self.equiped.name}"
        return output

    def getNameAndSpecies(self):
        return f"{self.name} [{self.speciesname}]"
    
    def getPronoun(self, case = 0, lowercase = True): #0 = subject(They), 1 = object(Them), 2 = possessive(Their), 3 = subject+verb(They're)
        if self.player:
            pronouns = ["You", "You", "Your", "You're"]
        else:
            pronouns = ["It", "It", "Its", "It's"]

        result = pronouns[case] if 0 <= case < len(pronouns) else "[Error: Invalid pronoun case]"
        return result.lower() if lowercase else result


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