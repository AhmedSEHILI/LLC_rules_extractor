from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget


class AnalyseDonneesPage(QWidget):
    # Page pour l'analyse et l'interrogation des données
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Analyse et interrogation des données")
        self.table = QTableWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)