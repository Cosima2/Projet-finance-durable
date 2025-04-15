import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import numpy as np
from datetime import datetime
import os

# -------------------------------
# TITRE ET INTRODUCTION
# -------------------------------
st.set_page_config(page_title="Partie spécifique thématique inclusion et équité", layout="wide")

st.title("Fonds d'investissement ESG")

st.markdown(
    "L'inclusion sociale et l'équité représentent des défis majeurs pour des sociétés plus justes : accès à l'emploi, "
    "réduction des inégalités, promotion de la diversité et inclusion financière. \n\n"
    "Dans le cadre de notre portefeuille ESG, la partie spécifique cible des entreprises et projets innovants "
    "qui développent des solutions transformatrices pour répondre à ces enjeux cruciaux. \n\n"
    "Nous avons sélectionné des obligations sociales, des fonds thématiques et des actions d'entreprises "
    "strictement alignés sur la thématique de **l'inclusion sociale**, alliant **impact sociétal tangible** et "
    "**performance économique durable**."
)

# -------------------------------
# VISUALISATION DE LA RÉPARTITION SPÉCIFIQUE
# -------------------------------
st.header("Composition de la partie spécifique liée à la thématique de l'inclusion")

composition_spe = {
    "Actifs Projet": 6,
    "Fonds à Impact": 1,
    "Obligations Corporate": 1,
    "Actions Durables Inclusion": 6
}
df_spe = pd.DataFrame(list(composition_spe.items()), columns=["Actif", "Poids (%)"])

# Camembert avec style
fig_spe = px.pie(
    df_spe,
    values="Poids (%)",
    names="Actif",
    title="Répartition de notre portefeuille spécialisé ESG",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Pinkyl
)

# Options de layout pour un rendu plus élégant
fig_spe.update_traces(textinfo='percent', pull=[0.05, 0.05, 0.1])  # Ajustez les valeurs de pull selon le nombre d'éléments
fig_spe.update_layout(
    title_font_size=20,
    title_x=0.5,
    legend_title="Catégories d'actifs",
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
)

# Affichage
st.plotly_chart(fig_spe, use_container_width=True)

# -------------------------------
# Performance du portefeuille inclusion sociale
# -------------------------------

# Configuration des pondérations 
ponderation = {
    "oblig": 0.20,  # Rendement yield-to-maturity (obligations souveraines)
    "fonds": 0.15,  # Mark-to-market
    "etfs": 0.10,   # Mark-to-market
    "driver": 0.55  # Actifs à impact social (remplace 'driver' du code original)
}

# Liste des actifs originaux (inchangée)
actifs = {
    "oblig": ["CRIIRLTLT01STM", "IRLTLT01CAM156N", "IRLTLT01ISM156N", 
              "IRLTLT01GBM156N", "IRLTLT01NOM156N", "COLIRLTLT01STM"],
    "fonds": ["0P0000G6X1.F", "0P0001IVQQ.F", "0P0000KU3M.F", 
              "0P0001HZQR.F", "0P00016ZNX.F"],
    "etfs": ["CYBO.SW", "REUS.L", "ISUN.L", "PAWD.L", "GSOV.DE", "CLMA.MI"],
    "driver": ["SW.PA", "CAP.PA", "EL.PA", "2353.TW", "7951.T"]  # Actions inclusion sociale
}

