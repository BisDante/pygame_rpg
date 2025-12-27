class Actor:
    def __init__(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']
        self.level = attributes['level']
        self.hp = self.max_hp = attributes['max_hp']
        self.attack = attributes['attack']
        self.defense = attributes['defense']
        self.mana = self.max_mana = attributes['max_mana']
        self.intelligence = attributes['intelligence']
        self.willpower = attributes['willpower']
        self.speed = attributes['speed']
        self.agility = attributes['agility']
        self.accuracy = attributes['accuracy']
        self.luck = attributes['luck']

class PlayerCharacter(Actor):
    def __init__(self, attributes):
        super().__init__(attributes)
        self.hp = attributes['hp']
        self.mana = attributes['mana']