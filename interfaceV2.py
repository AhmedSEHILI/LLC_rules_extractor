import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGroupBox, QPushButton, QLabel, QCheckBox, QLineEdit, QTextEdit, QToolButton,
    QStackedWidget, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextOption

# Importation de rdflib pour la conversion de formats RDF
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import XSD

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
# Modèle
# <-------------------------->
class RuleExtractionModel:
    def __init__(self):
        self.ontologies = []  # Liste des chemins vers les ontologies chargées
        self.regles = []      # Liste des règles extraites
    
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
# Pages pour le QStackedWidget
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
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ici, vous pouvez afficher et manipuler les ontologies chargées.")
        # Désactiver le retour à la ligne automatique
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        # Configurer l'option de texte par défaut pour être sûr que le wrap est désactivé
        option = QTextOption()
        option.setWrapMode(QTextOption.NoWrap)
        self.text_edit.document().setDefaultTextOption(option)
        
        # Afficher la barre de défilement horizontale (là où c'est nécessaire ou toujours)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

class ExtractionReglesPage(QWidget):
    # Page pour extraire, lister, visualiser, sauvegarder des règles
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Extraction et gestion des règles")
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ici, vous pouvez lancer l'extraction, visualiser et sauvegarder les règles.")
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

class QualiteValidationPage(QWidget):
    # Page pour mesurer la qualité des règles et les valider
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Qualité et validation des règles")
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ici, vous pouvez mesurer la qualité (support, confiance, etc.) et valider les règles.")
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

class AnalyseDonneesPage(QWidget):
    # Page pour l'analyse et l'interrogation des données
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Analyse et interrogation des données")
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ici, vous pouvez interroger et analyser les données.")
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

