import os
import re
import subprocess
import sys


sys.path.insert(1,"../views/")
import networkx as nx
import pyparsing
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QTextEdit
from matplotlib import pyplot as plt
from rdflib import Graph, URIRef, RDF, RDFS, OWL, BNode





class RuleExtractionController:
    """
    Contrôleur principal pour l'extraction de règles à partir d'une ontologie RDF/OWL.

    Ce contrôleur relie la vue (interface utilisateur) et le modèle (données et logique métier).
    Il gère :
    - les signaux connectés à l'interface utilisateur,
    - le chargement et la visualisation d'ontologies,
    - l'extraction et la validation de règles avec AMIE3,
    - l'affichage de graphes RDF,
    - l'exécution de requêtes SPARQL,
    - et les mesures de qualité des règles extraites.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        """
        Connecte tous les boutons et éléments interactifs de l'interface utilisateur
        aux méthodes du contrôleur correspondant à leur logique fonctionnelle.
        """
        # Gestion ontologies
        self.view.btn_charger_ontologie.clicked.connect(self.do_charger_ontologie)
        self.view.btn_visualiser_ontologie.clicked.connect(self.do_visualiser_ontologie)

        # Bouton "Afficher le graphe"
        self.view.page_gestion_onto.btn_afficher_graphe.clicked.connect(self.do_afficher_graphe_ontologie)

        # Extraction des règles
        self.view.btn_lister_regles.clicked.connect(self.do_lister_regles)
        self.view.btn_visualiser_regles.clicked.connect(self.do_visualiser_regles)
        self.view.btn_afficher_regles_validees.clicked.connect(self.do_lister_regles_validees)
        self.view.btn_sauver_regle.clicked.connect(self.do_sauvegarder_regles)
        self.view.btn_supp_regle.clicked.connect(self.do_supprimer_regles_valides)
        self.view.btn_sauver_regles.clicked.connect(self.sauvegarder_regles_extraites_fichier)

        # Qualité / Validation
        self.view.btn_mesurer_qualite_regle.clicked.connect(lambda: self.view.fenetre_saisie_regle.show())
        self.view.fenetre_saisie_regle.btn_valider_saisie.clicked.connect(lambda: self.do_mesurer_qualite_regle())
        self.view.fenetre_saisie_regle.btn_aide_proprietes.clicked.connect(self.afficher_proprietes)
        self.view.fenetre_saisie_regle.btn_aide_classes.clicked.connect(lambda: self.afficher_classes())

        self.view.btn_mesurer_qualite_regles.clicked.connect(self.view.fenetre_saisie_ens_regles.show)
        self.view.fenetre_saisie_ens_regles.btn_mesurer_regles.clicked.connect(self.do_mesurer_qualite_regles)
        self.view.btn_valider_regle.clicked.connect(self.do_valider_regle)

        # Analyse des données
        self.view.btn_interroger_donnees.clicked.connect(lambda: self.view.fenetre_requete.show())
        self.view.btn_tester_hypothese.clicked.connect(lambda: self.afficher_page(4))
        self.view.btn_marquer_donnees.clicked.connect(lambda: self.afficher_page(4))
        self.view.fenetre_requete.btn_executer_requete.clicked.connect(self.executer_requete)

        # Comparaison
        # self.view.btn_comparer_resultats.clicked.connect(lambda: self.afficher_page(5))
        self.view.btn_comparer_resultats.clicked.connect(self.do_comparer_resultats)
        self.view.page_comparaison.btn_charger_fichier.clicked.connect(self.charger_fichier_regles)

        # Bouton AMIE3
        self.view.btn_lancer_amie3.clicked.connect(self.extraire_regles_amie3)

        # Bouton Lancer AMIE3 + Sauvegarder
        self.view.btn_lancer_amie3_save.clicked.connect(self.do_lancer_amie3_avec_sauvegarde)

        # Boutons de zoom
        self.view.btn_zoom_in.clicked.connect(self.zoom_in)
        self.view.btn_zoom_out.clicked.connect(self.zoom_out)
        self.view.btn_reset_view.clicked.connect(self.reset_view)



    def do_charger_ontologie(self):
        """
        Ouvre une boîte de dialogue pour sélectionner un fichier OWL, le charge dans le modèle,
        et affiche une notification de confirmation ou d'erreur.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Charger une ontologie", "",
            "Fichiers OWL (*.owl);;Tous les fichiers (*)"
        )
        if file_path:
            if self.model.charger_ontologie(file_path):
                self.view.page_gestion_onto.text_edit.append(f"Ontologie chargée : {file_path}")
                QMessageBox.information(self.view, "Chargement",
                                        f"L'ontologie a été chargée avec succès.\nChemin : {file_path}")

                self.model.charger_classes_et_proprietes()
            else:
                QMessageBox.warning(self.view, "Erreur", "Le fichier sélectionné n'a pas pu être chargé.")

    def do_visualiser_ontologie(self):
        """
        Affiche la page de visualisation de l'ontologie si une ontologie est chargée.
        """
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
            self.model.generer_arbre_classes_networkx(owl_file=dernier_onto, output_image=image_path, fig_width=18, fig_height=12)

            self.view.afficher_graphe(image_path)

        except Exception as e:
            QMessageBox.warning(self.view, "Erreur", f"Impossible de générer le graphe : {e}")


    def do_extraire_regles(self):
        """
        Extrait une règle via le modèle et l’affiche dans l’interface utilisateur.
        """
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
        """
        Affiche toutes les règles extraites dans le tableau de résultats.
        """
        if len(self.model.regles) != 0:
            self.view.btn_valider_regle.setEnabled(True)
            columns = ['Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence', 'Positive Examples', 'Body size',
                       'PCA Body size', 'Functional variable', '']
            self.view.page_extraction_regles.table_resultats.clear()
            self.view.page_extraction_regles.table_resultats.setColumnCount(len(columns))
            self.view.page_extraction_regles.table_resultats.setRowCount(len(self.model.regles))
            self.view.page_extraction_regles.table_resultats.setHorizontalHeaderLabels(columns)

            for index_ligne, regle in enumerate(self.model.regles):
                for index_colonne, colonne in enumerate(regle):
                    self.view.page_extraction_regles.table_resultats.setItem(index_ligne, index_colonne,
                                                                             QTableWidgetItem(colonne))
                checkbox = QTableWidgetItem("Valider")
                checkbox.setCheckState(0)
                self.view.page_extraction_regles.table_resultats.setItem(index_ligne, len(columns) - 1, checkbox)

            self.view.page_extraction_regles.table_resultats.setHorizontalHeaderItem(len(columns) - 1,
                                                                                     QTableWidgetItem(''))
            self.view.btn_supp_regle.setEnabled(False)

            self.afficher_page(2)

    def do_lister_regles_validees(self):
        """
        Affiche les règles validées dans le tableau de résultats.
        """
        if len(self.model.regles_validees) != 0:
            columns = ['Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence', 'Positive Examples', 'Body size',
                       'PCA Body size', 'Functional variable', '']
            self.view.page_extraction_regles.table_resultats.clear()
            self.view.page_extraction_regles.table_resultats.setColumnCount(len(columns))
            self.view.page_extraction_regles.table_resultats.setRowCount(len(self.model.regles_validees))

            self.view.page_extraction_regles.table_resultats.setHorizontalHeaderLabels(columns)

            for index_ligne, regle in enumerate(self.model.regles_validees):
                for index_colonne, colonne in enumerate(regle):
                    self.view.page_extraction_regles.table_resultats.setItem(index_ligne, index_colonne,
                                                                             QTableWidgetItem(colonne))
                    checkbox = QTableWidgetItem("Supprimer")
                    checkbox.setCheckState(0)
                    self.view.page_extraction_regles.table_resultats.setItem(index_ligne, len(columns) - 1, checkbox)

            self.view.page_extraction_regles.table_resultats.setHorizontalHeaderItem(len(columns) - 1,
                                                                                     QTableWidgetItem(''))
            self.view.btn_sauver_regle.setEnabled(True)
            self.view.btn_supp_regle.setEnabled(True)

            self.afficher_page(2)

    def do_visualiser_regles(self):
        """
        Affiche toutes les règles extraites sous forme textuelle dans l'interface.
        """

        self.view.page_extraction_regles.text_edit.append("Détails des règles extraites :")
        for regle in self.model.regles:
            self.view.page_extraction_regles.text_edit.append(str(regle))
        self.afficher_page(2)

    def do_sauvegarder_regles(self):
        """
        Ouvre une boîte de dialogue pour sauvegarder les règles validées dans un fichier CSV.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Sauvegarder les règles validees", "", "CSV (*.csv)"
        )
        if file_path:
            if self.model.sauvegarder_regles(file_path):
                QMessageBox.information(self.view, "Sauvegarde", "Les règles ont été sauvegardées avec succès.")
            else:
                QMessageBox.warning(self.view, "Erreur", "Une erreur est survenue lors de la sauvegarde.")
        self.afficher_page(2)

    def sauvegarder_regles_extraites_fichier(self):
        """
        Sauvegarde toutes les règles extraites (y compris non validées) dans un fichier CSV.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Sauvegarder les règles validees", "", "CSV (*.csv)"
        )
        if file_path:
            if self.model.sauvegarder_regles_extraites(file_path):
                QMessageBox.information(self.view, "Sauvegarde", "Les règles ont été sauvegardées avec succès.")
            else:
                QMessageBox.warning(self.view, "Erreur", "Une erreur est survenue lors de la sauvegarde.")
        self.afficher_page(2)

    def do_mesurer_qualite_regle(self):
        """
        Mesure la qualité d'une règle saisie par l'utilisateur via l'interface,
        affiche les résultats dans le tableau dédié et passe à la page de résultats.
        """

        regle = self.view.fenetre_saisie_regle.champ_saisie.text()
        result = self.model.mesurer_regle(regle)
        self.afficher_resultats_mesure_regle(result)
        self.afficher_page(3)


    def afficher_resultats_mesure_regle(self, result):
        """
        Affiche les résultats de qualité (support, confiance, etc.) pour une seule règle
        dans le tableau prévu à cet effet sur la page de qualité.
        """

        self.view.page_qualite.table.clear()
        self.view.page_qualite.table.setColumnCount(len(result.keys()))
        self.view.page_qualite.table.setRowCount(1)
        self.view.page_qualite.table.setHorizontalHeaderLabels(result.keys())
        index_colonne = 0
        for colonne in result.keys():
            self.view.page_qualite.table.setItem(0, index_colonne, QTableWidgetItem(str(result[colonne])))
            index_colonne += 1

    def do_mesurer_qualite_regles(self):
        """
        Mesure la qualité de plusieurs règles saisies par l'utilisateur dans une zone de texte
        et affiche les résultats pour chaque règle dans le tableau.
        """
        regles = self.view.fenetre_saisie_ens_regles.champ_saisie.toPlainText().split('\n')
        self.view.fenetre_saisie_ens_regles.close()
        results = []
        for regle in regles:
            results.append(self.model.mesurer_regle(regle))

        self.view.page_qualite.table.clear()

        self.view.page_qualite.table.setColumnCount(len(results[0].keys()))
        self.view.page_qualite.table.setHorizontalHeaderLabels(results[0].keys())
        self.view.page_qualite.table.setRowCount(len(results))

        self.afficher_resultats_mesure_regles(results)
        self.afficher_page(3)

    def afficher_resultats_mesure_regles(self, results):
        """
        Affiche dans un tableau les mesures de qualité pour un ensemble de règles.
        """
        for index_ligne, result in enumerate(results):
            for index_colonne, colonne in enumerate(result.keys()):
                self.view.page_qualite.table.setItem(index_ligne, index_colonne, QTableWidgetItem(str(result[colonne])))

    def do_valider_regle(self):
        """
        Valide les règles cochées dans le tableau et les transfère dans la liste des règles validées.
        Supprime ces règles de la liste des règles extraites.
        """
        index_validees = []
        for index in range(self.view.page_extraction_regles.table_resultats.rowCount()):
            if self.view.page_extraction_regles.table_resultats.item(index,
                                                                     self.view.page_extraction_regles.table_resultats.columnCount() - 1).checkState() != 0:
                ligne = []
                for index2 in range(self.view.page_extraction_regles.table_resultats.columnCount() - 1):
                    ligne.append(self.view.page_extraction_regles.table_resultats.item(index, index2).text())
                self.model.regles_validees.append(ligne)
                index_validees.append(index)
        if len(index_validees) == 0:
            QMessageBox.warning(self.view, "Erreur", "Aucune règle a été selectionnée")
            return

        self.model.regles = [regle for index, regle in enumerate(self.model.regles) if index not in index_validees]
        self.do_lister_regles()
        self.view.btn_valider_regle.setEnabled(False)
        self.view.btn_afficher_regles_validees.setEnabled(True)

    def do_supprimer_regles_valides(self):
        """
        Supprime les règles validées sélectionnées et les remet dans la liste des règles extraites.
        Met à jour les boutons et le tableau en conséquence.
        """
        index_a_supprimer = []
        for index in range(self.view.page_extraction_regles.table_resultats.rowCount()):
            if self.view.page_extraction_regles.table_resultats.item(index,
                                                                     self.view.page_extraction_regles.table_resultats.columnCount() - 1).checkState() != 0:
                for index2 in range(self.view.page_extraction_regles.table_resultats.columnCount() - 1):
                    index_a_supprimer.append(index)
        if len(index_a_supprimer) == 0:
            QMessageBox.warning(self.view, "Erreur", "Aucune règle a été selectionnée")
            return

        a_rajouter = [regle for index, regle in enumerate(self.model.regles_validees) if index in index_a_supprimer]
        self.model.regles_validees = [regle for index, regle in enumerate(self.model.regles_validees) if
                                      index not in index_a_supprimer]
        self.do_lister_regles()

        self.model.regles += a_rajouter

        if len(self.model.regles_validees) == 0:
            self.view.btn_supp_regle.setEnabled(False)
            self.view.btn_sauver_regle.setEnabled(False)
            self.view.btn_afficher_regles_validees.setEnabled(False)

            QMessageBox.warning(self.view, "Message",
                                "Toutes les règles validées ont été supprimées")
            self.do_lister_regles()
        else:
            self.do_lister_regles_validees()



    def extraire_regles_amie3(self):
        """
        Lance AMIE3, enregistre les règles extraites dans le modèle, puis les affiche dans l’interface.
        """
        resultat = self.do_lancer_amie3()
        if not resultat is None:
            self.model.sauvegarder_regles_amie3(resultat)
            self.afficher_resultats_amie3(resultat)
            self.view.btn_sauver_regles.setEnabled(True)
            self.afficher_page(2)
        return

    def do_comparer_resultats(self):
        """
        Compare les règles extraites avec les règles chargées ou celles extraites par AMIE3.
        Affiche les résultats dans la page de comparaison.
        """
        if len(self.model.regles + self.model.regles_validees) == 0:
            output = self.do_lancer_amie3()
            if output:
                self.afficher_page(5)
                self.afficher_resultats_amie3_dans_table(output, self.view.page_comparaison.table_amie)
        else:
            self.view.page_comparaison.table_amie.clear()
            self.view.page_comparaison.table_amie.setColumnCount(1)
            self.view.page_comparaison.table_amie.setRowCount(len(self.model.regles + self.model.regles_validees))
            self.view.page_comparaison.table_amie.setHorizontalHeaderLabels(["Règle AMIE3"])

            for i, ligne in enumerate(self.model.regles + self.model.regles_validees):
                self.view.page_comparaison.table_amie.setItem(i, 0, QTableWidgetItem(ligne[0]))
            self.afficher_page(5)

    def afficher_resultats_amie3_dans_table(self, amie_result, table_widget):
        """
        Affiche les règles extraites par AMIE3 dans une table donnée.
        """
        lines = amie_result.split('\n')
        index = 0
        while index < len(lines) and not lines[index].__contains__("=>"):
            index += 1

        regles = [l.split('\t')[0] for l in lines[index:] if "=>" in l]

        table_widget.clear()
        table_widget.setColumnCount(1)
        table_widget.setRowCount(len(regles))
        table_widget.setHorizontalHeaderLabels(["Règle AMIE3"])

        for i, regle in enumerate(regles):
            table_widget.setItem(i, 0, QTableWidgetItem(regle))

    def charger_fichier_regles(self):
        """
        Charge un fichier contenant des règles textuelles et les affiche dans la table de comparaison.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Charger un fichier de règles", "", "Text files (*.txt *.csv);;All files (*)"
        )
        if file_path:
            with open(file_path, encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            self.view.page_comparaison.table_fichier.clear()
            self.view.page_comparaison.table_fichier.setRowCount(len(lines))
            self.view.page_comparaison.table_fichier.setColumnCount(1)
            self.view.page_comparaison.table_fichier.setHorizontalHeaderLabels(["Règle chargée"])

            for i, line in enumerate(lines):
                self.view.page_comparaison.table_fichier.setItem(i, 0, QTableWidgetItem(line))

    
    def do_lancer_amie3(self):
        """
        Lance l'exécution de l'outil AMIE3 après conversion de l'ontologie OWL en Turtle.
        Vérifie les prérequis et construit la commande avant exécution.
        Retourne la sortie standard si l'exécution réussit.
        """
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur", "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            self.afficher_page(2)
            return

        input_owl = self.model.ontologies[-1]
        ttl_path = os.path.join(os.getcwd(), "ontology.ttl")

        QMessageBox.warning(self.view, "En cours", f"Conversion de l'ontologie {input_owl} en Turtle...")
        if not self.model.convert_owl_to_ttl(input_owl, ttl_path):
            QMessageBox.warning(self.view, "Erreur", "La conversion de l'ontologie en TTL a échoué.")
            self.afficher_page(2)
            return

        amie_params = self.view.amie3_params_widget.build_amie3_params()
        jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amie3.jar")

        if not os.path.exists(jar_path):
            QMessageBox.warning(self.view, "Erreur", "Fichier amie3.jar introuvable.")
            self.afficher_page(2)
            return

        command = ["java", "-jar", jar_path] + amie_params + [ttl_path]

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate(timeout=120)
            return stdout
        except subprocess.TimeoutExpired:
            process.kill()
            QMessageBox.warning(self.view, "Erreur", "L'exécution d'AMIE3 a dépassé le temps imparti.")
            self.afficher_page(2)
        except Exception as e:
            QMessageBox.warning(self.view, "Erreur", f"Erreur lors du lancement d'AMIE3: {e}")
            self.afficher_page(2)

        os.remove(ttl_path)

    def do_lancer_amie3_avec_sauvegarde(self):
        """
        Lance AMIE3 et enregistre la sortie dans un fichier texte ou CSV selon le format choisi par l'utilisateur.
        Affiche les résultats extraits après l'exécution.
        """
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur", "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            self.afficher_page(2)
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self.view,
            "Enregistrer la sortie d'AMIE3",
            "",
            "Fichiers texte (*.txt);;Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )

        if not output_file:
            return

        resultat = self.do_lancer_amie3()

        if output_file.split('.')[-1] == 'csv':
            self.mode.amie_to_csv(output_file, resultat)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(resultat)

        self.afficher_resultats_amie3(resultat)
        self.afficher_page(2)

    def afficher_page(self, index):
        """
        Change la page affichée dans le stacked widget de l'interface.
        """
        self.view.stacked_widget.setCurrentIndex(index)

    def zoom_in(self):
        """
        Agrandit la taille de police des QTextEdit sur la page actuellement affichée.
        """
        current_page = self.view.stacked_widget.currentWidget()
        if current_page:
            for child in current_page.findChildren(QTextEdit):
                font = child.font()
                font.setPointSize(font.pointSize() + 1)
                child.setFont(font)

    def zoom_out(self):
        """
        Réduit la taille de police des QTextEdit sur la page actuellement affichée.
        """
        current_page = self.view.stacked_widget.currentWidget()
        if current_page:
            for child in current_page.findChildren(QTextEdit):
                font = child.font()
                new_size = max(1, font.pointSize() - 1)
                font.setPointSize(new_size)
                child.setFont(font)

    def reset_view(self):
        """
        Réinitialise la taille de police des QTextEdit à 10 points sur la page actuelle.
        """
        current_page = self.view.stacked_widget.currentWidget()
        if current_page:
            for child in current_page.findChildren(QTextEdit):
                font = child.font()
                font.setPointSize(10)
                child.setFont(font)

    def executer_requete(self):
        """
        Exécute une requête SPARQL saisie dans l’interface sur l'ontologie chargée,
        et affiche les résultats dans la page d'analyse.
        """
        self.view.fenetre_requete.close()
        self.afficher_page(4)
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur", "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            return

        g = Graph()
        g.parse(self.model.ontologies[-1])

        try:
            results = g.query(self.view.fenetre_requete.champ_saisie.toPlainText())
        except pyparsing.exceptions.ParseException:
            QMessageBox.warning(self.view, "Erreur", "Erreur lors de la saisie de la requête")
            return

        self.afficher_resultats_requete(results)

    def afficher_resultats_requete(self, results):
        """
        Affiche les résultats d'une requête SPARQL dans un tableau de la page d’analyse.
        """
        liste_variables = [x.toPython()[1:] for x in results.vars]
        self.view.page_analyse.table.clear()
        self.view.page_analyse.table.setColumnCount(len(liste_variables))
        self.view.page_analyse.table.setRowCount(len(results))
        self.view.page_analyse.table.setHorizontalHeaderLabels([x.toPython() for x in results.vars])
        index_ligne = 0
        index_colonne = 0
        for row in results:
            for var in liste_variables:
                self.view.page_analyse.table.setItem(index_ligne, index_colonne, QTableWidgetItem(row[var]))
                index_colonne += 1
            index_ligne += 1
            index_colonne = 0

    def afficher_resultats_amie3(self, amie_result):
        """
        Affiche les résultats extraits par AMIE3 dans un tableau de la page extraction.
        """
        index = 0
        lines = amie_result.split('\n')
        while not "=>" in lines[index]:
            index += 1

        columns = ['Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence', 'Positive Examples', 'Body size',
                'PCA Body size', 'Functional variable']
        lines = lines[index:]

        self.view.page_extraction_regles.table_resultats.clear()
        self.view.page_extraction_regles.table_resultats.setColumnCount(len(columns))
        self.view.page_extraction_regles.table_resultats.setHorizontalHeaderLabels(columns)
        regles = [line.split('\t') for line in lines if "=>" in line]
        self.view.page_extraction_regles.table_resultats.setRowCount(len(regles))

        for index_ligne, regle in enumerate(regles):
            for index_colonne in range(len(regle)):
                self.view.page_extraction_regles.table_resultats.setItem(index_ligne, index_colonne,
                                                                        QTableWidgetItem(regle[index_colonne]))

    def afficher_classes(self):
        """
        Affiche la liste des classes disponibles dans l'ontologie chargée.
        """
        if self.model.ontologies:
            self.view.fenetre_saisie_regle.box_classes.setDetailedText('\n'.join(self.model.onto_classes.keys()))
            self.view.fenetre_saisie_regle.box_classes.show()
        else:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")

    def afficher_proprietes(self):
        """
        Affiche la liste des propriétés disponibles dans l'ontologie chargée.
        """
        if self.model.ontologies:
            self.view.fenetre_saisie_regle.box_properties.setDetailedText('\n'.join(self.model.onto_properties.keys()))
            self.view.fenetre_saisie_regle.box_properties.show()
        else:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")
