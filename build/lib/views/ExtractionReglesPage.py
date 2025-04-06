from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget


class ExtractionReglesPage(QWidget):
    """
    Page dédiée à l'extraction, l'affichage et la gestion des règles.

    Cette vue permet de présenter les résultats de l'extraction de règles
    (issues d'AMIE3) dans un tableau.
    """

    def __init__(self, parent=None):
        """
        Initialise l'interface de la page d'extraction des règles.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut None.
        """
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("Page : Extraction et gestion des règles")
        self.table_resultats = QTableWidget()

        layout.addWidget(self.label)
        layout.addWidget(self.table_resultats)
        self.setLayout(layout)
