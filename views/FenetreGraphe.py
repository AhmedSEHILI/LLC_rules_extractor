from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QScrollArea


class FenetreGraphe(QWidget):
    def __init__(self, image_path=None, titre="Graphe de l'ontologie"):
        super().__init__()
        self.setWindowTitle(titre)
        self.image_path = image_path
        self.current_scale = 1.0

        layout = QVBoxLayout()
        controls = QHBoxLayout()

        self.btn_zoom_in = QPushButton("Zoom +")
        self.btn_zoom_out = QPushButton("Zoom -")
        self.btn_reset = QPushButton("Reset")

        self.btn_zoom_in.clicked.connect(self.zoom_in)
        self.btn_zoom_out.clicked.connect(self.zoom_out)
        self.btn_reset.clicked.connect(self.reset_zoom)

        controls.addWidget(self.btn_zoom_in)
        controls.addWidget(self.btn_zoom_out)
        controls.addWidget(self.btn_reset)

        layout.addLayout(controls)

        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignCenter)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.label_image)
        self.scroll_area.setWidgetResizable(True)

        layout.addWidget(self.scroll_area)
        self.setLayout(layout)



    def afficher_image(self):
        self.pixmap = QPixmap(self.image_path)
        self.update_pixmap()

    def update_pixmap(self):
        if self.pixmap:
            scaled = self.pixmap.scaled(
                int(self.pixmap.width() * self.current_scale),
                int(self.pixmap.height() * self.current_scale),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_image.setPixmap(scaled)

    def zoom_in(self):
        self.current_scale *= 1.25
        self.update_pixmap()

    def zoom_out(self):
        self.current_scale *= 0.8
        self.update_pixmap()

    def reset_zoom(self):
        self.current_scale = 1.0
        self.update_pixmap()

    def afficher_graphe(self,image_path):
        self.image_path = image_path
        self.afficher_image()
        self.show()