st.subheader("Performance du portefeuille avec thématique inclusion sociale")
st.markdown("""
**Évolution de notre allocation thématique sur 5 ans**  
Stratégie d'investissement social avec répartition :
- **55%** Actifs projets à impact social direct
- **20%** Obligations souveraines (stabilité)
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
# ---- Explications méthodologiques ----
with st.expander("Méthodologie détaillée"):
    st.markdown("""
    **Approche différenciée par classe d'actifs :**  
    
    - **Obligations souveraines** :  
      Intégration en **buy-and-hold** avec rendement actuariel (yield-to-maturity)  
      → Conversion annualisée → journalière pour stabilité à long terme  
      
    - **Fonds/ETFs thématiques** :  
      Valorisation **mark-to-market** avec filtrage ESG strict (★★★★ minimum)  
      → Capture de la dynamique marché + impact réel  
      
    - **Actifs projets d'inclusion** (55% du portefeuille) :  
      Évaluation trimestrielle basée sur :  
      ✓ Critères financiers (CA, croissance)  
      ✓ Indicateurs d'impact social (emplois créés, accès aux services)  
      ✓ Comparables cotés  
    
    **Indicateurs clés :**  
    - Volatilité annualisée : mesure du risque ajusté à l'horizon temporel  
    - Ratio de Sharpe : efficacité du rendement par unité de risque  
    - Score d'impact : suivi via les rapports d'activité des projets  
    """)

st.success("""
**Performance & Résilience :**  
Tendance haussière constante sur 5 ans malgré les turbulences marché  
Volatilité maîtrisée grâce à la diversification (projets + obligations)  
Marge de manœuvre accrue pour investir dans des initiatives sociales innovantes  

*"Notre approche combine stabilité financière et impact sociétal mesurable"*  
""")

st.markdown("---")

# -------------------------------
# DÉTAIL DES ACTIFS SPÉCIFIQUES
# -------------------------------
st.header("Analyse détaillée de la partie spécifique (55%)")
st.write(
    "Cette section présente la répartition détaillée des actifs composant la partie spécifique du portefeuille liée à la thématique de l'inclusion des populations défavorisées ou marginalisées. "
    "Les actifs sont sélectionnés en fonction de leur impact social positif et de leur contribution à un accès équitable et durable à la ressource en eau pour les populations défavorisées et marginalisées."
)

categorie_actifs_spe = list(composition_spe.keys())
choix = st.radio("Sélectionnez une catégorie d'actifs", categorie_actifs_spe)

# -------------------------------
#   ‼️ ACTIFS PROJET ‼️
# -------------------------------
if choix == "Actifs Projet":
    st.markdown("""
    ### Critères de sélection des Actifs Projet

    Nous sélectionnons des entreprises et initiatives sociales innovantes qui créent un impact tangible sur l'inclusion et l'équité.

    **Méthodologie de sélection :**
    - **Critères d'inclusion** : Impact social direct et mesurable ; Modèle économique viable combinant performance financière et utilité sociale ; Approche inclusive (genre, handicaps, territoires défavorisés) ; Innovation sociale et potentiel de réplication
    - **Critères d'exclusion** : Activités générant ou exacerbant des inégalités sociales ; Manque de transparence sur la mesure d'impact ; Modèle dépendant de subventions à long terme""")

    entreprises_projet = {
        "I Was A Sari": {
            "ticker": "?",
            "description": """Nous croyons que la mode peut être un levier de transformation sociale et environnementale.
            Le projet I Was A Sari, né à Mumbai, illustre cette conviction en transformant d’anciens saris en accessoires contemporains tout en formant des femmes issues de quartiers défavorisés aux métiers du textile. 
            Ce modèle circulaire permet à ces femmes d’accéder à un emploi stable, de gagner un revenu digne et de retrouver confiance en elles.
            Soutenu par le programme Gucci Equilibrium, le projet allie savoir-faire local, inclusion féminine et économie circulaire. Nous soutenons cette initiative à fort impact, qui transforme à la fois des déchets et des vies."""
        },
        "Simplon.co": {
            "ticker": "?",
            "description": """Simplon.co forme gratuitement aux métiers du numérique des personnes 
            éloignées de l’emploi (jeunes sans diplôme, réfugiés, femmes en reconversion, etc.), via des écoles inclusives en 
            France et à l’international. Leur pédagogie pratique et collaborative permet un fort taux de retour à l’emploi. 
            Avec plus de 25 000 personnes formées et un modèle équilibré financièrement, Simplon répond à deux enjeux majeurs : la pénurie de compétences tech et les inégalités sociales. 
            Nous soutenons ce projet à fort impact et à fort potentiel de réplication."""
        },
        "La Varappe": {
            "ticker": "?",
            "description": """La Varappe accompagne chaque année plus de 4 000 personnes très éloignées 
            de l’emploi via des chantiers dans le BTP, l’énergie ou le recyclage. Son modèle allie insertion 
            sociale, performance économique (90M€ de CA en 2023) et transition écologique. Forte d’un ancrage 
            territorial solide et d’une gouvernance exemplaire, La Varappe prouve que réinsertion et durabilité peuvent aller de pair. 
            Un investissement qui conjugue impact social, écologique et solidité économique."""
        },
        "Oreadis Productions": {
            "ticker": "?",
            "description": """OREADIS produit des films à fort impact social, diffusés à la fois dans 
            les circuits traditionnels et dans des lieux à fort ancrage éducatif et culturel. 
            L’entreprise met l’image au service de la mémoire, de l’inclusion et de la justice sociale. Elle répond à une demande croissante de récits porteurs de sens. Soutenir OREADIS, 
            c’est croire au pouvoir du cinéma pour éveiller les consciences et favoriser le lien social."""
        },
        "Axsol": {
            "ticker": "?",
            "description": """AXSOL conçoit et distribue des solutions pour rendre l’espace public accessible 
            aux personnes à mobilité réduite : rampes, mises à l’eau, équipements de sécurité… En 2023, elle a réalisé 2M€ de CA. 
            Son approche, centrée sur les besoins réels, combine innovation, inclusion et utilité concrète. Investir dans AXSOL, 
            c’est soutenir une entreprise qui agit pour une société plus équitable, où chacun peut participer pleinement à la vie sociale et citoyenne."""
        },
        "France Active": {
            "ticker": "?",
            "description": """France Active est un acteur clé de la finance solidaire, ayant mobilisé 491M€ en 2023 pour soutenir 
            37 000 entreprises à impact. À travers ses financements et son accompagnement, elle soutient l’entrepreneuriat engagé 
            et la transition sociale, écologique et territoriale. Investir dans France Active, 
            c’est choisir un modèle économique alternatif et résilient, aligné avec les ODD et porté par des entrepreneurs du changement."""
        },
    }

    # Sélection de l'actif projet
    choix = st.radio("Sélectionnez un projet", list(entreprises_projet.keys()))
    symbole = entreprises_projet[choix]["ticker"]
    description = entreprises_projet[choix]["description"]

    # Données financières
    st.markdown("""Société non cotée, pas de données financières disponibles""")

    if choix == "I Was A Sari":
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">Marque de mode circulaire basée à Mumbai : transformation de saris usagés en vêtements et accessoires contemporains. Présence sur les marchés internationaux.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">Savoir-faire artisanal dans la couture et la confection textile, valorisation de techniques traditionnelles. Design éco-responsable et durable.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">742% d’augmentation des ventes depuis 2018. Forte croissance sur le marché de la mode éthique. Potentiel élevé dans un secteur en mutation.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">Réduction des déchets textiles par l’upcycling de saris. Modèle fondé sur l’économie circulaire et la limitation de l’impact environnemental de la mode.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">247 femmes formées et employées en 2022, issues de quartiers défavorisés. +417% d’augmentation du nombre d’heures de travail justement rémunérées depuis 2018. Autonomisation et montée en compétences dans un contexte d’inégalités de genre.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Soutenu par Gucci Equilibrium, programme de mode durable et inclusive du groupe Kering.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">Croissance continue, notamment via l’export et la diversification des produits. Stratégie orientée vers l’élargissement de l’impact social et culturel.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Section Labels
        st.subheader("Évaluation ESG de I Was a Sari")

        labels = {
            "Circular Design Challenge Award": "I Was a Sari a remporté le Circular Design Challenge Award en 2019, la toute première récompense en Inde pour la mode durable.",
            "Responsible Disruptive Award": "En 2019, la marque a également reçu le Responsible Disruptive Award lors des Green Carpet Fashion Awards à Milan, qui célèbrent la mode éthique et responsable.",
            "ODD 1 – Pas de pauvreté": "I Was a Sari lutte contre la pauvreté en offrant un emploi stable et rémunéré de manière équitable à des femmes issues de milieux défavorisés.",
            "ODD 5 – Égalité entre les sexes": "La marque met les femmes au cœur de son modèle : les artisanes sont indépendantes, formées et travaillent dans un environnement flexible et digne.",
            "ODD 8 – Travail décent et croissance économique": "Elle favorise une croissance inclusive grâce à un modèle économique qui valorise les savoir-faire locaux tout en garantissant de bonnes conditions de travail.",
            "ODD 12 – Consommation et production responsables": "I Was a Sari transforme des saris existants en nouvelles pièces de mode, avec une politique de zéro déchet et une approche circulaire.",
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
                st.success(f"*{label}* : {description}")

        # Créer trois colonnes pour la section ESG
        col1, col2, col3 = st.columns(3)

        # Contenu pour la colonne 1 - Environnement
        with col1:
            st.markdown("### Environnement")
            st.markdown("""
            - *Zéro déchet* : Tous les produits sont fabriqués à partir de matériaux déjà existants (anciens saris), dans une logique d’économie circulaire.
            - *Production durable* : Utilisation de ressources déjà disponibles, réduisant l'impact environnemental lié à la production textile.
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("### Social")
            st.markdown("""
            - *Femmes artisanes indépendantes* : Grâce à des salaires équitables et un environnement de travail souple, les femmes gagnent en autonomie.
            - *Formation et inclusion* : Les artisanes sont formées à de nouveaux métiers, favorisant leur inclusion professionnelle durable.
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("### Gouvernance")
            st.markdown("""
            - *Réinvestissement des bénéfices* : Tous les profits sont réinjectés dans l’initiative pour favoriser l’égalité et renforcer l’impact social.
            - *Changement des pratiques* : La marque remet en question les standards de l'industrie de la mode pour les rendre plus humains et responsables.
            """)

        # Affichage de la description ESG
        description1 = entreprises_projet[choix]["description"]
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix == "Simplon.co":
        st.markdown("""
            <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color:#f2f2f2;">
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Activité</b></td>
                <td style="padding: 10px;">Formation gratuite aux métiers du numérique pour des publics éloignés de l’emploi.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Technologie</b></td>
                <td style="padding: 10px;">Pédagogie active et personnalisée : bootcamps, développement web, cybersécurité, cloud, etc.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact économique</b></td>
                <td style="padding: 10px;">Insertion professionnelle renforcée : simplonien·ne·s trouvent un emploi ou poursuivent leur formation après leur passage.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Impact environnemental</b></td>
                <td style="padding: 10px;">Utilisation d’équipements numériques reconditionnés, sensibilisation à l’impact du numérique.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact social</b></td>
                <td style="padding: 10px;">Inclusion de publics vulnérables (femmes, réfugiés, personnes en situation de handicap).</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Financement</b></td>
                <td style="padding: 10px;">Subventions publiques, mécénat privé et partenariats avec des entreprises tech.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Développement</b></td>
                <td style="padding: 10px;">Déploiement dans plusieurs pays, forte croissance des promotions de formation.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Données financières (2020-2023)</b></td>
                <td style="padding: 10px;">
                    Forte croissance du chiffre d'affaires (de 10,6M€ en 2020 à 28,9M€ en 2023) et amélioration significative de l’EBITDA (-3,2M€ à +1,58M€), témoignant d’un redressement financier.
                </td>
            </tr>
            </table>
            """, unsafe_allow_html=True)

        # Section ESG Simplon.co
        st.subheader("Évaluation ESG de Simplon.co")

        # Labels avec uniquement les infos fournies
        labels = {
            "Nombre de personnes formées": "Simplon.co a formé plus de 8 600 personnes, dont 37 % de femmes et 47 % de publics peu ou pas diplômés.",
            "Taux de sortie positif": "Grâce à des partenariats solides avec les éditeurs, entreprises et employeurs, 70 % des apprenant-es connaissent une sortie positive après leur formation.",
            "Réseau international": "Avec 99 Fabriques (écoles et CFA) en France et à l’étranger, Simplon.co est le plus grand et le plus inclusif des réseaux de la Grande École du Numérique, et le plus déployé à l'international.",
            "Satisfaction et certification": "93 % des apprenant-es sont satisfait-es de leur formation. Simplon.co est certifié Qualiopi pour les actions de formation, VAE et apprentissage.",
            "Diversité dans les formations Apple": "Parmi les formations Apple, 36 % des participant-es sont des femmes, soit 1 257 femmes formées.",
            "Niveau de diplôme": "54 % des personnes formées ont un niveau Bac ou infra Bac, témoignant de l’inclusivité des programmes."
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
                st.success(f"*{label}* : {description}")

        # Création des colonnes ESG
        col1, col2, col3 = st.columns(3)

        # Environnement 
        with col1:
            st.markdown("### Environnement")
            st.markdown(""" *Réutilisation des équipements : 100 % des équipements numériques sont reconditionnés et réutilisés.""")

        # Social
        with col2:
            st.markdown("### Social")
            st.markdown("""
            - *Formation inclusive* : 47 % des personnes formées sont peu ou pas diplômées, et 37 % sont des femmes.
            - *Accès pour tous* : Simplon.co vise l’égalité des chances grâce à des formations gratuites et accessibles.
            - *Accompagnement humain* : Un taux de satisfaction de 93 % témoigne de la qualité de l’accompagnement pédagogique.
            """)

        # Gouvernance
        with col3:
            st.markdown("### Gouvernance")
            st.markdown("""
            - *Réseau structuré et certifié* : Avec la certification Qualiopi et 99 Fabriques, Simplon.co offre une gouvernance rigoureuse et reconnue.
            - *Partenariats solides* : Les collaborations avec les entreprises renforcent l’impact et assurent des débouchés concrets.
            """)

        # Colonne vide pour équilibrer visuellement si besoin
        with col1:
            st.markdown("")

        # Affichage de la description ESG
        description1 = entreprises_projet[choix]["description"]
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)


    # -------------------------------
    elif choix == "La Varappe":
        st.markdown("""
            <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color:#f2f2f2;">
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Activité</b></td>
                <td style="padding: 10px;">Entreprise d’insertion alliant emploi, dignité et transition écologique.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Technologie</b></td>
                <td style="padding: 10px;">Méthodes d’accompagnement social couplées à des activités écologiques (BTP, recyclage).</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact économique</b></td>
                <td style="padding: 10px;">Insertion professionnelle durable pour des personnes très éloignées de l’emploi.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Impact environnemental</b></td>
                <td style="padding: 10px;">Activités basées sur le recyclage, l’économie circulaire, la rénovation énergétique.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact social</b></td>
                <td style="padding: 10px;">Accompagnement socio-professionnel et montée en compétences de profils fragiles.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Financement</b></td>
                <td style="padding: 10px;">Appels à projets publics, subventions et partenariats avec collectivités locales.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Développement</b></td>
                <td style="padding: 10px;">Présence en PACA et expansion vers d’autres régions françaises.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Performance et risque</b></td>
                <td style="padding: 10px;">
                    Croissance soutenue du chiffre d’affaires (de 66,5M€ en 2021 à 90M€ en 2023), mais baisse progressive du résultat net (1,36M€ à 0,3M€), signalant une pression sur la rentabilité.
                </td>
            </tr>
            </table>
            """, unsafe_allow_html=True)

        # Section ESG Simplon.co
        st.subheader("Évaluation ESG de La Varappe")

        labels_certifications = {
            "ISO 9001": "Norme de management de la qualité. Elle garantit que l’organisation met en œuvre des processus efficaces, avec une amélioration continue et une forte orientation client.",
            "ISO 14001": "Norme de management environnemental. Elle atteste que l’entreprise maîtrise et réduit ses impacts environnementaux de manière structurée et durable.",
            "Label RSEi – niveau 3 (confirmé)": "Label délivré par l’AFNOR CERTIFICATION. Il valorise l’engagement RSE des structures inclusives (IAE, EA, etc.). Le niveau 3 est le plus élevé, indiquant une maturité forte dans les pratiques sociales, environnementales et de gouvernance."
        }

        # Initialiser les états des boutons
        for label in labels_certifications:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons + contenu
        for label, description in labels_certifications.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]
            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")
        
        # Création des colonnes ESG
        col1, col2, col3 = st.columns(3)

        # Environnement
        with col1:
            st.markdown("### Environnement")
            st.markdown("""
            - **Déchets** : 524 586 tonnes évitées, réemployées ou recyclées en 2023.
            - **Eau** : 880 m³ économisés.
            - **Sol** : 4 837 m² de sol préservés.
            - **Décarbonation** : 2,9 T CO₂/ETP, soit 29 % de l’empreinte moyenne française.
            - **CO₂ évité** : 10 T via l’éco-construction.
            """)

        # Social
        with col2:
            st.markdown("### Social")
            st.markdown("""
            - **Insertion** : 9 958 personnes accompagnées, dont 27 % en situation de grande précarité.
            - **Sorties dynamiques** : 79 % en 2023.
            - **Heures rémunérées** : 3,6 millions en 2023 (1 781 ETP).
            - **Formation** : 91 099 heures en 2023.
            """)

        # Gouvernance
        with col3:
            st.markdown("### Gouvernance")
            st.markdown("""
            - **Conseils de surveillance** : 4 en 2023, avec 100 % de participation.
            - **Parité** : 42,86 % de femmes au conseil, 50 % dans le comité de direction.
            - **Actionnariat salarié** : 21 salariés actionnaires.
            """)

        # Affichage de la description ESG du projet
        description1 = entreprises_projet[choix]["description"]
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix == "Oreadis Productions":
        st.markdown("""
            <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color:#f2f2f2;">
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Activité</b></td>
                <td style="padding: 10px;">Production de films documentaires et de fiction à fort impact social.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Technologie</b></td>
                <td style="padding: 10px;">Outils de production audiovisuelle et de diffusion digitale pour atteindre un large public.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact économique</b></td>
                <td style="padding: 10px;">Création d’emplois dans le secteur culturel et renforcement des industries créatives locales.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Impact environnemental</b></td>
                <td style="padding: 10px;">Tournages écoresponsables, pratiques durables dans la production audiovisuelle.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact social</b></td>
                <td style="padding: 10px;">Promotion de la justice sociale, de la diversité et de l’éducation par l’image.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Financement</b></td>
                <td style="padding: 10px;">Aides du CNC, partenariats publics/privés, plateformes de streaming et fondations.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Développement</b></td>
                <td style="padding: 10px;">Projets de coproduction à l’international et festivals engagés.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Performance et risque</b></td>
                <td style="padding: 10px;">
                    <b>Rentabilité visée :</b> x2,02 en 5 ans (+102,26% bruts)<br>
                    Gain maximum : x3<br>
                    Gain minimum (si l’entreprise reste en activité) : x1,15<br><br>
                    <b>Risque :</b> Risque faible, évalué à 2,42/5 par les internautes lors de la phase d’évaluation.
                </td>
            </tr>
            </table>
            """, unsafe_allow_html=True)
        
        # Section ESG OREADIS Productions
        st.subheader("Engagement ESG d’OREADIS Productions")

        st.markdown("""
        OREADIS Productions s’illustre par son engagement dans la responsabilité sociale et environnementale à travers différentes initiatives et partenariats :
        - **Organisation d’événements engagés** : en tant que membre du bureau de l’association FCE 92, la fondatrice a co-organisé la soirée _« Devenir actrice du changement »_ en novembre, réunissant des femmes entrepreneures autour de l’impact sociétal.
        - **Partenaire du concours Made In 92** : implication en tant que jury, favorisant les échanges avec des entrepreneurs innovants.
        - **Participation aux Assises de l’Écoproduction** : engagement actif dans la 3e édition, renforçant l’expertise de la société en production audiovisuelle écoresponsable.
        """)

        # Création des colonnes ESG
        col1, col2, col3 = st.columns(3)

        # Environnement
        with col1:
            st.markdown("### Environnement")
            st.markdown("""
            - **Écoproduction** : participation active aux Assises de l’Écoproduction.
            - **Tournages responsables** : mise en œuvre de pratiques durables pendant les productions.
            - **Sensibilisation** : intégration de messages environnementaux dans les œuvres diffusées.
            """)

        # Social
        with col2:
            st.markdown("### Social")
            st.markdown("""
            - **Promotion de la diversité** : diffusion de récits inclusifs et porteurs de sens.
            - **Accès à la culture** : volonté de rendre les contenus accessibles à tous les publics.
            - **Soutien à l'entrepreneuriat féminin** : implication dans des réseaux comme FCE 92.
            """)

        # Gouvernance
        with col3:
            st.markdown("### Gouvernance")
            st.markdown("""
            - **Engagement associatif** : participation active à des réseaux professionnels engagés.
            - **Transparence** : volonté d'intégrer une gouvernance responsable dans le développement futur.
            - **Vision à long terme** : stratégie orientée vers l’impact culturel, social et écologique.
            """)

        # Affichage de la description ESG du projet
        description1 = entreprises_projet[choix]["description"]
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)


    # -------------------------------
    elif choix == "Axsol":
        st.markdown("""
            <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color:#f2f2f2;">
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Activité</b></td>
                <td style="padding: 10px;">Fabrication de solutions pour les personnes à mobilité réduite (PMR).</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Technologie</b></td>
                <td style="padding: 10px;">Développement d’équipements accessibles : rampes, plateformes, systèmes de mobilité.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact économique</b></td>
                <td style="padding: 10px;">Création d’emplois dans le secteur industriel et amélioration de l’accessibilité urbaine.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Impact environnemental</b></td>
                <td style="padding: 10px;">Matériaux durables, circuits courts de distribution et production locale.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact social</b></td>
                <td style="padding: 10px;">Amélioration concrète de l’inclusion des personnes handicapées dans la vie quotidienne.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Financement</b></td>
                <td style="padding: 10px;">Partenariats publics, appels d’offres, aides régionales à l’accessibilité.</td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Développement</b></td>
                <td style="padding: 10px;">Déploiement dans les collectivités locales, notamment zones rurales.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Performance et risque</b></td>
                <td style="padding: 10px;">
                    <b>Données financières</b><br>
                    Rentabilité visée : x1,40 en 3 ans (+40,00 % bruts)<br>
                    Risque de perte intégrale de l'investissement, gain maximum : x1,40<br>
                    Gain minimum tant que l'entreprise est en activité : x1,15<br><br>
                    <b>Risque</b><br>
                    Risque modéré évalué à 2.72/5 par les internautes lors de la phase d'évaluation<br><br>
                    <b>Royalties versées par trimestre</b><br>
                    2,05 % maximum du chiffre d'affaires versé à l'ensemble des investisseurs<br>
                    Pour 173 097,00 € levés, proportionnel au montant levé
                </td>
            </tr>
            </table>
            """, unsafe_allow_html=True)

        # Section ESG Axsol
        st.subheader("Engagement ESG d’Axsol")

        # Présentation des engagements ESG
        st.markdown("## Actions concrètes en faveur du développement durable")
        st.markdown("""
        Axsol intègre les principes de durabilité au cœur de son activité en concevant des rampes d’accessibilité innovantes, respectueuses de l’environnement et inclusives :
        - **Conception écoresponsable** : intégration de matériaux recyclés et biosourcés.
        - **Distribution durable** : optimisation logistique avec des emballages réutilisables.
        - **Vision d’impact** : plus de 22 000 clients touchés depuis la création, avec un objectif ambitieux de 80 à 100 000 sites équipés d’ici 2029.
        """)

        # Création des colonnes ESG
        col1, col2, col3 = st.columns(3)

        # Environnement
        with col1:
            st.markdown("### Environnement")
            st.markdown("""
            - **Matériaux** : usage de composants recyclés et biosourcés.
            - **Emballages** : recours à des systèmes de distribution avec emballages remployés.
            - **Durabilité** : rampes conçues pour résister aux intempéries sans corrosion.
            """)

        # Social
        with col2:
            st.markdown("### Social")
            st.markdown("""
            - **Accessibilité** : 22 000 clients déjà équipés en solutions d’accessibilité.
            - **Objectifs 2029** : entre 80 000 et 100 000 sites équipés en France.
            - **Inclusion** : amélioration concrète de l’accès aux bâtiments pour tous.
            """)

        # Gouvernance / Économie
        with col3:
            st.markdown("### Économie & Territoires")
            st.markdown("""
            - **Fabrication locale** : rampes produites en fibre de verre avec des composants sourcés localement.
            - **Emplois** : création de postes à St Quentin en Yvelines.
            - **Croissance responsable** : développement d’une chaîne de valeur ancrée localement.
            """)

        # Affichage de la description ESG du projet
        description1 = entreprises_projet[choix]["description"]
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix == "France Active":
        st.markdown("""
            <table style="width:100%; border-collapse: collapse; font-family: Arial, sans-serif;">
            <tr style="background-color:#f2f2f2; color:white;">
                <th style="padding: 12px; text-align:left; border-bottom: 2px solid #ddd;">Catégorie</th>
                <th style="padding: 12px; text-align:left; border-bottom: 2px solid #ddd;">Détails</th>
            </tr>

            <tr>
                <td style="padding: 10px; font-weight:bold;">Activité</td>
                <td style="padding: 10px;">Finance solidaire et accompagnement de l'économie sociale et solidaire (ESS) en France depuis 35 ans.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px; font-weight:bold;">Mission</td>
                <td style="padding: 10px;">Mobiliser des financements pour soutenir des entreprises à impact social, territorial et environnemental.</td>
            </tr>

            <tr>
                <td style="padding: 10px; font-weight:bold;">Impact économique</td>
                <td style="padding: 10px;">491 millions d'euros mobilisés en 2023 pour soutenir près de 37 000 entreprises.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px; font-weight:bold;">Modèle</td>
                <td style="padding: 10px;">Combinaison unique de financement, conseil et mise en réseau pour les entrepreneurs engagés.</td>
            </tr>

            <tr>
                <td style="padding: 10px; font-weight:bold;">Valeur ajoutée</td>
                <td style="padding: 10px;">Structuration de projets entrepreneuriaux transformateurs répondant aux ODD (Objectifs de Développement Durable).</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px; font-weight:bold;">Domaines d'intervention</td>
                <td style="padding: 10px;">
                    • Réduction des inégalités<br>
                    • Transition écologique<br>
                    • Revitalisation des territoires<br>
                    • Inclusion économique
                </td>
            </tr>

            <tr>
                <td style="padding: 10px; font-weight:bold;">Approche</td>
                <td style="padding: 10px;">Développement d'un modèle économique alternatif, inclusif et résilient.</td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px; font-weight:bold;">Performance et impact</td>
                <td style="padding: 10px;">
                    <b>Chiffres clés 2023</b><br>
                    • 36 440 entreprises accompagnées<br>
                    • +12% de croissance des emplois créés/consolidés vs 2022<br>
                    • 70% des créateurs accompagnés sont des femmes<br>
                    • 31% d'implantation en territoires fragiles<br>
                    • 10% de projets portés par des demandeurs d'emploi de longue durée<br><br>
                </td>
            </tr>
            </table>
            """, unsafe_allow_html=True)

        # Section ESG France Active
        st.subheader("Engagement ESG de France Active")

        # Présentation des engagements ESG
        st.markdown("### Actions concrètes en faveur du développement durable")
        st.markdown("""
        France Active soutient des projets à fort impact social, environnemental et économique :
        - **Accompagnement ciblé** : appui à des entrepreneurs engagés issus de territoires fragiles.
        - **Finance solidaire** : financement à impact social positif.
        - **Vision d’impact** : soutien à l’inclusion, à l’égalité des chances et à la transition écologique.
        """)

        # Création des colonnes ESG
        col1, col2, col3 = st.columns(3)

        # Environnement
        with col1:
            st.markdown("### Environnement")
            st.markdown("""
            - **Production locale** : valorisation de circuits courts.
            - **Transition écologique** : financement de projets à impact environnemental positif.
            - **Éco-innovation** : soutien à des entreprises durables et innovantes.
            """)

        # Social
        with col2:
            st.markdown("### Social")
            st.markdown("""
            - **Inclusion** : 70 % des porteurs de projets sont des femmes.
            - **Solidarité** : +10 % des projets issus de demandeurs d’emploi longue durée.
            - **Territoires fragiles** : 31 % des projets sont ancrés localement.
            """)

        # Gouvernance
        with col3:
            st.markdown("### Gouvernance")
            st.markdown("""
            - **Impact mesurable** : indicateurs de suivi clairs (emploi, diversité, inclusion).
            - **Accompagnement sur-mesure** : suivi des projets dans la durée.
            - **Transparence** : financements traçables et rapports d'impact.
            """)

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(entreprises_projet[choix]["description"])


# -------------------------------
#   ‼️ FONDS À IMPACT ‼️
# -------------------------------
elif choix=="Fonds à Impact":
    
    st.markdown("""
    ### Critères de sélection des Fonds à Impact

    Nous sélectionnons des fonds d'investissement offrant une combinaison de performance financière et d'impact social mesurable.

    **Méthodologie de sélection :**
    - **Critères d'inclusion** : Stratégie d'investissement clairement orientée impact ; Mesure et reporting transparents des indicateurs sociaux ; Approche best-in-class ESG ; Gestion active engagée
    - **Critères d'exclusion** : Greenwashing ou impact washing ; Frais de gestion excessifs ; Manque de transparence sur les holdings
    """)

    fonds = {
        "Candriam Sustainable Bond Euro Corporate": {
            "ISIN": "LU1313770536",
            "description": """Obligations d'entreprises européennes responsables intégrant des critères ESG stricts."""
        }
    }

    # Sélection de l'obligation durable
    choix = st.radio("Sélectionnez un", list(fonds.keys()))
    symbole = fonds[choix]["ISIN"]
    description = fonds[choix]["description"]

    if choix == "Candriam Sustainable Bond Euro Corporate":
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>
        <tr>
            <td style="padding: 10px;"><b>Stratégie d’investissement</b></td>
            <td style="padding: 10px;">Investit dans des obligations d’entreprises européennes respectant des critères ESG stricts, favorisant un impact positif social et environnemental.</td>
        </tr>
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
                - Sélection d’entreprises avec des pratiques ESG solides<br>
                - Contribue à la durabilité environnementale et sociale
            </td>
        </tr>
        <tr>
            <td style="padding: 10px;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
                - Performance en mars 2025 : <b>+7.7%</b><br>
                - Risque modéré<br>
                - Niveau de risque : <b>2 sur 7</b>
            </td>
        </tr>
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
                <b>Secteurs</b> : Finance, énergies renouvelables, technologies<br>
                <b>Pays</b> : Principalement zone Euro
            </td>
        </tr>
        <tr>
            <td style="padding: 10px;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
                - Sélection des émetteurs avec une forte politique ESG<br>
                - Promotion d’un avenir durable et inclusif
            </td>
        </tr>
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">Géré par <b>Candriam</b>, leader en investissement durable.</td>
        </tr>
        <tr>
            <td style="padding: 10px;"><b>Frais et commissions</b></td>
            <td style="padding: 10px;">
                - <b>Frais de gestion</b> : 0,75%<br>
                - <b>Frais courants</b> : 1,06%<br>
                - <b>Commission de souscription</b> : jusqu’à 3,5%<br>
                - <b>Valorisation</b> : quotidienne
            </td>
        </tr>
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Certifications et notations</b></td>
            <td style="padding: 10px;">
                - Classification SFDR : <b>Article 9</b><br>
                - Labellisé <b>ISR</b><br>
                - Notation Morningstar : <b>★★★★★</b>
            </td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS D'INVESTISSEMENT RESPONSABLE
        # -------------------------------
        st.markdown("### Labels d'investissement responsable")

        labels = {
            "Label ISR": """Créé en 2016 par le ministère de l’Économie et des Finances français, 
            ce label distingue les fonds appliquant une méthodologie robuste d’investissement socialement responsable, 
            aboutissant à des résultats mesurables et concrets.""",

            "Towards Sustainability": """Cette initiative aide les investisseurs à identifier des produits durables, 
            inspire confiance via une supervision indépendante, et veille à ce que les produits financiers respectent 
            des pratiques durables tout en garantissant une transparence totale.""",

            "LuxFLAG": """Label décerné par la Luxembourg Finance Labelling Agency, garantissant que les supports 
            d’investissement sont réellement gérés de manière responsable.""",

            "Article 9 SFDR": """Article 9 du règlement européen sur la publication d’informations en matière de durabilité
            dans le secteur des services financiers, qui exige que les produits financiers soient conçus pour
            promouvoir des caractéristiques environnementales ou sociales, ou un objectif d’investissement durable."""
        }

        # Initialiser les états des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage interactif
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.markdown(f" **{label}** : {description}")
        
        # Affichage de la description ESG du fonds
        st.markdown("#### Pourquoi ce projet ?")
        st.info(fonds[choix]["description"])

