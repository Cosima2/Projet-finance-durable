
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import numpy as np
from datetime import datetime

# -------------------------------
# TITRE ET INTRODUCTION
# -------------------------------
st.set_page_config(page_title="Partie spécifique thématique eau", layout="wide")

st.title("Portefeuille spécifique : thématique de l’eau")

st.markdown(
    "L’eau est au cœur des grands enjeux environnementaux du XXIe siècle : gestion des ressources, accès à l’eau potable, "
    "infrastructures durables, traitement et recyclage.  \n\n"
    "Dans le cadre de notre portefeuille ESG, la partie spécifique met l’accent sur des entreprises et projets qui "
    "offrent des solutions concrètes et innovantes pour répondre à ces défis.  \n\n"
    "Nous avons ainsi sélectionné des actions , des fonds d'investissement, ainsi que des projets d'entreprises qui sont "
    "strictement alignés avec la thématique de l’eau, en combinant **impact mesurable** et **potentiel de croissance à long terme**."
)
# -------------------------------
# VISUALISATION DE LA RÉPARTITION SPÉCIFIQUE
# -------------------------------
st.header("Composition de la partie spécifique liée à la thématique de l'eau")

# Données
composition_spe = {
    "Actifs Projet": 20,
    "Fonds": 15,
    "Actions": 20
}
df_generale = pd.DataFrame(list(composition_spe.items()), columns=["Actif", "Poids (%)"])

# Camembert stylisé
fig_generale = px.pie(
    df_generale,
    values="Poids (%)",
    names="Actif",
    title="Répartition des actifs – Thématique de l’eau",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Turbo
)

# Options de mise en page
fig_generale.update_traces(
    textinfo='percent',
    pull=[0.05] * len(df_generale)
)
fig_generale.update_layout(
    title_font_size=20,
    title_x=0.5,
    legend_title="Catégories d’actifs",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
)

# Affichage dans Streamlit
st.plotly_chart(fig_generale, use_container_width=True)

# -------------------------------
# Performance du fonds
# -------------------------------

import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# Configuration des pondérations
ponderation = {
    "oblig": 0.20,  # Rendement yield-to-maturity
    "fonds": 0.15,  # Mark-to-market
    "etfs": 0.10,   # Mark-to-market
    "driver": 0.55  # Mark-to-market
}

# Liste des actifs par catégorie
actifs = {
    "oblig": ["CRIIRLTLT01STM", "IRLTLT01CAM156N", "IRLTLT01ISM156N", 
              "IRLTLT01GBM156N", "IRLTLT01NOM156N", "COLIRLTLT01STM"],
    "fonds": ["0P0000G6X1.F", "0P0001IVQQ.F", "0P0000KU3M.F", 
              "0P0001HZQR.F", "0P00016ZNX.F"],
    "etfs": ["CYBO.SW", "REUS.L", "ISUN.L", "PAWD.L", "GSOV.DE", "CLMA.MI"],
    "driver": ["0P000111I9.F", "VIE.PA", "SIGN.SW", "TOM.OL", "EQIX"]
}

st.subheader("Performance du portefeuille avec thématique eau")
st.markdown("""
**Découvrez l'évolution de notre fonds ESG thématique eau sur 5 ans**  
Stratégie d'investissement durable avec allocation pondérée :
- **55%** Actifs drivers (actions du portefeuille spécifique à la thématique de l'eau)
- **20%** Obligations souveraines (rendement actuariel)
- **15%** Fonds spécialisés
- **10%** ETFs thématiques
""")

@st.cache_data
def load_data():
    # Chargement des données actions/fonds/ETFs
    df_actifs = pd.read_csv("financial_data/data_actifs.csv", parse_dates=[0], index_col=0)
    
    # Chargement des données obligataires (supposées être des yields)
    df_oblig = pd.read_csv("macro_data/obli_souveraines.csv", parse_dates=[0], index_col=0)
    
    # Conversion des taux en décimal et normalisation journalière
    df_oblig = df_oblig / 100 / 252  # Conversion % -> décimal et annualisé -> quotidien
    
    return pd.concat([df_actifs, df_oblig], axis=1)

df = load_data()
date_coupe = datetime.now() - pd.DateOffset(years=5)
df_filtered = df[df.index >= date_coupe].copy()

# Vérification des actifs manquants
missing_assets = [a for categorie in actifs.keys() 
                 for a in actifs[categorie] 
                 if a not in df_filtered.columns]
if missing_assets:
    st.error(f"Actifs manquants : {', '.join(missing_assets)}")
    st.stop()

# ---- Calcul des rendements pondérés ----
portfolio_returns = pd.Series(0, index=df_filtered.index)

for categorie, poids_categorie in ponderation.items():
    actifs_categorie = [a for a in actifs[categorie] if a in df_filtered.columns]
    poids_actif = poids_categorie / len(actifs_categorie)

    for asset in actifs_categorie:
        if categorie == "oblig":
            asset_returns = df_filtered[asset].fillna(0)  # Rendements déjà quotidiens
        else:
            asset_returns = df_filtered[asset].pct_change().fillna(0)

        portfolio_returns += asset_returns * poids_actif

portfolio_returns = portfolio_returns.fillna(0)  # Important pour éviter le NaN dans cumprod

# ---- Performance cumulée ----
portfolio_cumulative = (1 + portfolio_returns).cumprod() - 1

# ---- Visualisation de la performance cumulée ----
fig = px.area(
    portfolio_cumulative.to_frame('Performance'),
    title="Performance cumulée du portefeuille",
    labels={'value': 'Performance', 'variable': ''},
)

fig.update_layout(
    yaxis_tickformat='.1%',
    hovermode='x unified',
    xaxis_title='',
    yaxis_title='Performance cumulée (%)',
    title_font_size=22,
    title_font_family="Arial",
    title_x=0.02,
    plot_bgcolor='#fafafa',
    paper_bgcolor='#fafafa',
    margin=dict(t=60, b=40, l=0, r=0),
    height=420,
    font=dict(color="#333", size=13)
)

fig.update_yaxes(showgrid=True, gridcolor='#e5e5e5', zeroline=False)
fig.update_xaxes(showgrid=False)
fig.add_hline(y=0, line_dash="dot", line_color="grey", opacity=0.6)

st.plotly_chart(fig, use_container_width=True)


# ---- Indicateurs clés ----
def calculate_metrics(returns):
    returns = returns.fillna(0)  # Sécurité
    cumulative = (1 + returns).cumprod()
    metrics = {
        '5Y': cumulative.iloc[-1] - 1,
        'Annuel': (1 + returns.mean())**252 - 1,
        'Volatilité': returns.std() * np.sqrt(252),
        'Sharpe': returns.mean() / returns.std() * np.sqrt(252)
    }
    return metrics

