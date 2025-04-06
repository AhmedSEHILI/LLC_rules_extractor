"""
Fichier principal de l'application.

Ce module initialise l'application, crée les instances du modèle, de la vue
et du contrôleur pour l'extraction de règles à partir d'une ontologie.
Il lance ensuite l'interface graphique de l'application.
"""

import sys
from PyQt5.QtWidgets import QApplication

from controller.RuleExtractionController import RuleExtractionController
from models.RuleExtractionModel import RuleExtractionModel
from views.RuleExtractionView import RuleExtractionView


def main():
    """
    Point d'entrée de l'application.

    Cette fonction initialise l'application Qt, instancie le modèle, la vue et le contrôleur,
    puis affiche la vue principale. Elle exécute ensuite la boucle principale de l'application.
    """
    app = QApplication(sys.argv)

    model = RuleExtractionModel()
    view = RuleExtractionView()
    controller = RuleExtractionController(model, view)

    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