# -------------------------------
#   ‼️ OBLIGATIONS CORPORATES ‼️
# -------------------------------
elif choix=="Obligations Corporate":

    st.markdown("""
    ### Critères de sélection des Obligations Durables

    Nous sélectionnons des obligations émises par des institutions engagées dans le financement d'impacts sociaux et environnementaux tangibles.

    **Méthodologie de sélection :**
    - **Critères d'inclusion** : Projets financés clairement identifiés ; Reporting d'impact rigoureux ; Notation ESG élevée ; Émetteurs publics ou parapublics engagés
    - **Critères d'exclusion** : Obligations non alignées avec les ODD ; Manque de traçabilité des fonds ; Pratiques controversées de l'émetteur
    """)

    oblig_durables = {
        "Agence Française de Développement": {
            "ISIN": "AFD.PA",
            "description": """Le Groupe AFD a démontré la robustesse de son modèle économique et a atteint des niveaux d’activité jamais atteints, grâce à ses deux filiales Proparco et Expertise France.
            AFD a également obtenu une double labellisation AFNOR pour la Certification Diversité et l’Égalité professionnelle, tout cela en fait une obligation fortement engagée dans le développement durable et la responsabilité sociale.""",
        }
    }

    # Sélection de l'obligation durable
    choix = st.radio("Sélectionnez un", list(oblig_durables.keys()))
    symbole = oblig_durables[choix]["ISIN"]
    description = oblig_durables[choix]["description"]

    if choix == "Agence Française de Développement":
        # Valeur fixe du cours
        cours_fixe = 99.47  # ou la valeur que tu veux afficher

        # Affichage du cours sans graphique
        st.subheader(f"Cours du fonds {choix}")
        st.write(f"Le cours de l'obligation reste stable depuis l’émission : **{cours_fixe} €**")

        # Section sur la stratégie et les engagements en matière de développement durable
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>
        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Stratégie d’investissement</b></td>
            <td style="padding: 10px;">
            Investit dans des projets financés par l’AFD, visant à soutenir des initiatives durables pour un développement global.
            </td>
        </tr>
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Financement de projets à fort impact social et environnemental<br>
            - Aligné avec les Objectifs de Développement Durable (ODD)
            </td>
        </tr>
        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Portefeuille diversifié sur des projets internationaux<br>
            - Risque modéré grâce à la solidité de l'AFD<br>
            - Indice de risque : <b>2 sur 5</b>
            </td>
        </tr>
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Climat, éducation, gouvernance<br>
            <b>Pays</b> : Principalement les pays en développement
            </td>
        </tr>
        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Contribution à la lutte contre le changement climatique<br>
            - Soutien à l’inclusion sociale et au développement économique équitable
            </td>
        </tr>
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par <b>l’Agence Française de Développement</b>, acteur clé de la coopération internationale.
            </td>
        </tr>
        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Frais et commissions</b></td>
            <td style="padding: 10px;">
            - <b>Frais de gestion</b> : 0,30%<br>
            - <b>Commission de souscription</b> : Aucun frais<br>
            - <b>Valorisation quotidienne</b>
            </td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS ET CERTIFICATIONS
        # -------------------------------
        st.markdown("### Labels et Certifications")

        certifications = {
            "Double labellisation AFNOR": {
                "Certification Diversité": "Garantit que l'entreprise respecte des critères de diversité dans ses pratiques de recrutement et de gestion des talents.",
                "Certification Égalité professionnelle": "Délivrée aux entreprises qui respectent des critères stricts en matière d'égalité entre les femmes et les hommes au travail."
            }
        }

        # Initialiser les états des boutons
        for cert in certifications:
            if f"show_{cert}" not in st.session_state:
                st.session_state[f"show_{cert}"] = False

        # Affichage interactif
        for cert, details in certifications.items():
            if st.button(cert):
                st.session_state[f"show_{cert}"] = not st.session_state[f"show_{cert}"]

            if st.session_state[f"show_{cert}"]:
                st.markdown(f"**{cert}**")
                for sub_cert, description in details.items():
                    st.markdown(f"- **{sub_cert}** : {description}")

        # -------------------------------
        # ANALYSE FINANCIÈRE
        # -------------------------------
        st.markdown("### Analyse financière de l'AFD")

        st.write("**Rating S1P** : AA")
        st.write("**Engagements financiers** : Croissance de +10% par rapport à 2022, atteignant plus de 13 milliards d’euros.")
        st.write("**Bilan** : Le groupe AFD affiche un bilan en hausse à près de 70 milliards d’euros.")
        st.write("**Finance climat** : Première banque 100% alignée sur l’Accord de Paris, avec un niveau record de finance climat à 7,5 milliards € (85% de l'objectif de la France).")
        st.write("**Résultat net** : 371 millions d’euros avec un ratio de solvabilité stable à 14,95%.")

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(oblig_durables[choix]["description"])