class ComparaisonPage(QWidget):
    # Page pour comparer des résultats d'extraction
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Page : Comparaison des résultats")
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ici, vous pouvez comparer différents résultats d'extraction.")
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
        self.btn_lancer_amie3 = QPushButton("Lancer AMIE3")
        amie3_layout.addWidget(self.btn_lancer_amie3)
        # Champs pour -minc (standard confidence)
        self.label_minc = QLabel("Min standard confidence (-minc):")
        self.lineedit_minc = QLineEdit("0.0")  # Valeur par défaut
        amie3_layout.addWidget(self.label_minc)
        amie3_layout.addWidget(self.lineedit_minc)

        # Champs pour -minpca (PCA confidence)
        self.label_minpca = QLabel("Min PCA confidence (-minpca):")
        self.lineedit_minpca = QLineEdit("0.1")  # Par défaut 0.1 (à modifier si nécessaire)
        amie3_layout.addWidget(self.label_minpca)
        amie3_layout.addWidget(self.lineedit_minpca)

        # Champs pour -nc (nombre de threads)
        self.label_nc = QLabel("Nombre de threads (-nc):")
        self.lineedit_nc = QLineEdit("8")  # Par défaut 8
        amie3_layout.addWidget(self.label_nc)
        amie3_layout.addWidget(self.lineedit_nc)

        # Ajout d'un QCheckBox pour l'option -const
        self.checkbox_const = QCheckBox("Activer -const")
        amie3_layout.addWidget(self.checkbox_const)
        group_amie3.setLayout(amie3_layout)
        
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
        self.page_accueil = AccueilPage()                # index 0
        self.page_gestion_onto = GestionOntologiesPage()   # index 1
        self.page_extraction_regles = ExtractionReglesPage() # index 2
        self.page_qualite = QualiteValidationPage()        # index 3
        self.page_analyse = AnalyseDonneesPage()           # index 4
        self.page_comparaison = ComparaisonPage()          # index 5
        
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
        # Gestion des ontologies
        self.view.btn_charger_ontologie.clicked.connect(self.do_charger_ontologie)
        self.view.btn_visualiser_ontologie.clicked.connect(self.do_visualiser_ontologie)

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
        self.view.btn_interroger_donnees.clicked.connect(lambda: self.afficher_page(4))
        self.view.btn_tester_hypothese.clicked.connect(lambda: self.afficher_page(4))
        self.view.btn_marquer_donnees.clicked.connect(lambda: self.afficher_page(4))

        # Comparaison
        self.view.btn_comparer_resultats.clicked.connect(lambda: self.afficher_page(5))
        
        # Bouton AMIE3
        self.view.btn_lancer_amie3.clicked.connect(self.do_lancer_amie3)
        
        # Boutons de zoom
        self.view.btn_zoom_in.clicked.connect(self.zoom_in)
        self.view.btn_zoom_out.clicked.connect(self.zoom_out)
        self.view.btn_reset_view.clicked.connect(self.reset_view)

    # Fonctions de gestion des ontologies
    def do_charger_ontologie(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Charger une ontologie", "", "Fichiers OWL (*.owl);;Tous les fichiers (*)")
        if file_path:
            if self.model.charger_ontologie(file_path):
                self.view.page_gestion_onto.text_edit.append(f"Ontologie chargée : {file_path}")
                QMessageBox.information(self.view, "Chargement", f"L'ontologie a été chargée avec succès.\nChemin : {file_path}")
            else:
                QMessageBox.warning(self.view, "Erreur", "Le fichier sélectionné n'a pas pu être chargé.")
    
    def do_visualiser_ontologie(self):
        if self.model.ontologies:
            dernier = self.model.ontologies[-1]
            try:
                with open(dernier, "r", encoding="utf-8") as f:
                    contenu = f.read()
                self.view.page_gestion_onto.text_edit.setPlainText(contenu)
                self.afficher_page(1)
            except Exception as e:
                QMessageBox.warning(self.view, "Erreur", f"Impossible de lire le fichier : {e}")
        else:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")

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
    
    def do_lister_regles(self):
        self.view.page_extraction_regles.text_edit.append("Liste des règles extraites :")
        if not self.model.regles:
            self.view.page_extraction_regles.text_edit.append("Aucune règle extraite.")
        else:
            for idx, regle in enumerate(self.model.regles, start=1):
                self.view.page_extraction_regles.text_edit.append(f"{idx}. {regle['rule']}")
    
    def do_visualiser_regles(self):
        self.view.page_extraction_regles.text_edit.append("Détails des règles extraites :")
        for regle in self.model.regles:
            self.view.page_extraction_regles.text_edit.append(str(regle))

    
    def do_sauvegarder_regles(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Sauvegarder les règles extraites", "", "Text Files (*.txt);;Tous les fichiers (*)"
        )
        if file_path:
            if self.model.sauvegarder_regles(file_path):
                QMessageBox.information(self.view, "Sauvegarde", "Les règles ont été sauvegardées avec succès.")
            else:
                QMessageBox.warning(self.view, "Erreur", "Une erreur est survenue lors de la sauvegarde.")

    # Fonctions de qualité et validation (simulées)
    def do_mesurer_qualite_regle(self):
        self.view.page_qualite.text_edit.append("Mesure de qualité pour la règle sélectionnée :")
        self.view.page_qualite.text_edit.append("Support : 0.65, Confiance : 0.80")
    
    def do_mesurer_qualite_regles(self):
        self.view.page_qualite.text_edit.append("Mesure de qualité pour l'ensemble des règles :")
        self.view.page_qualite.text_edit.append("Moyenne Support : 0.60, Moyenne Confiance : 0.78")
    
    def do_valider_regle(self):
        self.view.page_qualite.text_edit.append("La règle a été validée avec succès.")

    # Fonction pour lancer AMIE3
    def do_lancer_amie3(self):
        # Vérifier qu'une ontologie a été chargée
        if not self.model.ontologies:
            self.view.page_extraction_regles.text_edit.append("Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            return
        
        # Récupérer le dernier fichier d'ontologie chargé (.owl)
        input_owl = self.model.ontologies[-1]
        # Définir le chemin pour le fichier TTL
        ttl_path = os.path.join(os.getcwd(), "ontology.ttl")
        
        self.view.page_extraction_regles.text_edit.append(f"Conversion de l'ontologie {input_owl} en Turtle...")
        if not convert_owl_to_ttl(input_owl, ttl_path):
            self.view.page_extraction_regles.text_edit.append("La conversion de l'ontologie en TTL a échoué.")
            return
        
        
        # Récupérer les paramètres saisis par l'utilisateur
        minc = self.view.lineedit_minc.text().strip()   # pour -minc
        minpca = self.view.lineedit_minpca.text().strip() # pour -minpca
        nc = self.view.lineedit_nc.text().strip()         # pour -nc

        # Déterminer le chemin du fichier amie3.jar (dans le même répertoire que ce script)
        jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amie3.jar")
        if not os.path.exists(jar_path):
            self.view.page_extraction_regles.text_edit.append("Fichier amie3.jar introuvable.")
            return
        
        # Construire la commande
        command = [
            "java", "-jar", jar_path,
            "-minc", minc,
            "-minpca", minpca,
            "-nc", nc,
            ttl_path
        ]
        
        # Ajouter l'option -const si la case est cochée
        if self.view.checkbox_const.isChecked():
            command.insert(3, "-const")

        try:
            self.view.page_extraction_regles.text_edit.append("Lancement d'AMIE3...")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd(), universal_newlines=True)
            stdout, stderr = process.communicate(timeout=120)
            output = stdout

            self.view.page_extraction_regles.text_edit.append("Résultats d'AMIE3 :")
            self.view.page_extraction_regles.text_edit.append(output)
            self.afficher_page(2)
        except subprocess.TimeoutExpired:
            process.kill()
            self.view.page_extraction_regles.text_edit.append("L'exécution d'AMIE3 a dépassé le temps imparti.")
        except Exception as e:
            self.view.page_extraction_regles.text_edit.append(f"Erreur lors du lancement d'AMIE3: {e}")

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
