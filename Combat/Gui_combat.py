from Structures import Npc, Pc
from DnD_Batle_code import import_npc, import_pcs, pc_roll, organize_by_initiative
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel
)

class combat(QWidget):
    def __init__(self):
        super().__init__()
        #titulo da janela
        self.setWindowTitle('Administrador de Combates em D&D')
        # Layout principal
        layout = QVBoxLayout()

        # Botão para adicionar players e npcs
        self.botao_add_npc = QPushButton("Adicionar NPC")
        self.botao_add_npc.clicked.connect(self.add_npc)
        layout.addWidget(self.botao_add_npc)

        self.botao_add_pc = QPushButton("Adicionar PC")
        self.botao_add_pc.clicked.connect(self.add_pc)
        layout.addWidget(self.botao_add_pc)




        #declara as propriedades excenciais para o combate
        self.npcs = None
        self.pcs = None
        self.creatures = None
        self.round_index = None

        # Aplica o layout à janela
        self.setLayout(layout)

    def add_npc(self):
        pass

    def add_pc(self):
        pass




if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = combat()
    janela.resize(3000, 1500)
    janela.show()
    sys.exit(app.exec_())
