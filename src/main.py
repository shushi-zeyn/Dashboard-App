import sys
import os

# Ajout du dossier parent au path pour permettre les imports relatifs si nécessaire
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.ui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