metrics = calculate_metrics(portfolio_returns)

# ---- Tableau d'indicateurs clés ----

# Mise en forme des métriques dans un DataFrame
df_metrics = pd.DataFrame({
    "Indicateur": [
        "Performance 5 ans",
        "Performance annualisée",
        "Volatilité annuelle",
        "Ratio de Sharpe"
    ],
    "Valeur": [
        f"{metrics['5Y']:+.1%}",
        f"{metrics['Annuel']:+.1%}",
        f"{metrics['Volatilité']:.1%}",
        f"{metrics['Sharpe']:.2f}"
    ]
})

# Affichage du tableau
st.dataframe(
    df_metrics.set_index("Indicateur"),
    use_container_width=True,
    hide_index=False
)


# ---- Explications méthodologiques ----
with st.expander("Méthodologie détaillée"):
    st.markdown("""
    Pour refléter au mieux la réalité économique de chaque classe d’actifs, nous avons mis en place une méthodologie différenciée.  
    Les obligations sont intégrées selon une logique **buy-and-hold**, en s’appuyant sur leur rendement actuariel (yield-to-maturity). Celui-ci est annualisé puis ramené à une base journalière pour refléter leur performance dans la durée, sans tenir compte des fluctuations de prix à court terme.  
    Pour les actions, les fonds et les ETFs, nous appliquons une approche **mark-to-market**, fondée sur l’évolution réelle des prix de marché. Cette méthode permet de capter la dynamique boursière et la volatilité propre à chaque actif.  

    Enfin, les indicateurs de performance s’appuient sur des standards reconnus :  
    - La **volatilité annualisée** traduit l’ampleur des variations quotidiennes sur une base annuelle.  
    - Le **ratio de Sharpe** permet d’évaluer l’efficacité du portefeuille en comparant le rendement obtenu au risque pris.
    """)
st.success("""
        La performance du fonds a été positive, avec une tendance à la hausse au cours des 5 dernières années pour une performance très forte, permettant
        ainsi une certaine marge de manoeuvre dans les investissements dans des projets moins établis et donc plus risqués que nous effectuons. 
        Dans le but de refléter notre engagement envers les investissements durables et la thématique de l'eau, ainsi que la solidité de nos actifs.
    """)

st.markdown("---") 

# -------------------------------
# DÉTAIL DES ACTIFS SPÉCIFIQUES
# -------------------------------
st.header("Analyse détaillée de la partie spécifique (55%)")
st.warning(
    "Cette section présente la répartition détaillée des actifs composant la partie spécifique du portefeuille liée à la thématique de l'eau. "
)

categorie_actifs_spe = list(composition_spe.keys())
choix = st.radio("Sélectionnez une catégorie d'actifs", categorie_actifs_spe)

