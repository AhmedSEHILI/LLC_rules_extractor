import sys
import os
import subprocess
import csv

import pyparsing
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QPushButton, QLabel, QCheckBox, QLineEdit, QTextEdit, QToolButton,
    QStackedWidget, QFileDialog, QMessageBox, QVBoxLayout, QScrollArea, QFormLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextOption, QPixmap

from RequeteSPARQLView import RequeteSPARQLView
from rdflib import Graph, URIRef, RDF, RDFS, OWL
import networkx as nx
import matplotlib.pyplot as plt


# <-------------------------->
# Fonctions de conversion d'ontologie
# <-------------------------->
def convert_owl_to_ttl(input_file, output_file):
    try:
        g = Graph()
        g.parse(input_file, format='xml')
        g.serialize(destination=output_file, format='turtle')
        print(f"Fichier converti : {input_file} → {output_file}")
        return True
    except Exception as e:
        print(f"Erreur lors de la conversion OWL->TTL: {e}")
        return False


# <-------------------------->
# Fonction pour générer le graphe BFS
# <-------------------------->
def generer_arbre_classes_networkx(owl_file, output_image="classes_arbre.png", fig_width=10, fig_height=5):
    # Lit un fichier OWL (RDF/XML), construit un graphe BFS de gauche à droite et enregistre dans output_image

    g = Graph()
    g.parse(owl_file, format="xml")
    print(f"[INFO] {len(g)} triplets chargés depuis {owl_file}.")

    # Récupérer les classes (URIRef)
    classes = set()
    for c in g.subjects(RDF.type, OWL.Class):
        if isinstance(c, URIRef):
            classes.add(c)
    for c in g.subjects(RDF.type, RDFS.Class):
        if isinstance(c, URIRef):
            classes.add(c)
    # print(f"Nombre de classes (URIRef) détectées : {len(classes)}")

    # Construire un graphe orienté (parent->enfant)
    nx_graph = nx.DiGraph()
    for c in classes:
        nx_graph.add_node(str(c))

    for child in classes:
        for parent in g.objects(child, RDFS.subClassOf):
            if parent in classes:
                nx_graph.add_edge(str(parent), str(child))

    # Trouve les racines
    roots = [n for n in nx_graph.nodes() if nx_graph.in_degree(n) == 0]

    # BFS => niveau
    level = {}
    queue = []
    for r in roots:
        level[r] = 0
        queue.append(r)

    while queue:
        current = queue.pop(0)
        curr_lvl = level[current]
        for ch in nx_graph.successors(current):
            new_lvl = curr_lvl + 1
            if ch not in level or level[ch] > new_lvl:
                level[ch] = new_lvl
                queue.append(ch)

    # Grouper par niveau
    level_dict = {}
    for node, lv in level.items():
        level_dict.setdefault(lv, []).append(node)

    # Positions : x=lv*4, y=-i*9
    pos = {}
    for lv, nodes_in_this_level in level_dict.items():
        nodes_in_this_level.sort()
        for i, node in enumerate(nodes_in_this_level):
            x = lv * 4
            y = -i * 9
            pos[node] = (x, y)

    # Labels (nom)
    labels = {}
    for node in nx_graph.nodes():
        uri_str = node
        if '#' in uri_str:
            local_name = uri_str.split('#')[-1]
        else:
            local_name = uri_str
        labels[node] = local_name

    # Figure de taille fig_width x fig_height
    plt.figure(figsize=(fig_width, fig_height))
    nx.draw(nx_graph, pos=pos, with_labels=False, node_size=100, node_color="#ccccff", arrowstyle="->", arrowsize=8,
            width=0.8)
    nx.draw_networkx_labels(nx_graph, pos, labels=labels, font_size=6)

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_image, dpi=90)
    plt.close()

    # print(f"Arbre généré dans {output_image}.")


