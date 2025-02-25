class Room:
    def __init__(self, name: str, 
                 description: str,):
        self.name = name
        self.description = description
        self.items = []
        self.entities = []
        self.exits = []
    
    def addTwoWay(self, other:"Room"):
        if other not in self.exits:
            self.exits.append(other)
        if self not in other.exits:
            other.exits.append(self)

    def __str__(self):
        output = f"{self.name}: {self.description}"
        if self.items:
            output += "\n\n-- You see the following items and objects: --"
            for i in self.items:
                output += "\n- " + i.getItemHeader()

        if self.entities:
            visible_entities = self.entities.copy()
            for x in visible_entities:
                if x.player:
                    visible_entities.remove(x)
            
            if visible_entities:
                output += "\n\n-- You see the following creatures: --"
                for i in visible_entities:
                    output += f"\n- {i.getNameAndSpecies()}"
        
        if self.exits:
            output += "\n\n-- You see the following exits: --"
            for i in self.exits:
                output += "\n- " + i.name
        return output