from Core.room import *

class Inventory:
    def __init__(self, name: str,
                 maxsize:float,):
        self.name = name
        self.maxsize = maxsize
        self.totalsize = 0
        self.content = []
    
    def dropContents(self, target:Room):
        dropped = 0
        for i in self.content:
            i.addToRoom(target)
            dropped += 1
        return dropped

    def __str__(self):
        output = f"{self.name} is empty\nWeight : [0/{self.maxsize}]"
        if self.content:
            output = f"-- {self.name} contains the following items: --\nWeight : [{self.totalsize}/{self.maxsize}]"
            for i in self.content:
                output += "\n- " + i.name
        return output