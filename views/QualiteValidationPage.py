from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget


class QualiteValidationPage(QWidget):
    # Page pour mesurer la qualité des règles et les valider
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Qualité et validation des règles")
        self.table = QTableWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)