pip i
import streamlit as st

st.set_page_config(
    page_title="Fonds ESG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Désactivation des éléments par défaut
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Navigation centrale
st.title("Fonds d'Investissement Responsable")
cols = st.columns(5)

pages = [
    ("Accueil", "Accueil"),
    ("Générale", "dashGE"),
    ("Écologique", "dashES"),
    ("Social", "dashSG"),
    ("Europe", "dashEG")
]

for i, (name, page) in enumerate(pages):
    with cols[i]:
        if st.button(name):
            st.switch_page(f"pages/{page}.py")

st.markdown("---")