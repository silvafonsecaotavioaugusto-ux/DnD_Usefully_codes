import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel
)
from Roll_Dice import code_roll

class dices(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rolador de Dados D&D")
        
        # Layout principal
        layout = QVBoxLayout()

        # Campo de entrada para o dado
        self.input = QLineEdit()
        self.input.setPlaceholderText("Digite o dado (ex: 1d20p5)")
        layout.addWidget(self.input)

        # Botão para rolar
        self.botao = QPushButton("Rolar Dado")
        self.botao.clicked.connect(self.rolar)
        layout.addWidget(self.botao)

        # Label de resultado
        self.resultado = QLabel("Resultado aparecerá aqui.")
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def rolar(self):
        try:
            expressao = self.input.text()
            resultado = code_roll(expressao)
            self.resultado.setText(
                f"O resultado de sua rolagem foi :{resultado}"
            )
        except Exception as e:
            self.resultado.setText(f"Erro: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = dices()
    janela.resize(300, 150)
    janela.show()
    sys.exit(app.exec_())