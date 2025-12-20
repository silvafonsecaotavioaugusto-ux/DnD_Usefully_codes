"""Código com interface gráfica gerado a partir do script DnD_Batle_code
utilizando o auxílio do Chat GPT.
Estou utilizando este código para estudar e aprender sobre a biblioteca PyQt5."""

import os
import sys
import random
from typing import List
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPalette, QBrush, QPixmap
# ---------------------- Modelos (simplificados) ----------------------
class Creature:
    def __init__(self, name: str, pv: int = 10, is_npc: bool = True):
        self.name = name
        self.max_pv = pv
        self.pv = pv
        self.is_npc = is_npc
        self.alive = True
        self.initiative = []  # pode ter múltiplas iniciativas (para NPCs em enxame ou velozes)
        self.it_regen = False
        self.regen_rate = 0
        self.pdf_path = ''

    def take_damage(self, damage: int):
        if self.alive:
            self.pv -= damage

        if self.pv <= 0:
            self.pv = 0
            self.alive = False

    def regen_pv(self):
        if self.alive:
            if self.it_regen and self.regen_rate > 0:
                self.pv = min(self.max_pv, self.pv + self.regen_rate) # impede que o pv passe do máximo

    def roll_for_initiative(self, n_rolls: int = 1, mod: int = 0):
        # Para PCs normalmente n_rolls == 1 e retorna um inteiro (1-40 cap)
        rolls = []
        for _ in range(n_rolls):
            r = random.randint(1, 20)
            # Nota: no script original, 0 e 1 são crit; aqui mantemos 1..20
            val = max(1, min(40, r + mod))
            rolls.append(val)
        self.initiative = sorted(rolls, reverse= True)
        if not self.is_npc:
            # PCs armazenam apenas um valor (compatibilidade)
            self.initiative = rolls[0]

    def show_sheet_text(self) -> str:
        return f"{self.name} - PV: {self.pv}/{self.max_pv} - Init: {self.initiative}"
    
    def show_sheet(self):
        pass


class Npc(Creature):
    def __init__(self, name: str, pv_dice: str = '1d8', init_mod: int = 0, n_inits: int = 1, regen_rate: int = 0, pdf_path: str = '', pdf_page: int = 0):
        # pv_dice expected like '2d6+3' or simple int string
        pv = code_roll(pv_dice)
        super().__init__(name, pv, is_npc=True)
        self.pv_dice = pv_dice
        self.init_mod = init_mod
        self.n_inits = n_inits
        self.regen_rate = regen_rate
        self.it_regen = regen_rate > 0
        self.pdf_path = pdf_path
        self.pdf_page = pdf_page

    def roll_for_initiative(self):
        super().roll_for_initiative(n_rolls=self.n_inits, mod=self.init_mod)

    def show_npc_sheet(self) -> str:
        return self.show_sheet_text()


class Pc(Creature):
    def __init__(self, name: str, pv: int = 1, pdf_path: str = ''):
        super().__init__(name, pv, is_npc=False)
        self.initiative = 1
        self.pdf_path = pdf_path

# ---------------------- Utilitários ----------------------

def code_roll(s: str) -> int:
    """Parse simples do formato NdM+K ou número inteiro."""
    s = str(s).strip()
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
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
        background_path = os.path.join(base,"..", "figures", "background.jpeg")
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        background_path = os.path.join(base, "figures", "background.jpeg")
    
    background_path = os.path.abspath(background_path)  # normaliza
    return background_path

def search_nopicture_path()-> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
        nopicture_path = os.path.join(base,"..", "figures", "nopicture.png")
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        nopicture_path = os.path.join(base, "figures", "nopicture.png")
    
    nopicture_path = os.path.abspath(nopicture_path)  # normaliza
    return nopicture_path
# ---------------------- GUI ----------------------

class CombatWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Combat Manager - PyQt5')
        self.resize(1500, 600)

        # Imagem de Fundo
        img_p = search_bacround_path()
        o_fundo = QPixmap(img_p)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(o_fundo))
        

        # estado
        self.pcs: List[Pc] = []
        self.npcs: List[Npc] = []
        self.creature_list: List[Creature] = []  # lista ordenada por iniciativa
        self.turn_index = 0
        self.round_number = 1
                #CSV's devem ficar no mesmo diretório que o executável, assim não há necessidade de procurar os documentos
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0])) + r'\dist'
        self.nopicpath = search_nopicture_path()

        # widgets
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        central.setAutoFillBackground(True)
        central.setPalette(palette)
        layout = QtWidgets.QVBoxLayout(central)

        # Top controls
        top_row = QtWidgets.QHBoxLayout()
        layout.addLayout(top_row)

        btn_import_players = QtWidgets.QPushButton('Importar PCs (CSV)')
        btn_import_players.clicked.connect(self.import_pcs)
        top_row.addWidget(btn_import_players)

        btn_import_npcs = QtWidgets.QPushButton('Importar NPCs (CSV)')
        btn_import_npcs.clicked.connect(self.import_npcs)
        top_row.addWidget(btn_import_npcs)

        btn_add_pc = QtWidgets.QPushButton('Adicionar PC')
        btn_add_pc.clicked.connect(self.add_pc)
        top_row.addWidget(btn_add_pc)

        btn_add_npc = QtWidgets.QPushButton('Adicionar NPC')
        btn_add_npc.clicked.connect(self.add_npc)
        top_row.addWidget(btn_add_npc)

        btn_roll_init = QtWidgets.QPushButton('Rolar Iniciativas')
        btn_roll_init.clicked.connect(self.roll_initiatives)
        top_row.addWidget(btn_roll_init)

        # List view and details
        middle = QtWidgets.QHBoxLayout()
        layout.addLayout(middle)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        middle.addWidget(self.list_widget, 6)

        right_panel = QtWidgets.QVBoxLayout()
        middle.addLayout(right_panel, 4)

        self.sheet = QtWidgets.QLabel()
        size = QSize(300,400)
        self.sheet.setFixedSize(size)
        self.sheet.setScaledContents(True)
        right_panel.addWidget(self.sheet)

        btn_show_sheet = QtWidgets.QPushButton('Mostrar ficha')
        btn_show_sheet.clicked.connect(self.show_sheet)
        right_panel.addWidget(btn_show_sheet)

        btn_apply_damage = QtWidgets.QPushButton('Aplicar dano ao selecionado')
        btn_apply_damage.clicked.connect(self.apply_damage_to_selected)
        right_panel.addWidget(btn_apply_damage)

        btn_next_turn = QtWidgets.QPushButton('Avançar 1 turno')
        btn_next_turn.clicked.connect(self.next_turn)
        right_panel.addWidget(btn_next_turn)

        btn_show_creatures = QtWidgets.QPushButton('Mostrar criaturas (popup)')
        btn_show_creatures.clicked.connect(self.show_creatures_popup)
        right_panel.addWidget(btn_show_creatures)

        btn_end = QtWidgets.QPushButton('Encerrar combate')
        btn_end.clicked.connect(self.end_combat)
        right_panel.addWidget(btn_end)

        # turn panel
        self.turn_panel = QtWidgets.QFrame()
        self.turn_panel.setStyleSheet("""
    background: white;
    border: 1px solid #888;
""")
        self.turn_layout = QtWidgets.QVBoxLayout(self.turn_panel)
        middle.addWidget(self.turn_panel, 5)

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

        # atalho double-click para mostrar ficha
        self.list_widget.itemDoubleClicked.connect(self.show_sheet)

        # atalho ctrl-T para avançar turno
        atalho_turno = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+T"), self)
        atalho_turno.activated.connect(self.next_turn)

        # atalho ctrl-R para rolar iniciativa        
        atalho_roll_for_initiative = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        atalho_roll_for_initiative.activated.connect(self.roll_initiatives)

        #atalho ctrl-I para importar jogadores
        atalho_import = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+I"), self)
        atalho_import.activated.connect(self.import_pcs)

    # ---------- handlers ----------
    def import_pcs(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir CSV de PCs',
                                                        self.base_dir,
                                                         filter='CSV Files (*.csv);;All Files (*)')
        if not path:
            return
        try:
            df = pd.read_csv(path)
            names = df['name'].tolist()
            pdf_paths = df['pdf_path'].tolist()
            self.pcs = [Pc(name= n, pdf_path= p) for n, p in zip(names, pdf_paths)]
            self.status.setText(f'Importados {len(self.pcs)} PCs')
            self.refresh_list()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Falha ao importar PCs:\n{e}')

    def import_npcs(self):        
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir CSV de NPCs',
                                                        self.base_dir,
                                                        filter='CSV Files (*.csv);;All Files (*)')
        if not path:
            return
        try:
            df = pd.read_csv(path)
            names = df['name'].tolist()
            pv_dice = df['pv_dice'].tolist() if 'pv_dice' in df.columns else ["1d8"]*len(names)
            init_mod = df['initiative_modifier'].tolist() if 'initiative_modifier' in df.columns else [0]*len(names)
            n_inits = df['number_of_initiatives'].tolist() if 'number_of_initiatives' in df.columns else [1]*len(names)
            r_r = df['r_r'].tolist() if 'r_r' in df.columns else [0]*len(names)
            pdf_paths = df['pdf_path'].tolist() if 'pdf_path' in df.columns else ['']*len(names)
            pdf_pages = df['pdf_page'].tolist() if 'pdf_page' in df.columns else [0]*len(names)

            self.npcs = []
            for i, name in enumerate(names):
                npc = Npc(name, pv_dice[i], int(init_mod[i]), int(n_inits[i]), int(r_r[i]), pdf_paths[i], int(pdf_pages[i]))
                self.npcs.append(npc)
            self.status.setText(f'Importados {len(self.npcs)} NPCs')
            self.refresh_list()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Falha ao importar NPCs:\n{e}')

    def add_pc(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Adicionar PC', 'Nome do PC:')
        if ok and text.strip():
            pc = Pc(text.strip())
            self.pcs.append(pc)
            self.refresh_list()

    def add_npc(self):
        dlg = AddNpcDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            npc = Npc(data['name'], data['pv_dice'], data['init_mod'], data['n_inits'], data['regen_rate'])
            self.npcs.append(npc)
            self.refresh_list()

    def roll_initiatives(self):
        pcs = []
        for pc in self.pcs:
            pcs.append(pc)
        # Abrir janela para PCs
        if pcs:
            dlg = PcInitiativeDialog(pcs, self)
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                dlg.apply_results()

        # NPCs
        for npc in self.npcs:
            npc.roll_for_initiative()
        # organizar
        self.organize_by_initiative()
        self.status.setText('Iniciativas roladas e lista organizada')
        self.turn_index = 0
        self.turn_number = 0
        self.refresh_list()

    def organize_by_initiative(self):
        # base: iniciativas possíveis de 1 a 40
        bins = [[] for _ in range(40)]
        # pcs: iniciativa é único inteiro
        for pc in self.pcs:
            idx = max(1, min(40, int(pc.initiative))) - 1
            bins[idx].append(pc)
        # npcs: iniciativa é lista
        for npc in self.npcs:
            for i in npc.initiative:
                idx = max(1, min(40, int(i))) - 1
                bins[idx].append(npc)
        # concatena em ordem decrescente
        ordered = []
        for i in range(39, -1, -1):
            ordered += bins[i]
        self.creature_list = ordered

    def refresh_list(self):
        self.list_widget.clear()
        count_names = {}
        for idx, c in enumerate(self.creature_list):
            name = c.name
            if not name in count_names.keys():
                count_names[f'{name}'] = 0
            else:
                count_names[f'{name}'] += 1
            str1 = f"{idx+1:02d} - {name}"
            if c.is_npc:
                pv = f"{c.pv}/{c.max_pv}"
                ini = c.initiative[count_names[f'{name}']]
                str2 = f"| PV: {pv:<7} | Initiative: {ini:<2} |"
            else:
                str2 = f"| Initiative: {c.initiative:<2} |"
            item = QtWidgets.QListWidgetItem(f"{str1:<32}{str2:>32}")
            # store object
            item.setData(QtCore.Qt.UserRole, c)
            self.list_widget.addItem(item)
                # Fonte
        font = QtGui.QFont("Courier New")
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self.list_widget.setFont(font)


    def show_sheet(self):
        item = self.list_widget.currentItem()
        if not item:
            QtWidgets.QMessageBox.information(self, 'Info', 'Selecione uma criatura na lista')
            return
        c: Creature = item.data(QtCore.Qt.UserRole)
        path = str(c.pdf_path).strip()
        if path in ('', 'nan', 'None'):
            self.sheet.setPixmap(QtGui.QPixmap())  # limpa imagem anterior
            self.sheet.setText(c.show_sheet_text())     # aqui você coloca o sumário
        elif os.path.exists(path):
            pix = QtGui.QPixmap(path)
            self.sheet.setPixmap(pix)
        else:
            self.sheet.setPixmap(QtGui.QPixmap())
            self.sheet.setText("Path não encontrado!")

    def apply_damage_to_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            QtWidgets.QMessageBox.information(self, 'Info', 'Selecione uma criatura na lista')
            return
        c: Creature = item.data(QtCore.Qt.UserRole)
        dmg, ok = QtWidgets.QInputDialog.getInt(self, 'Dano', f'Quanto de dano aplicar a {c.name}?', 1, 0, 9999)
        if ok:
            c.take_damage(dmg)
            if not c.alive:
                QtWidgets.QMessageBox.information(self, 'Morto', f'{c.name} morreu!')
                # se era NPC, remove da lista principal
                if c.is_npc:
                    try:
                        self.npcs.remove(c)
                    except ValueError:
                        pass
                else:
                    try:
                        self.pcs.remove(c)
                    except ValueError:
                        pass
            self.refresh_list()

    def next_turn(self):
        if not self.creature_list:
            QtWidgets.QMessageBox.information(self, 'Info', 'Nenhuma criatura na lista. Rolar iniciativas primeiro.')
            return

        # Regra: cada "turn" percorre a lista atual
        # aplicar regen no começo do turno para criatura
        cur_idx = self.turn_index % len(self.creature_list)
        creature = self.creature_list[cur_idx]
        if creature.is_npc and getattr(creature, 'it_regen', False):
            creature.regen_pv()
        # mostrar quem é o atual
        self.status.setText(f"Round {self.round_number} Turn {self.turn_index + 1} - {creature.name}'s turn")
        
        self.show_turn_widget(creature)

        # após ações, checar mortos e limpar
        self.cleanup_dead()
        self.round_number += (self.turn_index + 1) // max(1, len(self.creature_list))
        self.turn_index = (self.turn_index + 1) % max(1, len(self.creature_list))
        self.refresh_list()

    def show_turn_widget(self, creature):
        # apagar o conteúdo visual anterior
        
        self.clear_turn_panel()

        # criar o novo widget do turno
        tw = TurnWidget(creature, self.creature_list)
        self.turn_layout.addWidget(tw)

        self.current_turn_widget = tw

    def cleanup_dead(self):
        removed = 0
        new_npcs = []
        for npc in self.npcs:
            if npc.alive:
                new_npcs.append(npc)
            else:
                removed += 1
        self.npcs = new_npcs
        new_pcs = []
        for pc in self.pcs:
            if pc.alive:
                new_pcs.append(pc)
            else:
                removed += 1
        self.pcs = new_pcs
        # rebuild creature_list removing dead
        self.creature_list = [c for c in self.creature_list if c.alive]
        if removed > 0:
            QtWidgets.QMessageBox.information(self, 'Remoção', f'{removed} criaturas removidas (mortas)')

    def show_creatures_popup(self):
        text = '\n'.join([c.show_sheet_text() for c in unique(self.creature_list)])
        QtWidgets.QMessageBox.information(self, 'Criaturas', text if text else 'Nenhuma criatura')

    def end_combat(self):
        if QtWidgets.QMessageBox.question(self, 'Encerrar', 'Deseja encerrar o combate?') == QtWidgets.QMessageBox.Yes:
            self.pcs = []
            self.npcs = []
            self.creature_list = []
            self.turn_index = 0
            self.turn_number = 0
            self.refresh_list()
            self.status.setText('Combate encerrado')

    def _clear_layout(self, layout):
        """Limpa recursivamente um layout: remove widgets e sublayouts."""
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                # desconecta sinais opcionais aqui, se necessário
                widget.setParent(None)
                widget.deleteLater()
            else:
                # pode ser um sublayout
                sublay = item.layout()
                if sublay is not None:
                    self._clear_layout(sublay)

    def clear_turn_panel(self):
        """Limpa todo o conteúdo do turn_layout de forma segura."""
        if not hasattr(self, 'turn_layout'):
            return

        self._clear_layout(self.turn_layout)

        # forçar atualização visual
        self.turn_panel.update()
        self.turn_panel.repaint()

# ---------------------- Dialogs ----------------------
class PcInitiativeDialog(QtWidgets.QDialog):
    def __init__(self, pcs, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Iniciativas dos Jogadores")
        self.setModal(True)

        self.pcs = pcs
        self.inputs = {}

        layout = QtWidgets.QFormLayout()

        for pc in pcs:
            spin = QtWidgets.QSpinBox()
            spin.setRange(-5, 50)
            spin.setValue(pc.initiative if pc.initiative else 0)
            self.inputs[pc] = spin
            layout.addRow(pc.name + ":", spin)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout.addWidget(btns)
        self.setLayout(layout)

    def apply_results(self):
        for pc, spin in self.inputs.items():
            pc.initiative = spin.value()


class AddNpcDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Adicionar NPC')
        self.resize(300, 200)
        layout = QtWidgets.QFormLayout(self)

        self.name_edit = QtWidgets.QLineEdit('NPC')
        self.pv_dice_edit = QtWidgets.QLineEdit('1d8')
        self.init_mod_spin = QtWidgets.QSpinBox()
        self.init_mod_spin.setRange(-10, 10)
        self.n_inits_spin = QtWidgets.QSpinBox()
        self.n_inits_spin.setRange(1, 8)
        self.regen_spin = QtWidgets.QSpinBox()
        self.regen_spin.setRange(0, 50)
        self.pdf_path_edit = QtWidgets.QLineEdit('Path')


        layout.addRow('Nome:', self.name_edit)
        layout.addRow('PV dice:', self.pv_dice_edit)
        layout.addRow('Init mod:', self.init_mod_spin)
        layout.addRow('Número de iniciativas:', self.n_inits_spin)
        layout.addRow('Taxa de regen:', self.regen_spin)
        layout.addRow('Caminho para imagem:', self.pdf_path_edit)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def get_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'pv_dice': self.pv_dice_edit.text().strip(),
            'init_mod': int(self.init_mod_spin.value()),
            'n_inits': int(self.n_inits_spin.value()),
            'regen_rate': int(self.regen_spin.value()),
            'pdf_path': self.pdf_path_edit.text().strip()
        }


# ---------------------- Turn Widget ----------------------
class ImageLabel(QtWidgets.QLabel):
    def __init__(self, path, parent=None, max_width: int = 440):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("border: 2px solid #888;")
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred
        )
        self.setMaximumWidth(max_width)
        self.setMaximumHeight(max_width)

        self.pixmap_original = QtGui.QPixmap(path)

    def resizeEvent(self, event):
        if not self.pixmap_original.isNull():
            self.setPixmap(
                self.pixmap_original.scaled(
                    self.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )
            )
        super().resizeEvent(event)