# -------------------------------
#   ACTIFS PROJET 
# -------------------------------
if choix == "Actifs Projet":

    st.markdown("""
    ### Critères de sélection des Actifs Projet

    Nous avons sélectionné des entreprises innovantes et engagées dans la transition écologique, en particulier dans la gestion durable de l’eau, la réduction des déchets plastiques et l’économie circulaire.

    **Méthodologie de sélection :**
    - **Critères d’inclusion** : Impact environnemental mesurable ; Solutions concrètes en lien avec la **réduction des déchets**, l’**optimisation de l’usage de l’eau** ou l’**économie circulaire** ; Innovation, traçabilité et potentiel de croissance
    - **Critères d’exclusion** : Activités polluantes non maîtrisées ; Manque de transparence sur les performances durables """)


    entreprises_projet = {
        "Plastic Repair System": {
            "ticker": "none",
            "description": """Créee en 2011, Plastic Repair System (PRS) est une entreprise d’économie circulaire dédiée à la réparation et à l’entretien d’objets en plastique, 
            principalement des emballages de transport réutilisables (ETRs), tels que des palettes, des boîtes, des Layer Pads, des conteneurs.
            La solution fournie par PRS est 187x meilleure en termes d’émissions de CO2 que le recyclage et le remplacement. 
            La vision de PRS est d’être reconnue comme l’entreprise leader dans la réparation et la maintenance d’objets en plastique, en se distinguant par son innovation et son engagement 
             envers la durabilité environnementale. """
        },
        "Biocoop": {
            "ticker": "none",
            "description": """Créée en 1986, Biocoop est le premier réseau de magasins bio en France en partenariat avec plus de 3 000 fermes. L'entreprise se consacre à la vente de produits biologiques et équitables, 
            avec un engagement fort envers le développement durable et la préservation de l'environnement. Biocoop promeut une agriculture respectueuse de l'environnement 
            et soutient les producteurs locaux. L'entreprise s'engage également à réduire son empreinte carbone et à favoriser l'économie circulaire."""
        },        
        "CarbonCure": {
            "ticker": "none",
            "description": """ Fondée en 2012, CarbonCure est une companie nord-américaine qui propose une solution innovante pour réduire l'empreinte carbone de l'industrie du béton, contribuant 
            ainsi à un futur plus durable pour la construction.
            """
        },
        }

    st.markdown("---") 

    # Sélection de l'actif projet
    choix = st.radio("Sélectionnez un projet", list(entreprises_projet.keys()))
    symbole = entreprises_projet[choix]["ticker"]
    description1 = entreprises_projet[choix]["description"]


    if choix == "Plastic Repair System":
        # Données financières
        st.markdown("""Société non cotée, pas de données financières disponibles""")
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Réparation d’emballages réutilisables : palettes, boîtes, caisses en plastique</li>
                    <li>Utilisation dans le transport et la logistique</li>
                    <li>Sites en Espagne, Pologne, Mexique</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Soudure plastique brevetée</li>
                    <li>Automatisation des processus</li>
                    <li>Étiquettes d'identification par radiofréquence intégrées</li>
                    <li>Amélioration de la traçabilité des plastiques</li>
                    <li>Solutions adaptées au type de dommage et aux besoins du client</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">Économie de 70% par rapport à l’achat neuf, récupération de 98% de la résistance.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">311 fois plus efficace que le recyclage en termes de CO2, </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">+100 emplois en insertion, objectif 550 d’ici 2027 (dont >450 peu qualifiés et 200 en Europe).</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Société privée. 6M$ levés par des VC.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Expansion au Royaume-Uni et au Portugal</li>
                    <li>Objectif d'obtenir la certification ISO 22000 (sécurité des denrées alimentaires)</li>
                </ul>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Section Labels
        st.subheader("Evaluation ESG de PRS")

        labels = {
            "ISO 14067": "ISO 14067 est une norme internationale qui certifie le calcul rigoureux de "
            "l’empreinte carbone d’un produit sur l’ensemble de son cycle de vie.",
            "Conformité norme Industry 4.0" : "Industry 4.0 désigne la 4ᵉ révolution industrielle, marquée par l’automatisation "
            "intelligente des processus grâce aux technologies numériques comme l’IoT, l’IA et la robotique.",
            "Programme Horizon 2020 de l'UE":"Horizon 2020 est le programme-cadre de l'UE pour la recherche et l'innovation"
        }

        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage dynamique des descriptions
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # Créer trois colonnes pour la section ESG
        col1, col2, col3 = st.columns(3)

        # Contenu pour la colonne 1 - Environnement
        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - **Économie circulaire** : réparation au lieu de remplacer
            - Émissions de CO2 réduites de 311 fois par rapport au recyclage
            - Allongement de la durée de vie des objets en plastique industriels
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Emplois en insertion : >100 actuellement, objectif 550 (dont 450 peu qualifiés)
            - Intégration de personnes en situation de handicap
            - Formation à un nouveau métier (soudeur de plastique)
            - Présence locale dans plusieurs régions
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - R&D interne et développement de solutions brevetées
            - Financements publics et privés (Horizon 2020, FEDER, Impact Partners)
            - Transparence sur les données clients via numérisation du process
            """)


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix == "Biocoop":
        # Données financières
        st.markdown("""Société non cotée, pas de données financières disponibles""")
        
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                Réseau coopératif de distribution alimentaire biologique, équitable et locale. 
                782 magasins indépendants en France engagés dans une charte stricte de produits 100% bio.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                Outils de traçabilité avancés, 
                transport biogaz, plateforme digitale pour les circuits courts et le vrac.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>+1,4 Mds € de chiffre d’affaires annuel</li>
                    <li>+7,6 M€ investis dans la structuration de filières locales</li>
                    <li>Partage équitable de la valeur avec 700 partenaires agricoles français</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>100 % énergies renouvelables</li>
                    <li>Suppression progressive du plastique à usage unique</li>
                    <li>34 % de produits sans emballage ou en emballage réutilisable</li>
                    <li>87 % des produits d'origine France, 18 % locaux</li>
                    <li>100% d'éléctricité verte consommée</li>
                    <li>0 transports en avion</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>94 % de salariés en CDI</li>
                    <li>Fonds de solidarité interne</li>
                    <li>Soutien à l’emploi local via les magasins indépendants</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">
                Modèle coopératif autofinancé. 
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                Objectif de 1 000 magasins d’ici 2030. Renforcement des filières bio françaises, élargissement de la consigne et du vrac.
                Développement de nouveaux outils numériques.
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)


        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Évaluation ESG de Biocoop")

        labels = {
            "89% Ecocert 26000": "Label basé sur la norme ISO 26000, évaluant l’engagement RSE d’une organisation selon 7 critères (gouvernance, droits humains, environnement, etc.).",
            "BioED": "Label interne de Biocoop récompensant les magasins les plus vertueux sur les plans écologique, éthique et social.",
            "HQE": "Label Haute Qualité Environnementale pour les bâtiments, garantissant une construction durable et respectueuse de l'environnement.",
            "ISO 14001": "La norme ISO 14001 est un standard international qui spécifie les exigences relatives à un système de management environnemental (SME) efficace.",
            "93/100 Index de l'égalité salariale": "L’index de l’égalité salariale est un outil qui mesure, sur 100 points, les écarts de rémunération entre les femmes et les hommes dans "
            "les entreprises, afin de favoriser l’égalité professionnelle.",
            "45% des magasins statut ESS":"Le statut ESS (Économie Sociale et Solidaire) pour un magasin désigne une entreprise qui privilégie l'intérêt collectif, l'insertion sociale et la durabilité, "
            "tout en étant gouvernée démocratiquement.",
            "Bio équitable":"Le label bio équitable en France certifie que les produits sont issus de l'agriculture biologique et respectent des critères de commerce équitable, garantissant des "
            "conditions de production et de rémunération justes pour les producteurs."
        }

        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage dynamique des descriptions
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # Colonnes ESG
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - Réduction massive de l’empreinte carbone (logistique, énergie, transport)
            - 100 % énergies renouvelables
            - Objectif zéro déchet : consigne, vrac, suppression plastique
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - 63% des magasins engagés sur les territoires dans au moins un programme de solidarité du Fonds de dotation Biocoop
            - Soutien à la filière bio locale
            - Dialogue social fort, intégration des parties prenantes
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Coopérative à gouvernance partagée (4 collèges)
            - Décisions prises collectivement
            - Transparence et vote en AG
            - 42% de femmes au conseil d'administration
            - 94 % CDI
            """)

        # Pourquoi ce projet ?
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix =="CarbonCure":
        # Données financières
        st.markdown("""Société non cotée, pas de données financières disponibles""")
        
        # Table CarbonCure
        st.markdown("""
                <table style="width:100%; border-collapse: collapse;">
                <tr style="background-color:#f2f2f2;">
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Activité</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Développement de technologies intégrant du CO₂ capturé dans le béton frais</li>
                            <li>Réduction de l’empreinte carbone de l’industrie du béton</li>
                            <li>Maintien des performances techniques du béton</li>
                        </ul>
                    </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Technologie</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Injection de CO₂ recyclé dans le béton</li>
                            <li>Minéralisation du CO₂ pendant le mélange</li>
                            <li>Amélioration de la durabilité du béton</li>
                            <li>12–15 kg de CO₂ économisés par m³</li>
                            <li>Technologie en place sur plus de 500 sites</li>
                        </ul>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact économique</b></td>
                    <td style="padding: 10px;">Réduction des coûts de production en remplaçant une partie du ciment par du CO₂ minéralisé et possibilité d’obtenir des crédits carbone.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Impact environnemental</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Réduction de l’empreinte carbone de l’industrie du béton</li>
                            <li>Valorisation du CO₂ capturé</li>
                            <li>Réduction des émissions mondiales de CO₂ associées à la production de béton</li>
                        </ul>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact social</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Soutien à la transition vers des pratiques plus durables dans la construction</li>
                            <li>Création de partenariats mondiaux pour déployer la technologie</li>
                        </ul>
                    </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Financement</b></td>
                    <td style="padding: 10px;">Companie privée non côtée.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Développement</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Expansion mondiale avec des milliers de systèmes opérant dans l’industrie du béton</li>
                            <li>Investissements dans des projets au Canada</li>
                        </ul>
                    </td>
                </tr>

                </table>
                """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Evaluation ESG de CarbonCure")

        labels = {
            "Grand Prix NRG COSIA Carbon XPRIZE competition" : "Le Grand Prix NRG COSIA Carbon XPRIZE est une compétition internationale récompensant les technologies "
            "les plus innovantes de valorisation du CO₂, transformant les émissions en produits à forte valeur ajoutée.",
            "Global Cleantech 100" : "Le Global Cleantech 100 est un classement annuel des 100 entreprises privées les plus innovantes et prometteuses au monde dans "
            "le domaine des technologies propres.",
            "North America’s 2020 Cleantech Company of the Year" : "Le titre de North America’s Cleantech Company of the Year est décerné par le Cleantech Group à "
            "l'entreprise nord-américaine la mieux classée dans le Global Cleantech 100, reconnaissant son impact exceptionnel en matière d'innovation durable et de décarbonation.",
            "BloombergNEF New Energy Pioneers" :"Le BloombergNEF New Energy Pioneers est un programme qui distingue chaque année les entreprises les plus innovantes contribuant à "
            "la transition mondiale vers une énergie propre et décarbonée.",
        }

        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage dynamique des descriptions
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # Créer trois colonnes pour la section ESG
        col1, col2, col3 = st.columns(3)

        # Contenu pour la colonne 1 - Environnement
        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - Réduction de l’empreinte carbone du béton
            - Valorisation du CO₂ capturé et réutilisé dans la production
            - Optimisation de l’utilisation de ciment dans la production de béton
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Création de partenariats mondiaux pour la diffusion de la technologie
            - Collaboration avec les gouvernements et industriels
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Expansion mondiale avec un impact croissant dans l’industrie du béton
            - Partenariats avec des entreprises leaders dans le secteur de la construction
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)


