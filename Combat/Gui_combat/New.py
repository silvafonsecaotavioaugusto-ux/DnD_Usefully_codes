"""This notebook will be used to write the GUI_Combat.py from scratch"""
# Importing Libraries
import os
import sys
import random
from typing import List
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPalette, QBrush, QPixmap

#------------------------Modelos------------------------
# Note que os modelos originais já eram de minha altoria

class Creature:
    def __init__(self, 
                 name: str , 
                 pv: int = 0, 
                 is_npc: bool = True):
        self.name = name
        self.max_pv = pv
        self.pv = pv
        self.is_npc = is_npc
        self.alive = True
        self.initiative = []
        self.it_regen = False
        self.regen_rate = 0
        self.pdf_path = ''

    def take_damage(self, damage: int):
        
        #Only Npc Take Damage
        if not self.is_npc:
            return
        
        #Aply Damage
        if self.alive:
            self.pv -= damage
        
        #Kill if pv <= 0
        if self.pv <= 0:
            self.pv = 0
            self.alive = False

    def regen_pv(self):
        #Only Npc Regen
        if not self.is_npc:
            return

        #Regen
        if self.alive:
            if self.it_regen and self.regen_rate > 0:
                self.pv = min(self.max_pv, self.pv + self.regen_rate) # impede que o pv passe do máximo

    def roll_for_initiative(self, n_rolls: int = 1, mod: int = 0):
        if not self.is_npc:
            return
        rolls = []
        for _ in range(n_rolls):
            r = random.randint(1, 20)
            if r == 1 or r == 20:
                r = (r - 10)*10 
                # se 1 r == -90 e se 20 r == 100, logo val será 1 ou 40
            val = max(1, min(40, r + mod))
            rolls.append(val)
        self.initiative = sorted(rolls, reverse= True)

    def show_sheet_text(self) -> str:
        if self.is_npc:
            return f"NPC: {self.name} - PV: {self.pv}/{self.max_pv} - Init: {self.initiative}"
        return f"PC: {self.name} -  Init: {self.initiative}"
    
    def show_sheet(self):
        pass

# a classe creature define a base das nossas classes principais. Perceba que várias funções não são aproveitadas pelos PC

class Npc(Creature):
    def __init__(self,
                 name: str,
                 pv_dices: str = '1d8',
                 init_modifier: int = 0,
                 n_initiatives: int = 1,
                 regen_rate: int = 0,
                 pdf_path: str = '',
                 pdf_page: int = 0):
        pv = code_roll(pv_dices)
        super().__init__(name, pv, is_npc=True)
        self.pv_dice = pv_dices
        self.init_mod = init_modifier
        self.n_inits = n_initiatives
        self.regen_rate = regen_rate
        self.it_regen = regen_rate > 0
        self.pdf_path = pdf_path
        self.pdf_page = pdf_page

    def roll_for_initiative(self):
        super().roll_for_initiative(n_rolls=self.n_inits, mod=self.init_mod)

    def show_npc_sheet(self) -> str:
        return self.show_sheet_text()


class Pc(Creature):
    def __init__(self,
                 name: str,
                 pdf_path: str = ''):
        super().__init__(name, is_npc= False)
        self.pdf_path = pdf_path
        self.initiative = 1



#----------------------Funções Úteis-----------------------

def code_roll(pv_dices: str = '0'):
    """
    Docstring for code_roll
    
    :param pv_dices: String with the forma "AdB+C" A is the number of dices, B is the size and C the modifier
    :type pv_dices: str
    """
    s = str(pv_dices).strip().lower()
    if s.isdigit():
        return int(s)
    try:
        # ex: '2d6+3' ou 'd8' ou '3d4'
        total = 0
        if 'd' in s:
            left, *right = s.split('d')
            n = int(left) if left else 1
            if '+' in right[0]:
                m_part, k_part = right[0].split('+', 1)
                m = int(m_part)
                k = int(k_part)
            elif '-' in right[0]:
                m_part, k_part = right[0].split('-', 1)
                m = int(m_part)
                k = -int(k_part)
            else:
                m = int(right[0])
                k = 0
            for _ in range(n):
                total += random.randint(1, m)
            total += k
            return max(1, total)
    except Exception:
        pass
    # fallback
    return 10


def unique(_creatures: list)-> list:
    s_creatures = []
    for i in _creatures:
        if not i in s_creatures:
            s_creatures.append(i)
    return s_creatures    

def search_bacround_path()-> str:
    base = os.path.dirname(os.path.abspath(__file__))

    if getattr(sys, 'frozen', False):
        background_path = os.path.join(base,"..", "figures", "background.jpeg")
    else:
        background_path = os.path.join(base, "figures", "background.jpeg")
    
    background_path = os.path.abspath(background_path)  # normaliza
    return background_path


