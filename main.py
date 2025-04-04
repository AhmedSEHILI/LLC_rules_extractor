import sys

from PyQt5.QtWidgets import QApplication

from controllers.RuleExtractionController import RuleExtractionController
from models.RuleExtractionModel import RuleExtractionModel
from views.RuleExtractionView import RuleExtractionView


def main():
    app = QApplication(sys.argv)

    model = RuleExtractionModel()
    view = RuleExtractionView()
    controller = RuleExtractionController(model, view)

    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()