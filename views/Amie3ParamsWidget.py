# <-------------------------->
# Paramètres AMIE3
# <-------------------------->
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFormLayout, QLineEdit, QLabel, QCheckBox


class Amie3ParamsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.form_layout = QFormLayout(content_widget)

        # Paramètres numériques ou textuels

        self.lineedit_mins = QLineEdit("100")  # -mins
        self.form_layout.addRow(QLabel("-mins (min-support)"), self.lineedit_mins)

        self.lineedit_minis = QLineEdit("100")  # -minis
        self.form_layout.addRow(QLabel("-minis (min-initial-support)"), self.lineedit_minis)

        self.lineedit_minhc = QLineEdit("0.01")  # -minhc
        self.form_layout.addRow(QLabel("-minhc (min-head-coverage)"), self.lineedit_minhc)

        self.lineedit_pm = QLineEdit("headcoverage")  # -pm
        self.form_layout.addRow(QLabel("-pm (pruning-metric)"), self.lineedit_pm)

        self.lineedit_bexr = QLineEdit("")  # -bexr
        self.form_layout.addRow(QLabel("-bexr (body-excluded-relations)"), self.lineedit_bexr)

        self.lineedit_hexr = QLineEdit("")  # -hexr
        self.form_layout.addRow(QLabel("-hexr (head-excluded-relations)"), self.lineedit_hexr)

        self.lineedit_iexr = QLineEdit("")  # -iexr
        self.form_layout.addRow(QLabel("-iexr (instantiation-excluded-relations)"), self.lineedit_iexr)

        self.lineedit_htr = QLineEdit("")  # -htr
        self.form_layout.addRow(QLabel("-htr (head-target-relations)"), self.lineedit_htr)

        self.lineedit_btr = QLineEdit("")  # -btr
        self.form_layout.addRow(QLabel("-btr (body-target-relations)"), self.lineedit_btr)

        self.lineedit_itr = QLineEdit("")  # -itr
        self.form_layout.addRow(QLabel("-itr (instantiation-target-relations)"), self.lineedit_itr)

        self.lineedit_maxad = QLineEdit("3")  # -maxad
        self.form_layout.addRow(QLabel("-maxad (max-depth)"), self.lineedit_maxad)

        self.lineedit_minpca = QLineEdit("0.0")  # -minpca
        self.form_layout.addRow(QLabel("-minpca (min-pca-confidence)"), self.lineedit_minpca)

        self.lineedit_bias = QLineEdit("default")  # -bias
        self.form_layout.addRow(QLabel("-bias (oneVar|default|lazy|...)"), self.lineedit_bias)

        self.lineedit_rl = QLineEdit("")  # -rl (recursivity-limit)
        self.form_layout.addRow(QLabel("-rl (recursivity-limit)"), self.lineedit_rl)

        self.lineedit_nc = QLineEdit("8")  # -nc
        self.form_layout.addRow(QLabel("-nc (n-threads)"), self.lineedit_nc)

        self.lineedit_minc = QLineEdit("0.0")  # -minc
        self.form_layout.addRow(QLabel("-minc (min-std-confidence)"), self.lineedit_minc)

        self.lineedit_vo = QLineEdit("fun")  # -vo
        self.form_layout.addRow(QLabel("-vo (variableOrder)"), self.lineedit_vo)

        self.lineedit_ef = QLineEdit("")  # -ef (extraFile)
        self.form_layout.addRow(QLabel("-ef (extraFile)"), self.lineedit_ef)

        self.lineedit_d = QLineEdit("")  # -d (delimiter)
        self.form_layout.addRow(QLabel("-d (delimiter)"), self.lineedit_d)

        # Paramètres booléens (checkBox)

        self.checkbox_oute = QCheckBox("-oute (output-at-end)")
        self.form_layout.addRow(self.checkbox_oute)

        # Garder cette option toujours activée pour faciliter la conversion en CSV
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

        # Scroll
        content_widget.setLayout(self.form_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    # Fonction qui construit la liste d'arguments AMIE3
    def build_amie3_params(self):
        params = []

        # -mins
        if self.lineedit_mins.text().strip():
            params += ["-mins", self.lineedit_mins.text().strip()]

        # -minis
        if self.lineedit_minis.text().strip():
            params += ["-minis", self.lineedit_minis.text().strip()]

        # -minhc
        if self.lineedit_minhc.text().strip():
            params += ["-minhc", self.lineedit_minhc.text().strip()]

        # -pm
        if self.lineedit_pm.text().strip():
            params += ["-pm", self.lineedit_pm.text().strip()]

        # -bexr
        if self.lineedit_bexr.text().strip():
            params += ["-bexr", self.lineedit_bexr.text().strip()]

        # -hexr
        if self.lineedit_hexr.text().strip():
            params += ["-hexr", self.lineedit_hexr.text().strip()]

        # -iexr
        if self.lineedit_iexr.text().strip():
            params += ["-iexr", self.lineedit_iexr.text().strip()]

        # -htr
        if self.lineedit_htr.text().strip():
            params += ["-htr", self.lineedit_htr.text().strip()]

        # -btr
        if self.lineedit_btr.text().strip():
            params += ["-btr", self.lineedit_btr.text().strip()]

        # -itr
        if self.lineedit_itr.text().strip():
            params += ["-itr", self.lineedit_itr.text().strip()]

        # -maxad
        if self.lineedit_maxad.text().strip():
            params += ["-maxad", self.lineedit_maxad.text().strip()]

        # -minpca
        if self.lineedit_minpca.text().strip():
            params += ["-minpca", self.lineedit_minpca.text().strip()]

        # -bias
        if self.lineedit_bias.text().strip():
            params += ["-bias", self.lineedit_bias.text().strip()]

        # -rl
        if self.lineedit_rl.text().strip():
            params += ["-rl", self.lineedit_rl.text().strip()]

        # -nc
        if self.lineedit_nc.text().strip():
            params += ["-nc", self.lineedit_nc.text().strip()]

        # -minc
        if self.lineedit_minc.text().strip():
            params += ["-minc", self.lineedit_minc.text().strip()]

        # -vo
        if self.lineedit_vo.text().strip():
            params += ["-vo", self.lineedit_vo.text().strip()]

        # -ef
        if self.lineedit_ef.text().strip():
            params += ["-ef", self.lineedit_ef.text().strip()]

        # -d
        if self.lineedit_d.text().strip():
            params += ["-d", self.lineedit_d.text().strip()]

        # ----- Lecture des checkboxes -----
        if self.checkbox_oute.isChecked():
            params.append("-oute")

        if self.checkbox_datalog.isChecked():
            params.append("-datalog")

        if self.checkbox_const.isChecked():
            params.append("-const")

        if self.checkbox_fconst.isChecked():
            params.append("-fconst")

        if self.checkbox_caos.isChecked():
            params.append("-caos")

        if self.checkbox_optimcb.isChecked():
            params.append("-optimcb")

        if self.checkbox_optimfh.isChecked():
            params.append("-optimfh")

        if self.checkbox_verbose.isChecked():
            params.append("-verbose")

        if self.checkbox_auta.isChecked():
            params.append("-auta")

        if self.checkbox_deml.isChecked():
            params.append("-deml")

        if self.checkbox_dqrw.isChecked():
            params.append("-dqrw")

        if self.checkbox_dpr.isChecked():
            params.append("-dpr")

        if self.checkbox_oout.isChecked():
            params.append("-oout")

        if self.checkbox_full.isChecked():
            params.append("-full")

        if self.checkbox_noHeuristics.isChecked():
            params.append("-noHeuristics")

        if self.checkbox_noKbRewrite.isChecked():
            params.append("-noKbRewrite")

        if self.checkbox_noKbExistsDetection.isChecked():
            params.append("-noKbExistsDetection")

        if self.checkbox_noSkyline.isChecked():
            params.append("-noSkyline")

        if self.checkbox_ostd.isChecked():
            params.append("-ostd")

        if self.checkbox_optimai.isChecked():
            params.append("-optimai")

        if self.checkbox_mlg.isChecked():
            params.append("-mlg")

        return params