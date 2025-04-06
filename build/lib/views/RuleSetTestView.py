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


class RuleSetTestView(QMainWindow):
    """
    Fenêtre de saisie et de mesure de qualité pour un ensemble de règles.

    Permet à l'utilisateur d'entrer plusieurs règles (une par ligne),
    puis de déclencher leur évaluation à l'aide d'un bouton.
    """

    def __init__(self, mere=None):
        """
        Initialise l'interface de saisie des règles.

        Args:
            mere (QWidget, optional): Fenêtre parente. Par défaut None.
        """
        super().__init__()
        self.resize(1200, 800)
        self.mere = mere
        self.setWindowTitle("Zone Saisie Règles")

        main_layout = QHBoxLayout()

        saisie_layout = QHBoxLayout()
        self.champ_saisie = QTextEdit()
        self.champ_saisie.setPlaceholderText("Saisissez vos règles séparées par un saut de ligne !!!")
        saisie_layout.addWidget(self.champ_saisie)

        buttons_layout = QVBoxLayout()
        self.btn_mesurer_regles = QPushButton("Mesurer les règles")
        buttons_layout.addWidget(self.btn_mesurer_regles)

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
        Connecte les signaux des boutons à leurs méthodes respectives.
        """
        self.btn_nettoyer.clicked.connect(self.nettoyer)

    def nettoyer(self):
        """
        Vide le champ de saisie des règles.
        """
        self.champ_saisie.clear()
