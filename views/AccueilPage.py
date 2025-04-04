from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class AccueilPage(QWidget):
    # Page d'accueil (message de bienvenue, etc.)
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label_info = QLabel(
            "Bienvenue sur notre application.\n"
            "Vous trouverez ici les informations générales.\n"
            "Sélectionnez une section à gauche pour continuer."
        )
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setStyleSheet("border: 2px solid red; color: black;")
        layout.addWidget(self.label_info)
        self.setLayout(layout)