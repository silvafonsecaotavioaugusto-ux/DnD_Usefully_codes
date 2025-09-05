#importation of usefully Modules
import pandas as pd
from Error_t import get_integer
from Structures import Npc, Pc
from Text_op import print_line, space

#Manualy create NPCs
def npc_list():
    npc_s = []
    print_line(double= True)
    n = get_integer('Number of NPCs: ')
    for i in range(n):
        npc_s.append(Npc(input("NPC's name: "), input("NPC's pv dices: "), get_integer(f"NPC's initiative modifier: ")))
    return npc_s

#Import NPCs
def import_npc(path: str):
    df = pd.read_csv(path)
    names = df['name'].tolist()
    pv_dices = df['pv_dice'].tolist()
    initiative_modifiers = df['initiative_modifier'].tolist()
    duble_turn = df['duble_turn'].tolist()
    npc_s = []
    for i in range(len(names)):
        npc_s.append(Npc(names[i], str(pv_dices[i]), initiative_modifiers[i], duble_turn[i]))
    return npc_s

#Manualy create PCs
def pc_list():
    pcs = []
    print_line(double= True)
    n = get_integer("Number of Player's: ")
    for i in range(n):
        pcs.append(Pc(input("PC's Name: "),))
    print_line(double= True)
    return pcs

#Import PCs
def import_pcs(path):
    df = pd.read_csv(path)
    names = df['name'].tolist()
    pcs = []
    for name in names:
        pcs.append(Pc(name))
    return pcs

#Roll for Initiative!!!!!!
def pc_roll(pcs):
    for pc in pcs:
        pc.roll_for_initiative()
    return pcs

#NPCs must take damage!
def life_edit(creature_list:list, target: str, damage: int):
    for item in creature_list:
        if item.name == target:
            item.take_damage(damage)
    for idx in range(len(creature_list)-1, -1, -1):
        if not creature_list[idx].alive:
            creature_list.pop(idx)
    return creature_list

#organise by initiative
def organize_by_initiative(npc_list_1: list, pc_list_1: list):
    initiative_list = []
    initiative_numbers = []
    print_line()
    print('Organizing by initiative...')
    print_line()
    #cria uma lista de listas que representa todas as iniciativas possíveis
    for i in range(40):
        initiative_numbers.append([])

    #designa cada pc à sua posição adequada
    for pc in pc_list_1:
        initiative_numbers[pc.initiative-1].append(pc)
    #designa cada npc à sua posição adequada
    for npc in npc_list_1:
        initiative_numbers[npc.initiative-1].append(npc)
        if npc.duble_turn:
            initiative_numbers[npc.second_initiative-1].append(npc)
    #concatena todas as iniciativas em ordem decrecente
    for i in range(len(initiative_numbers)):
        initiative_list += initiative_numbers[len(initiative_numbers)-i-1]
    return initiative_list

#define one turn of a specific creature
def turn(creature, creature_list: list):
                
    print(f"{creature.name}'s turn!")
    if creature.is_npc: #NPC's turn
        print(f"Actual HP:{creature.pv}.")
    n_targets = get_integer(f"Number of targets: ")
    for i in range(n_targets):
        target = str(input("Which creature would you like to target? " \
        "")).strip()
        damage = get_integer('How much damage? ')
        creature_list = life_edit(creature_list, target, damage)
    return creature_list

#define 6 seconds of combat
def combat(creature_list: list,n:int):
    print(f'Turn {n}')
    for creature in creature_list:
        creature_list = turn(creature, creature_list)
    return creature_list

#show creatures for visualization
def show_creatures(creature_list: list):
    for creature in creature_list:
        if creature.is_npc:
            if creature.alive:
                print(f"{creature.name}:{creature.pv}PV")
            else:
                print(f"{creature.name}:Dead")

#show npc's initiatives
def show_initiatives(npcs: list):
    print_line()
    str1, str2 = 'Name', 'Initiative'

    print(f'{str1:^15}:{str2:^15}')
    for npc in npcs:
        if npc.duble_turn:
            print(f"{npc.name:^15}:{npc.initiative:^6} e {npc.second_initiative:^6}")
        else:
            print(f"{npc.name:^15}:{npc.initiative:^15}")

def main():
    print("'end' to finish the combat")
    print("'add player' to add player")
    print("'add npc' to add npc")
    print("In initiative fase, 0 means a critical success and 1 means a critical fail")
    player = []
    npc = []
    op = get_integer("""
Choose an option:
1 - São Paulo
2 - Araçatuba
3 - Personalizado
""")
    if op == 2:
        player = pc_roll(import_pcs('Combat\\araçatuba_players.CSV'))
    elif op == 1:
        player = pc_roll(import_pcs('Combat\\são_paulo_players.CSV'))
    elif op == 3:
        player = pc_roll(pc_list())
    op = get_integer("""
Choose an option:
1 - Encontro Personalizado
2 - Encontro Preparado
""")
    
    if op == 1:
        npc = npc_list()
    elif op == 2:
        npc = import_npc("Combat\\npcs.CSV")
    show_initiatives(npc)
    creature_list = organize_by_initiative(npc, player)
    n = 0
    while True:
        n += 1
        creature_list = combat(creature_list, n)
        op = input("Press any key to go next turn: ")
        if op == "show":
            show_creatures(creature_list)
            op = input("Press any key to go next turn: ")
        if op == "end":
            break
        if op == "add npc":
            o = get_integer("""
Choose an option:
1 - Encontro Personalizado
2 - Encontro Preparado
""")
            if o == 1:
                new_npc = npc_list()
            elif o ==  2:
                new_npc = import_npc('Combat\\npcs1.CSV')
            show_initiatives(new_npc)
            creature_list = organize_by_initiative(creature_list, new_npc)
        if op == "add player":
            new_players = pc_roll(pc_list())
            creature_list = organize_by_initiative(creature_list, new_players)

main()