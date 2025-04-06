import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt


class RuleTestView(QMainWindow):
    """
    Fenêtre de saisie d'une règle individuelle.

    Cette interface permet à l'utilisateur d'entrer une seule règle
    et de consulter les classes et propriétés disponibles dans l'ontologie.
    """

    def __init__(self, mere=None):
        """
        Initialise la fenêtre.

        Args:
            mere (QWidget, optional): La fenêtre parente. Par défaut None.
        """
        super().__init__()
        self.resize(800, 100)
        self.mere = mere
        self.setWindowTitle("Requête SPARQL")

        main_layout = QVBoxLayout()

        self.box_classes = QMessageBox()
        self.box_classes.setWindowTitle("Classes disponibles")

        self.box_properties = QMessageBox()
        self.box_properties.setWindowTitle("Propriétés disponibles")

        saisie_layout = QVBoxLayout()
        self.champ_saisie = QLineEdit()
        self.champ_saisie.setPlaceholderText("Saisissez une règle : A(?x)$B(?y) -> C(?z)  NB : $ représente la conjonction")
        saisie_layout.addWidget(self.champ_saisie)

        buttons_layout = QHBoxLayout()
        self.btn_valider_saisie = QPushButton("Valider la saisie")
        self.btn_aide_proprietes = QPushButton("Voir propriétés disponibles")
        self.btn_aide_classes = QPushButton("Voir classes disponibles")

        buttons_layout.addWidget(self.btn_valider_saisie)
        buttons_layout.addWidget(self.btn_aide_proprietes)
        buttons_layout.addWidget(self.btn_aide_classes)

        main_layout.addLayout(saisie_layout)
        main_layout.addLayout(buttons_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def connect_signals(self):
        """
        Connecte les actions des boutons à leurs méthodes associées.
        """
        self.btn_valider_saisie.clicked.connect(self.lireSaisie)
        self.btn_aide_classes.clicked.connect(self.box_classes.show)
        self.btn_aide_proprietes.clicked.connect(self.box_properties.show)

    def lireSaisie(self):
        """
        Lit et affiche la règle saisie dans le terminal (à des fins de test).
        """
        print(self.champ_saisie.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = RuleTestView()
    mainWin.show()
    sys.exit(app.exec_())
