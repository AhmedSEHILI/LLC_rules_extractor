import os
from rdflib import Graph, URIRef, RDF, RDFS, OWL, BNode
import networkx as nx

class RuleExtractionModel:
    def __init__(self):
        self.ontologies = []  # Liste des chemins vers les ontologies chargées
        self.regles = []  # Liste des règles extraites
        self.regles_validees = []  # Liste des règles validées
        self.onto_classes = {}
        self.onto_properties = {}

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
        columns = ['Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence', 'Positive Examples', 'Body size',
                   'PCA Body size', 'Functional variable', '']
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(';'.join(columns) + '\n')
                for line in self.regles_validees:
                    f.write(';'.join(line) + '\n')
                f.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

    def sauvegarder_regles_extraites(self,file_path) :
        columns = ['Rule', 'Head Coverage', 'Std Confidence', 'PCA Confidence', 'Positive Examples', 'Body size',
                   'PCA Body size', 'Functional variable', '']
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(';'.join(columns) + '\n')
                for line in (self.regles_validees + self.regles):
                    f.write(';'.join(line) + '\n')
                f.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

    def charger_classes_et_proprietes(self):
        g = Graph()
        g.parse(self.ontologies[-1])



        #Liste des predicats
        for prop in list(g.predicates()):
            self.onto_properties[str(prop).split('#')[-1]] = str(prop)


        # Liste des classes
        for subj, pred, obj in g:
            if str(obj) == 'http://www.w3.org/2002/07/owl#Class' and type(subj) != BNode :
                self.onto_classes[str(subj).split('#')[-1]] = str(subj)
