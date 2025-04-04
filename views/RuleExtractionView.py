from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton, QToolButton, \
    QLineEdit, QLabel, QStackedWidget

from  views.Amie3ParamsWidget import Amie3ParamsWidget
from  views.AnalyseDonneesPage import AnalyseDonneesPage
from  views.ComparaisonPage import ComparaisonPage
from  views.ExtractionReglesPage import ExtractionReglesPage
from  views.GestionOntologiesPage import GestionOntologiesPage
from  views.AccueilPage import AccueilPage
from  views.QualiteValidationPage import QualiteValidationPage
from  views.RequeteSPARQLView import RequeteSPARQLView
from  views.RuleTestview import RuleTestView
from  views.RuleSetTestView import RuleSetTestView
from  views.FenetreGraphe import FenetreGraphe


class RuleExtractionView(QMainWindow):
    # La fenêtre principale (vue) avec un QStackedWidget pour basculer entre les différentes pages (ontologies, extraction de règles, etc.).
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application d'extraction de règles de LLC")
        self.resize(2400, 800)

        # Widget central pour QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal (horizontal) : colonne de gauche + zone centrale
        main_layout = QHBoxLayout(central_widget)

        # <-------------------------->
        # 1) Colonne de gauche
        # <-------------------------->
        self.left_panel = QVBoxLayout()

        # Groupe : Gestion des ontologies
        group_ontologies = QGroupBox("Gestion des ontologies")
        ontologies_layout = QVBoxLayout()
        self.btn_charger_ontologie = QPushButton("Charger une ontologie")
        self.fenetre_graphe = FenetreGraphe()
        self.btn_visualiser_ontologie = QPushButton("Visualiser une ontologie")
        ontologies_layout.addWidget(self.btn_charger_ontologie)
        ontologies_layout.addWidget(self.btn_visualiser_ontologie)
        group_ontologies.setLayout(ontologies_layout)

        # Groupe : Extraction et gestion des règles
        group_regles = QGroupBox("Extraction et gestion des règles")
        regles_layout = QVBoxLayout()
        # self.btn_extraire_regles = QPushButton("Extraire un ensemble de règles")
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
        # regles_layout.addWidget(self.btn_extraire_regles)
        regles_layout.addWidget(self.btn_lister_regles)
        regles_layout.addWidget(self.btn_visualiser_regles)

        regles_layout.addWidget(self.btn_valider_regle)
        regles_layout.addWidget(self.btn_afficher_regles_validees)
        regles_layout.addWidget(self.btn_sauver_regle)
        regles_layout.addWidget(self.btn_supp_regle)
        regles_layout.addWidget(self.btn_sauver_regles)

        group_regles.setLayout(regles_layout)

        # Groupe : Qualité et validation des règles
        group_qualite = QGroupBox("Qualité et validation des règles")
        qualite_layout = QVBoxLayout()

        self.fenetre_saisie_regle = RuleTestView()
        self.fenetre_saisie_ens_regles = RuleSetTestView()

        self.btn_mesurer_qualite_regle = QPushButton("Mesurer la qualité d'une règle")
        self.btn_mesurer_qualite_regles = QPushButton("Mesurer la qualité d'un ensemble de règles")
        #self.btn_valider_regle = QPushButton("Valider une règle extraite")
        qualite_layout.addWidget(self.btn_mesurer_qualite_regle)
        qualite_layout.addWidget(self.btn_mesurer_qualite_regles)
        #qualite_layout.addWidget(self.btn_valider_regle)
        group_qualite.setLayout(qualite_layout)

        # Groupe : Analyse et interrogation des données
        self.fenetre_requete = RequeteSPARQLView()
        group_analyse = QGroupBox("Analyse et interrogation des données")
        analyse_layout = QVBoxLayout()
        self.btn_interroger_donnees = QPushButton("Interroger les données")
        self.btn_tester_hypothese = QPushButton("Tester une hypothèse")
        self.btn_marquer_donnees = QPushButton("Marquer les données")

        analyse_layout.addWidget(self.btn_interroger_donnees)
        analyse_layout.addWidget(self.btn_tester_hypothese)
        analyse_layout.addWidget(self.btn_marquer_donnees)

        group_analyse.setLayout(analyse_layout)

        # Groupe : Comparaison
        group_comparaison = QGroupBox("Comparaison")
        comparaison_layout = QVBoxLayout()
        self.btn_comparer_resultats = QPushButton("Comparer des résultats d'extraction")
        comparaison_layout.addWidget(self.btn_comparer_resultats)
        group_comparaison.setLayout(comparaison_layout)

        # Groupe : AMIE3
        group_amie3 = QGroupBox("AMIE3")
        amie3_layout = QVBoxLayout()
        # Widget paramétrable
        self.amie3_params_widget = Amie3ParamsWidget()
        amie3_layout.addWidget(self.amie3_params_widget)

        self.btn_lancer_amie3 = QPushButton("Lancer AMIE3")
        amie3_layout.addWidget(self.btn_lancer_amie3)

        group_amie3.setLayout(amie3_layout)

        self.btn_lancer_amie3_save = QPushButton("Lancer AMIE3 + Sauvegarder")
        amie3_layout.addWidget(self.btn_lancer_amie3_save)

        # Empilement des groupes dans la colonne de gauche
        self.left_panel.addWidget(group_ontologies)
        self.left_panel.addWidget(group_regles)
        self.left_panel.addWidget(group_qualite)
        self.left_panel.addWidget(group_analyse)
        self.left_panel.addWidget(group_comparaison)
        self.left_panel.addWidget(group_amie3)
        self.left_panel.addStretch()

        # <-------------------------->
        # 2) Zone centrale
        # <-------------------------->
        self.central_layout = QVBoxLayout()
        self.label_titre = QLabel("APPLICATION D’EXTRACTION DE RÈGLES DE LLC")
        self.label_titre.setAlignment(Qt.AlignCenter)
        self.label_titre.setStyleSheet("background-color: #C8F7C5; font-weight: bold;")
        font_titre = self.label_titre.font()
        font_titre.setPointSize(16)
        self.label_titre.setFont(font_titre)

        # Barre d'outils
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

        # QStackedWidget : pages
        self.stacked_widget = QStackedWidget()
        self.page_accueil = AccueilPage()  # index 0
        self.page_gestion_onto = GestionOntologiesPage()  # index 1
        self.page_extraction_regles = ExtractionReglesPage()  # index 2
        self.page_qualite = QualiteValidationPage()  # index 3
        self.page_analyse = AnalyseDonneesPage()  # index 4
        self.page_comparaison = ComparaisonPage()  # index 5

        self.stacked_widget.addWidget(self.page_accueil)
        self.stacked_widget.addWidget(self.page_gestion_onto)
        self.stacked_widget.addWidget(self.page_extraction_regles)
        self.stacked_widget.addWidget(self.page_qualite)
        self.stacked_widget.addWidget(self.page_analyse)
        self.stacked_widget.addWidget(self.page_comparaison)

        self.central_layout.addWidget(self.label_titre)
        self.central_layout.addLayout(tools_layout)
        self.central_layout.addWidget(self.stacked_widget)

        # Assemblage du layout principal
        main_layout.addLayout(self.left_panel, 1)
        main_layout.addLayout(self.central_layout, 3)

    def afficher_graphe(self,image_path):
        self.fenetre_graphe.afficher_graphe(image_path)