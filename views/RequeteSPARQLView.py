import sys
import os
import subprocess
import csv

import pyparsing
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QPushButton, QLabel, QCheckBox, QLineEdit, QTextEdit, QToolButton,
    QStackedWidget, QFileDialog, QMessageBox, QScrollArea, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextOption, QPixmap

from rdflib import Graph, URIRef, RDF, RDFS, OWL
import networkx as nx
import matplotlib.pyplot as plt


class RequeteSPARQLView(QMainWindow):
    """
    Fenêtre dédiée à l'exécution de requêtes SPARQL.

    Cette interface permet à l'utilisateur de saisir une requête SPARQL,
    de l'exécuter ou de nettoyer le champ de saisie.
    """

    def __init__(self, mere=None):
        """
        Initialise la fenêtre de requête SPARQL.

        Args:
            mere (QWidget, optional): Fenêtre parente. Par défaut None.
        """
        super().__init__()
        self.resize(1200, 800)
        self.mere = mere
        self.setWindowTitle("Requête SPARQL")

        main_layout = QHBoxLayout()

        saisie_layout = QHBoxLayout()
        self.champ_saisie = QTextEdit()
        self.champ_saisie.setPlaceholderText("Veuillez entrer une requête SPARQL")
        saisie_layout.addWidget(self.champ_saisie)

        buttons_layout = QVBoxLayout()
        self.btn_executer_requete = QPushButton("Exécuter la requête")
        buttons_layout.addWidget(self.btn_executer_requete)

        self.btn_nettoyer = QPushButton("Effacer")
        buttons_layout.addWidget(self.btn_nettoyer)

        main_layout.addLayout(saisie_layout)
        main_layout.addLayout(buttons_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self._connect_signals()

    def _connect_signals(self):
        """
        Connecte les signaux des boutons à leurs fonctions respectives.
        """
        self.btn_nettoyer.clicked.connect(self.nettoyer)

    def nettoyer(self):
        """
        Vide le champ de saisie de la requête SPARQL.
        """
        self.champ_saisie.clear()
