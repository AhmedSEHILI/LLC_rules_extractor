from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget


class AnalyseDonneesPage(QWidget):
    """
    Vue dédiée à l’analyse et l’interrogation des données.

    Cette page contient un tableau pour afficher les résultats des requêtes sur l’ontologie médicale.
    """

    def __init__(self, parent=None):
        """
        Initialise la page d'analyse des données

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut None.
        """
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("Page : Analyse et interrogation des données")
        self.table = QTableWidget()

        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)
