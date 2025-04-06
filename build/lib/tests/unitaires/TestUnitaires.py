import os
import tempfile
import unittest
from rdflib import Graph
from models.RuleExtractionModel import RuleExtractionModel


class TestUnitaires(unittest.TestCase):
    """
    Classe de tests unitaires pour les méthodes du modèle RuleExtractionModel.
    """

    def test_charger_ontologie_avec_fichier_existant(self):
        """
        Vérifie que la méthode 'charger_ontologie' retourne True
        et ajoute le chemin du fichier à la liste des ontologies
        lorsque le fichier existe réellement.
        """
        model = RuleExtractionModel()
        with tempfile.NamedTemporaryFile(suffix=".owl", delete=False) as tmp:
            tmp_path = tmp.name

        resultat = model.charger_ontologie(tmp_path)
        self.assertTrue(resultat)
        self.assertIn(tmp_path, model.ontologies)

        print("charger_ontologie avec fichier existant : succès")
        os.remove(tmp_path)

    def test_charger_ontologie_avec_fichier_inexistant(self):
        """
        Vérifie que la méthode 'charger_ontologie' retourne False
        et ne modifie pas la liste des ontologies lorsqu'on lui donne
        un chemin invalide ou inexistant.
        """
        model = RuleExtractionModel()
        chemin_fake = "nullepart.owl"

        resultat = model.charger_ontologie(chemin_fake)
        self.assertFalse(resultat)
        self.assertNotIn(chemin_fake, model.ontologies)

        print("charger_ontologie avec fichier inexistant : échec attendu")


    def test_sauvegarder_regles(self):
        """
        Vérifie que la méthode 'sauvegarder_regles' crée correctement un fichier CSV
        avec les règles validées, et retourne True en cas de succès.
        """
        model = RuleExtractionModel()
        model.regles_validees = [
            ['règle1', '0.7', '0.8', '0.75', '50', '2', '2', '?x', '']
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name

        resultat = model.sauvegarder_regles(tmp_path)
        self.assertTrue(resultat)
        self.assertTrue(os.path.exists(tmp_path))

        with open(tmp_path, "r", encoding="utf-8") as f:
            contenu = f.read()
            self.assertIn("Rule;Head Coverage;Std Confidence", contenu)
            self.assertIn("règle1", contenu)

        print("sauvegarder_regles : fichier créé et contenu conforme")
        os.remove(tmp_path)


    def test_convert_owl_to_ttl(self):
        """
        Vérifie que la méthode 'convert_owl_to_ttl' convertit bien un fichier OWL valide
        en un fichier Turtle (.ttl) et retourne True.
        """
        model = RuleExtractionModel()

        owl_content = """<?xml version="1.0"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                xmlns:owl="http://www.w3.org/2002/07/owl#"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
                xmlns:ex="http://example.org/ontology#">

            <owl:Ontology rdf:about="http://example.org/ontology"/>

            <owl:Class rdf:about="http://example.org/ontology#Person"/>
        </rdf:RDF>
        """

        with tempfile.NamedTemporaryFile(suffix=".owl", delete=False, mode='w', encoding="utf-8") as tmp_in:
            tmp_in.write(owl_content)
            input_path = tmp_in.name

        with tempfile.NamedTemporaryFile(suffix=".ttl", delete=False) as tmp_out:
            output_path = tmp_out.name

        result = model.convert_owl_to_ttl(input_path, output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))

        g = Graph()
        g.parse(output_path, format="turtle")
        self.assertGreater(len(g), 0)

        print("convert_owl_to_ttl : conversion réussie et fichier .ttl valide")

        os.remove(input_path)
        os.remove(output_path)



    def test_mesurer_regle(self):
        """
        Vérifie que 'mesurer_regle' retourne bien des métriques calculées à partir d'une règle RDF simple.
        """
        model = RuleExtractionModel()

        ttl_content = """
        @prefix : <http://example.org/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        :Person a owl:Class .
        :City a owl:Class .
        :livesIn a owl:ObjectProperty .

        :alice a :Person .
        :bob a :Person .
        :paris a :City .

        :alice :livesIn :paris .
        :bob :livesIn :paris .
        """

        with tempfile.NamedTemporaryFile(suffix=".ttl", delete=False, mode='w', encoding="utf-8") as tmp:
            tmp.write(ttl_content)
            ttl_path = tmp.name

        model.charger_ontologie(ttl_path)

        model.onto_classes = {
            'Person': 'http://example.org/Person',
            'City': 'http://example.org/City'
        }
        model.onto_properties = {
            'livesIn': 'http://example.org/livesIn'
        }

        regle = "Person(?x) $ livesIn(?x, ?y) -> City(?y)"

        result = model.mesurer_regle(regle)

        self.assertIsInstance(result, dict)
        self.assertIn('Confiance', result)
        self.assertGreaterEqual(result['Support'], 0)
        self.assertIn('Lift', result)

        print("mesurer_regle : métriques calculées avec succès")

        os.remove(ttl_path)



if __name__ == '__main__':
    unittest.main()