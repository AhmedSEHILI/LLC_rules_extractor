# LLCrulesExtractor

**LLCrulesExtractor** est une application interactive en Python permettant d'extraire, visualiser, valider et analyser des règles à partir d'une ontologie RDF/OWL. Basée sur AMIE3, PyQt5 et RDFLib, elle fournit une interface graphique complète pour la manipulation de données sémantiques.

---

## 🚀 Fonctionnalités principales

- 📂 Chargement et visualisation d'ontologies OWL
- 🌳 Génération de graphe de classes avec NetworkX
- 🧠 Extraction de règles avec AMIE3
- ✅ Validation et sauvegarde des règles extraites
- 📊 Analyse de la qualité des règles (support, confiance, lift…)
- 🔍 Requêtes SPARQL personnalisées
- 🧪 Tests unitaires inclus

---

## 🧱 Architecture du projet

```
LLCrulesExtractor/
│
├── controller/            # Logique de contrôle (MVC)
│   └── RuleExtractionController.py
│
├── models/                # Gestion du modèle et des règles
│   └── RuleExtractionModel.py
│
├── views/                 # Interface utilisateur (PyQt5)
│   ├── *.py
│
├── tests/                 # Tests unitaires
│   └── unitaire/
│       └── test_model.py
│
├── app/
|   └── main.py            # Point d'entrée de l’application               
├── requirements.txt
├── setup.py               # Pour l'installation via pip
└── docs/                  # Documentation générée avec Sphinx
```

---

## 📦 Installation

### 🔧 Prérequis

- Python 3.8+
- Java (JDK 8 ou plus) pour faire tourner AMIE3
- AMIE3 (fichier `amie3.jar`) dans le dossier controller du projet

### 📥 Installation locale

1. Clone le dépôt :
   ```bash
   git clone https://github.com/votre-nom/LLC_rules_extractor.git
   cd LLC_rules_extractor
   ```

2. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lance l’application :
   ```bash
   python3 app/main.py
   ```

---

## 🧪 Lancer les tests

```bash
python3 -m unittest tests/unitaires/TestUnitaires.py
```

---

## 📚 Documentation

La documentation complète est disponible dans le dossier `docs/index.html`

Pour la régénérer :
```bash
cd docs
make html
```

---

## 🧠 Auteur

Développé par **SupGalilée ING2**
