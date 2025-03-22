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

class RequeteSPARQLView(QMainWindow):
    def __init__(self,mere=None):
        super().__init__()
        self.resize(1200, 800)
        self.mere = mere
        self.setWindowTitle("Requếte SPARQL")




        main_layout = QHBoxLayout()


        #Champ de saisie
        saisie_layout = QHBoxLayout()
        self.champ_saisie = QTextEdit()
        self.champ_saisie.setPlaceholderText("Veuillez entrer une requête SPARQL")

        saisie_layout.addWidget(self.champ_saisie)

        #Boutons
        buttons_layout = QVBoxLayout()
        self.btn_executer_requete = QPushButton("Exécuter la requête")
        buttons_layout.addWidget(self.btn_executer_requete)

        self.btn_nettoyer = QPushButton("Effacer")
        buttons_layout.addWidget(self.btn_nettoyer)

        self.btn_ajt_prefixe = QPushButton("Ajouter un préfixe")
        buttons_layout.addWidget(self.btn_ajt_prefixe)

        main_layout.addLayout(saisie_layout)
        main_layout.addLayout(buttons_layout)


        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self._connect_signals()

    def _connect_signals(self):
        # Activation des boutons
        self.btn_nettoyer.clicked.connect(self.nettoyer)
        self.btn_ajt_prefixe.clicked.connect(self.ajouter_prefixe)

    def envoyer_requete(self):
        print(self.champ_saisie.toPlainText())
        if self.mere != None :
            self.mere.executer_requete()
        else:
            self.close()



    def nettoyer(self):
        self.champ_saisie.clear()

    def ajouter_prefixe(self):
        return
