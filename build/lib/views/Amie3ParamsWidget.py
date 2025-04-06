from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFormLayout, QLineEdit, QLabel, QCheckBox


class Amie3ParamsWidget(QWidget):
    """
    Widget graphique permettant de configurer les paramètres d'exécution de AMIE3.

    Il regroupe des champs de saisie textuelle pour les options numériques et des cases à cocher
    pour les options, et construit la liste des arguments à fournir à AMIE3.
    """

    def __init__(self, parent=None):
        """
        Initialise tous les éléments nécessaires à la configuration d'AMIE3.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut None.
        """
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.form_layout = QFormLayout(content_widget)

        self.lineedit_mins = QLineEdit("100")
        self.form_layout.addRow(QLabel("-mins (min-support)"), self.lineedit_mins)

        self.lineedit_minis = QLineEdit("100")
        self.form_layout.addRow(QLabel("-minis (min-initial-support)"), self.lineedit_minis)

        self.lineedit_minhc = QLineEdit("0.01")
        self.form_layout.addRow(QLabel("-minhc (min-head-coverage)"), self.lineedit_minhc)

        self.lineedit_pm = QLineEdit("headcoverage")
        self.form_layout.addRow(QLabel("-pm (pruning-metric)"), self.lineedit_pm)

        self.lineedit_bexr = QLineEdit("")
        self.form_layout.addRow(QLabel("-bexr (body-excluded-relations)"), self.lineedit_bexr)

        self.lineedit_hexr = QLineEdit("")
        self.form_layout.addRow(QLabel("-hexr (head-excluded-relations)"), self.lineedit_hexr)

        self.lineedit_iexr = QLineEdit("")
        self.form_layout.addRow(QLabel("-iexr (instantiation-excluded-relations)"), self.lineedit_iexr)

        self.lineedit_htr = QLineEdit("")
        self.form_layout.addRow(QLabel("-htr (head-target-relations)"), self.lineedit_htr)

        self.lineedit_btr = QLineEdit("")
        self.form_layout.addRow(QLabel("-btr (body-target-relations)"), self.lineedit_btr)

        self.lineedit_itr = QLineEdit("")
        self.form_layout.addRow(QLabel("-itr (instantiation-target-relations)"), self.lineedit_itr)

        self.lineedit_maxad = QLineEdit("3")
        self.form_layout.addRow(QLabel("-maxad (max-depth)"), self.lineedit_maxad)

        self.lineedit_minpca = QLineEdit("0.0")
        self.form_layout.addRow(QLabel("-minpca (min-pca-confidence)"), self.lineedit_minpca)

        self.lineedit_bias = QLineEdit("default")
        self.form_layout.addRow(QLabel("-bias (oneVar|default|lazy|...)"), self.lineedit_bias)

        self.lineedit_rl = QLineEdit("")
        self.form_layout.addRow(QLabel("-rl (recursivity-limit)"), self.lineedit_rl)

        self.lineedit_nc = QLineEdit("8")
        self.form_layout.addRow(QLabel("-nc (n-threads)"), self.lineedit_nc)

        self.lineedit_minc = QLineEdit("0.0")
        self.form_layout.addRow(QLabel("-minc (min-std-confidence)"), self.lineedit_minc)

        self.lineedit_vo = QLineEdit("fun")
        self.form_layout.addRow(QLabel("-vo (variableOrder)"), self.lineedit_vo)

        self.lineedit_ef = QLineEdit("")
        self.form_layout.addRow(QLabel("-ef (extraFile)"), self.lineedit_ef)

        self.lineedit_d = QLineEdit("")
        self.form_layout.addRow(QLabel("-d (delimiter)"), self.lineedit_d)

        self.checkbox_oute = QCheckBox("-oute (output-at-end)")
        self.form_layout.addRow(self.checkbox_oute)

        self.checkbox_datalog = QCheckBox("-datalog (datalog-output)")
        self.form_layout.addRow(self.checkbox_datalog)
        self.checkbox_datalog.setCheckState(2)

        self.checkbox_const = QCheckBox("-const (allow-constants)")
        self.form_layout.addRow(self.checkbox_const)

        self.checkbox_fconst = QCheckBox("-fconst (only-constants)")
        self.form_layout.addRow(self.checkbox_fconst)

        self.checkbox_caos = QCheckBox("-caos (count-always-on-subject)")
        self.form_layout.addRow(self.checkbox_caos)

        self.checkbox_optimcb = QCheckBox("-optimcb (optim-confidence-bounds)")
        self.form_layout.addRow(self.checkbox_optimcb)

        self.checkbox_optimfh = QCheckBox("-optimfh (optim-func-heuristic)")
        self.form_layout.addRow(self.checkbox_optimfh)

        self.checkbox_verbose = QCheckBox("-verbose")
        self.form_layout.addRow(self.checkbox_verbose)

        self.checkbox_auta = QCheckBox("-auta (avoid-unbound-type-atoms)")
        self.form_layout.addRow(self.checkbox_auta)

        self.checkbox_deml = QCheckBox("-deml (do-not-exploit-max-length)")
        self.form_layout.addRow(self.checkbox_deml)

        self.checkbox_dqrw = QCheckBox("-dqrw (disable-query-rewriting)")
        self.form_layout.addRow(self.checkbox_dqrw)

        self.checkbox_dpr = QCheckBox("-dpr (disable-perfect-rules)")
        self.form_layout.addRow(self.checkbox_dpr)

        self.checkbox_oout = QCheckBox("-oout (only-output)")
        self.form_layout.addRow(self.checkbox_oout)

        self.checkbox_full = QCheckBox("-full (enable all enhancements)")
        self.form_layout.addRow(self.checkbox_full)

        self.checkbox_noHeuristics = QCheckBox("-noHeuristics")
        self.form_layout.addRow(self.checkbox_noHeuristics)

        self.checkbox_noKbRewrite = QCheckBox("-noKbRewrite")
        self.form_layout.addRow(self.checkbox_noKbRewrite)

        self.checkbox_noKbExistsDetection = QCheckBox("-noKbExistsDetection")
        self.form_layout.addRow(self.checkbox_noKbExistsDetection)

        self.checkbox_noSkyline = QCheckBox("-noSkyline")
        self.form_layout.addRow(self.checkbox_noSkyline)

        self.checkbox_ostd = QCheckBox("-ostd (ommit-std-conf)")
        self.form_layout.addRow(self.checkbox_ostd)

        self.checkbox_optimai = QCheckBox("-optimai (adaptive-instantiations)")
        self.form_layout.addRow(self.checkbox_optimai)

        self.checkbox_mlg = QCheckBox("-mlg (multilingual)")
        self.form_layout.addRow(self.checkbox_mlg)

        content_widget.setLayout(self.form_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def build_amie3_params(self):
        """
        Construit et retourne la liste des paramètres AMIE3 à partir des champs de saisie
        et des options sélectionnées par l'utilisateur.

        Returns:
            list: Une liste de chaînes représentant les arguments en ligne de commande à passer à AMIE3.
        """
        params = []

        def add_param(flag, widget):
            if widget.text().strip():
                params.extend([flag, widget.text().strip()])

        add_param("-mins", self.lineedit_mins)
        add_param("-minis", self.lineedit_minis)
        add_param("-minhc", self.lineedit_minhc)
        add_param("-pm", self.lineedit_pm)
        add_param("-bexr", self.lineedit_bexr)
        add_param("-hexr", self.lineedit_hexr)
        add_param("-iexr", self.lineedit_iexr)
        add_param("-htr", self.lineedit_htr)
        add_param("-btr", self.lineedit_btr)
        add_param("-itr", self.lineedit_itr)
        add_param("-maxad", self.lineedit_maxad)
        add_param("-minpca", self.lineedit_minpca)
        add_param("-bias", self.lineedit_bias)
        add_param("-rl", self.lineedit_rl)
        add_param("-nc", self.lineedit_nc)
        add_param("-minc", self.lineedit_minc)
        add_param("-vo", self.lineedit_vo)
        add_param("-ef", self.lineedit_ef)
        add_param("-d", self.lineedit_d)

        for checkbox in [
            self.checkbox_oute, self.checkbox_datalog, self.checkbox_const,
            self.checkbox_fconst, self.checkbox_caos, self.checkbox_optimcb,
            self.checkbox_optimfh, self.checkbox_verbose, self.checkbox_auta,
            self.checkbox_deml, self.checkbox_dqrw, self.checkbox_dpr,
            self.checkbox_oout, self.checkbox_full, self.checkbox_noHeuristics,
            self.checkbox_noKbRewrite, self.checkbox_noKbExistsDetection,
            self.checkbox_noSkyline, self.checkbox_ostd, self.checkbox_optimai,
            self.checkbox_mlg
        ]:
            if checkbox.isChecked():
                params.append(checkbox.text().split()[0])

        return params
