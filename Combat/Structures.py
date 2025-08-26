import Roll_Dice as Rd
from Error_t import get_integer
#NPC creation
class Npc:
    def __init__(self, name: str = '', pv_dices:'' = '', ini_modifier: int = 0):
        self.name = name
        self.is_npc = True
        self.pv_dices = pv_dices
        self.pv = Rd.code_roll(self.pv_dices)
        self.alive = True
        self.ini_modifier = ini_modifier
        self.initiative = self.roll_initiative()

    def take_damage(self):
        damage = get_integer('How many damage?')
        self.pv -= damage
        if self.pv < 0:
            print(f'{self.name} is dead!')
            self.alive = False
    
    def roll_initiative(self):
        initiative = (Rd.code_roll(f'1d20'))
        if initiative == 20:
            return 0
        elif initiative == 1:
            return 1
        return initiative + self.ini_modifier

#Player creation
class Pc:
    def __init__(self, name: str = ''):
        self.name = name
        self.is_npc = False
        self.initiative = 0

    def roll_for_initiative(self):
        self.initiative += get_integer(f"{self.name}'s initiative roll: ")

