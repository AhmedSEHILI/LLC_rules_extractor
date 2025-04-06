from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy


class AccueilPage(QWidget):
    """
    Page d'accueil de l'application.

    Cette vue affiche un message de bienvenue centré, ainsi qu’un bouton 
    permettant d’ouvrir une page Wikipédia sur la Leucémie lymphoïde chronique (LLC).
    """

    def __init__(self, parent=None):
        """
        Initialise la page d'accueil.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut None.
        """
        super().__init__(parent)    

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setSpacing(20)

        label = QLabel(
            "Bienvenue sur notre application.\n"
            "Vous trouverez ici les informations générales.\n"
            "Sélectionnez une section à gauche pour continuer.\n\n"
            "👉 Si vous souhaitez en savoir plus sur la maladie LLC (Leucémie lymphoïde chronique), cliquez ci-dessous."
        )
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12))

        btn = QPushButton("En savoir plus sur la LLC")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        btn.clicked.connect(self.ouvrir_lien_llc)

        container_layout.addWidget(label)
        container_layout.addWidget(btn, alignment=Qt.AlignCenter)
        container.setLayout(container_layout)

        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def ouvrir_lien_llc(self):
        """
        Ouvre une page Wikipédia expliquant la maladie LLC.
        """
        QDesktopServices.openUrl(QUrl("https://fr.wikipedia.org/wiki/Leucémie_lymphoïde_chronique"))
