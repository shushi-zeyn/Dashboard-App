import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd

class GraphManager:
    @staticmethod
    def create_figure(df, graph_type, x_col, y_col, scale=None):
        """
        Génère une figure Matplotlib en fonction des paramètres.
        """
        # Création de la figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Vérification basique
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            ax.text(0.5, 0.5, "Colonnes invalides", ha='center', va='center')
            return fig

        # Préparation des données
        try:
            # On ne garde que les colonnes utiles
            data = df[[x_col, y_col]].copy()
            
            # Conversion en numérique pour l'axe Y si possible (sauf pour Camembert où Y est la valeur)
            # Pour Scatter, Line, Bar, Y doit être numérique.
            if "Camembert" not in graph_type:
                data[y_col] = pd.to_numeric(data[y_col], errors='coerce')
            
            # On supprime les lignes avec des NaN (valeurs manquantes ou conversion échouée)
            data = data.dropna()

            if data.empty:
                ax.text(0.5, 0.5, "Aucune donnée valide à afficher.\nVérifiez que la colonne Y contient des nombres.", 
                        ha='center', va='center', color='red')
                return fig

            x = data[x_col]
            y = data[y_col]

            # Génération du graphique
            if "Ligne" in graph_type:
                # Si X est aussi numérique, on trie pour éviter les gribouillis
                if pd.api.types.is_numeric_dtype(x):
                    data_sorted = data.sort_values(by=x_col)
                    ax.plot(data_sorted[x_col], data_sorted[y_col], marker='o', linestyle='-')
                else:
                    ax.plot(x, y, marker='o', linestyle='-')
                
                ax.set_title(f"{y_col} par rapport à {x_col}")
                
            elif "Barres" in graph_type:
                ax.bar(x, y)
                ax.set_title(f"{y_col} par {x_col}")
                
            elif "Nuage" in graph_type: # Scatter
                ax.scatter(x, y, alpha=0.7)
                ax.set_title(f"Nuage de points : {y_col} vs {x_col}")
                
            elif "Camembert" in graph_type:
                # Pour le camembert : X = Labels, Y = Valeurs
                # On regroupe si X a des doublons
                pie_data = data.groupby(x_col)[y_col].sum()
                ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                ax.set_title(f"Répartition de {y_col} par {x_col}")
            
            # Configuration des axes (sauf Pie)
            if "Camembert" not in graph_type:
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.grid(True, linestyle='--', alpha=0.6)
                
                # Rotation des labels X si ce sont des chaînes de caractères
                if not pd.api.types.is_numeric_dtype(x):
                    fig.autofmt_xdate(rotation=45)

        except Exception as e:
            ax.clear()
            ax.text(0.5, 0.5, f"Erreur lors du tracé :\n{str(e)}", 
                    ha='center', va='center', color='red', wrap=True)

        fig.tight_layout()
        return fig
