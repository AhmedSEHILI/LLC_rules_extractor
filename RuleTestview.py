import sys
import os
import subprocess
import csv

import pyparsing
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QPushButton, QLabel, QCheckBox, QLineEdit, QTextEdit, QToolButton,
    QStackedWidget, QFileDialog, QMessageBox, QVBoxLayout, QScrollArea, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextOption, QPixmap

from rdflib import Graph, URIRef, RDF, RDFS, OWL
import networkx as nx
import matplotlib.pyplot as plt

# Feneter pour les requetes SPARQL

class RuleTestView(QMainWindow):
    def __init__(self,mere=None):
        super().__init__()
        self.resize(800,100)
        self.mere = mere
        self.setWindowTitle("Requếte SPARQL")




        main_layout = QVBoxLayout()

        #Fenetres d'aide
        self.box_classes = QMessageBox()
        self.box_classes.setWindowTitle("Classes disponibles              ")

        self.box_properties = QMessageBox()
        self.box_properties.setWindowTitle("Propriétes disponibles                  ")



        #Champ de saisie
        saisie_layout = QVBoxLayout()
        self.champ_saisie = QLineEdit()
        self.champ_saisie.setPlaceholderText("Saisissez une règle : A(?x)$B(?y) -> C(?z)  NB : $ Représente la conjonction")

        saisie_layout.addWidget(self.champ_saisie)

        # Boutons
        buttons_layout = QHBoxLayout()
        self.btn_valider_saisie = QPushButton("Valider la saisie")
        buttons_layout.addWidget(self.btn_valider_saisie)

        self.btn_aide_proprietes = QPushButton("Voir propriétés disponibles")
        buttons_layout.addWidget(self.btn_aide_proprietes)

        self.btn_aide_classes = QPushButton("Voir classes disponibles")
        buttons_layout.addWidget(self.btn_aide_classes)

        main_layout.addLayout(saisie_layout)
        main_layout.addLayout(buttons_layout)


        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # self.connect_signals()


    def connect_signals(self):
        self.btn_valider_saisie.clicked.connect(self.lireSaisie)
        self.btn_aide_classes.clicked.connect(self.box_classes.show)
        self.btn_aide_proprietes.clicked.connect(self.box_properties.show)

    def lireSaisie(self):
        print(self.champ_saisie.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = RuleTestView()
    mainWin.show()
    sys.exit(app.exec_())