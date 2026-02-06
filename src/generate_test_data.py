import pandas as pd
import os

def generate_files():
    # Données pour le CSV
    data_csv = {
        'Mois': ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 
                 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'],
        'Ventes': [1500, 1800, 1200, 2200, 2500, 2100, 2800, 1600, 1900, 2300, 2600, 3000],
        'Benefice': [300, 450, 200, 600, 750, 550, 900, 350, 480, 650, 800, 1000],
        'Clients': [50, 60, 45, 80, 90, 75, 100, 55, 65, 85, 95, 120]
    }
    
    # Données pour l'Excel
    data_excel = {
        'Produit': ['Pomme', 'Banane', 'Orange', 'Fraise', 'Kiwi', 'Mangue', 'Raisin'],
        'Prix_Unitaire': [1.2, 0.8, 1.5, 3.0, 2.5, 4.0, 2.8],
        'Quantite_Vendue': [150, 200, 120, 80, 60, 40, 90],
        'Categorie': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit']
    }

    # Chemin racine du projet Dashboard
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    csv_path = os.path.join(base_dir, 'test_ventes.csv')
    xlsx_path = os.path.join(base_dir, 'test_produits.xlsx')

    # Création du CSV
    df_csv = pd.DataFrame(data_csv)
    df_csv.to_csv(csv_path, index=False)
    print(f"Fichier créé : {csv_path}")

    # Création de l'Excel
    try:
        df_excel = pd.DataFrame(data_excel)
        df_excel.to_excel(xlsx_path, index=False)
        print(f"Fichier créé : {xlsx_path}")
    except ImportError:
        print("Impossible de créer le fichier Excel (module openpyxl manquant ?)")
        print("Installez-le avec : pip install openpyxl")

if __name__ == "__main__":
    generate_files()
