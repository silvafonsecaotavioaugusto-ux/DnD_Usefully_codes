import Roll_Dice as Rd
from Error_t import get_integer

#NPC creation
class Npc:
    def __init__(self, name: str = '', pv_dices: str = '', ini_modifier: int = 0, number_of_initiatives: int = 1, regeneration: int = 0):
        self.name = name
        self.is_npc = True
        self.pv_dices = pv_dices
        self.pv = Rd.code_roll(self.pv_dices)
        self.alive = True
        self.ini_modifier = ini_modifier
        self.number_of_initiatives = number_of_initiatives
        self.initiative = self.roll_initiative()
        self.it_regen = True if regeneration != 0 else False
        self.regeneration = regeneration

    def regen_pv(self):
        self.pv += self.regeneration
        print(f'{self.name} regenerated {self.regeneration}PV')


    def take_damage(self, damage: int):
        self.pv -= damage
        if self.pv < 0:
            self.alive = False
    
    def roll_initiative(self):
        initiatives = []
        for i in range(self.number_of_initiatives):
            initiative = (Rd.code_roll(f'1d20'))
            if initiative == 20: #critical success
                initiatives.append(0)
            elif initiative == 1: #critical failure
                initiatives.append(1)
            else:
                initiatives.append(initiative + self.ini_modifier)
        return initiatives

#Player creation
class Pc:
    def __init__(self, name: str = ''):
        self.name = name
        self.is_npc = False
        self.initiative = 0

    def roll_for_initiative(self):
        self.initiative += get_integer(f"{self.name}'s initiative roll: ")
