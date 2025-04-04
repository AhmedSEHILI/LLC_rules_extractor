from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget


class ExtractionReglesPage(QWidget):
    # Page pour extraire, lister, visualiser, sauvegarder des règles
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Extraction et gestion des règles")
        #self.text_edit = QTextEdit()
        self.table_resultats = QTableWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.table_resultats)
        self.setLayout(layout)