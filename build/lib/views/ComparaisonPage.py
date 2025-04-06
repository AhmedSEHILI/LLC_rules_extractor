from PyQt5.QtWidgets import QTableWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget


class ComparaisonPage(QWidget):
    """
    Page d'interface pour comparer des ensembles de règles.

    Cette vue affiche deux panneaux côte à côte :
    - à gauche, les règles chargées depuis un fichier ;
    - à droite, les règles générées automatiquement par AMIE3.
    """

    def __init__(self, parent=None):
        """
        Initialise la page de comparaison avec deux tableaux
        et un bouton de chargement de fichier.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut None.
        """
        super().__init__(parent)
        layout = QHBoxLayout()

        self.left_panel = QVBoxLayout()
        self.label_gauche = QLabel("Règles chargées depuis un fichier :")
        self.btn_charger_fichier = QPushButton("Charger un fichier de règles")
        self.table_fichier = QTableWidget()

        self.left_panel.addWidget(self.label_gauche)
        self.left_panel.addWidget(self.btn_charger_fichier)
        self.left_panel.addWidget(self.table_fichier)

        self.right_panel = QVBoxLayout()
        self.label_droite = QLabel("Règles générées par AMIE3 :")
        self.table_amie = QTableWidget()

        self.right_panel.addWidget(self.label_droite)
        self.right_panel.addWidget(self.table_amie)

        layout.addLayout(self.left_panel)
        layout.addLayout(self.right_panel)
        self.setLayout(layout)
