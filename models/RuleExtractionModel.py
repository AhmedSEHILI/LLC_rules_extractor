import os
import re
from rdflib import Graph, URIRef, RDF, RDFS, OWL, BNode
import networkx as nx
from matplotlib import pyplot as plt



class RuleExtractionModel:
    """
    Modèle principal de l'application d'extraction de règles.

    Il gère le chargement des ontologies, l'extraction simulée des règles, 
    leur sauvegarde, ainsi que la récupération des classes et propriétés de l'ontologie.
    """

    def __init__(self):
        """
        Initialise les structures internes du modèle.
        """
        self.ontologies = []  # Liste des chemins vers les ontologies chargées
        self.regles = []  # Liste des règles extraites
        self.regles_validees = []  # Liste des règles validées
        self.onto_classes = {}  # Dictionnaire des classes extraites
        self.onto_properties = {}  # Dictionnaire des propriétés extraites

    def charger_ontologie(self, path):
        """
        Charge une ontologie depuis un fichier local.

        Args:
            path (str): Chemin vers le fichier de l'ontologie.

        Returns:
            bool: True si le fichier existe et est chargé, False sinon.
        """
        if os.path.exists(path):
            self.ontologies.append(path)
            return True
        return False

    def extraire_regles(self):
        """
        Simule l'extraction d'une règle logique.

        Returns:
            dict: Une règle contenant des métriques simulées.
        """
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
        """
        Sauvegarde les règles validées dans un fichier CSV.

        Args:
            file_path (str): Chemin du fichier de sortie.

        Returns:
            bool: True si la sauvegarde est réussie, False sinon.
        """
        columns = [
            'Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence',
            'Positive Examples', 'Body size', 'PCA Body size', 'Functional variable', ''
        ]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(';'.join(columns) + '\n')
                for line in self.regles_validees:
                    f.write(';'.join(line) + '\n')
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

    def sauvegarder_regles_extraites(self, file_path):
        """
        Sauvegarde toutes les règles (extraites + validées) dans un fichier CSV.

        Args:
            file_path (str): Chemin du fichier de sortie.

        Returns:
            bool: True si la sauvegarde est réussie, False sinon.
        """
        columns = [
            'Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence',
            'Positive Examples', 'Body size', 'PCA Body size', 'Functional variable', ''
        ]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(';'.join(columns) + '\n')
                for line in (self.regles_validees + self.regles):
                    f.write(';'.join(line) + '\n')
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

    def charger_classes_et_proprietes(self):
        """
        Extrait les classes et propriétés RDF/OWL à partir de la dernière ontologie chargée.

        Remplit les dictionnaires `onto_classes` et `onto_properties` avec les URI formatées.
        """
        g = Graph()
        g.parse(self.ontologies[-1])

        for prop in list(g.predicates()):
            self.onto_properties[str(prop).split('#')[-1]] = str(prop)

        for subj, pred, obj in g:
            if str(obj) == 'http://www.w3.org/2002/07/owl#Class' and not isinstance(subj, BNode):
                self.onto_classes[str(subj).split('#')[-1]] = str(subj)


    def convert_owl_to_ttl(self, input_file, output_file):
        try:
            g = Graph()
            g.parse(input_file, format='xml')
            g.serialize(destination=output_file, format='turtle')
            print(f"Fichier converti : {input_file} → {output_file}")
            return True
        except Exception as e:
            print(f"Erreur lors de la conversion OWL->TTL: {e}")
            return False


    def generer_arbre_classes_networkx(self, owl_file, output_image="classes_arbre.png", fig_width=10, fig_height=5):
        """
        Génère un graphe hiérarchique des classes d'une ontologie OWL et l'enregistre sous forme d'image.

        Les relations de sous-classes sont parcourues selon un parcours en largeur (BFS)
        pour déterminer la hiérarchie des classes, puis visualisées avec NetworkX et Matplotlib.

        Paramètres :
            owl_file (str) : Chemin du fichier OWL à analyser.
            output_image (str) : Nom du fichier image de sortie.
            fig_width (int) : Largeur de la figure.
            fig_height (int) : Hauteur de la figure.
        """
        g = Graph()
        g.parse(owl_file, format="xml")
        classes = set()
        for c in g.subjects(RDF.type, OWL.Class):
            if isinstance(c, URIRef):
                classes.add(c)
        for c in g.subjects(RDF.type, RDFS.Class):
            if isinstance(c, URIRef):
                classes.add(c)

        nx_graph = nx.DiGraph()
        for c in classes:
            nx_graph.add_node(str(c))
        for child in classes:
            for parent in g.objects(child, RDFS.subClassOf):
                if parent in classes:
                    nx_graph.add_edge(str(parent), str(child))

        roots = [n for n in nx_graph.nodes() if nx_graph.in_degree(n) == 0]
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

        level_dict = {}
        for node, lv in level.items():
            level_dict.setdefault(lv, []).append(node)

        pos = {}
        for lv, nodes_in_this_level in level_dict.items():
            nodes_in_this_level.sort()
            for i, node in enumerate(nodes_in_this_level):
                x = lv * 4
                y = -i * 9
                pos[node] = (x, y)

        labels = {}
        for node in nx_graph.nodes():
            uri_str = node
            if '#' in uri_str:
                local_name = uri_str.split('#')[-1]
            else:
                local_name = uri_str
            labels[node] = local_name

        plt.figure(figsize=(fig_width, fig_height))
        nx.draw(nx_graph, pos=pos, with_labels=False, node_size=100, node_color="#ccccff", arrowstyle="->", arrowsize=8, width=0.8)
        nx.draw_networkx_labels(nx_graph, pos, labels=labels, font_size=6)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_image, dpi=90)
        plt.close()


    def mesurer_regle(self, regle):
        """
        Évalue une règle logique en la convertissant en requêtes SPARQL pour calculer
        des métriques de qualité : confiance, support, lift, et nombre d'instances positives.

        La règle peut être au format 'corps -> tête' ou 'corps => tête'.

        Paramètre :
            regle (str) : Règle à évaluer.

        Retour :
            dict : Dictionnaire contenant les métriques calculées.
        """
        regle = regle.replace('=>', '->')
        body, head = regle.split('->')
        head = head[1:]
        variables = set(re.findall('\\' + "?" + "[a-zA-Z0-9_]+", regle))
        variables_body = set(re.findall('\\' + "?" + "[a-zA-Z0-9_]+", body))
        variables_head = set(re.findall('\\' + "?" + "[a-zA-Z0-9_]+", head))

        body_parts = [x.rstrip(' ') for x in body.split('$')]
        if len(head.split('$')) != 1:
            QMessageBox.warning(self.view, "Erreur", "Une seule conclusion dans la partie droite de la règle")
            return

        filters = []
        check_filter = [part.startswith("FILTER(") for part in body_parts]
        nb_filters = 0
        if any(check_filter):
            for atome in body_parts:
                if atome.startswith("FILTER("):
                    nb_filters += 1
                    filters += re.findall(r'\(([^\)]+)\)', atome)[-1].split(',')
            if nb_filters > 1:
                QMessageBox.warning(self.view, "Erreur", "Trop de filtres. Un seul atome doit représenter les filtres")
                return
            body_parts = [body_parts[i] for i, value in enumerate(check_filter) if not value]

        body_to_sparql = []
        for atome in body_parts:
            prop = re.findall(r'\w+\(', atome)[-1][:-1]
            elts = re.findall(r'\(([^\)]+)\)', atome)[0].split(',')
            if len(elts) == 1:
                body_to_sparql.append(elts[0] + ' a ' + '<' + self.onto_classes[prop] + '>')
            elif len(elts) == 2:
                body_to_sparql.append(elts[0] + ' ' + '<' + self.onto_properties[prop] + '>' + ' ' + elts[1])
            else:
                QMessageBox.warning(self.view, "Erreur", "Contrainte de triplet non respectée dans le corps de la règle")
                return

        body_query = '.\n'.join(body_to_sparql) + '.'
        if len(filters) > 0:
            body_query += ' ' + '\nFILTER( ' + ' '.join(filters) + ' ).'

        head_query = ""
        prop_head = re.findall(r'\w+\(', head)[-1][:-1]
        elts = re.findall(r'\(([^\)]+)\)', head)[0].split(',')
        if len(elts) == 1:
            head_query = elts[0] + ' a ' + '<' + self.onto_classes[prop_head] + '>' + '.'
        elif len(elts) == 2:
            head_query = elts[0] + ' ' + '<' + self.onto_properties[prop_head] + '>' + ' ' + elts[1] + '.'
        else:
            QMessageBox.warning(self.view, "Erreur", "Contrainte de triplet non respectée dans la tête de la règle")
            return

        body_full_query = "SELECT DISTINCT " + ' '.join(variables_body) + "\nWHERE{\n" + body_query + "\n}"
        head_full_query = "SELECT DISTINCT " + ' '.join(variables_head) + "\nWHERE{\n" + head_query + "\n}"
        rule_full_query = "SELECT DISTINCT " + ' '.join(variables) + "\nWHERE{\n" + head_query + '\n' + body_query + "\n}"

        g = Graph()
        g.parse(self.ontologies[-1])

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

        return {
            'Regle': ' '.join(body_parts) + ' => ' + head,
            'Confiance': confiance,
            'Support': support,
            'Lift': lift,
            'Instances positives': instance_pos
        }



    def amie_to_csv(self, file_path, amie_result):
        """
        Convertit le résultat brut d'AMIE3 en fichier CSV.

        Extrait les colonnes et les règles à partir du texte généré par AMIE3, puis les écrit dans un fichier CSV.

        Paramètres :
            file_path (str) : Chemin du fichier de sortie CSV.
            amie_result (str) : Résultat brut d'AMIE3 sous forme de texte.
        """
        index = 0
        lines = amie_result.split('\n')
        while not lines[index].startswith("Starting the mining phase..."):
            index += 1
        columns = lines[index + 1].split('\t')
        lines = lines[index + 2:]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(';'.join(columns) + '\n')
                for line in lines:
                    if "=>" in line:
                        f.write(';'.join(line.split('\t')) + '\n')
                f.close()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")




    def sauvegarder_regles_amie3(self, resultat):
        """
        Extrait les règles contenant '=>' à partir du résultat d'AMIE3, et les ajoute à la liste des règles du modèle.

        Paramètre :
            resultat (str) : Résultat brut d'AMIE3 (stdout).
        """
        index = 0
        lines = resultat.split('\n')
        while not lines[index].__contains__("=>"):
            index += 1
        lines = lines[index:]
        for line in lines:
            if "=>" in line:
                self.regles.append(line.split('\t'))
