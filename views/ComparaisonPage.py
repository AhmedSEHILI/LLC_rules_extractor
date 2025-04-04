from PyQt5.QtWidgets import QTableWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget


class ComparaisonPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()

        # Partie gauche : chargement d'un fichier
        self.left_panel = QVBoxLayout()
        self.label_gauche = QLabel("Règles chargées depuis un fichier :")
        self.btn_charger_fichier = QPushButton("Charger un fichier de règles")
        self.table_fichier = QTableWidget()

        self.left_panel.addWidget(self.label_gauche)
        self.left_panel.addWidget(self.btn_charger_fichier)
        self.left_panel.addWidget(self.table_fichier)

        # Partie droite : résultats AMIE3
        self.right_panel = QVBoxLayout()
        self.label_droite = QLabel("Règles générées par AMIE3 :")
        self.table_amie = QTableWidget()

        self.right_panel.addWidget(self.label_droite)
        self.right_panel.addWidget(self.table_amie)

        layout.addLayout(self.left_panel)
        layout.addLayout(self.right_panel)
        self.setLayout(layout)