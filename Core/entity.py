from Core.room import *
from Core.inventory import *
import sys

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
        self.dead = False
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

    def update(self): #Runs everytime the player executes a gameplay-impacting command
        pass

    def damage(self, dmg):
        self.sethp(self.hp - dmg)
    def heal(self, heal):
        if self.hp < self.maxhp:
            self.sethp(self.hp + heal)
            return True
        else:
            return False
    def sethp(self, hp):
        self.hp = min(self.maxhp, hp)
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.hp = 0
        self.remove()
        self.dead = True
        if self.player:
            print("You died!")
            sys.exit()
    
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
    def __init__(self, name, description, hp, hunger:float, thirst:float):
        super().__init__(name, description, hp)
        self.speciesname = "Alive"
        self.index = "alive"
        self.hunger = hunger
        self.thirst = thirst
        self.maxhunger = hunger
        self.maxthirst = thirst
    
    def desatiate(self, amount):
        self.sethunger(self.hunger - amount)
    def satiate(self, amount):
        if self.hunger < self.maxhunger:
            self.sethunger(self.hunger + amount)
            return True
        else:
            return False
    def sethunger(self, amount):
        self.hunger = min(self.maxhunger, amount)
        if self.hunger <= 0:
            self.hunger = 0
            self.damage(10)
            if self.player:
                print("You feel very hungry.")
    
    def dehydrate(self, amount):
        self.setthirst(self.thirst - amount)
    def hydrate(self, amount):
        if self.thirst < self.maxthirst:
            self.setthirst(self.thirst + amount)
            return True
        else:
            return False
    def setthirst(self, amount):
        self.thirst = min(self.maxthirst, amount)
        if self.thirst <= 0:
            self.thirst = 0
            self.damage(20)
            if self.player:
                print("You feel very thirsty.")
    
    def update(self): #Runs everytime the player executes a gameplay-impacting command
        self.desatiate(1)
        self.dehydrate(2)

        return super().update()

    def __str__(self):
        output = super().__str__()+f"\nHunger : {self.hunger}/{self.maxhunger}\nThirst : {self.thirst}/{self.maxthirst}"
        if self.hunger < 1 and self.thirst < 1:
            output += f"\n{self.getPronoun(3,False)} starving and thirsting"
        elif self.hunger < 1:
            output += f"\n{self.getPronoun(3,False)} starving"
        elif self.thirst < 1:
            output += f"\n{self.getPronoun(3,False)} thirsting"
        return output

class Human(Alive):
    def __init__(self, name, description):
        super().__init__(name, description, 100, 100, 100)
        self.speciesname = "Human"
        self.inv = Inventory(self.name + "'s inventory",15)
        self.index = "human"
    
    def __str__(self):
        return super().__str__()