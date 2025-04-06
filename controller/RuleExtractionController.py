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

                self.model.charger_classes_et_proprietes()
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

            self.view.afficher_graphe(image_path)

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
        self.view.page_extraction_regles.text_edit.append("Détails des règles extraites :")
        for regle in self.model.regles:
            self.view.page_extraction_regles.text_edit.append(str(regle))
        self.afficher_page(2)

    def do_sauvegarder_regles(self):
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
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Sauvegarder les règles validees", "", "CSV (*.csv)"
        )
        if file_path:
            if self.model.sauvegarder_regles_extraites(file_path):
                QMessageBox.information(self.view, "Sauvegarde", "Les règles ont été sauvegardées avec succès.")
            else:
                QMessageBox.warning(self.view, "Erreur", "Une erreur est survenue lors de la sauvegarde.")
        self.afficher_page(2)

    # Fonctions de qualité et validation (simulées)
    def do_mesurer_qualite_regle(self):
        # self.view.page_qualite.text_edit.append("Mesure de qualité pour la règle sélectionnée :")
        # self.view.page_qualite.text_edit.append("Support : 0.65, Confiance : 0.80")

        regle = self.view.fenetre_saisie_regle.champ_saisie.text()
        result = self.mesurer_regle(regle)
        self.afficher_resultats_mesure_regle(result)
        self.afficher_page(3)

    def mesurer_regle(self, regle):
        body, head = regle.split('->')
        head = head[1:]
        # Extraction des variables de la règle entière
        variables = set(re.findall('\\' + "?" + "[a-zA-Z0-9_]+", regle))

        # Extraction des variables de la partie gauche de la règle
        variables_body = set(re.findall('\\' + "?" + "[a-zA-Z0-9_]+", body))
        # Extraction des variables de la partie droite de la règle
        variables_head = set(re.findall('\\' + "?" + "[a-zA-Z0-9_]+", head))

        # Conversion partie gauche de la règle en requête SPARQL

        body_parts = [x.rstrip(' ') for x in body.split('$')]
        if len(head.split('$')) != 1:
            QMessageBox.warning(self.view, "Erreur",
                                "Une seule conclusion dans la partie droite de la règle")
            return
        filters = []
        # Si y'a des filtres SPARQL a gauche de la regle
        check_filter = [True if part.startswith("FILTER(") else False for part in body_parts]
        nb_filters = 0
        if any(check_filter):
            for atome in body_parts:
                if atome.startswith("FILTER("):
                    nb_filters += 1
                    filters += re.findall(r'\(([^\)]+)\)', atome)[-1].split(',')

            if nb_filters > 1:
                print('Erreur :  Trop de filtres')
                QMessageBox.warning(self.view, "Erreur",
                                    "Trop de filtres. Un seul atome doit representer les filtres")
                return
            # RETIRER Les filtres
            body_parts = [body_parts[index] for index, value in enumerate(check_filter) if not value]

        body_to_sparql = []

        for atome in body_parts:
            # Propriété
            prop = re.findall(r'\w+\(', atome)[-1][:-1]

            # Contenu des parentheses
            elts = re.findall(r'\(([^\)]+)\)', atome)[0].split(',')
            if len(elts) == 1:
                body_to_sparql.append(elts[0] + ' a ' + '<' + self.model.onto_classes[prop] + '>')
            elif len(elts) == 2:
                body_to_sparql.append(elts[0] + ' ' + '<' + self.model.onto_properties[prop] + '>' + ' ' + elts[1])
            else:
                QMessageBox.warning(self.view, "Erreur",
                                    "Contrainte de triplet no respectée dans la partie gauche de la règle")
                return

        body_query = '.\n'.join(body_to_sparql) + '.'

        if len(filters) > 0:
            body_query += ' ' + '\nFILTER( ' + ' '.join(filters) + ' ).'
        # Conversion partie droite de la règle en requête SPARQL
        head_query = " "

        prop_head = re.findall(r'\w+\(', head)[-1][:-1]
        # Contenu des parentheses
        elts = re.findall(r'\(([^\)]+)\)', head)[0].split(',')

        if len(elts) == 1:
            head_query = elts[0] + ' a ' + '<' + self.model.onto_classes[prop_head] + '>' + '.'

        elif len(elts) == 2:
            head_query = elts[0] + ' ' + '<' + self.model.onto_properties[prop_head] + '>' + ' ' + elts[1] + '.'
        else:
            QMessageBox.warning(self.view, "Erreur",
                                "Contrainte de triplet no respectée dans la partie droite de la règle")
            return

        # Requête SPARQL pour la partie gauche de la règle
        body_full_query = "SELECT DISTINCT " + ' '.join(variables_body) + "\nWHERE{\n" + body_query + "\n}"
        # Requête SPARQL pour la partie droite de la règle
        head_full_query = "SELECT DISTINCT " + ' '.join(variables_head) + "\nWHERE{\n" + head_query + "\n}"

        # Requête SPARQL pour la règle entière
        rule_full_query = "SELECT DISTINCT " + ' '.join(
            variables) + "\nWHERE{\n" + head_query + '\n' + body_query + "\n}"

        g = Graph()
        g.parse(self.model.ontologies[-1])


        query_body = g.query(body_full_query)
        query_head = g.query(head_full_query)
        rule_query = g.query(rule_full_query)

        try:
            confiance = len(rule_query) / len(query_body)
        except ZeroDivisionError:
            confiance = 0
        support = len(rule_query)
        try:
            lift = len(rule_query) / (len(query_body) * len(query_head))
        except ZeroDivisionError:
            lift = 0
        instance_pos = len(rule_query)

        return {'Regle': ' '.join(body_parts) + ' => ' + head, 'Confiance': confiance, 'Support': support, 'Lift': lift,
                'Instances positives': instance_pos}

    def afficher_resultats_mesure_regle(self, result):

        self.view.page_qualite.table.clear()
        self.view.page_qualite.table.setColumnCount(len(result.keys()))
        self.view.page_qualite.table.setRowCount(1)
        self.view.page_qualite.table.setHorizontalHeaderLabels(result.keys())
        index_colonne = 0
        for colonne in result.keys():
            self.view.page_qualite.table.setItem(0, index_colonne, QTableWidgetItem(str(result[colonne])))
            index_colonne += 1

    def do_mesurer_qualite_regles(self):
        regles = self.view.fenetre_saisie_ens_regles.champ_saisie.toPlainText().split('\n')
        self.view.fenetre_saisie_ens_regles.close()
        results = []
        for regle in regles:
            results.append(self.mesurer_regle(regle))

        self.view.page_qualite.table.clear()

        self.view.page_qualite.table.setColumnCount(len(results[0].keys()))
        self.view.page_qualite.table.setHorizontalHeaderLabels(results[0].keys())
        self.view.page_qualite.table.setRowCount(len(results))

        self.afficher_resultats_mesure_regles(results)
        self.afficher_page(3)

    def afficher_resultats_mesure_regles(self, results):
        for index_ligne, result in enumerate(results):
            for index_colonne, colonne in enumerate(result.keys()):
                self.view.page_qualite.table.setItem(index_ligne, index_colonne, QTableWidgetItem(str(result[colonne])))

    def do_valider_regle(self):
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

    # Fonction pour lancer AMIE3
    def extraire_regles_amie3(self):
        resultat = self.do_lancer_amie3()
        if not resultat is None:
            self.sauvegarder_regles_amie3(resultat)
            self.afficher_resultats_amie3(resultat)
            self.view.btn_sauver_regles.setEnabled(True)
            self.afficher_page(2)
        return

    def do_comparer_resultats(self):
        # Lancer AMIE3 automatiquement
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
        lines = amie_result.split('\n')
        index = 0
        while index < len(lines) and not lines[index].__contains__("=>"):
            index += 1

        regles = [l.split('\t')[0] for l in lines[index:] if "=>" in l]

        # Affichage dans la table
        table_widget.clear()
        table_widget.setColumnCount(1)
        table_widget.setRowCount(len(regles))
        table_widget.setHorizontalHeaderLabels(["Règle AMIE3"])

        for i, regle in enumerate(regles):
            table_widget.setItem(i, 0, QTableWidgetItem(regle))

    def charger_fichier_regles(self):
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
        # Vérifier qu'une ontologie a été chargée
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur",
                                "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
            self.afficher_page(2)
            return

        # Récupérer le dernier fichier d'ontologie chargé (.owl)
        input_owl = self.model.ontologies[-1]
        # Définir le chemin pour le fichier TTL
        ttl_path = os.path.join(os.getcwd(), "ontology.ttl")

        # Conversion en TTL
        QMessageBox.warning(self.view, "En cours", "Conversion de l'ontologie {input_owl} en Turtle...")
        if not convert_owl_to_ttl(input_owl, ttl_path):
            QMessageBox.warning(self.view, "Erreur", "La conversion de l'ontologie en TTL a échoué.")
            self.afficher_page(2)
            return

        # Récupérer la liste d'arguments dynamiques
        amie_params = self.view.amie3_params_widget.build_amie3_params()

        # Déterminer le chemin du fichier amie3.jar (dans le même répertoire que ce script)
        jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amie3.jar")
        if not os.path.exists(jar_path):
            QMessageBox.warning(self.view, "Erreur", "Fichier amie3.jar introuvable.")
            self.afficher_page(2)
            return

        # Construire la commande
        command = ["java", "-jar", jar_path] + amie_params + [ttl_path]

        # self.view.page_extraction_regles.text_edit.append("Commande AMIE3 : " + " ".join(command))

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate(timeout=120)
            output = stdout

            # self.view.page_extraction_regles.text_edit.append("Résultats d'AMIE3 :")
            # self.view.page_extraction_regles.text_edit.append(output)
            return output
        except subprocess.TimeoutExpired:
            process.kill()
            QMessageBox.warning(self.view, "Erreur", "L'exécution d'AMIE3 a dépassé le temps imparti.")
            self.afficher_page(2)
        except Exception as e:
            QMessageBox.warning(self.view, "Erreur", "Erreur lors du lancement d'AMIE3: {e}")
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

        if output_file.split('.')[-1] == 'csv':
            self.amie_to_csv(output_file, resultat)
        else:
            # Enregistrer la sortie stdout
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(resultat)

        self.afficher_resultats_amie3(resultat)

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
        self.view.fenetre_requete.close()
        self.afficher_page(4)
        if not self.model.ontologies:
            QMessageBox.warning(self.view, "Erreur",
                                "Aucune ontologie chargée. Veuillez charger une ontologie d'abord.")
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

    def amie_to_csv(self, file_path, amie_result):
        index = 0
        lines = amie_result.split('\n')

        # Arriver jusqu'au colonnes
        while not lines[index].startswith("Starting the mining phase..."):
            index += 1

        columns = lines[index + 1].split('\t')

        # On se place sur la première règle extraite
        lines = lines[index + 2:]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(';'.join(columns) + '\n')
                for line in lines:
                    if line.__contains__("=>"):
                        f.write(';'.join(line.split('\t')) + '\n')
                f.close()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def afficher_resultats_amie3(self, amie_result):
        index = 0
        lines = amie_result.split('\n')

        # Arriver jusqu'au colonnes
        while not lines[index].__contains__("=>"):
            index += 1

        columns = ['Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence', 'Positive Examples', 'Body size',
                   'PCA Body size', 'Functional variable']
        # On se place sur la première règle extraite
        lines = lines[index:]

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
            # self.model.regles.append(regle)
            for index in range(len(regle)):
                self.view.page_extraction_regles.table_resultats.setItem(index_ligne, index,
                                                                         QTableWidgetItem(regle[index]))
            index_ligne += 1

    def afficher_classes(self):

        if self.model.ontologies:
            self.view.fenetre_saisie_regle.box_classes.setDetailedText('\n'.join(self.model.onto_classes.keys()))
            self.view.fenetre_saisie_regle.box_classes.show()
        else:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")

    def afficher_proprietes(self):

        if self.model.ontologies:
            self.view.fenetre_saisie_regle.box_properties.setDetailedText('\n'.join(self.model.onto_properties.keys()))
            self.view.fenetre_saisie_regle.box_properties.show()
        else:
            QMessageBox.information(self.view, "Information", "Aucune ontologie n'a été chargée.")

    def sauvegarder_regles_amie3(self, resultat):
        index = 0
        lines = resultat.split('\n')
        # Arriver à ma premiere règle
        while not lines[index].__contains__("=>"):
            index += 1

        lines = lines[index:]
        for line in lines:
            if line.__contains__("=>"):
                self.model.regles.append(line.split('\t'))