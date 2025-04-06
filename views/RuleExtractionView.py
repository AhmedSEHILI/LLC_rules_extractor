from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
    QPushButton, QToolButton, QLineEdit, QLabel, QStackedWidget
)

from views.Amie3ParamsWidget import Amie3ParamsWidget
from views.AnalyseDonneesPage import AnalyseDonneesPage
from views.ComparaisonPage import ComparaisonPage
from views.ExtractionReglesPage import ExtractionReglesPage
from views.GestionOntologiesPage import GestionOntologiesPage
from views.AccueilPage import AccueilPage
from views.QualiteValidationPage import QualiteValidationPage
from views.RequeteSPARQLView import RequeteSPARQLView
from views.RuleTestview import RuleTestView
from views.RuleSetTestView import RuleSetTestView
from views.FenetreGraphe import FenetreGraphe


class RuleExtractionView(QMainWindow):
    """
    Fenêtre principale de l'application d'extraction de règles à partir d'ontologies.

    Cette vue intègre toutes les pages fonctionnelles de l’application (chargement
    d’ontologies, extraction, validation, comparaison...) via un QStackedWidget
    et une interface graphique organisée autour d’un panneau latéral de navigation.
    """

    def __init__(self):
        """
        Initialise l'ensemble de l'interface utilisateur de l'application.
        """
        super().__init__()
        self.setWindowTitle("Application d'extraction de règles de LLC")
        self.resize(2400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        self.left_panel = QVBoxLayout()

        # Bloc : Gestion des ontologies
        group_ontologies = QGroupBox("Gestion des ontologies")
        ontologies_layout = QVBoxLayout()
        self.btn_charger_ontologie = QPushButton("Charger une ontologie")
        self.fenetre_graphe = FenetreGraphe()
        self.btn_visualiser_ontologie = QPushButton("Visualiser une ontologie")
        ontologies_layout.addWidget(self.btn_charger_ontologie)
        ontologies_layout.addWidget(self.btn_visualiser_ontologie)
        group_ontologies.setLayout(ontologies_layout)

        # Bloc : Extraction des règles
        group_regles = QGroupBox("Extraction et gestion des règles")
        regles_layout = QVBoxLayout()
        self.btn_lister_regles = QPushButton("Lister les règles")
        self.btn_visualiser_regles = QPushButton("Visualiser les règles")
        self.btn_afficher_regles_validees = QPushButton("Afficher les règles validées")
        self.btn_valider_regle = QPushButton("Valider une règle extraite")
        self.btn_sauver_regle = QPushButton("Sauvegarder règles validées")
        self.btn_supp_regle = QPushButton("Supprimer règles validées")
        self.btn_sauver_regles = QPushButton("Sauvegarder règles extraites")
        self.btn_valider_regle.setEnabled(False)
        self.btn_sauver_regle.setEnabled(False)
        self.btn_supp_regle.setEnabled(False)
        self.btn_afficher_regles_validees.setEnabled(False)
        self.btn_sauver_regles.setEnabled(False)

        regles_layout.addWidget(self.btn_lister_regles)
        regles_layout.addWidget(self.btn_visualiser_regles)
        regles_layout.addWidget(self.btn_valider_regle)
        regles_layout.addWidget(self.btn_afficher_regles_validees)
        regles_layout.addWidget(self.btn_sauver_regle)
        regles_layout.addWidget(self.btn_supp_regle)
        regles_layout.addWidget(self.btn_sauver_regles)
        group_regles.setLayout(regles_layout)

        # Bloc : Qualité des règles
        group_qualite = QGroupBox("Qualité et validation des règles")
        qualite_layout = QVBoxLayout()
        self.fenetre_saisie_regle = RuleTestView()
        self.fenetre_saisie_ens_regles = RuleSetTestView()
        self.btn_mesurer_qualite_regle = QPushButton("Mesurer la qualité d'une règle")
        self.btn_mesurer_qualite_regles = QPushButton("Mesurer la qualité d'un ensemble de règles")
        qualite_layout.addWidget(self.btn_mesurer_qualite_regle)
        qualite_layout.addWidget(self.btn_mesurer_qualite_regles)
        group_qualite.setLayout(qualite_layout)

        # Bloc : Analyse des données
        group_analyse = QGroupBox("Analyse et interrogation des données")
        analyse_layout = QVBoxLayout()
        self.fenetre_requete = RequeteSPARQLView()
        self.btn_interroger_donnees = QPushButton("Interroger les données")
        self.btn_tester_hypothese = QPushButton("Tester une hypothèse")
        self.btn_marquer_donnees = QPushButton("Marquer les données")
        analyse_layout.addWidget(self.btn_interroger_donnees)
        analyse_layout.addWidget(self.btn_tester_hypothese)
        analyse_layout.addWidget(self.btn_marquer_donnees)
        group_analyse.setLayout(analyse_layout)

        # Bloc : Comparaison
        group_comparaison = QGroupBox("Comparaison")
        comparaison_layout = QVBoxLayout()
        self.btn_comparer_resultats = QPushButton("Comparer des résultats d'extraction")
        comparaison_layout.addWidget(self.btn_comparer_resultats)
        group_comparaison.setLayout(comparaison_layout)

        # Bloc : Paramètres AMIE3
        group_amie3 = QGroupBox("AMIE3")
        amie3_layout = QVBoxLayout()
        self.amie3_params_widget = Amie3ParamsWidget()
        self.btn_lancer_amie3 = QPushButton("Lancer AMIE3")
        self.btn_lancer_amie3_save = QPushButton("Lancer AMIE3 + Sauvegarder")
        amie3_layout.addWidget(self.amie3_params_widget)
        amie3_layout.addWidget(self.btn_lancer_amie3)
        amie3_layout.addWidget(self.btn_lancer_amie3_save)
        group_amie3.setLayout(amie3_layout)

        # Empilement dans la colonne de gauche
        self.left_panel.addWidget(group_ontologies)
        self.left_panel.addWidget(group_regles)
        self.left_panel.addWidget(group_qualite)
        self.left_panel.addWidget(group_analyse)
        self.left_panel.addWidget(group_comparaison)
        self.left_panel.addWidget(group_amie3)
        self.left_panel.addStretch()

        # Zone centrale avec le QStackedWidget
        self.central_layout = QVBoxLayout()
        self.label_titre = QLabel("APPLICATION D’EXTRACTION DE RÈGLES DE LLC")
        self.label_titre.setAlignment(Qt.AlignCenter)
        self.label_titre.setStyleSheet("background-color: #C8F7C5; font-weight: bold;")
        font_titre = self.label_titre.font()
        font_titre.setPointSize(16)
        self.label_titre.setFont(font_titre)

        tools_layout = QHBoxLayout()
        self.btn_zoom_in = QToolButton()
        self.btn_zoom_in.setText("+")
        self.btn_zoom_out = QToolButton()
        self.btn_zoom_out.setText("-")
        self.btn_reset_view = QToolButton()
        self.btn_reset_view.setText("Home")
        self.lineedit_recherche = QLineEdit()
        self.lineedit_recherche.setPlaceholderText("Rechercher une règle, une ontologie, ...")
        tools_layout.addWidget(self.btn_zoom_in)
        tools_layout.addWidget(self.btn_zoom_out)
        tools_layout.addWidget(self.btn_reset_view)
        tools_layout.addStretch()
        tools_layout.addWidget(self.lineedit_recherche)

        self.stacked_widget = QStackedWidget()
        self.page_accueil = AccueilPage()
        self.page_gestion_onto = GestionOntologiesPage()
        self.page_extraction_regles = ExtractionReglesPage()
        self.page_qualite = QualiteValidationPage()
        self.page_analyse = AnalyseDonneesPage()
        self.page_comparaison = ComparaisonPage()

        self.stacked_widget.addWidget(self.page_accueil)
        self.stacked_widget.addWidget(self.page_gestion_onto)
        self.stacked_widget.addWidget(self.page_extraction_regles)
        self.stacked_widget.addWidget(self.page_qualite)
        self.stacked_widget.addWidget(self.page_analyse)
        self.stacked_widget.addWidget(self.page_comparaison)

        self.central_layout.addWidget(self.label_titre)
        self.central_layout.addLayout(tools_layout)
        self.central_layout.addWidget(self.stacked_widget)

        main_layout.addLayout(self.left_panel, 1)
        main_layout.addLayout(self.central_layout, 3)

    def afficher_graphe(self, image_path):
        """
        Affiche une image de graphe dans une fenêtre dédiée.

        Args:
            image_path (str): Chemin de l'image à afficher.
        """
        self.fenetre_graphe.afficher_graphe(image_path)
