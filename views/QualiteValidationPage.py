from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget


class QualiteValidationPage(QWidget):
    """
    Page dédiée à la qualité et à la validation des règles extraites.

    Cette vue permet d’afficher les règles dans un tableau afin de mesurer
    leur qualité (selon des métriques spécifiques) et de les valider ou non.
    """

    def __init__(self, parent=None):
        """
        Initialise la page qualité/validation.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut None.
        """
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("Page : Qualité et validation des règles")
        self.table = QTableWidget()

        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)