# -----------------------Gui------------------------
class CombatWindow(QtWidgets.QMainWindow): #Cria a janela
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D Combat with Python") #Define um titulo
        self.showMaximized() #Define o Tamanho da janela (tela cheia sem cobrir icones e barra de tarefa)

        # Determina o caminho para a imagem de fundo (sempre deve estar em uma pasta adjacente à do executável)
        img_p = search_bacround_path()
        o_fundo = QPixmap(img_p) #abre a imagem 
        palette = QPalette() #cria um fundo
        palette.setBrush(QPalette.Window, QBrush(o_fundo)) #Transforma o fundo na imagem
        self.setPalette(palette) #aplica o fundo

        # Definimos nossas estruturas importantes, como lista de npcs
        # lista de pcs, lista de criaturas, número do round e número do turno
        self.pcs: List[Pc] = []  # lista não organizada de personagens jogaveis
        self.npcs: List[Npc] = []  # lista não organizada de personagens do mestre
        self.creature_list: List[Creature] = []  # lista ordenada por iniciativa
        self.turn_index = 0  # determina qual jogador jogará agora
        self.round_number = 1  # determina o número do turno atual, a fim de se organizar quanto a duração de magias e efeitos

        #CSV's devem ficar no mesmo diretório que o executável, assim não há necessidade de procurar os documentos
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0])) + r'\dist'


        # Criamos os layouts da nossa interface gráfica
        """
 _______________________________________
|_______|_______|_______|_______|_______|-> top
|               |       |               |
|               |       |               |
|               |       |               |
|               |_______|               |
|               |_______|_______________|-> midle
|               |_______|_______________|
|               |_______|_______________|
|_______________|_______|_______________|
|_______________________________________|-> boton
  Creature list  funcions  combat whindow
"""
        
        # Widget Central/Principal
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # top
        top_roll = QtWidgets.QHBoxLayout()
        layout.addLayout(top_roll)

            #botão de importar players + atalho
        btn_import_players = QtWidgets.QPushButton("Importar PC's")
        btn_import_players.clicked.connect(self.importpcs)
        top_roll.addWidget(btn_import_players)

        import_players_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+P"), self)
        import_players_shortcut.activated.connect(self.importpcs)

            #botão de importar npcs + atalho
        btn_import_npcs = QtWidgets.QPushButton("Importar NPC's")
        btn_import_npcs.clicked.connect(self.importnpcs)
        top_roll.addWidget(btn_import_npcs)

        import_npcs_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+N"), self)
        import_npcs_shortcut.activated.connect(self.importnpcs)

            #botão de adicionar player
        btn_add_player = QtWidgets.QPushButton("Adicionar PC's")
        btn_add_player.clicked.connect(self.addplayer)
        top_roll.addWidget(btn_add_player)

            #botão de adicionar npcs
        btn_add_npc = QtWidgets.QPushButton("Adicionar NPC's")
        btn_add_npc.clicked.connect(self.addnpc)
        top_roll.addWidget(btn_add_npc)

            #botão de rolar iniciaitvas + atalho
        btn_roll_for_initiative = QtWidgets.QPushButton("Roll for Initiative!")
        btn_roll_for_initiative.clicked.connect(self.rollforinitiative)
        top_roll.addWidget(btn_roll_for_initiative)

        roll_for_initiative_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        roll_for_initiative_shortcut.activated.connect(self.rollforinitiative)

        # Middle

        middle = QtWidgets.QHBoxLayout()
        layout.addLayout(middle)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        middle.addWidget(self.list_widget, 3)

        right_panel = QtWidgets.QVBoxLayout()
        middle.addLayout(right_panel, 2)

        self.sheet = QtWidgets.QLabel()
        self.sheet.setScaledContents(True)
        right_panel.addWidget(self.sheet)

        btn_show_sheet = QtWidgets.QPushButton('Mostrar ficha')
        btn_show_sheet.clicked.connect(self.showsheet)
        right_panel.addWidget(btn_show_sheet)

        btn_apply_damage = QtWidgets.QPushButton('Aplicar dano ao selecionado')
        btn_apply_damage.clicked.connect(self.applydamagetoselected)
        right_panel.addWidget(btn_apply_damage)

        btn_next_turn = QtWidgets.QPushButton('Avançar 1 turno')
        btn_next_turn.clicked.connect(self.nextturn)
        right_panel.addWidget(btn_next_turn)

        btn_show_creatures = QtWidgets.QPushButton('Mostrar criaturas (popup)')
        btn_show_creatures.clicked.connect(self.showcreaturespopup)
        right_panel.addWidget(btn_show_creatures)

        btn_end = QtWidgets.QPushButton('Encerrar combate')
        btn_end.clicked.connect(self.endcombat)
        right_panel.addWidget(btn_end)

        # turn panel
                # turn panel
        self.turn_panel = QtWidgets.QFrame()
        self.turn_panel.setStyleSheet("""
    background: white;
    border: 1px solid #888;
""")
        self.turn_layout = QtWidgets.QVBoxLayout(self.turn_panel)
        middle.addWidget(self.turn_panel, 2)

        # boton
        # status bar
        self.status = QtWidgets.QLabel('Pronto')
        self.statusBar().addWidget(self.status)
        self.statusBar().setStyleSheet("""
        QStatusBar {
                    background-color: white;
                    color: black;
                    border-top: 1px solid #888;
        }
        QStatusBar::item {
            border: 0px;     /* remove borda feia ao redor dos itens */
        }
""")




    # Funções do Código
    def importpcs(self):
        pass
    
    def importnpcs(self):
        pass

    def addplayer(self):
        pass        

    def addnpc(self):
        pass

    def rollforinitiative(self):
        pass

    def showsheet(self):
        pass

    def applydamagetoselected(self):
        pass

    def nextturn(self):
        pass

    def showcreaturespopup(self):
        pass

    def endcombat(self):
        pass
# ---------------------- Main ----------------------

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = CombatWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
