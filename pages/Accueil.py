import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px

# Configuration de la page — À placer en tout premier
st.set_page_config(
    page_title="Fonds ESG - Investissement Responsable",
    layout="wide",
    menu_items={
        'Get Help': 'https://votresite.com/aide',
        'Report a bug': "https://votresite.com/bug",
        'About': "### Fonds ESG - Par Reghina, Coline & Cosima"
    }
)

# Style CSS personnalisé
st.markdown("""
<style>
    .big-font {
        font-size:20px !important;
        text-align: justify;
    }
    .header-style {
        color: #2e8b57;
        border-bottom: 2px solid #2e8b57;
        padding-bottom: 10px;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        background-color: #f0f2f6;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header avec logo
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://via.placeholder.com/150x150.png?text=ESG+FONDS", width=150)
with col2:
    st.title("Notre Fonds d'Investissement Responsable")
    st.markdown("**Allier performance financière et impact positif**")

# Introduction
st.markdown("""
<div class="big-font">
Investir autrement, c'est possible. Notre fonds ESG innovant vous propose une approche d'investissement qui concilie 
rentabilité financière et contribution aux grands enjeux sociétaux et environnementaux de notre temps.
</div>
""", unsafe_allow_html=True)

# Structure du fonds
st.markdown("---")
st.markdown("## Structure de notre fonds", unsafe_allow_html=True)
st.markdown("""
<div class="big-font">
Notre portefeuille est structuré en deux composantes complémentaires :
</div>
""", unsafe_allow_html=True)

# Cartes explicatives
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>Partie Générale (45%)</h3>
        <p>Une base solide et diversifiée composée de :</p>
        <ul>
            <li>Obligations gouvernementales sélectionnées</li>
            <li>Fonds d'investissement à impact</li>
            <li>ETFs durables</li>
        </ul>
        <p>Cette partie assure la stabilité du portefeuille.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>Partie Spécifique (55%)</h3>
        <p>Votre investissement personnalisé selon vos convictions :</p>
        <ul>
            <li>Thématiques au choix (écologie, social, gouvernance)</li>
            <li>Actifs projets concrets</li>
            <li>Obligations corporate engagées</li>
        </ul>
        <p>Cette partie maximise votre impact selon vos valeurs.</p>
    </div>
    """, unsafe_allow_html=True)

# Graphique de répartition
st.markdown("---")
st.markdown("## Répartition du portefeuille")

composition = {
    "Partie Générale": 45,
    "Partie Spécifique": 55
}

df = pd.DataFrame(list(composition.items()), columns=["Composante", "Pourcentage"])

fig = px.pie(df, 
             values="Pourcentage", 
             names="Composante",
             color_discrete_sequence=["#88b290", "#7fa6d1"],
             hole=0.4)

fig.update_traces(textposition='inside', 
                 textinfo='percent+label',
                 pull=[0, 0.1])

st.plotly_chart(fig, use_container_width=True)

# Processus d'investissement
st.markdown("---")
st.markdown("## Comment ça marche ?")

steps = [
    {"icon": "1️", "title": "Choix de votre thématique", "desc": "Sélectionnez la cause qui vous tient à cœur"},
    {"icon": "2️", "title": "Allocation automatique", "desc": "Notre algorithme construit votre portefeuille personnalisé"},
    {"icon": "3️", "title": "Suivi transparent", "desc": "Accès à votre dashboard de performance et d'impact"},
    {"icon": "4️", "title": "Réajustement trimestriel", "desc": "Actualisation selon les nouvelles opportunités"}
]

for step in steps:
    with st.expander(f"{step['icon']} {step['title']}"):
        st.markdown(step["desc"])

# Désactive le menu par défaut
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Dans la section des boutons :
cols = st.columns(4)
with cols[0]:
    if st.button("Partie Générale", help="Voir les actifs stables"):
        st.switch_page("pages/dashGE.py")
with cols[1]:
    if st.button("Thème Écologique"):
        st.switch_page("pages/dashES.py")
with cols[2]:
    if st.button("Thème Social"):
        st.switch_page("pages/dashSG.py")
with cols[3]:
    if st.button("Thème Européen"):
        st.switch_page("pages/dashEG.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 14px;">
    © 2025 ESG Invest - Tous droits réservés<br>
    Une approche responsable de l'investissement
</div>
""", unsafe_allow_html=True)