class TurnWidget(QtWidgets.QWidget):

    def __init__(self, creature: Creature, creature_list: List[Creature], parent =None):
        super().__init__(parent)
        self.creature = creature
        self.creature_list = creature_list

        turn_layout = QtWidgets.QVBoxLayout(self)

        path = str(creature.pdf_path)
        if path in ['', 'nan', 'None']:
            path = search_nopicture_path()
        img = ImageLabel(path=path)
        turn_layout.addWidget(img)


        label = QtWidgets.QLabel(f"É a vez de {creature.name}!")
        turn_layout.addWidget(label)


        damage_box = QtWidgets.QHBoxLayout(self)
        self.damage_spin = QtWidgets.QSpinBox()
        self.damage_spin.setRange(0, 9999)
        self.targets_combo = QtWidgets.QComboBox()
        for c in creature_list:
            if c is not creature and c.alive:
                self.targets_combo.addItem(f"{c.name} ({'NPC' if c.is_npc else 'PC'})", userData=c)

        damage_box.addWidget(QtWidgets.QLabel('Dano a aplicar:'),2)
        damage_box.addWidget(self.damage_spin, 1)
        damage_box.addWidget(self.targets_combo, 7)
        turn_layout.addLayout(damage_box)


        btn_attack = QtWidgets.QPushButton('Aplicar dano')
        btn_attack.clicked.connect(self.apply_damage)
        turn_layout.addWidget(btn_attack)
    

    def apply_damage(self):
        idx = self.targets_combo.currentIndex()
        if idx < 0:
            QtWidgets.QMessageBox.information(self, 'Info', 'Nenhum alvo disponível')
            return
        target: Creature = self.targets_combo.currentData()
        dmg = int(self.damage_spin.value())
        target.take_damage(dmg)
        QtWidgets.QMessageBox.information(self, 'Ataque', f'{target.name} recebeu {dmg} de dano. PV agora: {target.pv}/{target.max_pv}')
        # se morreu, remover da combobox
        if not target.alive:
            self.targets_combo.removeItem(idx)

# ---------------------- Main ----------------------

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = CombatWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
