from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QLineEdit, QFrame, QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Import du gestionnaire de graphiques
try:
    from src.core.graph_manager import GraphManager
except ImportError:
    from core.graph_manager import GraphManager

class ConfigPage(QWidget):
    def __init__(self, file_name, df):
        super().__init__()
        self.file_name = file_name
        self.df = df
        self.columns = df.columns.tolist()
        
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- En-tête : Nom du fichier ---
        self.title_label = QLabel(f"Fichier : {self.file_name}")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("pageTitle")
        main_layout.addWidget(self.title_label)

        # --- Corps : Panneau Gauche + Zone Graphique Droite ---
        body_layout = QHBoxLayout()
        body_layout.setSpacing(30)

        # 1. Panneau de Gauche (Contrôles)
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)

        # Type de graphique
        lbl_graph_type = QLabel("Type de graphique :")
        self.combo_graph_type = QComboBox()
        self.combo_graph_type.addItems(["Ligne (Line Plot)", "Barres (Bar Chart)", "Nuage de points (Scatter)", "Camembert (Pie Chart)"])
        left_layout.addWidget(lbl_graph_type)
        left_layout.addWidget(self.combo_graph_type)

        # Axes X et Y
        lbl_axes = QLabel("Choix des axes :")
        left_layout.addWidget(lbl_axes)

        axes_layout = QHBoxLayout()
        
        # Axe X
        self.combo_x = QComboBox()
        self.combo_x.setPlaceholderText("Axe X")
        self.combo_x.addItems(self.columns)
        axes_layout.addWidget(self.combo_x)

        # Axe Y
        self.combo_y = QComboBox()
        self.combo_y.setPlaceholderText("Axe Y")
        self.combo_y.addItems(self.columns)
        axes_layout.addWidget(self.combo_y)
        
        left_layout.addLayout(axes_layout)

        # Échelle
        lbl_scale = QLabel("Échelle (Optionnel) :")
        self.input_scale = QLineEdit()
        self.input_scale.setPlaceholderText("Laisser vide pour auto")
        left_layout.addWidget(lbl_scale)
        left_layout.addWidget(self.input_scale)

        # Bouton Valider
        self.btn_validate = QPushButton("Générer le graphique")
        self.btn_validate.setCursor(Qt.PointingHandCursor)
        self.btn_validate.setObjectName("btnValidate")
        self.btn_validate.clicked.connect(self.generate_graph)
        left_layout.addWidget(self.btn_validate)

        # Spacer pour pousser les contrôles vers le haut
        left_layout.addStretch()

        # Ajout du panneau gauche au layout principal (prend 1/3 de la largeur)
        body_layout.addWidget(left_panel, 1)

        # 2. Panneau de Droite (Zone Graphique)
        self.graph_container = QFrame()
        self.graph_container.setObjectName("graphContainer")
        self.graph_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout pour le graphique
        self.graph_layout = QVBoxLayout(self.graph_container)
        
        # Placeholder text pour l'instant
        self.lbl_placeholder = QLabel("Le graphique s'affichera ici")
        self.lbl_placeholder.setAlignment(Qt.AlignCenter)
        self.lbl_placeholder.setStyleSheet("color: #888; font-style: italic; border: none;")
        self.graph_layout.addWidget(self.lbl_placeholder)

        # Ajout du panneau droit (prend 2/3 de la largeur)
        body_layout.addWidget(self.graph_container, 2)

        main_layout.addLayout(body_layout)

    def generate_graph(self):
        """Récupère les paramètres et affiche le graphique"""
        x_col = self.combo_x.currentText()
        y_col = self.combo_y.currentText()
        graph_type = self.combo_graph_type.currentText()
        scale = self.input_scale.text()

        if not x_col or not y_col:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner les axes X et Y.")
            return

        # Nettoyer le conteneur graphique (supprimer l'ancien graphe ou le placeholder)
        while self.graph_layout.count():
            child = self.graph_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Générer la figure via le GraphManager
        fig = GraphManager.create_figure(self.df, graph_type, x_col, y_col, scale)

        # Créer le canvas Matplotlib et l'ajouter au layout
        canvas = FigureCanvas(fig)
        self.graph_layout.addWidget(canvas)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F1F8E9;
                font-size: 14px;
                color: #33691E;
            }
            
            #pageTitle {
                font-size: 24px;
                font-weight: bold;
                color: #33691E;
                padding: 10px;
                background-color: #C5E1A5;
                border-radius: 15px;
            }

            #leftPanel {
                background-color: #FFFFFF;
                border: 1px solid #AED581;
                border-radius: 20px;
                padding: 20px;
            }

            #graphContainer {
                background-color: #FFFFFF;
                border: 2px dashed #AED581;
                border-radius: 20px;
            }

            /* ComboBox et LineEdit arrondis */
            QComboBox, QLineEdit {
                padding: 8px;
                border: 1px solid #C5E1A5;
                border-radius: 12px;
                background-color: #FAFAFA;
            }
            
            /* Style du menu déroulant (la liste qui s'ouvre) */
            QComboBox QAbstractItemView {
                border: 1px solid #C5E1A5;
                background-color: #FAFAFA;
                border-radius: 10px;
                selection-background-color: #AED581;
                selection-color: #1B5E20;
                outline: none;
                padding: 4px;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                border-left: 2px solid #C5E1A5;
                width: 0; 
                height: 0; 
                border-top: 5px solid #33691E;
                border-right: 5px solid transparent;
                border-left: 5px solid transparent;
                margin-top: 2px;
            }
            
            QPushButton#btnValidate {
                background-color: #558B2F;
                color: white;
                font-weight: bold;
                padding: 12px;
                border-radius: 12px;
                margin-top: 10px;
            }
            QPushButton#btnValidate:hover {
                background-color: #33691E;
            }

            /* ScrollBar Stylisée */
            QScrollBar:vertical {
                border: none;
                background: #F1F8E9;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #AED581;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9CCC65;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
