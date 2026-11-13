import pandas as pd
import streamlit as st

@st.cache_data # Cette décoration met les données en cache (optimisation des performances)
def charger_stats_joueuses(chemin_fichier):
    # Charge le CSV exporté manuellement (ou généré par vos scripts précédents)
    try:
        df = pd.read_csv(chemin_fichier)
        # Nettoyage de base : retirer les lignes vides
        df = df.dropna(subset=['Player'])
        return df
    except FileNotFoundError:
        return pd.DataFrame()