from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton


class GestionOntologiesPage(QWidget):
    """
    Page de l'application dédiée à la gestion des ontologies.

    Cette vue permet d'afficher, manipuler et visualiser les ontologies chargées,
    notamment sous forme textuelle et graphique.
    """

    def __init__(self, parent=None):
        """
        Initialise la page de gestion des ontologies.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut None.
        """
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("Page : Gestion des ontologies")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ici, vous pouvez afficher et manipuler les ontologies chargées.")
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)

        option = QTextOption()
        option.setWrapMode(QTextOption.NoWrap)
        self.text_edit.document().setDefaultTextOption(option)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(self.text_edit)

        self.btn_afficher_graphe = QPushButton("Afficher le graphe de l’ontologie")
        layout.addWidget(self.btn_afficher_graphe)

        self.label_graphe = QLabel()
        layout.addWidget(self.label_graphe)

        self.setLayout(layout)
