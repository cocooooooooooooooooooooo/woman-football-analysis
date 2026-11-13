import streamlit as st
import pandas as pd
from src.data_loader import charger_stats_joueuses

# 1. Configuration de la page
st.set_page_config(page_title="LFC Women Analytics", layout="wide")
st.title("🔴 Liverpool WFC - Dashboard Analytique")

# 2. Chargement des données
# Assurez-vous d'avoir mis votre export FBref en format CSV dans le dossier 'data'
df_stats = charger_stats_joueuses("data/liverpool_stats.csv")

if df_stats.empty:
    st.error("⚠️ Fichier de données introuvable. Placez votre CSV dans le dossier 'data/'.")
else:
    # 3. Création de la barre latérale pour les filtres
    st.sidebar.header("Filtres")
    min_minutes = st.sidebar.slider("Minutes jouées minimum", 0, 2000, 500)

    # Application du filtre
    # On convertit la colonne 'Min' en numérique (en gérant les virgules si besoin)
    df_stats['Min'] = pd.to_numeric(df_stats['Min'].astype(str).str.replace(',', ''), errors='coerce')
    df_filtre = df_stats[df_stats['Min'] >= min_minutes]

    # 4. Affichage des indicateurs de performance (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Joueuses dans la rotation", len(df_filtre))
    col2.metric("Meilleure Buteuse",
                df_filtre.loc[df_filtre['Gls'].idxmax()]['Player'] if not df_filtre.empty else "N/A")
    col3.metric("Meilleure Créatrice (Ast)",
                df_filtre.loc[df_filtre['Ast'].idxmax()]['Player'] if not df_filtre.empty else "N/A")

    # 5. Affichage du tableau de données interactif
    st.subheader("Statistiques de l'effectif")
    colonnes_a_afficher = ['Player', 'Age', 'Min', 'Gls', 'Ast', 'xG', 'xAG']
    st.dataframe(df_filtre[colonnes_a_afficher], use_container_width=True)