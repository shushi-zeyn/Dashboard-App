import os
import pandas as pd
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt

# On tente un import absolu qui fonctionnera grâce au sys.path modifié dans main.py
try:
    from src.ui.config_page import ConfigPage
except ImportError:
    # Fallback si on lance depuis un autre contexte (ex: tests)
    from ui.config_page import ConfigPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shushi Dashboard")
        self.resize(1000, 700) # Un peu plus grand pour accueillir le graphe

        self.init_home_ui()
        self.apply_styles()

    def init_home_ui(self):
        """Initialise l'interface de la page d'accueil"""
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal vertical
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # --- En-tête (Header) ---
        self.header_widget = QWidget()
        self.header_widget.setObjectName("headerWidget")
        
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        self.app_name_label = QLabel("Shushi DashBoard")
        self.app_name_label.setObjectName("appNameLabel")
        header_layout.addWidget(self.app_name_label)
        
        header_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        header_layout.addItem(header_spacer)
        
        self.main_layout.addWidget(self.header_widget)

        # Conteneur pour le contenu changeant (Accueil ou Config)
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_container)

        # Afficher le contenu de l'accueil par défaut
        self.show_home_content()

    def show_home_content(self):
        """Affiche les boutons de l'accueil dans le content_container"""
        # Nettoyer le layout existant s'il y en a un
        self.clear_content_layout()

        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignCenter)

        layout.addStretch()

        # Message de bienvenue
        welcome_label = QLabel("Bienvenue")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setObjectName("welcomeLabel")
        layout.addWidget(welcome_label)

        # Bouton: Choisir un fichier
        btn_select_file = QPushButton("Choisir un fichier")
        btn_select_file.setFixedWidth(250)
        btn_select_file.setCursor(Qt.PointingHandCursor)
        btn_select_file.clicked.connect(self.open_file_dialog)
        layout.addWidget(btn_select_file)

        # Bouton: Derniers fichiers
        btn_recent_files = QPushButton("Derniers fichiers")
        btn_recent_files.setFixedWidth(250)
        btn_recent_files.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_recent_files)

        # Bouton: À propos
        btn_about = QPushButton("À propos")
        btn_about.setFixedWidth(250)
        btn_about.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_about)

        layout.addStretch()
        
        self.content_layout.addWidget(home_widget)

    def clear_content_layout(self):
        """Supprime tous les widgets du layout de contenu"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F1F8E9;
            }
            
            /* Header */
            #headerWidget {
                background-color: #C5E1A5;
                border-bottom: 2px solid #AED581;
            }
            #appNameLabel {
                font-size: 20px;
                font-weight: bold;
                color: #33691E;
            }

            /* Bienvenue */
            #welcomeLabel {
                font-size: 48px;
                font-weight: bold;
                color: #558B2F;
                margin-bottom: 20px;
            }

            /* Boutons */
            QPushButton {
                background-color: #C5E1A5;
                color: #33691E;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #AED581;
                color: #1B5E20;
            }
            QPushButton:pressed {
                background-color: #9CCC65;
            }
        """)

    def open_file_dialog(self):
        """Ouvre une boîte de dialogue pour choisir un fichier CSV ou Excel"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier de données",
            "",
            "Fichiers de données (*.csv *.xlsx *.xls)"
        )

        if file_path:
            try:
                # Lecture du fichier pour récupérer les colonnes
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                
                file_name = os.path.basename(file_path)

                # Afficher la page de configuration en passant le DataFrame complet
                self.show_config_page(file_name, df)

            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier :\n{str(e)}")

    def show_config_page(self, file_name, df):
        """Remplace le contenu de l'accueil par la page de configuration"""
        self.clear_content_layout()
        
        # On passe maintenant le DataFrame complet
        config_page = ConfigPage(file_name, df)
        self.content_layout.addWidget(config_page)