# -------------------------------
#   ACTIONS DURABLES INCLUSION
# -------------------------------
elif choix == "Actions Durables Inclusion":

    st.markdown("""
    ### Critères de sélection des Actions Durables Inclusion
    Nous sélectionnons des actions d'entreprises qui démontrent un engagement fort en matière de diversité, d'inclusion et de responsabilité sociale.
    **Méthodologie de sélection :** 
    - **Critères d'inclusion** : Engagement mesurable en matière de diversité et d'inclusion ; Pratiques de gouvernance responsables ; Impact social positif démontré ; Bon score ESG
    - **Critères d'exclusion** : Pratiques controversées ; Manque de transparence sur les initiatives sociales ; Greenwashing
    """)

    # Liste des entreprises
    actions = {
    "Sodexo": {
        "ticker": "SW.PA",
        "description": """Présente dans 60+ pays, Sodexo agit pour un environnement inclusif, 
        valorisant diversité, équité salariale, et inclusion LGBTQ+. En 2023, elle obtient 91,9% au 
        Workplace Pride Benchmark. Parité forte : 35% de femmes au Comex, 60% au CA."""
    },
    "Capgemini": {
        "ticker": "CAP.PA",
        "description": """Capgemini promeut la diversité via formations numériques pour publics sous-représentés 
        et inclusion des personnes handicapées. Elle fixe des objectifs de mixité dans les fonctions 
        tech et managériales, intégrant inclusion dans sa stratégie RSE."""
    },
    "EssilorLuxottica": {
        "ticker": "EL.PA",
        "description": """Le groupe met l’humain au cœur de sa stratégie. Avec le programme Eyes 
        on Inclusion et la plateforme Leonardo (5,5M heures de formation), il renforce l’employabilité. 
        La fondation OneSight vise à éliminer les troubles visuels évitables d’ici 2050."""
    },
    "Acer": {
        "ticker": "2353.TW",
        "description": """Acer lutte contre la fracture numérique avec des produits accessibles et
        des formations. Elle allie inclusion sociale, neutralité carbone, gouvernance éthique et 
        économie circulaire dans l’électronique."""
    },
    "Yamaha": {
        "ticker": "7951.T",
        "description": """Yamaha agit localement pour la culture, l’environnement et la cohésion 
        sociale. Exemples : tournoi de golf féminin écoresponsable, recyclage de bois pour les 
        écoles, et projets musicaux communautaires via Oto-Machi."""
    },
    "APM Group": {
        "ticker": "?",
        "description": """ Spécialisée dans l’inclusion sociale, APM accompagne les personnes 
        vulnérables vers l’emploi et le bien-être. Présente dans 10+ pays, son modèle économique 
        repose sur l’impact social mesuré, alliant rentabilité et utilité publique."""
    }
}

    # Sélection de l'action
    choix = st.radio("Sélectionnez un actif", list(actions.keys()))
    symbol = actions[choix]["ticker"]
    description = actions[choix]["description"]

    # -------------------------------
    if choix == "Sodexo":
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbol]].dropna().reset_index()
        df_plot.columns = ["Date", symbol]

        # Affichage du cours du fonds
        st.subheader(f"Cours de l’action {choix}")
        fig = px.line(df_plot, x="Date", y=symbol, title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("### Caractéristiques générales de l'actif")

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Thématique ESG</b></td>
            <td style="padding: 10px;">Inclusion sociale, diversité en entreprise, égalité des chances, parité et lutte contre les discriminations.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Score Inclusion</b></td>
            <td style="padding: 10px;">91,90% selon le Workplace Pride Global Benchmark (2023).</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Parité & Gouvernance</b></td>
            <td style="padding: 10px;">
            - 35% de femmes au Comité Exécutif<br>
            - 60% au Conseil d’Administration<br>
            - Classement n°2 en 2019 pour la mixité parmi les sociétés cotées françaises.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Engagement sociétal</b></td>
            <td style="padding: 10px;">
            - Inclusion des personnes en situation de handicap<br>
            - Programmes d’égalité salariale<br>
            - Recrutement équitable
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Zone géographique</b></td>
            <td style="padding: 10px;">Présence dans plus de 60 pays avec une forte exposition en Europe et en Amérique du Nord</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Structure & gestion</b></td>
            <td style="padding: 10px;">Société française cotée, acteur historique des services externalisés et pionnière en ESG.</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS D'INVESTISSEMENT RESPONSABLE
        # -------------------------------
        st.markdown("### Labels d'investissement responsable pour Sodexo")

        labels = {
            "ISO 14001": "Certification du système de management environnemental, garantissant que l'entreprise gère efficacement ses impacts environnementaux.",
            "EcoVadis Gold": "Certification reconnaissant les performances de l'entreprise en matière de Responsabilité Sociétale des Entreprises (RSE), y compris l'environnement, le social et la gouvernance."
        }

        # Gestion des états des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage interactif
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.markdown(f" **{label}** : {description}")

        # -------------------------------
        # ANALYSE DES ENGAGEMENTS
        # -------------------------------
        st.markdown("### Engagements de Sodexo")

        st.write("""
        - **Amélioration de la qualité de vie** : Programme visant à offrir un meilleur bien-être aux employés et à promouvoir une diversité accrue dans l'entreprise.
        - **Réduction de l'empreinte environnementale** : Initiatives de durabilité, y compris des efforts pour minimiser les déchets et la consommation d'énergie dans les opérations mondiales.
        - **Promotion de la diversité et de l'inclusion** : Engagement envers l'inclusivité sur le lieu de travail, en créant un environnement où toutes les voix sont entendues et respectées.
        """)

        # -------------------------------
        # ANALYSE FINANCIERE ET PERFORMANCE DE SODEXO
        # -------------------------------
        st.markdown("### Analyse ESG de Sodexo")

        # Performance historique (données fictives pour l'exemple)
        st.markdown("### Performance historique de Sodexo")

        with st.expander("Voir les performances détaillées"):
            st.markdown("""
            - **2024** : +7,64% (vs indice -2,45%)  
            - **2023** : +12.00% (vs indice +18.00%)  
            - **2022** : -5.00%  
            - **3 ans** : +8.50% (vs +6,26%)  
            - **5 ans** : +8.06% annualisé   
            - **Depuis le lancement** : +974.18% 
            """)

        # Analyse comparative
        st.subheader("Comparaison des Notations ESG")
        esg_data = pd.DataFrame({
            "Entreprise": ["Sodexo", "Capgemini", "EssilorLuxottica", "Acer", "Yamaha"],
            "Score ESG": [59, 80, 64, 88, 59]
        })
        fig = px.bar(esg_data, x="Entreprise", y="Score ESG", color="Score ESG", title="Comparaison des Scores ESG")
        st.plotly_chart(fig)

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(actions[choix]["description"])

    # -------------------------------
    elif choix == "Capgemini":
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbol]].dropna().reset_index()
        df_plot.columns = ["Date", symbol]

        # Affichage du cours du fonds
        st.subheader(f"Cours de l’action {choix}")
        fig = px.line(df_plot, x="Date", y=symbol, title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("### Caractéristiques générales de l'actif")

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Thématique ESG</b></td>
            <td style="padding: 10px;">Inclusion numérique, diversité, accessibilité, équité professionnelle, et développement des compétences.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Initiatives Inclusion</b></td>
            <td style="padding: 10px;">
            - Formations numériques pour publics sous-représentés<br>
            - Campagnes pour l'inclusion des personnes en situation de handicap<br>
            - Réseaux internes pour soutenir les minorités (LGBTQ+, femmes dans la tech, etc.)
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Parité & Mixité</b></td>
            <td style="padding: 10px;">
            - Objectif d’atteindre 30% de femmes dans les postes de direction d’ici 2025<br>
            - Suivi régulier des indicateurs de mixité et inclusion<br>
            - Programmes de mentorat pour renforcer la diversité dans les fonctions tech
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Engagement sociétal</b></td>
            <td style="padding: 10px;">
            - Partenariats avec des ONG et institutions éducatives<br>
            - Soutien aux jeunes issus de milieux défavorisés<br>
            - Actions locales en faveur de l’éducation et de l’accès au numérique
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Zone géographique</b></td>
            <td style="padding: 10px;">Implantation mondiale avec forte présence en Europe, Amérique du Nord et Asie</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Structure & gestion</b></td>
            <td style="padding: 10px;">Groupe français coté, leader mondial des services informatiques et du conseil en technologie.</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS D'INVESTISSEMENT RESPONSABLE
        # -------------------------------
        st.markdown("### Labels d'investissement responsable pour Capgemini")

        labels = {
            "ISO 14001": "Certification du système de management environnemental, garantissant que l'entreprise gère efficacement ses impacts environnementaux."
        }

        # Gestion des états des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage interactif
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.markdown(f" **{label}** : {description}")

        # -------------------------------
        # ANALYSE DES ENGAGEMENTS
        # -------------------------------
        st.markdown("### Engagements de Capgemini")

        st.write("""
        - **Pratiques durables** : Capgemini s'engage à intégrer des pratiques durables dans ses opérations mondiales pour réduire son empreinte environnementale.
        - **Diversité et inclusion** : L'entreprise met en œuvre des politiques favorisant l'inclusion de tous, avec des programmes ciblant la diversité des genres et des origines.
        """)

        # -------------------------------
        # ANALYSE FINANCIERE ET PERFORMANCE DE CAPGEMINI
        # -------------------------------
        st.markdown("### Analyse ESG de Capgemini")

        # Performance historique (données fictives pour l'exemple)
        st.markdown("### Performance historique de Capgemini")

        with st.expander("Voir les performances détaillées"):
            st.markdown("""
            - **2024** : +2,65% (vs indice +14.50%)  
            - **2023** : +11.50% (vs indice +17.00%)  
            - **2022** : -6.00%  
            - **3 ans** : -34,40% (vs +6.00%)  
            - **5 ans** : +51,95% annualisé   
            - **Depuis le lancement** : +149.55%  
            """)

        # Analyse comparative
        st.subheader("Comparaison des Notations ESG")
        esg_data = pd.DataFrame({
            "Entreprise": ["Sodexo", "Capgemini", "EssilorLuxottica", "Acer", "Yamaha"],
            "Score ESG": [59, 80, 64, 88, 59]
        })
        fig = px.bar(esg_data, x="Entreprise", y="Score ESG", color="Score ESG", title="Comparaison des Scores ESG")
        st.plotly_chart(fig)

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(actions[choix]["description"])

    # -------------------------------
    elif choix == "EssilorLuxottica":
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbol]].dropna().reset_index()
        df_plot.columns = ["Date", symbol]

        # Affichage du cours du fonds
        st.subheader(f"Cours de l’action {choix}")
        fig = px.line(df_plot, x="Date", y=symbol, title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("### Caractéristiques générales de l'actif")

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Thématique ESG</b></td>
            <td style="padding: 10px;">Accès aux soins visuels, inclusion sociale, égalité des chances, développement durable.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Initiatives Inclusion</b></td>
            <td style="padding: 10px;">
            - Programmes de santé visuelle pour les populations défavorisées<br>
            - Actions locales en faveur des femmes dans les pays émergents<br>
            - Charte de diversité et inclusion
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Parité & Gouvernance</b></td>
            <td style="padding: 10px;">
            - Comité exécutif mixte<br>
            - Promotion interne équitable<br>
            - Engagement pour l’égalité salariale
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Engagement sociétal</b></td>
            <td style="padding: 10px;">
            - 500 millions de personnes aidées via Essilor Vision Foundation<br>
            - Partenariats avec des ONG de santé<br>
            - Investissements dans la recherche médicale
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Zone géographique</b></td>
            <td style="padding: 10px;">Implantation mondiale, fort ancrage en Europe, Amérique Latine et Asie</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Structure & gestion</b></td>
            <td style="padding: 10px;">Groupe franco-italien, leader mondial de l’optique ophtalmique et des montures.</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS D'INVESTISSEMENT RESPONSABLE
        # -------------------------------
        st.markdown("### Labels d'investissement responsable pour EssilorLuxottica")

        labels = {
            "ISO 14001": "Certification du système de management environnemental, garantissant que l'entreprise gère efficacement ses impacts environnementaux."
        }

        # Gestion des états des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage interactif
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.markdown(f" **{label}** : {description}")

        # -------------------------------
        # ANALYSE DES ENGAGEMENTS
        # -------------------------------
        st.markdown("### Engagements d'EssilorLuxottica")

        st.write("""
        - **Améliorer la santé visuelle** : EssilorLuxottica œuvre pour améliorer la qualité de vie des populations en rendant l'accès à la santé visuelle plus abordable et accessible.
        - **Inclusion sociale** : L'entreprise est activement impliquée dans des initiatives visant à offrir des soins oculaires aux populations défavorisées à travers le monde.
        """)

        # -------------------------------
        # ANALYSE FINANCIERE ET PERFORMANCE D'ESSILORLUXOTTICA
        # -------------------------------
        st.markdown("### Analyse ESG d'EssilorLuxottica")

        # Performance historique (données fictives pour l'exemple)
        st.markdown("### Performance historique d'EssilorLuxottica")

        with st.expander("Voir les performances détaillées"):
            st.markdown("""
            - **2024** : 1,62% (vs indice -2,15%)  
            - **2023** : +10.50% (vs indice +15.50%)  
            - **2022** : -7.00%  
            - **3 ans** : +51,99% (vs +8,68%)  
            - **5 ans** : +129,23% annualisé (vs +57,05%)  
            - **Depuis le lancement** : 1,435.33%   
            """)
        
        # Analyse comparative
        st.subheader("Comparaison des Notations ESG")
        esg_data = pd.DataFrame({
            "Entreprise": ["Sodexo", "Capgemini", "EssilorLuxottica", "Acer", "Yamaha"],
            "Score ESG": [59, 80, 64, 88, 59]
        })
        fig = px.bar(esg_data, x="Entreprise", y="Score ESG", color="Score ESG", title="Comparaison des Scores ESG")
        st.plotly_chart(fig)

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(actions[choix]["description"])

    # -------------------------------
    elif choix == "Acer":
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbol]].dropna().reset_index()
        df_plot.columns = ["Date", symbol]

        # Affichage du cours du fonds
        st.subheader(f"Cours de l’action {choix}")
        fig = px.line(df_plot, x="Date", y=symbol, title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("### Caractéristiques générales de l'actif")

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Thématique ESG</b></td>
            <td style="padding: 10px;">Accessibilité technologique, éducation numérique, durabilité environnementale.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Initiatives Inclusion</b></td>
            <td style="padding: 10px;">
            - Programmes d’éducation en ligne pour zones rurales<br>
            - Technologies accessibles aux personnes âgées ou handicapées<br>
            - Égalité dans le recrutement
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Parité & Engagement</b></td>
            <td style="padding: 10px;">
            - Promotion de la mixité dans les équipes R&D<br>
            - Campagnes de sensibilisation internes<br>
            - Chartes d’éthique professionnelle
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Engagement sociétal</b></td>
            <td style="padding: 10px;">
            - Ordinateurs durables & emballages recyclables<br>
            - Partenariats avec des écoles publiques<br>
            - Responsabilité numérique promue
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Zone géographique</b></td>
            <td style="padding: 10px;">Entreprise taïwanaise, forte présence en Asie, Europe, Amérique du Sud</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Structure & gestion</b></td>
            <td style="padding: 10px;">Fabricant mondial de matériel informatique engagé dans l'éducation et l'environnement.</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS D'INVESTISSEMENT RESPONSABLE
        # -------------------------------
        st.markdown("### Labels d'investissement responsable - Acer")

        labels_acer = {
            "ISO 14001": "Certification environnementale pour le management des impacts environnementaux.",
            "Neutralité Carbone": "Acer est engagée dans des initiatives visant la neutralité carbone et l'économie circulaire.",
            "Économie Circulaire": "Acer soutient des pratiques d'économie circulaire pour réduire son empreinte écologique."
        }

        # Gestion des états des boutons
        for label in labels_acer:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage interactif
        for label, description in labels_acer.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.markdown(f" **{label}** : {description}")

        # -------------------------------
        # ENGAGEMENTS SOCIETAUX
        # -------------------------------
        st.markdown("### Engagements de Acer")

        st.write("**Engagements clés :**")
        st.markdown("""
        - **Neutralité Carbone** : Acer met en œuvre des initiatives pour atteindre la neutralité carbone.
        - **Réduction de l'empreinte écologique** : L'entreprise soutient des pratiques visant à réduire son impact écologique.
        - **Économie Circulaire** : Promotion des pratiques d'économie circulaire à travers ses produits et services.
        """)

        # -------------------------------
        # ANALYSE ESG DE ACER
        # -------------------------------
        st.markdown("### Analyse ESG de Acer")

        st.write("**Score ESG** : données internes à venir")
        st.write("**Environnement** : Engagement pour la neutralité carbone et la réduction de l'empreinte écologique.")
        st.write("**Social** : Initiatives pour améliorer la durabilité et la responsabilité sociale des entreprises.")
        st.write("**Gouvernance** : Pratiques de gouvernance transparentes et responsables.")

        # -------------------------------
        # ANALYSE FINANCIERE ET PERFORMANCE D'ACER
        # -------------------------------
        st.markdown("### Analyse ESG d'ACER")


        # Performance historique (données fictives pour l'exemple)
        st.markdown("### Performance historique d'Acer")

        with st.expander("Voir les performances détaillées"):
            st.markdown("""
            - **2024** : 1,62% (vs indice -2,15%)  
            - **2023** : +10.50% (vs indice +15.50%)  
            - **2022** : -7.00%  
            - **3 ans** : +26,10 % (vs +14,55 %)  
            - **5 ans** : +165,37 % annualisé  (vs +92,26 %)
            - **Depuis le lancement** : -46,3%   
            """)
        
        # Analyse comparative
        st.subheader("Comparaison des Notations ESG")
        esg_data = pd.DataFrame({
            "Entreprise": ["Sodexo", "Capgemini", "EssilorLuxottica", "Acer", "Yamaha"],
            "Score ESG": [59, 80, 64, 88, 59]
        })
        fig = px.bar(esg_data, x="Entreprise", y="Score ESG", color="Score ESG", title="Comparaison des Scores ESG")
        st.plotly_chart(fig)

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(actions[choix]["description"])

    # -------------------------------
    elif choix == "Yamaha":
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbol]].dropna().reset_index()
        df_plot.columns = ["Date", symbol]

        # Affichage du cours du fonds
        st.subheader(f"Cours de l’action {choix}")
        fig = px.line(df_plot, x="Date", y=symbol, title=f"{choix} - Cours")
        st.plotly_chart(fig)

        st.markdown("### Caractéristiques générales de l'actif")

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Thématique ESG</b></td>
            <td style="padding: 10px;">Éducation musicale, inclusion culturelle, innovation écoresponsable.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Initiatives Inclusion</b></td>
            <td style="padding: 10px;">
            - Programmes de musique pour enfants défavorisés<br>
            - Accès facilité à la pratique musicale pour les personnes handicapées<br>
            - Collaboration avec des écoles dans les pays en développement
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Parité & Diversité</b></td>
            <td style="padding: 10px;">
            - Représentation féminine dans les métiers techniques<br>
            - Diversité des talents dans la production artistique<br>
            - Partenariats culturels mondiaux
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Engagement sociétal</b></td>
            <td style="padding: 10px;">
            - Instruments écoconçus<br>
            - Ateliers de musique pour la réinsertion<br>
            - Projets communautaires dans la culture musicale
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Zone géographique</b></td>
            <td style="padding: 10px;">Entreprise japonaise, forte présence en Asie, Europe et Amérique du Nord</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Structure & gestion</b></td>
            <td style="padding: 10px;">Groupe diversifié dans la musique, l’électronique et la mobilité, engagé dans la culture et la durabilité.</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS D'INVESTISSEMENT RESPONSABLE
        # -------------------------------
        st.markdown("### Labels d'investissement responsable - Yamaha")

        labels_yamaha = {
            "ISO 14001": "Certification environnementale pour le management des impacts environnementaux.",
            "Initiatives Culturelles et Sociales": "Yamaha soutient des initiatives culturelles et sociales dans le monde entier."
        }

        # Gestion des états des boutons
        for label in labels_yamaha:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage interactif
        for label, description in labels_yamaha.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.markdown(f" **{label}** : {description}")

        # -------------------------------
        # ENGAGEMENTS SOCIETAUX
        # -------------------------------
        st.markdown("### Engagements de Yamaha")

        st.write("**Engagements clés :**")
        st.markdown("""
        - **Initiatives Culturelles et Sociales** : Soutien aux initiatives culturelles et environnementales à travers le monde. 
        - **Communautés Locales** : Contribue au bien-être des communautés locales par diverses actions.
        """)

        # -------------------------------
        # ANALYSE ESG DE YAMAHA
        # -------------------------------
        st.markdown("### Analyse ESG de Yamaha")

        st.write("**Score ESG** : données internes à venir")
        st.write("**Environnement** : Certifiée ISO 14001 pour la gestion des impacts environnementaux.")
        st.write("**Social** : Initiatives pour le soutien culturel et social des communautés.")
        st.write("**Gouvernance** : Gouvernance responsable avec un engagement à long terme pour la durabilité.")

        # Performance historique (données fictives pour l'exemple)
        st.markdown("### Performance historique d'Yamaha")

        with st.expander("Voir les performances détaillées"):
            st.markdown("""
            - **2024** : 1,62% (vs indice -2,15%)  
            - **2023** : +10.50% (vs indice +15.50%)  
            - **2022** : -7.00%  
            - **3 ans** : -38.30% (vs +25.22 %)  
            - **5 ans** : -23.40% annualisé (vs +72.25 %)
            - **Depuis le lancement** : +325.56%   
            """)

        # Analyse comparative
        st.subheader("Comparaison des Notations ESG")
        esg_data = pd.DataFrame({
            "Entreprise": ["Sodexo", "Capgemini", "EssilorLuxottica", "Acer", "Yamaha"],
            "Score ESG": [59, 80, 64, 88, 59]
        })
        fig = px.bar(esg_data, x="Entreprise", y="Score ESG", color="Score ESG", title="Comparaison des Scores ESG")
        st.plotly_chart(fig)

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(actions[choix]["description"])

    # -------------------------------
    elif choix == "APM Group":

        # Chemin de l'image (local ou URL)
        image_path = "APM_12avr25.png"

        # Affichage de l'image
        st.image(image_path, caption="Cours de l'action APM Group le 12 avril 2025", use_container_width=True)


        st.markdown("### Caractéristiques générales de l'actif")

        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Thématique ESG</b></td>
            <td style="padding: 10px;">Emploi inclusif, réadaptation, santé mentale, soutien aux populations vulnérables.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Initiatives Inclusion</b></td>
            <td style="padding: 10px;">
            - Programmes pour l’intégration des personnes en situation de handicap<br>
            - Partenariats avec des ONG et gouvernements pour soutenir l’emploi et la réinsertion<br>
            - Support aux jeunes et aux personnes vulnérables
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Parité & Éthique</b></td>
            <td style="padding: 10px;">
            - Pratiques de gouvernance responsable<br>
            - Engagement pour la diversité et l'inclusion<br>
            - Indicateurs de performance sociale dans les contrats
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Engagement sociétal</b></td>
            <td style="padding: 10px;">
            - Collaboration avec des gouvernements et des entreprises pour des solutions d'inclusion<br>
            - Mesure de l'impact social à travers des indicateurs de bien-être et d'emploi durable<br>
            - Soutien aux politiques publiques et aux enjeux sociaux contemporains
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Zone géographique</b></td>
            <td style="padding: 10px;">Présence mondiale, avec des implantations majeures en Europe, Australie, Asie et Amérique du Nord</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Structure & gestion</b></td>
            <td style="padding: 10px;">Entreprise cotée en bourse australienne, basée sur un modèle économique d’impact social mesurable.</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # -------------------------------
        # LABELS D'INVESTISSEMENT RESPONSABLE
        # -------------------------------
        st.markdown("### Labels d'investissement responsable")

        labels = {
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "SDG": "Alignement avec les Objectifs de Développement Durable (ODD) des Nations Unies.",
            "Impact Investissement": "Focus sur l'impact social mesurable, avec des indicateurs tels que l’emploi durable et le bien-être des bénéficiaires."
        }

        # Gestion des états des boutons
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage interactif
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.markdown(f" **{label}** : {description}")

        # -------------------------------
        # ANALYSE ESG & PERFORMANCE HISTORIQUE
        # -------------------------------
        st.markdown("### Analyse ESG de APM Group")

        st.write("**Score ESG** : 12.3 (selon Morningstar)")
        st.write("**Environnement** : Faible exposition aux risques environnementaux, engagement envers les pratiques durables.")
        st.write("**Social** : Forte implication dans l’inclusion sociale, soutien aux personnes vulnérables et programmes de réadaptation.")
        st.write("**Gouvernance** : Transparence dans les pratiques de gouvernance, soutien à l’inclusion dans le management et à la diversité.")

        st.markdown("### Performance historique")

        with st.expander("Voir les performances détaillées"):
            st.markdown("""
            - **2025 YTD** : +17.96% 
            - **1 an** : -27.02% (vs sector -32.18%)  
            - **5 ans** : -56.61%
            """)

        # Analyse comparative
        st.subheader("Comparaison des Notations ESG")
        esg_data = pd.DataFrame({
            "Entreprise": ["Sodexo", "Capgemini", "EssilorLuxottica", "Acer", "Yamaha"],
            "Score ESG": [59, 80, 64, 88, 59]
        })
        fig = px.bar(esg_data, x="Entreprise", y="Score ESG", color="Score ESG", title="Comparaison des Scores ESG")
        st.plotly_chart(fig)

        # Affichage de la description ESG du projet
        st.markdown("#### Pourquoi ce projet ?")
        st.info(actions[choix]["description"])

# -------------------------------
# INFOS FOOTER
# -------------------------------
    st.sidebar.info("Ce dashboard présente le portefeuille d'un investisseur responsable. Il est conçu pour aider les investisseurs à prendre des décisions éclairées en matière d'investissement responsable et inclusif.")
    st.markdown("---")
    st.caption("© 2025 - Dashboard ESG_Reghina&Coline&Cosima | Streamlit prototype | Données publiques.")