# <-------------------------->
# Modèle
# <-------------------------->
class RuleExtractionModel:
    def __init__(self):
        self.ontologies = []  # Liste des chemins vers les ontologies chargées
        self.regles = []  # Liste des règles extraites

    def charger_ontologie(self, path):
        if os.path.exists(path):
            self.ontologies.append(path)
            return True
        return False

    def extraire_regles(self):
        # Logique d'extraction de règles (simulation ici)
        regle = {
            "rule": "A(x) ∧ B(x,y) → C(y)",
            "head_coverage": 0.75,
            "std_confidence": 0.80,
            "pca_confidence": 0.78,
            "positive_examples": 120,
            "body_size": 2
        }
        self.regles.append(regle)
        return regle

    def sauvegarder_regles(self, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for regle in self.regles:
                    f.write(f"{regle}\n")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False


# <-------------------------->
# Pages
# <-------------------------->
class AccueilPage(QWidget):
    # Page d'accueil (message de bienvenue, etc.)
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label_info = QLabel(
            "Bienvenue sur notre application.\n"
            "Vous trouverez ici les informations générales.\n"
            "Sélectionnez une section à gauche pour continuer."
        )
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setStyleSheet("border: 2px solid red; color: black;")
        layout.addWidget(self.label_info)
        self.setLayout(layout)


class GestionOntologiesPage(QWidget):
    # Page pour la gestion des ontologies (chargement, visualisation...)
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Gestion des ontologies")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ici, vous pouvez afficher et manipuler les ontologies chargées.")
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        option = QTextOption()
        option.setWrapMode(QTextOption.NoWrap)
        self.text_edit.document().setDefaultTextOption(option)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        layout.addWidget(self.text_edit)

        # Bouton "Afficher le graphe"
        self.btn_afficher_graphe = QPushButton("Afficher le graphe de l’ontologie")
        layout.addWidget(self.btn_afficher_graphe)

        # Champs pour la taille de la figure
        fig_layout = QHBoxLayout()
        fig_layout.addWidget(QLabel("Largeur figure:"))
        self.lineedit_fig_width = QLineEdit("18")
        fig_layout.addWidget(self.lineedit_fig_width)

        fig_layout.addWidget(QLabel("Hauteur figure:"))
        self.lineedit_fig_height = QLineEdit("12")
        fig_layout.addWidget(self.lineedit_fig_height)
        layout.addLayout(fig_layout)

        # Bouton "Rafraîchir le graphe"
        self.btn_rafraichir_graphe = QPushButton("Rafraîchir le graphe")
        layout.addWidget(self.btn_rafraichir_graphe)

        # Label pour l'image
        self.label_graphe = QLabel()
        layout.addWidget(self.label_graphe)

        self.setLayout(layout)


class ExtractionReglesPage(QWidget):
    # Page pour extraire, lister, visualiser, sauvegarder des règles
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Extraction et gestion des règles")
        #self.text_edit = QTextEdit()
        self.table_resultats = QTableWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.table_resultats)
        self.setLayout(layout)


class QualiteValidationPage(QWidget):
    # Page pour mesurer la qualité des règles et les valider
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Qualité et validation des règles")
        self.text_edit = QTextEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)


class AnalyseDonneesPage(QWidget):
    # Page pour l'analyse et l'interrogation des données
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Analyse et interrogation des données")
        self.table = QTableWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)


class ComparaisonPage(QWidget):
    # Page pour comparer des résultats d'extraction
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Comparaison des résultats")
        self.text_edit = QTextEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)


# <-------------------------->
# Vue
# <-------------------------->
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
        self.btn_visualiser_ontologie = QPushButton("Visualiser une ontologie")
        ontologies_layout.addWidget(self.btn_charger_ontologie)
        ontologies_layout.addWidget(self.btn_visualiser_ontologie)
        group_ontologies.setLayout(ontologies_layout)

        # Groupe : Extraction et gestion des règles
        group_regles = QGroupBox("Extraction et gestion des règles")
        regles_layout = QVBoxLayout()
        self.btn_extraire_regles = QPushButton("Extraire un ensemble de règles")
        self.btn_lister_regles = QPushButton("Lister les règles")
        self.btn_visualiser_regles = QPushButton("Visualiser les règles")
        self.btn_sauvegarder_regles = QPushButton("Sauvegarder les règles extraites")
        regles_layout.addWidget(self.btn_extraire_regles)
        regles_layout.addWidget(self.btn_lister_regles)
        regles_layout.addWidget(self.btn_visualiser_regles)
        regles_layout.addWidget(self.btn_sauvegarder_regles)
        group_regles.setLayout(regles_layout)

        # Groupe : Qualité et validation des règles
        group_qualite = QGroupBox("Qualité et validation des règles")
        qualite_layout = QVBoxLayout()
        self.btn_mesurer_qualite_regle = QPushButton("Mesurer la qualité d'une règle")
        self.btn_mesurer_qualite_regles = QPushButton("Mesurer la qualité d'un ensemble de règles")
        self.btn_valider_regle = QPushButton("Valider une règle extraite")
        qualite_layout.addWidget(self.btn_mesurer_qualite_regle)
        qualite_layout.addWidget(self.btn_mesurer_qualite_regles)
        qualite_layout.addWidget(self.btn_valider_regle)
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


