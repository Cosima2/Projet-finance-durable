import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Fonds ESG", layout="wide")

# -------------------------------
# TITRE 
# -------------------------------
st.title("Fonds d'investissement ESG")
st.markdown("Ce dashboard présente la composition d'un portefeuille structuré selon les critères ESG, avec une thématique *eau*.")

# -------------------------------
# PARTIE GÉNÉRALE
# -------------------------------
st.header("Composition Générale du Portefeuille (45%)")

composition_generale = {
    "Obligations (gouvernementales ou vertes)": 15,
    "Fonds à impact": 20,
    "ETF durables": 5,
    "Crypto verte": 5
}
df_generale = pd.DataFrame(list(composition_generale.items()), columns=["Actif", "Poids (%)"])
fig_generale = px.pie(df_generale, values="Poids (%)", names="Actif", title="Répartition de la partie générale")
st.plotly_chart(fig_generale, use_container_width=True)

# -------------------------------
# PARTIE SPÉCIFIQUE
# -------------------------------
st.header("Choix de la Partie Spécifique (55%)")
choix_strategie = st.radio("Choisissez la dimension ESG que vous souhaitez explorer :", ["ES (Environnement & Social)", "SG (Social & Gouvernance)", "EG (Environnement & Gouvernance)"])

composition_specifique = {
    "Actifs Projet": 20,
    "Obligations Corporate Vertes": 15,
    "Actions Durables": 20
}
df_specifique = pd.DataFrame(list(composition_specifique.items()), columns=["Type d'actif", "Poids (%)"])
fig_spec = px.bar(df_specifique, x="Type d'actif", y="Poids (%)", color="Type d'actif",
                  title=f"Répartition pour la stratégie : {choix_strategie}")
st.plotly_chart(fig_spec, use_container_width=True)

# -------------------------------
# PARTIE SPÉCIFIQUE : ES
# -------------------------------
if "ES" in choix_strategie:
    st.header("Portefeuille ES Thématique Eau")

    # Liste des entreprises du portefeuille (ajustez avec vos symboles)
    entreprises = {
        "Veolia": "VEOEY",
        "Xylem": "XYL",
        "Danaher": "DHR",
        "Geberit": "GEBN.SW",
        "Pentair": "PNR"
    }

    # Sélection de l'entreprise
    choix = st.sidebar.selectbox("Sélectionnez une entreprise", list(entreprises.keys()))
    symbole = entreprises[choix]

    # Récupération des données financières
    data = yf.download(symbole, period="1y")
    data.reset_index(inplace=True)

    # Affichage du cours de l'action
    st.subheader(f"Cours de l'action de {choix} sur un an")
    fig = px.line(data, x="Date", y=data["Close"].squeeze(), title=f"Cours de {choix}")
    st.plotly_chart(fig)

    # Section ESG
    st.subheader(f"Notation ESG de {choix}")
    st.write("**Score ESG** : Données à intégrer")  # À remplacer par API ou table réelle
    st.write("**Environnement** : Données à intégrer")
    st.write("**Social** : Données à intégrer")
    st.write("**Gouvernance** : Données à intégrer")

    # Analyse comparative
    st.subheader("Comparaison des Notations ESG")
    esg_data = pd.DataFrame({
        "Entreprise": ["Veolia", "Xylem", "Danaher", "Geberit", "Pentair"],
        "Score ESG": [75, 80, 78, 82, 77]
    })
    fig = px.bar(esg_data, x="Entreprise", y="Score ESG", color="Score ESG", title="Comparaison des Scores ESG")
    st.plotly_chart(fig)

# -------------------------------
# INFOS FOOTER
# -------------------------------
st.sidebar.info("Ce dashboard présente les performances financières et les notations ESG des entreprises spécialisées dans le secteur de l'eau.")
st.markdown("---")
st.caption("© 2025 - Dashboard ESG | Streamlit prototype | Données fictives ou publiques.")