# -------------------------------
#    FONDS 
# -------------------------------
elif choix == "Fonds":
    st.markdown("""
    ### Critères de sélection des Fonds d'investissement

    Les fonds que nous sélectionnons intègrent une stratégie d’investissement thématique centrée sur la durabilité, en particulier dans la gestion de l’eau, la réduction des déchets et l’économie circulaire. 

    **Méthodologie d’analyse et de sélection :**
    - **Critères d’inclusion** : Impact environnemental mesurable ; Solutions concrètes en lien avec la **réduction des déchets**, l’**optimisation de l’usage de l’eau** ou l’**économie circulaire** ; Innovation, traçabilité et potentiel de croissance
    - **Critères d’exclusion** : Investissements dans des entreprises fortement émettrices de CO2 ; Manque de transparence sur les performances durables
    """)
    
    fonds_eau = {
        "Pictet Water": {
            "ticker": "0P000111I9.F",
            "description": """Le fonds Pictet Water est un fonds thématique investissant dans des entreprises liées à l’eau, à la gestion des déchets et à l’efficacité énergétique. 
            Il soutient des entreprises qui apportent des solutions concrètes à la crise de l’eau, tout en visant une rentabilité à long terme."""
        },
        "Sustainable Solutions Fund IV": {
            "ticker": "none",
            "description": """Le Sustainable Solutions Fund IV de Generation Investment Management investit dans des entreprises en croissance qui développent des solutions durables. 
            Le fonds applique une approche ESG rigoureuse et collabore avec les entreprises du portefeuille pour définir des indicateurs d’impact concrets. En tant que société indépendante 
            et détenue par ses associés, Generation cultive une culture d’investissement responsable et alignée avec les intérêts de ses clients. Elle s’engage à promouvoir un capitalisme 
            plus durable à travers ses investissements, son dialogue avec les entreprises et l’action de la Generation Foundation. Au 30 septembre 2024, elle gère 35,6 milliards de dollars d’actifs."""
        },
        }
    # Sélection du fonds à thématique eau
    choix = st.radio("Sélectionnez un", list(fonds_eau.keys()))
    symbole = fonds_eau[choix]["ticker"]
    description1 = fonds_eau[choix]["description"]

    if choix == "Pictet Water":
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)

        # Table Pictet Water
        st.markdown("""
                <table style="width:100%; border-collapse: collapse;">
                <tr style="background-color:#f2f2f2;">
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Activité</b></td>
                    <td style="padding: 10px;">Fonds thématique qui investit principalement dans les entreprises liées à l’approvisionnement, au traitement de l’eau, et aux services environnementaux connexes. 
                    Principalement orienté vers la gestion des déchets et l'approvisionnement en eau, avec des investissements significatifs aux États-Unis (71.17 %), un peu au Canada et au Royaume-Uni. </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Approche</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Gestion active axée sur une analyse fondamentale des entreprises du secteur de l’eau</li>
                        <li>Intégration poussée des critères ESG</li>
                        <li>Exclusions strictes</li>
                        <li>Engagement actionnarial avec les entreprises du portefeuille</li>
                    </ul>
                </td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact économique</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Historique de performance solide depuis le lancement (+404.17 %)</li>
                            <li>Volatilité importante (15.19 %)</li>
                        </ul>
                    </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Impact environnemental</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Investit massivement dans des entreprises œuvrant pour la gestion durable de l’eau</li>
                            <li>Très faible exposition aux combustibles fossiles (0.02 %)</li>
                            <li>Très faible exposition aux armes (0.30 %)</li>
                        </ul>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact social</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Favorise les entreprises promouvant l’accès à l’eau</li>
                            <li>Soutien à la santé publique et aux services essentiels dans le monde entier</li>
                            <li>Présence dans les marchés émergents comme la Chine</li>
                        </ul>
                    </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Financement</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Géré activement par Pictet Asset Management</li>
                            <li>Taille : 7 102 M€ au 10/04/2025</li>
                        </ul>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Développement</b></td>
                    <td style="padding: 10px;">
                        <ul>
                            <li>Fonds lancé en 2006 avec une stratégie consolidée</li>
                            <li>Exposition majeure aux marchés développés, principalement aux États-Unis (71 %)</li>
                            <li>Diversification sectorielle axée sur l’eau et la gestion des déchets</li>
                        </ul>
                    </td>
                </tr>
                </table>
                """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels - Récompenses ESG (exemples à adapter ou compléter)
        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "Fonds UCITS de droit luxembourgeois" : "Un Fonds UCITS de droit luxembourgeois est un fonds d’investissement conforme à la réglementation européenne "
            "UCITS, domicilié au Luxembourg, offrant une protection renforcée des investisseurs et la possibilité de distribution transfrontalière au sein de l’Union européenne.",
            "A MSCI ESG Rating" : "Le MSCI ESG Rating évalue les performances environnementales, sociales et de gouvernance d'une entreprise, attribuant "
            "une note de AAA à CCC pour refléter sa gestion des risques et opportunités ESG.",
            }
        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage dynamique des descriptions
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # Créer trois colonnes pour la section ESG
        col1, col2, col3 = st.columns(3)

        # Contenu pour la colonne 1 - Environnement
        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - Investissements orientés vers la gestion durable de l’eau
            - Faible exposition aux énergies fossiles
            - Utilisation de critères ESG exigeants dans la sélection
            - 15,4 % du chiffre d'affaires total généré par les actifs du fonds provient d’activités vertes.
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Contribution à l’accès à l’eau potable dans les marchés émergents
            - Engagement pour la santé publique et les infrastructures essentielles
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Exercice actif des droits de vote
            - Transparence dans les politiques d’exclusion
            - 37.9% de femmes dans les conseils d’administration des entreprises du portefeuille
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix == "Sustainable Solutions Fund IV":   
        # Récupération des données financières
        st.markdown("Ce fonds étant un fonds de private equity, nous ne disposons pas de données financières en temps réel.")

        # Table Generation Investment Management
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>
                    
        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Fonds de capital-investissement axé sur les entreprises en croissance</li>
                    <li>Développement de solutions durables dans les domaines suivants :
                        <ul>
                            <li>Santé planétaire</li>
                            <li>Santé des personnes</li>
                            <li>Inclusion financière</li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Approche</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Investissements minoritaires dans des entreprises à fort potentiel</li>
                    <li>Intégration approfondie des critères ESG</li>
                    <li>Collaboration étroite pour définir des indicateurs d'impact spécifiques</li>
                    <li>86% des investissements réalisés en Amérique du Nord</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>35,387 tCO₂e (0% scope 1, 12% scope 2)</li>
                    <li>Investissements dans des entreprises à forte croissance</li>
                    <li>Tickets de 50 à 150 millions USD</li>
                    <li>Objectif : rendements ajustés au risque attractifs</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Soutien à des solutions bas carbone</li>
                    <li>Promotion de l'économie circulaire</li>
                    <li>Préservation de la biodiversité</li>
                    <li>Indicateurs d’impact environnemental définis en partenariat avec les entreprises du portefeuille</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>5.7K emplois créés</li>
                    <li>Accès aux soins de santé abordables</li>
                    <li>Promotion de l’inclusion financière</li>
                    <li>Investissements favorisant la cohésion sociale et la réduction des inégalités</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Fonds de 1.7 milliard USD</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Support continu aux entreprises du portefeuille</li>
                    <li>Objectif : impact positif et croissance économique</li>
                </ul>
            </td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "B-Corp": "Certification pour les entreprises conciliant but lucratif et impact sociétal et environnemental positif.",
            "Signataire des PRI": "Signataire des Principes pour l'Investissement Responsable soutenus par les Nations Unies, intégrant les facteurs ESG dans les décisions d'investissement.",
        }

        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - Investissements dans des solutions bas carbone et l'économie circulaire
            - Définition d'indicateurs d'impact environnemental en collaboration avec les entreprises
            - Suivi des performances environnementales à l'échelle du portefeuille
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Promotion de l'accès aux soins de santé abordables
            - Soutien à l'inclusion financière et à la cohésion sociale
            - Engagement pour la diversité et l'inclusion au sein des entreprises du portefeuille
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Parité homme-femme au sein des partners et de l'équipe d'investisseemnt
            - Collaboration étroite avec les entreprises pour définir des indicateurs d'impact spécifiques
            - Engagement actif auprès des entreprises pour promouvoir des pratiques durables
            """)

        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

# -------------------------------
#   ACTIONS DURABLES EAU
# -------------------------------
elif choix=="Actions":

    st.markdown("""
    ### Critères de sélection des Actions Durables 
    Nous sélectionnons des actions d'entreprises qui démontrent un engagement fort en matière de protection de l'environnement, réduction des déchets et traitement de l'eau.
    **Méthodologie de sélection :** 
    - **Critères d'inclusion** : Engagement mesurable en matière de diversité et d'inclusion ; Objectif de protection de l'environnement et/ou de garantir un accès à l'eau ; Impact environnemental positif démontré ; Bon score ESG
    - **Critères d'exclusion** : Pratiques controversées ; Manque de transparence sur les initiatives environnementales ; Greenwashing
    """)

    actions = {
        "Equinix": {
            "ticker": "EQIX",
            "description": """Fondée dans la Silicon Valley en 1998, Equinix est leader mondial des infrastructures numériques en tant que fournisseur de services de datacentres multi-tenant indépendants. 
            À travers ses engagements ESG, l’entreprise connecte les organisations tout en minimisant son empreinte environnementale et en renforçant sa responsabilité sociale et éthique. 
            Son ambition : bâtir l’infrastructure numérique la plus durable au monde.
            """
        },
        "Tomra": {
            "ticker": "TOM.OL",
            "description": """Tomra Systems ASA fournit des solutions de tri et de recyclage pour aider ses clients à gérer les déchets. L'entreprise conçoit et fournit des solutions basées sur des capteurs qui contribuent 
            à une productivité optimale des ressources dans des domaines tels que l'emballage, la collecte, la compaction, le recyclage, le tri des minerais et la production alimentaire. Elle propose des distributeurs automatiques 
            inversés, des machines de tri basées sur des capteurs, des solutions post-récolte intégrées, des capteurs pour les applications de tri des déchets, ainsi que d'autres produits et solutions connexes. Les segments d'activité de 
            l'entreprise sont : TOMRA Collection, qui génère les principaux revenus, TOMRA Recycling, TOMRA Horizon et TOMRA Food. Géographiquement, l'entreprise génère ses revenus principalement en Europe (hors Europe du Nord), 
            suivie de l'Europe du Nord, de l'Amérique, de l'Asie et de l'Océanie."""
        },
        "SIG Group": {
            "ticker": "SIGN.SW",
            "description": """Créee en 1853 puis renommée en 2022, SIG est un leader mondial dans les systèmes d'emballage aseptiques pour les produits alimentaires et les boissons. 
            L'entreprise propose des lignes de remplissage aseptiques, des manchons et des fermetures pour cartons aseptiques, ainsi que des solutions telles que bag-in-box et pouch à bec. 
            Elle opère principalement en Europe, en Inde, au Moyen-Orient, en Afrique, dans la région Asie-Pacifique et en Amérique. 
            Son modèle commercial repose sur une innovation continue, une forte collaboration avec ses clients et un engagement à fournir des solutions respectueuses de l'environnement à l'échelle mondiale."""
        },
        "Veolia": {
            "ticker": "VIE.PA",
            "description": """Veolia vise à devenir l'entreprise de référence pour la transformation écologique, en apportant des solutions innovantes et durables dans la gestion de l'eau, des déchets et de l'énergie.
            """
        },
        "Chia": {
            "ticker":"XCH-EUR",
            "description":"""Chia propose une solution de blockchain décentralisée, durable et énergétiquement efficace. Cette alternative verte de crypto-minage utilise l’espace libre sur les disques durs des participants au réseau, en y écrivant des « tracés » de 10 Go. 
            Ces graphiques sont ensuite utilisés pour valider de nouveaux blocs sur le réseau, mais de manière peu gourmande en énergie. Selon le site Internet de Chia, cette approche signifie 
            que Chia consomme 500 fois moins d’électricité que le réseau Bitcoin."""
        },
        }

    # Sélection de l'action à thématique eau
    choix = st.radio("Sélectionnez un actif", list(actions.keys()))
    symbole = actions[choix]["ticker"]
    description1 = actions[choix]["description"]

    if choix == "Equinix":
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours d' {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("### Caractéristiques générales de l'actif")

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>260 centres de données répartis dans 71 marchés</li>
                    <li>Fournisseur de solutions d’interconnexion et de colocation</li>
                    <li>Plus de 10 000 clients, dont :
                        <ul>
                            <li>2 100 fournisseurs de réseaux</li>
                            <li>Acteurs dans les secteurs cloud, télécoms, médias, finance et entreprises</li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Exploitation d’une plateforme mondiale optimisée pour :
                        <ul>
                            <li>La connectivité</li>
                            <li>L'efficacité énergétique</li>
                            <li>La résilience</li>
                        </ul>
                    </li>
                    <li>Intégration de technologies durables</li>
                    <li>Utilisation d’énergies renouvelables</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>70 % du chiffre d'affaires provient de la location d'espaces et services associés</li>
                    <li>Plus de 15 % proviennent des interconnexions</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>96 % d’énergie renouvelable en 2023</li>
                    <li>Réduction de 24 % des émissions (Scope 1 et 2) depuis 2019</li>
                    <li>21 contrats PPA soutenant plus de 3 millions de MWh d’énergie propre</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Répartition géographique :
                        <ul>
                            <li>44 % Amériques</li>
                            <li>35 % EMEA</li>
                            <li>21 % Asie-Pacifique</li>
                        </ul>
                    </li>
                    <li>1,9 M$ en dons communautaires</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Société cotée au NASDAQ sous le symbole EQIX</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Poursuite de l’expansion mondiale avec de nouveaux centres de données</li>
                    <li>Investissements dans l'efficacité énergétique et l’innovation durable</li>
                    <li>Engagement à :
                        <ul>
                            <li>Atteindre 100 % d’énergie renouvelable d’ici 2030</li>
                            <li>Renforcer les interconnexions numériques pour la transformation numérique mondiale</li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Section Labels
        st.subheader("Évaluation ESG d’Equinix")

        labels = {
            "ISO 14001": "La norme ISO 14001 est un standard international qui spécifie les exigences relatives à un système de management environnemental (SME) efficace.",
            "ISO 45001": "La norme ISO 45001 est une norme internationale qui spécifie les exigences relatives à un système de management de la santé et de la sécurité au travail (SST).",
            "ISO 50001": "Optimisation du management de l’énergie sur tous les sites en EMEA, Asie-Pacifique et plusieurs États américains.",
            "LEED Gold / Platinum": "Tous les nouveaux bâtiments d’Equinix sont certifiés pour leur performance énergétique selon les normes LEED.",
            "CDP A List (Climat)": "Reconnue pour la transparence climatique, Equinix figure pour la 2e année consécutive sur la liste A du CDP.",
            "Green Power Reports (GPR)": "Rapports permettant aux clients de connaître leur part d’énergie renouvelable selon le GHG Protocol.",
            "13.1 ESG Risk Rating Sustainalytics":"Le Sustainalytics ESG Risk Rating évalue les risques ESG d'une entreprise, en attribuant une note allant "
            "de Faible=0 à Élevé=100 pour indiquer l'ampleur des risques liés aux facteurs environnementaux, sociaux et de gouvernance.",
            "60 S&P Global ESG Score":"Le S&P Global ESG Score évalue la performance d'une entreprise en matière de gestion des risques et des opportunités "
            "liés aux critères environnementaux, sociaux et de gouvernance (ESG), sur une échelle de 0 à 100.",
            "Silver 2023 ecovadis Sustainability Rating":"La distinction Silver 2023 d’EcoVadis correspond à une évaluation de la performance RSE plaçant "
            "l’entreprise dans le top 25 % des entreprises les mieux notées en matière de durabilité environnementale, sociale, éthique et d’achats responsables.",
            "Alliance for Global Inclusion Index Companies 2023":"L’Alliance for Global Inclusion Index Companies 2023 reconnaît les entreprises qui s’engagent activement à promouvoir la diversité, l’équité et l’inclusion (DEI) à l’échelle mondiale, en se basant sur des indicateurs mesurables et des actions concrètes."
        }

        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # ESG Columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - 96 % d’énergie renouvelable couverte en 2023.
            - Réduction de 24 % des émissions opérationnelles scope 1 et 2 depuis 2019.
            - 78 millions de dollars investis dans l’efficacité énergétique. 
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - 53 % des employés US issus de groupes marginalisés.
            - +17 % de femmes employées, +14 % d’Afro-Américains en 2023.
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Gestion rigoureuse de la cybersécurité et de la gouvernance des données.
            - Intégration systématique de la durabilité dans toutes les opérations.
            - Membre fondateur de l'Association des Centres de Données de la région Asie-Pacifique, 
            la première association professionnelle de ce type dans la région.
            """)

        # Pourquoi ce projet ?
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

        
    # -------------------------------
    elif choix == "SIG Group":

        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours de {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Fournisseur leader de solutions d'emballage aseptique</li>
                    <li>Types d’emballages :
                        <ul>
                            <li>Carton</li>
                            <li>Bag-in-box</li>
                            <li>Pouch avec embout</li>
                        </ul>
                    </li>
                    <li>Destiné aux produits alimentaires et boissons</li>
                    <li>Présence dans les marchés émergents et établis</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Innovations dans l'emballage aseptique</li>
                    <li>Ingénierie technique avancée</li>
                    <li>Services de R&D pour co-créer des solutions avec les clients</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Croissance du chiffre d'affaires de 4,3 % en 2024</li>
                    <li>Chiffre d'affaires : 3,33 milliards d'euros</li>
                    <li>Marge EBITDA ajustée de 24,6 %</li>
                    <li>Expansion continue dans les emballages aseptiques et bag-in-box</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>100 % de l'énergie utilisée issue de sources renouvelables</li>
                    <li>Réduction des émissions de CO₂ de 20,1 kilotonnes (scope 1 et 2)</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>9 600 employés dans le monde</li>
                    <li>Présence locale dans divers marchés émergents</li>
                    <li>Création de synergies commerciales entre types d'emballages</li>
                    <li>Soutien aux entreprises locales</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Société cotée à la bourse Suisse</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Expansion dans les marchés émergents, notamment en Inde</li>
                    <li>Focus sur :
                        <ul>
                            <li>L’augmentation de la part de marché pour les emballages bag-in-box</li>
                            <li>Le développement des emballages pouch</li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Section Labels
        st.subheader("Evaluation ESG de SIG")

        labels = {
            "Platinum EcoVadis Rating": "SIG a obtenu une note Platinum d'EcoVadis avec un score record de 96/100 en 2024, comparé à 86/100 en 2023.",
            "AAA MSCI ESG Rating": "Le MSCI ESG Rating évalue les performances environnementales, sociales et de gouvernance d'une entreprise, attribuant "
            "une note de AAA à CCC pour refléter sa gestion des risques et opportunités ESG.",
            "Ba1 Moddys Rating": "Le Moody's Rating évalue la solvabilité des entreprises et des gouvernements, attribuant des notes de Aaa à C "
            "pour indiquer le risque de crédit et la capacité de remboursement.",
            "BBB S&P Rating": "Le S&P Rating évalue la solvabilité des emprunteurs, attribuant des notes de AAA à D pour indiquer "
            "le risque de crédit et la probabilité de défaut. ",
            "10.5 ESG Risk Rating Sustainalytics":"Le Sustainalytics ESG Risk Rating évalue les risques ESG d'une entreprise, en attribuant une note allant "
            "de Faible=0 à Élevé=100 pour indiquer l'ampleur des risques liés aux facteurs environnementaux, sociaux et de gouvernance.",
            "FTSE4Good Index Series":"La FTSE4Good Index Series est une série d'indices boursiers qui évalue les entreprises en fonction de leurs performances "
            "environnementales, sociales et de gouvernance (ESG), servant de référence pour les investissements responsables.", 
            "Green Packaging Star Award":"Le Green Packaging Star Award est un prix qui reconnaît les entreprises et innovations exceptionnelles dans le domaine de "
            "l'emballage durable, récompensant les efforts visant à réduire l'impact environnemental des solutions d'emballage.", 
            "WorldStar for Packaging award 2024":"Les WorldStar Packaging Awards sont des distinctions internationales décernées par la World Packaging Organisation (WPO) "
            "pour récompenser l'excellence en matière de design et d'innovation dans le domaine de l'emballage.",
            "FSC™ Certified":"Le label FSC™ Certified est une certification délivrée par le Forest Stewardship Council (FSC), une organisation internationale à but non lucratif "
            "créée en 1993 pour promouvoir la gestion responsable des forêts mondiales. Ce label garantit que les produits portant cette certification proviennent de forêts gérées "
            "de manière environnementalement appropriée, socialement bénéfique et économiquement viable.",
        }

        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage dynamique des descriptions
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # Créer trois colonnes pour la section ESG
        col1, col2, col3 = st.columns(3)

        # Contenu pour la colonne 1 - Environnement
        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - **Emballage durable** : Des solutions aseptiques conçues pour minimiser l'impact environnemental 
            et favoriser un système d'emballage régénératif, contribuant ainsi à la protection des écosystèmes et à la lutte contre le changement climatique.
            - **100% d'énergie renouvelable** utilisée pour la production, réduisant l'empreinte carbone et soutenant une économie circulaire durable.
            - **Émissions de CO2** pour les scopes 1 et 2 s'élèvent à 20,1 kilotonnes de CO2 équivalent.
            """)


        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Présence dans les marchés émergents : Développement économique et emploi local.
            - Innovation collaborative avec les clients dans les centres R&D mondiaux.
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Entreprise privée avec une forte gouvernance familiale.
            - 25% de femmes dans des positions dirigeantes.
            - Financements durables et partenariats stratégiques à l'international.
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)
    
    # -------------------------------
    elif choix =="Tomra":

        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours de {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>70 % de part de marché des distributeurs automatiques de déconsigne</li>
                    <li>50 % du marché des machines de tri</li>
                    <li>Fournisseur de solutions technologiques pour le recyclage, le tri des déchets et l’optimisation de la production alimentaire</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Capteurs avancés pour automatiser la collecte, le tri et le recyclage</li>
                    <li>Solutions de calibrage, tri, épluchage et analyse</li>
                    <li>Amélioration des rendements et rentabilité des entreprises alimentaires</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Chiffre d'affaires de 1,35 milliard d'euros en 2024</li>
                    <li>Marge EBITDA de 13,4 %</li>
                    <li>Croissance des solutions de recyclage et de tri automatisés</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>45 milliards de cannettes et bouteilles collectées chaque année</li>
                    <li>Réduction des déchets et préservation des ressources naturelles</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>5 300 employés</li>
                    <li>Présence dans plus de 100 marchés</li>
                    <li>Facilite le recyclage pour les consommateurs et les entreprises</li>
                    <li>Réduction des pertes alimentaires mondiales</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Entreprise cotée sur la bourse norvégienne</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Expansion dans les technologies de recyclage et d’automatisation</li>
                    <li>Déploiement de systèmes de consigne en Europe et en Asie (Singapour, Portugal, Grèce, Espagne, Angleterre...)</li>
                </ul>
            </td>
        </tr>


        </table>
        """, unsafe_allow_html=True)

        # Section Labels
        st.subheader("Evaluation ESG de TOMRA")

        labels = {
            "ISO 14001": "La norme ISO 14001 est un standard international qui spécifie les exigences relatives à un système de management environnemental (SME) efficace.",
            "ISO 45001": "La norme ISO 45001 est une norme internationale qui spécifie les exigences relatives à un système de management de la santé et de la sécurité au travail (SST).",
            "ISO 9001": "La norme ISO 9001 est une norme internationale qui spécifie les exigences relatives à un système de management de la qualité (SMQ).",
            "A- Scope Rating": "Le Scope Rating est une agence de notation financière européenne qui évalue la solvabilité des entreprises, institutions financières, États et émissions obligataires, "
            "en tenant compte des risques financiers, économiques et parfois ESG (environnementaux, sociaux et de gouvernance).",
            "27.4 ESG Risk Rating Sustainalytics": "Le Sustainalytics ESG Risk Rating de TOMRA est de 9,2, ce qui reflète un faible niveau de risques ESG, prouvant son engagement à réduire les impacts environnementaux et sociaux.",
            "34 S&P Global ESG Score":"Le S&P Global ESG Score évalue la performance d'une entreprise en matière de gestion des risques et des opportunités liés aux critères environnementaux, sociaux et de gouvernance (ESG), sur une échelle de 0 à 100.",
        }

        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage dynamique des descriptions
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # Créer trois colonnes pour la section ESG
        col1, col2, col3 = st.columns(3)

        # Contenu pour la colonne 1 - Environnement
        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - **Recyclage avancé** : Solutions innovantes de tri basées sur des capteurs pour automatiser la récupération et le recyclage de matériaux, améliorant la qualité des matériaux recyclés et réduisant les déchets.
            - 82 000 automates de déconsigne sur plus de 60 marchés.
            - 13 800 unités de tri et de traitement post-récolte pour améliorer la sécurité alimentaire et réduire les pertes alimentaires mondiales (produits frais et aliments transformés)
            - 9 000 machines de tri pour le recyclage des déchets plastiques, métalliques et électroniques.
            - 31 476 tonnes métriques d'émissions scope 1 et 2 de CO2.
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Améliore l'accès au recyclage et réduire l'empreinte écologique des consommateurs.
            - Améliore la sécurité et la durabilité des produits alimentaires à l'échelle mondiale.
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            -  Pratiques de gouvernance strictes pour assurer une gestion responsable des technologies et des ressources naturelles.
            - 26% de femmes dans des postes de direction.
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix == "Veolia":
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours de {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Traitement de l’eau</li>
                    <li>Gestion des déchets et services énergétiques</li>
                    <li>Présence en France, Royaume-Uni, Allemagne, États-Unis et Australie</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Recyclage avancé</li>
                    <li>Réutilisation de l'eau</li>
                    <li>Valorisation énergétique des déchets</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Chiffre d'affaires de 44,7 milliards d’euros en 2024</li>
                    <li>572 000 entreprises clientes dans le monde</li>
                    <li>Acteur clé dans les secteurs de l’eau, des déchets et de l’énergie</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>65 millions de tonnes de déchets traités par an</li>
                    <li>861 unités de traitement</li>
                    <li>42 millions de MWh d’énergie verte produits</li>
                    <li>Réduction des déchets et préservation des ressources naturelles</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>111 millions de personnes servies en eau potable</li>
                    <li>Amélioration de la qualité de vie et accès aux ressources essentielles</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Entreprise cotée à la bourse de Paris</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Innovations en gestion de l’eau, recyclage et énergies renouvelables</li>
                    <li>Objectif : devenir le leader mondial de la transformation écologique</li>
                </ul>
            </td>
        </tr>


        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Evaluation ESG de Veolia")

        labels = {
            "ISO 14001": "La norme ISO 14001 est un standard international qui spécifie les exigences relatives à un système de management environnemental (SME) efficace.",
            "ISO 45001": "La norme ISO 45001 est une norme internationale qui spécifie les exigences relatives à un système de management de la santé et de la sécurité au travail (SST).",
            "ISO 9001": "La norme ISO 9001 est une norme internationale qui spécifie les exigences relatives à un système de management de la qualité (SMQ).",
            "A- Scope Rating": "Le Scope Rating est une agence de notation financière européenne qui évalue la solvabilité des entreprises, institutions financières, États et émissions obligataires, "
            "en tenant compte des risques financiers, économiques et parfois ESG (environnementaux, sociaux et de gouvernance).",
            "79 S&P Global ESG Score":"Le S&P Global ESG Score de Veolia est de 79/100, reflétant une solide performance en matière de gestion des risques et des opportunités liés aux critères ESG.",
            "25.5 ESG Risk Rating Sustainalytics": "Le Sustainalytics ESG Risk Rating de Veolia est de 25.5, indiquant un faible risque ESG et prouvant son engagement dans la gestion durable des ressources.",
        }

        # État des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage dynamique des descriptions
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")

        # Créer trois colonnes pour la section ESG
        col1, col2, col3 = st.columns(3)

        # Contenu pour la colonne 1 - Environnement
        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - 65 millions de tonnes de déchets traités chaque année, avec des solutions innovantes de recyclage et de valorisation énergétique.
            - 3 879 usines de production d'eau potable et 3 198 usines de traitement des eaux usées.
            - Engagement dans la préservation des ressources naturelles et l'amélioration de la qualité de l'eau.
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - 215 000 collaborateurs dans plus de 50 pays
            - Accès à des services essentiels pour des communautés dans le besoin, améliorant la qualité de vie des habitants.
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Gestion transparente et responsable des ressources.
            - Normes strictes en matière de sécurité, de santé au travail et de durabilité environnementale.
            - 30% de femmes dans des postes de direction.
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)


 # -------------------------------
    elif choix =="Chia":

        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours de {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Alternative verte au crypto-minage</li>
                    <li>Utilise l’espace disque pour valider des blocs sur la blockchain</li>
                    <li>Consommation estimée 500 fois inférieure à celle du réseau Bitcoin</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Consensus Proof of Space and Time (PoST)</li>
                    <li>Utilisation de l’espace de stockage disponible</li>
                    <li>Alternative économe au Proof of Work (PoW)</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Soutien à l’économie circulaire du stockage</li>
                    <li>Réduction des déchets électroniques</li>
                    <li>Prolonge la durée de vie des disques durs</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Faible consommation énergétique</li>
                    <li>Empreinte carbone réduite par rapport au Bitcoin</li>
                    <li>Recyclage des disques durs</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Blockchain accessible et durable</li>
                    <li>Facilite l’inclusion financière des populations sous-bancarisées</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Société privée financée par du capital-risque</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Développement continu de l’écosystème Chia</li>
                    <li>Soutien aux développeurs</li>
                    <li>Intégration de solutions de finance verte (ex. Chia Climate App, Chia Registry App)</li>
                </ul>
            </td>
        </tr>


        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Évaluation ESG de Chia")

        # ESG Columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - Réduction significative de la consommation d’énergie par rapport à Bitcoin.
            - Adoption de technologies permettant une économie circulaire du stockage et la réduction des déchets électroniques.
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Accès équitable aux solutions financières et à la technologie blockchain pour les populations sous-bancarisées.
            - Soutien à l'innovation et à l'inclusivité par l'appui aux développeurs et aux projets open-source.
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Engagement envers la conformité réglementaire mondiale.
            - Utilisation de la transparence et de la blockchain pour renforcer la confiance dans les marchés des crédits carbone.
            """)

        # Pourquoi ce projet ?
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)



# -------------------------------
# INFOS FOOTER
# -------------------------------
st.sidebar.info("Ce dashboard présente les performances financières et les évaluations ESG des actifs séléctionnées par notre fonds.")
st.markdown("---")
st.caption("© 2025 - Dashboard ESG_Reghina&Coline&Cosima | Streamlit prototype | Projet Finance Durable")
