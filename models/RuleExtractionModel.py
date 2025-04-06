import os
from rdflib import Graph, URIRef, RDF, RDFS, OWL, BNode
import networkx as nx


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