# <-------------------------->
# Contrôleur
# <-------------------------->
class RuleExtractionController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        # Gestion ontologies
        self.view.btn_charger_ontologie.clicked.connect(self.do_charger_ontologie)
        self.view.btn_visualiser_ontologie.clicked.connect(self.do_visualiser_ontologie)

        # Bouton "Afficher le graphe"
        self.view.page_gestion_onto.btn_afficher_graphe.clicked.connect(self.do_afficher_graphe_ontologie)
        # Bouton "Rafraîchir le graphe (taille)"
        self.view.page_gestion_onto.btn_rafraichir_graphe.clicked.connect(self.do_rafraichir_graphe_ontologie)

        # Extraction des règles
        self.view.btn_extraire_regles.clicked.connect(self.do_extraire_regles)
        self.view.btn_lister_regles.clicked.connect(self.do_lister_regles)
        self.view.btn_visualiser_regles.clicked.connect(self.do_visualiser_regles)
        self.view.btn_sauvegarder_regles.clicked.connect(self.do_sauvegarder_regles)

        # Qualité / Validation
        self.view.btn_mesurer_qualite_regle.clicked.connect(self.do_mesurer_qualite_regle)
        self.view.btn_mesurer_qualite_regles.clicked.connect(self.do_mesurer_qualite_regles)
        self.view.btn_valider_regle.clicked.connect(self.do_valider_regle)

        # Analyse des données
        self.view.btn_interroger_donnees.clicked.connect(lambda: self.view.fenetre_requete.show())
        self.view.btn_tester_hypothese.clicked.connect(lambda: self.afficher_page(4))
        self.view.btn_marquer_donnees.clicked.connect(lambda: self.afficher_page(4))
        self.view.fenetre_requete.btn_executer_requete.clicked.connect(self.executer_requete)

        # Comparaison
        self.view.btn_comparer_resultats.clicked.connect(lambda: self.afficher_page(5))

        # Bouton AMIE3
        self.view.btn_lancer_amie3.clicked.connect(self.extraire_regles_amie3)

        # Bouton Lancer AMIE3 + Sauvegarder
        self.view.btn_lancer_amie3_save.clicked.connect(self.do_lancer_amie3_avec_sauvegarde)

        # Boutons de zoom
        self.view.btn_zoom_in.clicked.connect(self.zoom_in)
        self.view.btn_zoom_out.clicked.connect(self.zoom_out)
        self.view.btn_reset_view.clicked.connect(self.reset_view)

    # Fonctions de gestion des ontologies
    def do_charger_ontologie(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Charger une ontologie", "",
            "Fichiers OWL (*.owl);;Tous les fichiers (*)"
        )
        if file_path:
            if self.model.charger_ontologie(file_path):
                self.view.page_gestion_onto.text_edit.append(f"Ontologie chargée : {file_path}")
                QMessageBox.information(self.view, "Chargement",
                                        f"L'ontologie a été chargée avec succès.\nChemin : {file_path}")
            else:
                QMessageBox.warning(self.view, "Erreur", "Le fichier sélectionné n'a pas pu être chargé.")

    def do_visualiser_ontologie(self):
        if self.model.ontologies:
            dernier = self.model.ontologies[-1]
            try:
                self.afficher_page(1)
            except Exception as e:
                QMessageBox.warning(self.view, "Erreur", f"Impossible de lire le fichier : {e}")
        else:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")

    # Fonction pour afficher le graphe de l’ontologie
    def do_afficher_graphe_ontologie(self):
        if not self.model.ontologies:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")
            return

        dernier_onto = self.model.ontologies[-1]
        try:
            image_path = "classes_arbre.png"

            # BFS avec taille par défaut 18x12
            generer_arbre_classes_networkx(owl_file=dernier_onto, output_image=image_path, fig_width=18, fig_height=12)

            pix = QPixmap(image_path)
            self.view.page_gestion_onto.label_graphe.setPixmap(pix)
            self.view.page_gestion_onto.label_graphe.setScaledContents(True)

            self.afficher_page(1)
        except Exception as e:
            QMessageBox.warning(self.view, "Erreur", f"Impossible de générer le graphe : {e}")

    # Fonction qui lit fig_width, fig_height dans la page et refait le BFS
    def do_rafraichir_graphe_ontologie(self):
        if not self.model.ontologies:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")
            return

        dernier_onto = self.model.ontologies[-1]
        try:
            fw_str = self.view.page_gestion_onto.lineedit_fig_width.text().strip()
            fh_str = self.view.page_gestion_onto.lineedit_fig_height.text().strip()

            fig_w = float(fw_str) if fw_str else 18.0
            fig_h = float(fh_str) if fh_str else 12.0

            image_path = "classes_arbre.png"
            generer_arbre_classes_networkx(
                owl_file=dernier_onto,
                output_image=image_path,
                fig_width=fig_w,
                fig_height=fig_h
            )

            pix = QPixmap(image_path)
            self.view.page_gestion_onto.label_graphe.setPixmap(pix)
            self.view.page_gestion_onto.label_graphe.setScaledContents(True)

            self.afficher_page(1)

        except Exception as e:
            QMessageBox.warning(self.view, "Erreur", f"Impossible de générer le graphe : {e}")

    # Fonctions d'extraction et de gestion des règles
    def do_extraire_regles(self):
        regle = self.model.extraire_regles()
        self.view.page_extraction_regles.text_edit.append("Règle extraite :")
        self.view.page_extraction_regles.text_edit.append(
            f"Rule: {regle['rule']}\n"
            f"Head Coverage: {regle['head_coverage']}\n"
            f"Std Confidence: {regle['std_confidence']}\n"
            f"PCA Confidence: {regle['pca_confidence']}\n"
            f"Positive Examples: {regle['positive_examples']}\n"
            f"Body Size: {regle['body_size']}\n"
        )
        self.afficher_page(2)

    def do_lister_regles(self):
        self.view.page_extraction_regles.text_edit.append("Liste des règles extraites :")
        if not self.model.regles:
            self.view.page_extraction_regles.text_edit.append("Aucune règle extraite.")
        else:
            for idx, regle in enumerate(self.model.regles, start=1):
                self.view.page_extraction_regles.text_edit.append(f"{idx}. {regle['rule']}")
        self.afficher_page(2)

    def do_visualiser_regles(self):
        self.view.page_extraction_regles.text_edit.append("Détails des règles extraites :")
        for regle in self.model.regles:
            self.view.page_extraction_regles.text_edit.append(str(regle))
        self.afficher_page(2)

    def do_sauvegarder_regles(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Sauvegarder les règles extraites", "", "Text Files (*.txt);;Tous les fichiers (*)"
        )
        if file_path:
            if self.model.sauvegarder_regles(file_path):
                QMessageBox.information(self.view, "Sauvegarde", "Les règles ont été sauvegardées avec succès.")
            else:
                QMessageBox.warning(self.view, "Erreur", "Une erreur est survenue lors de la sauvegarde.")
        self.afficher_page(2)

    # Fonctions de qualité et validation (simulées)
    def do_mesurer_qualite_regle(self):
        self.view.page_qualite.text_edit.append("Mesure de qualité pour la règle sélectionnée :")
        self.view.page_qualite.text_edit.append("Support : 0.65, Confiance : 0.80")
        self.afficher_page(3)

    def do_mesurer_qualite_regles(self):
        self.view.page_qualite.text_edit.append("Mesure de qualité pour l'ensemble des règles :")
        self.view.page_qualite.text_edit.append("Moyenne Support : 0.60, Moyenne Confiance : 0.78")
        self.afficher_page(3)

    def do_valider_regle(self):
        self.view.page_qualite.text_edit.append("La règle a été validée avec succès.")
        self.afficher_page(3)

    # Fonction pour lancer AMIE3
    def extraire_regles_amie3(self):
        resultat = self.do_lancer_amie3()
        if not resultat is None:
            self.afficher_resultats_amie3(resultat)
            self.afficher_page(2)
        return

    def do_lancer_amie3(self):
        # Vérifier qu'une ontologie a été chargée
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur", "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            self.afficher_page(2)
            return

        # Récupérer le dernier fichier d'ontologie chargé (.owl)
        input_owl = self.model.ontologies[-1]
        # Définir le chemin pour le fichier TTL
        ttl_path = os.path.join(os.getcwd(), "ontology.ttl")

        # Conversion en TTL
        QMessageBox.warning(self.view, "En cours","Conversion de l'ontologie {input_owl} en Turtle...")
        if not convert_owl_to_ttl(input_owl, ttl_path):
            QMessageBox.warning(self.view, "Erreur","La conversion de l'ontologie en TTL a échoué.")
            self.afficher_page(2)
            return

        # Récupérer la liste d'arguments dynamiques
        amie_params = self.view.amie3_params_widget.build_amie3_params()

        # Déterminer le chemin du fichier amie3.jar (dans le même répertoire que ce script)
        jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amie3.jar")
        if not os.path.exists(jar_path):
            QMessageBox.warning(self.view, "Erreur","Fichier amie3.jar introuvable.")
            self.afficher_page(2)
            return

        # Construire la commande
        command = ["java", "-jar", jar_path] + amie_params + [ttl_path]

        #self.view.page_extraction_regles.text_edit.append("Commande AMIE3 : " + " ".join(command))

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate(timeout=120)
            output = stdout

            #self.view.page_extraction_regles.text_edit.append("Résultats d'AMIE3 :")
            #self.view.page_extraction_regles.text_edit.append(output)
            return output
        except subprocess.TimeoutExpired:
            process.kill()
            QMessageBox.warning(self.view, "Erreur","L'exécution d'AMIE3 a dépassé le temps imparti.")
            self.afficher_page(2)
        except Exception as e:
            QMessageBox.warning(self.view, "Erreur","Erreur lors du lancement d'AMIE3: {e}")
            self.afficher_page(2)

        os.remove(ttl_path)
    # Fonction qui fait la meme chose que do_lancer_amie3, mais on enregistre la sortie stdout dans un fichier
    def do_lancer_amie3_avec_sauvegarde(self):
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur",
                "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            self.afficher_page(2)
            return

        # Demander le nom du fichier de sortie
        output_file, _ = QFileDialog.getSaveFileName(
            self.view,
            "Enregistrer la sortie d'AMIE3",
            "",  # chemin par défaut
            "Fichiers texte (*.txt);;Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )

        if not output_file:  # si l'utilisateur annule
            return

        # Execution d'AMIE3
        resultat = self.do_lancer_amie3()



        if output_file.split('.')[-1] == 'csv' :
            self.amie_to_csv(output_file,resultat)
        else :
        # Enregistrer la sortie stdout
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(resultat)

        self.afficher_resultats_amie3(resultat)
            # Afficher dans la text_edit
            #self.view.page_extraction_regles.text_edit.clear()
            #self.view.page_extraction_regles.text_edit.append("Résultats d'AMIE3 :")
            #self.view.page_extraction_regles.text_edit.append(stdout)
        self.afficher_page(2)



    # Navigation entre pages
    def afficher_page(self, index):

        self.view.stacked_widget.setCurrentIndex(index)

    # Fonctions de zoom
    def zoom_in(self):
        current_page = self.view.stacked_widget.currentWidget()
        if current_page:
            for child in current_page.findChildren(QTextEdit):
                font = child.font()
                font.setPointSize(font.pointSize() + 1)
                child.setFont(font)

    def zoom_out(self):
        current_page = self.view.stacked_widget.currentWidget()
        if current_page:
            for child in current_page.findChildren(QTextEdit):
                font = child.font()
                new_size = max(1, font.pointSize() - 1)
                font.setPointSize(new_size)
                child.setFont(font)


    def reset_view(self):
        current_page = self.view.stacked_widget.currentWidget()
        if current_page:
            for child in current_page.findChildren(QTextEdit):
                font = child.font()
                font.setPointSize(10)
                child.setFont(font)


    def executer_requete(self):
        print('Controller',self.view.fenetre_requete.champ_saisie.toPlainText())
        self.view.fenetre_requete.close()
        self.afficher_page(4)
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur", "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            return

        g = Graph()
        g.parse(self.model.ontologies[-1])

        try:
            results = g.query(self.view.fenetre_requete.champ_saisie.toPlainText())
        except pyparsing.exceptions.ParseException :
            QMessageBox.warning(self.view, "Erreur", "Erreur lors de la saisie de la requête")
            return
        self.afficher_resultats_requete(results)

    def afficher_resultats_requete(self,results):

        liste_variables = [x.toPython()[1:] for x in results.vars]
        self.view.page_analyse.table.clear()
        self.view.page_analyse.table.setColumnCount(len(liste_variables))
        self.view.page_analyse.table.setRowCount(len(results))
        self.view.page_analyse.table.setHorizontalHeaderLabels([x.toPython() for x in results.vars])
        index_ligne = 0
        index_colonne = 0
        for row in results:
            for var in liste_variables :
                self.view.page_analyse.table.setItem(index_ligne, index_colonne, QTableWidgetItem(row[var]))
                index_colonne+=1
            index_ligne+=1
            index_colonne = 0


    def amie_to_csv(self,file_path,amie_result):
        index = 0
        lines = amie_result.split('\n')

        #Arriver jusqu'au colonnes
        while not lines[index].startswith("Starting the mining phase...") :
            index+=1

        columns = lines[index +1].split('\t')

        #On se place sur la première règle extraite
        lines = lines[index + 2:]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(';'.join(columns)+'\n')
                for line in lines:
                    if line.__contains__("=>"):
                        f.write(';'.join(line.split('\t'))+'\n')
                f.close()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def afficher_resultats_amie3(self, amie_result):
        index = 0
        lines = amie_result.split('\n')

        # Arriver jusqu'au colonnes
        while not lines[index].startswith("Starting the mining phase..."):
            index += 1

        columns = lines[index + 1].split('\t')

        # On se place sur la première règle extraite
        lines = lines[index + 2:]

        self.view.page_extraction_regles.table_resultats.clear()
        self.view.page_extraction_regles.table_resultats.setColumnCount(len(columns))
        self.view.page_extraction_regles.table_resultats.setHorizontalHeaderLabels(columns)
        regles = []
        for line in lines:
            if line.__contains__("=>"):
                regles += [line.split('\t')]

        self.view.page_extraction_regles.table_resultats.setRowCount(len(regles))

        index_ligne = 0
        for regle in regles:
            for index in range(len(regle)) :
                self.view.page_extraction_regles.table_resultats.setItem(index_ligne, index, QTableWidgetItem(regle[index]))
            index_ligne += 1


# <-------------------------->
# Paramètres AMIE3
# <-------------------------->
class Amie3ParamsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.form_layout = QFormLayout(content_widget)

        # Paramètres numériques ou textuels

        self.lineedit_mins = QLineEdit("100")  # -mins
        self.form_layout.addRow(QLabel("-mins (min-support)"), self.lineedit_mins)

        self.lineedit_minis = QLineEdit("100")  # -minis
        self.form_layout.addRow(QLabel("-minis (min-initial-support)"), self.lineedit_minis)

        self.lineedit_minhc = QLineEdit("0.01")  # -minhc
        self.form_layout.addRow(QLabel("-minhc (min-head-coverage)"), self.lineedit_minhc)

        self.lineedit_pm = QLineEdit("headcoverage")  # -pm
        self.form_layout.addRow(QLabel("-pm (pruning-metric)"), self.lineedit_pm)

        self.lineedit_bexr = QLineEdit("")  # -bexr
        self.form_layout.addRow(QLabel("-bexr (body-excluded-relations)"), self.lineedit_bexr)

        self.lineedit_hexr = QLineEdit("")  # -hexr
        self.form_layout.addRow(QLabel("-hexr (head-excluded-relations)"), self.lineedit_hexr)

        self.lineedit_iexr = QLineEdit("")  # -iexr
        self.form_layout.addRow(QLabel("-iexr (instantiation-excluded-relations)"), self.lineedit_iexr)

        self.lineedit_htr = QLineEdit("")  # -htr
        self.form_layout.addRow(QLabel("-htr (head-target-relations)"), self.lineedit_htr)

        self.lineedit_btr = QLineEdit("")  # -btr
        self.form_layout.addRow(QLabel("-btr (body-target-relations)"), self.lineedit_btr)

        self.lineedit_itr = QLineEdit("")  # -itr
        self.form_layout.addRow(QLabel("-itr (instantiation-target-relations)"), self.lineedit_itr)

        self.lineedit_maxad = QLineEdit("3")  # -maxad
        self.form_layout.addRow(QLabel("-maxad (max-depth)"), self.lineedit_maxad)

        self.lineedit_minpca = QLineEdit("0.0")  # -minpca
        self.form_layout.addRow(QLabel("-minpca (min-pca-confidence)"), self.lineedit_minpca)

        self.lineedit_bias = QLineEdit("default")  # -bias
        self.form_layout.addRow(QLabel("-bias (oneVar|default|lazy|...)"), self.lineedit_bias)

        self.lineedit_rl = QLineEdit("")  # -rl (recursivity-limit)
        self.form_layout.addRow(QLabel("-rl (recursivity-limit)"), self.lineedit_rl)

        self.lineedit_nc = QLineEdit("8")  # -nc
        self.form_layout.addRow(QLabel("-nc (n-threads)"), self.lineedit_nc)

        self.lineedit_minc = QLineEdit("0.0")  # -minc
        self.form_layout.addRow(QLabel("-minc (min-std-confidence)"), self.lineedit_minc)

        self.lineedit_vo = QLineEdit("fun")  # -vo
        self.form_layout.addRow(QLabel("-vo (variableOrder)"), self.lineedit_vo)

        self.lineedit_ef = QLineEdit("")  # -ef (extraFile)
        self.form_layout.addRow(QLabel("-ef (extraFile)"), self.lineedit_ef)

        self.lineedit_d = QLineEdit("")  # -d (delimiter)
        self.form_layout.addRow(QLabel("-d (delimiter)"), self.lineedit_d)

        # Paramètres booléens (checkBox)

        self.checkbox_oute = QCheckBox("-oute (output-at-end)")
        self.form_layout.addRow(self.checkbox_oute)

        # Garder cette option toujours activée pour faciliter la conversion en CSV
        self.checkbox_datalog = QCheckBox("-datalog (datalog-output)")
        self.form_layout.addRow(self.checkbox_datalog)
        self.checkbox_datalog.setCheckState(2)

        self.checkbox_const = QCheckBox("-const (allow-constants)")
        self.form_layout.addRow(self.checkbox_const)

        self.checkbox_fconst = QCheckBox("-fconst (only-constants)")
        self.form_layout.addRow(self.checkbox_fconst)

        self.checkbox_caos = QCheckBox("-caos (count-always-on-subject)")
        self.form_layout.addRow(self.checkbox_caos)

        self.checkbox_optimcb = QCheckBox("-optimcb (optim-confidence-bounds)")
        self.form_layout.addRow(self.checkbox_optimcb)

        self.checkbox_optimfh = QCheckBox("-optimfh (optim-func-heuristic)")
        self.form_layout.addRow(self.checkbox_optimfh)

        self.checkbox_verbose = QCheckBox("-verbose")
        self.form_layout.addRow(self.checkbox_verbose)

        self.checkbox_auta = QCheckBox("-auta (avoid-unbound-type-atoms)")
        self.form_layout.addRow(self.checkbox_auta)

        self.checkbox_deml = QCheckBox("-deml (do-not-exploit-max-length)")
        self.form_layout.addRow(self.checkbox_deml)

        self.checkbox_dqrw = QCheckBox("-dqrw (disable-query-rewriting)")
        self.form_layout.addRow(self.checkbox_dqrw)

        self.checkbox_dpr = QCheckBox("-dpr (disable-perfect-rules)")
        self.form_layout.addRow(self.checkbox_dpr)

        self.checkbox_oout = QCheckBox("-oout (only-output)")
        self.form_layout.addRow(self.checkbox_oout)

        self.checkbox_full = QCheckBox("-full (enable all enhancements)")
        self.form_layout.addRow(self.checkbox_full)

        self.checkbox_noHeuristics = QCheckBox("-noHeuristics")
        self.form_layout.addRow(self.checkbox_noHeuristics)

        self.checkbox_noKbRewrite = QCheckBox("-noKbRewrite")
        self.form_layout.addRow(self.checkbox_noKbRewrite)

        self.checkbox_noKbExistsDetection = QCheckBox("-noKbExistsDetection")
        self.form_layout.addRow(self.checkbox_noKbExistsDetection)

        self.checkbox_noSkyline = QCheckBox("-noSkyline")
        self.form_layout.addRow(self.checkbox_noSkyline)

        self.checkbox_ostd = QCheckBox("-ostd (ommit-std-conf)")
        self.form_layout.addRow(self.checkbox_ostd)

        self.checkbox_optimai = QCheckBox("-optimai (adaptive-instantiations)")
        self.form_layout.addRow(self.checkbox_optimai)

        self.checkbox_mlg = QCheckBox("-mlg (multilingual)")
        self.form_layout.addRow(self.checkbox_mlg)

        # Scroll
        content_widget.setLayout(self.form_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    # Fonction qui construit la liste d'arguments AMIE3
    def build_amie3_params(self):
        params = []

        # -mins
        if self.lineedit_mins.text().strip():
            params += ["-mins", self.lineedit_mins.text().strip()]

        # -minis
        if self.lineedit_minis.text().strip():
            params += ["-minis", self.lineedit_minis.text().strip()]

        # -minhc
        if self.lineedit_minhc.text().strip():
            params += ["-minhc", self.lineedit_minhc.text().strip()]

        # -pm
        if self.lineedit_pm.text().strip():
            params += ["-pm", self.lineedit_pm.text().strip()]

        # -bexr
        if self.lineedit_bexr.text().strip():
            params += ["-bexr", self.lineedit_bexr.text().strip()]

        # -hexr
        if self.lineedit_hexr.text().strip():
            params += ["-hexr", self.lineedit_hexr.text().strip()]

        # -iexr
        if self.lineedit_iexr.text().strip():
            params += ["-iexr", self.lineedit_iexr.text().strip()]

        # -htr
        if self.lineedit_htr.text().strip():
            params += ["-htr", self.lineedit_htr.text().strip()]

        # -btr
        if self.lineedit_btr.text().strip():
            params += ["-btr", self.lineedit_btr.text().strip()]

        # -itr
        if self.lineedit_itr.text().strip():
            params += ["-itr", self.lineedit_itr.text().strip()]

        # -maxad
        if self.lineedit_maxad.text().strip():
            params += ["-maxad", self.lineedit_maxad.text().strip()]

        # -minpca
        if self.lineedit_minpca.text().strip():
            params += ["-minpca", self.lineedit_minpca.text().strip()]

        # -bias
        if self.lineedit_bias.text().strip():
            params += ["-bias", self.lineedit_bias.text().strip()]

        # -rl
        if self.lineedit_rl.text().strip():
            params += ["-rl", self.lineedit_rl.text().strip()]

        # -nc
        if self.lineedit_nc.text().strip():
            params += ["-nc", self.lineedit_nc.text().strip()]

        # -minc
        if self.lineedit_minc.text().strip():
            params += ["-minc", self.lineedit_minc.text().strip()]

        # -vo
        if self.lineedit_vo.text().strip():
            params += ["-vo", self.lineedit_vo.text().strip()]

        # -ef
        if self.lineedit_ef.text().strip():
            params += ["-ef", self.lineedit_ef.text().strip()]

        # -d
        if self.lineedit_d.text().strip():
            params += ["-d", self.lineedit_d.text().strip()]

        # ----- Lecture des checkboxes -----
        if self.checkbox_oute.isChecked():
            params.append("-oute")

        if self.checkbox_datalog.isChecked():
            params.append("-datalog")

        if self.checkbox_const.isChecked():
            params.append("-const")

        if self.checkbox_fconst.isChecked():
            params.append("-fconst")

        if self.checkbox_caos.isChecked():
            params.append("-caos")

        if self.checkbox_optimcb.isChecked():
            params.append("-optimcb")

        if self.checkbox_optimfh.isChecked():
            params.append("-optimfh")

        if self.checkbox_verbose.isChecked():
            params.append("-verbose")

        if self.checkbox_auta.isChecked():
            params.append("-auta")

        if self.checkbox_deml.isChecked():
            params.append("-deml")

        if self.checkbox_dqrw.isChecked():
            params.append("-dqrw")

        if self.checkbox_dpr.isChecked():
            params.append("-dpr")

        if self.checkbox_oout.isChecked():
            params.append("-oout")

        if self.checkbox_full.isChecked():
            params.append("-full")

        if self.checkbox_noHeuristics.isChecked():
            params.append("-noHeuristics")

        if self.checkbox_noKbRewrite.isChecked():
            params.append("-noKbRewrite")

        if self.checkbox_noKbExistsDetection.isChecked():
            params.append("-noKbExistsDetection")

        if self.checkbox_noSkyline.isChecked():
            params.append("-noSkyline")

        if self.checkbox_ostd.isChecked():
            params.append("-ostd")

        if self.checkbox_optimai.isChecked():
            params.append("-optimai")

        if self.checkbox_mlg.isChecked():
            params.append("-mlg")

        return params


# <-------------------------->
# Point d'entrée
# <-------------------------->
def main():
    app = QApplication(sys.argv)

    model = RuleExtractionModel()
    view = RuleExtractionView()
    controller = RuleExtractionController(model, view)

    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()