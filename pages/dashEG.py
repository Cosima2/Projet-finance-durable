
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import numpy as np
from datetime import datetime

# -------------------------------
# TITRE ET INTRODUCTION
# -------------------------------
st.set_page_config(page_title="Partie spécifique thématique Futur de l'Europe", layout="wide")

st.title("Portefeuille spécifique : thématique Futur de l'Europe")

st.markdown(
    "La protection de l'environnement et le soutien à l'économie européenne sont des enjeux cruciaux pour l'avenir."
    " Face aux défis globaux liés au changement climatique et à la transition énergétique, il est essentiel de soutenir "
    "des initiatives qui allient durabilité et innovation.\n\n"
    "Dans le cadre de notre portefeuille ESG, nous mettons en avant des entreprises et projets qui contribuent activement "
    "à la préservation de la planète tout en favorisant la croissance économique de l'Europe.\n\n"
    "Ainsi, nous avons sélectionné des investissements stratégiques, européens pour la plupart, en privilégiant des solutions écologiques concrètes "
    "et un fort potentiel de développement à long terme, contribuant à renforcer le tissu économique européen."
)

# -------------------------------
# VISUALISATION DE LA RÉPARTITION SPÉCIFIQUE
# -------------------------------
st.header("Composition de la partie spécifique liée à la thématique Futur de l'Europe")

# Données
composition_spe = {
    "Actif Projet": 3,
    "ETFs": 3,
    "Fonds": 4,
    "Actions Durables": 6
}
df_generale = pd.DataFrame(list(composition_spe.items()), columns=["Actif", "Poids (%)"])

# Camembert stylisé
fig_generale = px.pie(
    df_generale,
    values="Poids (%)",
    names="Actif",
    title="Répartition des actifs – Thématique Futur de l'Europe",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Reds
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
    "driver": ["XZRE.L", "EMEC.DE", "ECN.PA", "ENEL.MI", "VOLV-B.ST", "SAP", "OVH.PA", "IBE.MC", "CA.PA"]
}
st.subheader("Performance du portefeuille avec thématique Futur de l'Europe")
st.markdown("""
**Découvrez l'évolution de notre fonds ESG thématique Futur de l'Europe sur 5 ans**  
Stratégie d'investissement durable avec allocation pondérée :
- **55%** Actifs drivers (actions du portefeuille spécifique à la thématique Futur de l'Europe)
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
        Le portefeuille a affiché une performance cumulative solide depuis juillet 2020, avec une hausse continue jusqu'à août 2021, suivie d'une correction en 2022 et d'une reprise en 2023, culminant à 20.3% de performance au 26 août 2023. Sur une période de 5 ans, il a enregistré une performance globale de +31.0%, indiquant une croissance stable malgré les fluctuations de marché. La performance annuelle du portefeuille s'établit à +4.6%, suggérant un rendement modéré à court terme. Avec une volatilité annuelle de 7.7% et un ratio de Sharpe de 0.59, il montre un rendement raisonnable par rapport au risque encouru, ce qui témoigne d'une gestion équilibrée et d'un bon contrôle du risque dans le cadre de son développement à long terme.
    """)

st.markdown("---") 

# -------------------------------
# DÉTAIL DES ACTIFS SPÉCIFIQUES
# -------------------------------
st.header("Analyse détaillée de la partie spécifique (55%)")
st.warning(
    "Cette section présente la répartition détaillée des actifs composant la partie spécifique du portefeuille liée à la thématique Futur de l'Europe. "
)
categorie_actifs_spe = list(composition_spe.keys())
choix = st.radio("Sélectionnez une catégorie d'actifs", categorie_actifs_spe)


# -------------------------------
#   ACTIFS PROJET 
# -------------------------------
if choix == "Actif Projet":

    st.markdown("""
    ### Critères de sélection des Actifs Projet

    Dans le cadre de notre partie spécifique **Futur de l'Europe**, nous avons sélectionné des entreprises projets qui contribuent activement à la **transition énergétique**, à l'**économie circulaire** et au financement durable de l'économie à l'échelle européenne.

    **Méthodologie de sélection :**
    - **Critères d’inclusion :** Contribution à la **transition énergétique** et à la **réduction de l'empreinte carbone** ; soutien de **l'économie circulaire** ; focus sur des solutions favorisant l'innovation et la durabilité des modèles d'entreprises européennes
    - **Critères d’exclusion :** Manque de clarté sur les objectifs de durabilité ; absence de transparence dans les pratiques de gouvernance ; secteurs controversés
    """)


    entreprises_projet = {
        "Patagonia": {
            "ticker": "none",
            "description": """Patagonia est une entreprise de vêtements et d'équipements de plein air fondée en 1973, reconnue pour son engagement en faveur de l'environnement. Elle se distingue par l'utilisation de matériaux durables et recyclés, comme le polyester recyclé pour ses vestes et le coton organique pour ses vêtements, afin de réduire son empreinte écologique. En parallèle, son programme Worn Wear encourage la réparation et la réutilisation des produits, permettant ainsi d’allonger leur durée de vie et de diminuer la consommation de nouvelles ressources. Cette approche soutient un modèle de consommation circulaire qui s’intègre parfaitement dans une démarche durable, permettent à Patagonia de s’inscrire dans un portefeuille d'investissement éthique et responsable. """
        },
        "Néolithe" : {
            "ticker": "none",
            "description": """Néolithe est une start-up française fondée en 2019, qui révolutionne la gestion des déchets grâce à une innovation de taille : la Fossilisation Accélérée®, un procédé unique qui transforme les déchets non-recyclables en granulats minéraux pour la construction. Cette technique permet de substituer l'enfouissement et l'incinération, deux pratiques fortement polluantes, par une solution durable qui séquestre le carbone. En réutilisant ces granulats dans la fabrication de bétons à faible empreinte carbone, Néolithe contribue activement à la décarbonation du secteur du BTP. Cette approche novatrice ouvre la voie à une gestion des déchets plus écologique et s’inscrit dans un modèle circulaire porteur d’avenir."""
        },
        "Prometeia": {
            "ticker": "none",
            "description": """Prometeia est une entreprise italienne fondée en 1974, spécialisée dans les services de conseil financier, les solutions technologiques et la recherche économique. Elle accompagne les entreprises dans l'intégration des risques climatiques, en proposant des outils d'analyse avancés pour évaluer l'impact des risques physiques et de transition liés au changement climatique sur leurs activités. Par exemple, l'outil Nature-Retaled Risk (NRR) aide les clients à comprendre comment les bilans de leurs entreprises peuvent être affectés par leurs interactions et dépendances au capital naturel."""
        },
        }

    st.markdown("---") 

    # Sélection de l'actif projet
    choix = st.radio("Sélectionnez un projet", list(entreprises_projet.keys()))
    symbole = entreprises_projet[choix]["ticker"]
    description1 = entreprises_projet[choix]["description"]

    
    if choix == "Patagonia":
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
                    <li>Stratégie axée sur la durabilité avec des matériaux recyclés et biologiques</li>
                    <li>Engagement en faveur de l'économie circulaire et de la réparabilité des produits</li>
                    <li>Activités dans le secteur des vêtements, équipements de plein air et accessoires</li>
                </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Utilisation de matériaux recyclés dans la production de vêtements et accessoires</li>
                    <li>Soutien à l'économie circulaire avec des services de réparation et revente via Worn Wear</li>
                    <li>Technologies pour réduire l'empreinte carbone et améliorer la durabilité des produits</li>
                </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">En 2022, 96% de ses produits étaient fabriqués sans produits chimiques nocifs et 85% étaient certifiés commerce équitable.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">Patagonia s'engage à atteindre la neutralité carbone d'ici 2025 et met en place des pratiques responsables pour réduire son empreinte écologique.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">L'entreprise reverse 1% de son chiffre d'affaires annuel à des organisations environnementales et soutient des projets de préservation avec ses employés.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Sur son site, Patagonia met en avant et invite à rejoindre des <b>projets de terrain</b> visant à protéger l'environnement et offre la possibilité à ses clients de <b>faire des dons</b> pour soutenir des initiatives écologiques à travers sa fondation.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">
                <ul>
                    <li>Expansion géographique avec une présence croissante au niveau mondial, en particulier en Europe et en Asie</li>
                    <li>Transfert de la propriété de l'entreprise à un trust dédié à la conservation de la planète pour assurer la pérennité des valeurs environnementales</li>
                </ul>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        st.subheader("Evaluation ESG de Patagonia")

# Dictionnaire des labels avec descriptions
        labels = {
            "B-Corp": "Certification pour les entreprises conciliant but lucratif et impact sociétal et environnemental positif.",
            "Fair Trade Certified™": "Label indiquant des conditions de travail équitables, respect des droits des travailleurs, normes environnementales strictes.",
            "Global Organic Textile Standard (GOTS)": "Certification pour les textiles organiques, critères environnementaux et sociaux stricts dans la production.",
            "OEKO-TEX® Standard 100": "Label garantissant l'absence de substances chimiques nocives dans les produits textiles.",
            "Bluesign®": "Certification garantissant sécurité des consommateurs, impact environnemental réduit, chaîne de production responsable.",
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
            - Utilisation de matériaux recyclés (dans près de 70% de ses produits)
            - Réduction de son empreinte carbone par l'utilisation d'énergies renouvelables dans ses processus de production 
            - Promotion d'un modèle durable dans une industrie très polluante 
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Partenariat avec Fair Trade USA pour garantir des conditions de travail viables et un salaire juste pour ses travailleurs et partenaires
            - Membre de l'Ethical Trading Initiative, veillant au respect des droits des travailleurs de ses partenaires commerciaux 
            - Promotion de projets à impact social sur le site Internet
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Entièreté des actions transférées à une fiducie et organisation à but non lucratif en 2022 pour soutenir des causes environnementales
            - Publication transparente de rapports détaillés sur ses pratiques, notamment sur la chaîne d'approvisionnement 
            - Certifiée B-Corp, répondant ainsi à des critères de gouvernance stricts 
            """)


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)
        

    elif choix == "Néolithe":
    # Données financières
        st.markdown("""Société non cotée, pas de données financières disponibles""")
    
    # Section labels et stratégie
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
                        <li>Transformation des déchets non-recyclables en granulats minéraux pour le secteur du BTP via la technologie de Fossilisation Accélérée®.</li>
                        <li>Offre une alternative circulaire à l'enfouissement et à l'incinération.</li>
                    </ul>
                </td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Technologie</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Procédé breveté de Fossilisation Accélérée® permettant de séquestrer le CO₂ et de le transformer en granulats minéraux.</li>
                        <li>Technologie innovante contribuant à la réduction de l'empreinte carbone dans la gestion des déchets.</li>
                    </ul>
                </td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact économique</b></td>
                <td style="padding: 10px;">
                    Néolithe a levé plus de 80 millions d'euros pour financer l'industrialisation de sa technologie et prévoit l'ouverture de nouvelles usines en France, avec une capacité de traitement de 100 000 tonnes de déchets par an.
                </td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Impact environnemental</b></td>
                <td style="padding: 10px;">
                    Le procédé de Fossilisation Accélérée® est 311 fois plus efficace que le recyclage traditionnel en termes de réduction de CO₂, contribuant ainsi à la décarbonation du secteur du BTP.
                </td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact social</b></td>
                <td style="padding: 10px;">
                    Néolithe crée des emplois en insertion, avec un objectif de 550 emplois d'ici 2027, dont plus de 450 postes pour des travailleurs peu qualifiés, principalement en Europe.
                </td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Financement</b></td>
                <td style="padding: 10px;">
                    Néolithe a levé plus de 80 millions d'euros auprès de capital-risqueurs pour financer l'industrialisation de sa technologie et l'ouverture de nouvelles usines.
                </td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Développement</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Expansion géographique avec l'ouverture prévue de nouvelles usines en France, au Royaume-Uni et au Portugal.</li>
                        <li>Reconnaissance parmi les "100 start-up où investir" par le magazine Challenges, soulignant son potentiel d'innovation et d'impact environnemental.</li>
                        <li>Objectif d'obtenir la certification ISO 22000 pour garantir la sécurité des denrées alimentaires dans ses processus.</li>
                    </ul>
                </td>
            </tr>

            </table>
            """, unsafe_allow_html=True)

        # Séparateur visuel

        # Section Labels
        st.subheader("Évaluation ESG de Néolithe")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Agrément du Centre Scientifique et Technique du Bâtiment (CSTB)": "Certification assurant que les constructions respectent les normes actuelles ainsi que les exigences de sécurité et d'intégration urbaine.",
            "Partenariat Cerema": "Expert technique dans divers domaines de l'aménagement, des transports, des infrastructures, des risques, du bâtiment, de l'environnement.",
            "Label Pépite": "Prix attribué aux jeunes entreprises innovantes, récompensant les initiatives technologiques et environnementales.",
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
            - Procédé de Fossilisation Accélérée® : technologie innovante pour transformer les déchets non recyclables en granulats bas carbone utilisables pour le bâtiment
            - Valorisation des déchets du BTP
            - Réduction de l'empreinte carbone de nos déchets 
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Création d'emplois locaux favorisant l'insertion professionnelle et contribuant au développement économique des territoires (France)
            - Engagement en faveur de l'économie circulaire 
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Structure de gouvernance transparente 
            - Collaborations avec des institutions publiques 
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(
        "En contribuant à la décarbonation du secteur du BTP, Néolithe ouvre la voie à une économie circulaire et offre une solution concrète aux défis environnementaux. Son modèle prometteur, à la fois rentable et responsable, fait de Néolithe une entreprise à suivre de près et un investissement stratégique pour un avenir durable."        
        )


    elif choix == "Prometeia":
    # Données financières
        st.markdown("""Société non cotée, pas de données financières disponibles""")
    
    # Section tableau
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
                        <li>Fournisseur de services de conseil, de solutions logicielles et de recherche économique axés sur la gestion des risques, la gestion de patrimoine et des actifs.</li>
                        <li>Partenaire de plus de 400 clients dans plus de 20 pays, y compris des groupes bancaires de premier plan, des gestionnaires de patrimoine, des gestionnaires d'actifs et des assureurs.</li>
                    </ul>
                </td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Technologie</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Développement de solutions logicielles pour la gestion des risques, la conformité réglementaire et l'analyse financière.</li>
                        <li>Utilisation de l'intelligence artificielle et de l'apprentissage automatique pour améliorer les processus décisionnels dans le secteur financier.</li>
                    </ul>
                </td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact économique</b></td>
                <td style="padding: 10px;">
                    <ul>
                    <li>Fourniture de services qui aident les institutions financières à améliorer leur efficacité opérationnelle et à réduire les risques.</li>
                        <li>Contribution à la stabilité du secteur financier en fournissant des outils d'analyse avancés pour la gestion des risques.</li>
                    </ul>
                </td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Impact environnemental</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Offre des solutions pour aider les institutions financières à évaluer et à gérer les risques liés au changement climatique.</li>
                        <li>Collaboration avec des partenaires pour intégrer les facteurs environnementaux dans les processus décisionnels financiers.</li>
                    </ul>
                </td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Impact social</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Promotion de la culture ESG pour encourager des pratiques commerciales durables et la création de valeur à long terme.</li>
                        <li>Fourniture de programmes de formation pour améliorer les compétences en matière de durabilité au sein des institutions financières.</li>
                    </ul>
                </td>
            </tr>

            <tr style="background-color:#f9f9f9;">
                <td style="padding: 10px;"><b>Financement</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Partenariat avec LSEG pour intégrer des scores et des analyses ESG transparents dans ses plateformes de conseil en investissement.</li>
                        <li>Offre de solutions permettant aux clients de se conformer aux réglementations européennes sur la finance durable.</li>
                    </ul>
                </td>
            </tr>

            <tr>
                <td style="padding: 10px;"><b>Développement</b></td>
                <td style="padding: 10px;">
                    <ul>
                        <li>Expansion de ses services à plus de 20 pays, soutenant des clients dans le secteur financier mondial.</li>
                        <li>Reconnaissance dans le classement RiskTech100® 2023 par Chartis Research pour ses solutions innovantes en gestion des risques.</li>
                    </ul>
                </td>
            </tr>
            </table>
            """, unsafe_allow_html=True)

    # Séparateur visuel
        st.markdown("---")

    # Section Labels
        st.subheader("Évaluation ESG de Prometeia")



        # Dictionnaire des labels avec descriptions
        labels = {
            "LEED® Gold Certification": "Certification pour attester de la conformité à des standards élevés en matière de construction immobilière durable" ,
            "PRI": "Principes engageant à intégrer les facteurs dans les processus d'investissement",
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
            - Intégration des risques climatiques dans les services de conseil
            - Promotion de l'efficacité énergétique dans son siège social de Bologne 
            - Contribution à l'accompagnement des entreprises dans leurs défis climatiques 
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Formation éducative en continu du personnel sur les enjeux ESG
            - Collaboration étroite avec les clients et parties prenantes 
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Établissement d'une politique de durabilité et d'un comité dédié 
            - Transparence des communications en matière d'ESG 
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(
        "Soutenir Prometeia, c'est parier sur une entreprise qui combine expertise en conseil stratégique, recherche économique interne et capacité à aider les entreprises à naviguer dans les défis financiers et environnementaux, en offrant des solutions durables et adaptées aux enjeux de demain."
        )




# -------------------------------
#     ETFs
# -------------------------------      
elif choix == "ETFs":
    st.markdown("""
### Critères de sélection des ETFs

Les ETFs que nous sélectionnons sont centrés sur des investissements durables, favorisant à la fois la **protection de l'environnement** et le **dynamisme économique européen**. Ces fonds visent à soutenir la transition énergétique et l'économie circulaire, tout en promouvant des solutions concrètes pour un développement économique durable.

**Méthodologie d’analyse et de sélection :**
- **Critères d’inclusion :** Engagement ferme en faveur de la **transition énergétique** ; soutien à des entreprises et projets européens dynamiques, innovants et en croissance durable, contribuant à la **création d'emplois** et à des **infrastructures vertes**.
- **Critères d’exclusion :** Secteurs polluants, controversés, ou non conformes aux normes environnementales et aux critères de gouvernance durable.
""")
    
    etf_EG = {
        "BNP Paribas Easy Low Carbon 100 Europe PAB": {
            "ticker": "ECN.PA",
            "description": """Le fonds investit dans des actions européennes des entreprises ayant un faible niveau d’émissions de carbone. Il suit l'indice Low Carbon 100 Europe PAB (Paris-Aligned Benchmark), composé d'entreprises qui contribuent activement à la réduction des émissions de gaz à effet de serre. L'objectif est de surperformer le marché européen tout en minimisant l'empreinte carbone du portefeuille. Le fonds adopte une approche passive, suivant de manière transparente cet indice."""
        },
        "BNP Paribas Easy ECPI Circular Economy Leaders": {
            "ticker": "EMEC.DE",
            "description": """Le fonds investit dans des entreprises mondiales leaders dans le domaine de l'économie circulaire, une approche qui vise à réduire les déchets et à prolonger la durée de vie des produits. Il suit un indice spécifique qui sélectionne des sociétés innovantes impliquées dans des activités comme la recyclabilité, la réutilisation des ressources et la gestion durable des matériaux. La stratégie repose sur une gestion active et cherche à surperformer son indice de référence en identifiant des entreprises pionnières dans cette transition économique."""
        },
        "Xtrackers Developed Green Real Estate ESG" : {
            "ticker": "XZRE.L",
            "description": """Ce fonds investit dans des sociétés immobilières développées qui sont leaders dans la gestion verte et durable de leurs actifs. L’objectif est de répliquer la performance de l'indice Green Real Estate en sélectionnant des entreprises du secteur immobilier qui adoptent des pratiques durables, comme des bâtiments écologiques et des initiatives d'efficacité énergétique."""
        },
        }

    # Sélection du fonds à thématique EG
    choix = st.radio("Sélectionnez un", list(etf_EG.keys()))
    symbole = etf_EG[choix]["ticker"]
    description1 = etf_EG[choix]["description"]

    if choix == "BNP Paribas Easy Low Carbon 100 Europe PAB":
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)

        # Table BNP Paribas Easy Low Carbon 100 Europe PAB
        st.markdown("""
                <table style="width:100%; border-collapse: collapse;">
                <tr style="background-color:#f2f2f2;">
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Activité</b></td>
                    <td style="padding: 10px;">ETF qui suit l'indice Low Carbon 100 Europe PAB, composé des 100 entreprises européennes ayant un faible niveau d'émissions de carbone. </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Approche</b></td>
                    <td style="padding: 10px;">L'approche est axée sur la sélection d'entreprises réduisant leur empreinte carbone tout en respectant les critères de performance financière, dans le cadre d'une gestion passive suivant l'indice.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact économique</b></td>
                    <td style="padding: 10px;">Le fonds investit dans des entreprises leaders en termes d'innovation verte et de transition énergétique, contribuant à la croissance économique durable en Europe.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Impact environnemental</b></td>
                    <td style="padding: 10px;">Il vise à réduire l'empreinte carbone des entreprises du portefeuille en privilégiant celles qui ont des pratiques plus respectueuses de l'environnement.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact social</b></td>
                    <td style="padding: 10px;">Indirectement, il soutient les entreprises qui participent à la transition énergétique et à la réduction des inégalités environnementales à l’échelle européenne.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Financement</b></td>
                    <td style="padding: 10px;">L'ETF peut être échangé sur les marchés financiers, donc il dispose de liquidités importantes.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Développement</b></td>
                    <td style="padding: 10px;">ETF ouvert en 2016. </td>
                </tr>

                </table>
                """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels - Récompenses ESG (exemples à adapter ou compléter)
        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 8 (SFDR)": "Catégorie de la réglementation SFDR pour un fonds qui promeut des caractéristiques environnementales ou sociales.",
            "Label ISR" : "Label garantissant que le fonds intègre des critères environnementaux, sociaux et de gouvernance (ESG) dans sa stratégie d'investissement.",
            "Low Carbon 100 Europe® PAB Index" : "Indice conçu pour refléter les performances des entreprises européennes ayant réduit leur intensité carbone, en alignement avec les objectifs de l'Accord de Paris, tout en excluant les sociétés liées aux combustibles fossiles.",
            "Label Towards Sustainability":"Label délivré par le Forum Nachhaltige Geldanlagen (FNG), attestant de l'engagement du fonds envers des pratiques d'investissement durables et responsables",
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
            - Objectif de réduction de l'intensité carbone de l'indice de 50% par rapport à l'univers d'investissement initial
            - Alignement avec la taxonomie européenne  
            - Indice de référence visant une décarbonation de 7% par an 
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Investissement indirectement guidé par le respect des droits des travailleurs et des communautés 
            - Soutien indirect des secteurs de l'innovation dans la décarbonation 
            - Investissement créateur indirect d'emplois dans des industries durables  
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Responsabilisation des entreprises sur la gestion des risques et transparence des activités 
            - Accent porté à la protection des actionnaires minoritaires 
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi cet actif ?")
        st.info(description1)

    # -------------------------------
    elif choix == "BNP Paribas Easy ECPI Circular Economy Leaders":   
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)

        # Table BNP Paribas Easy ECPI Circular Economy Leaders
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">Le fonds investit dans des entreprises leaders de l'économie circulaire, en se concentrant sur des secteurs liés au recyclage, à la réutilisation des matériaux, et à la gestion durable des ressources naturelles.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Approche</b></td>
            <td style="padding: 10px;">Stratégie passive en répliquant l'indice ECPI Circular Economy Leaders Equity (NR), qui sélectionne des entreprises selon des critères ESG stricts et favorise la transition vers une économie durable, avec un écart de suivi maximal de 1%.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">Cible une croissance durable de long terme, avec des rendements prévus entre 1,60% et 14,84% par an selon les scénarios.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">Le fonds soutient des entreprises qui réduisent leur empreinte écologique en excluant celles ayant une exposition élevée aux combustibles fossiles et en contribuant activement à la réduction des émissions de gaz à effet de serre grâce à des solutions de recyclage et d’économie circulaire.
        </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;"> Le fonds privilégie les entreprises qui investissent dans le capital humain, favorisant des conditions de travail équitables, et qui contribuent à la réduction des déchets, améliorant ainsi les conditions sociales en lien avec des pratiques responsables et durables.

        </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Le fonds offre une liquidité quotidienne, selon l'état du marché.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">Fonds récent et basé sur un objectif de croissance stable et durable à long terme. </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)
        
        st.markdown("---")


        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 8 (SFDR)": "Catégorie de la réglementation SFDR pour un fonds qui promeut des caractéristiques environnementales ou sociales.",
            "ECPI Circular Economy Leaders Equity": "Indice suivant la performance des entreprises leaders dans l'économie circulaire.",
            "Label ISR" : "Label garantissant que le fonds intègre des critères environnementaux, sociaux et de gouvernance (ESG) dans sa stratégie d'investissement.",
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
            - Investissements dans des solutions de recyclage, de réutilisation des matériaux et de prolongation de la durée de vie des produits 
            - Réduction de l'exposition aux combustibles fossiles 
            - Exclusion d'entreprises à l'impact ESG négatif 
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Contribution à la création de meilleurs produits pour le consommateur final 
            - Financement d'entreprises promouvant des conditions de travail respectueuses 
            - Facilitation de l'accès à des produits et services durables pour les communautés 
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Exclusion d'entreprises aux controverses majeures (violation des principes du Pacte mondial des Nations unies)
            - Promotion de pratiques transparentes et éthiques 
            """)

        st.markdown("#### Pourquoi cet actif ?")
        st.info(description1)

# -------------------------------
    elif choix == "Xtrackers Developed Green Real Estate ESG":   
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)
        # Table Xtrackers Developed Green Real Estate ESG
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">Le fonds investit dans des sociétés immobilières des marchés développés, qui répondent à des critères environnementaux, sociaux et de gouvernance (ESG), en se basant sur l’indice Dow Jones Developed Green Real Estate.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Approche</b></td>
            <td style="padding: 10px;">Gestion passive : le fonds cherche à répliquer la performance de l'indice en investissant dans des titres immobiliers respectant des critères ESG stricts, avec un écart de suivi estimé à 1 % dans des conditions normales de marché.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;"> Le fonds permet aux investisseurs de participer à la croissance des entreprises du secteur immobilier tout en respectant des objectifs de durabilité.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;"> L'indice de référence vise une réduction minimale de l'intensité des gaz à effet de serre (GES) des sociétés qu'il inclut, en comparaison avec l'indice parent. Ce fonds contribue à réduire cette intensité, ce qui peut se traduire par des réductions de CO2 équivalent de l’ordre de 15-25% dans les sociétés de son portefeuille en fonction des secteurs.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;"> Le fonds exclut les sociétés impliquées dans des activités controversées comme la production de tabac, les armes controversées et l'extraction de combustibles fossiles, et favorise des entreprises respectant les droits de l'homme et les normes sociales.
        </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Le fonds est un ETF négociable quotidiennement, bénéficiant d'une bonne liquidité.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">Le fonds met l'accent sur la durabilité et l'investissement à long terme en immobiliers verts, avec des exclusions ESG rigoureuses et un objectif d’investir au moins 25 % de ses actifs dans des investissements durables alignés sur des objectifs environnementaux et sociaux.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 8 (SFDR)": "Catégorie de la réglementation SFDR pour un fonds qui promeut des caractéristiques environnementales ou sociales.",
            "UCITS": "Respect des normes européennes en matière de fonds d'investissement, garantissant une gestion transparente et réglementée.",
            "Dow Jones Developed Green Real Estate Index": "Indice suivant des sociétés immobilières développées qui se distinguent par leurs pratiques de développement durable et leurs engagements environnementaux (réduction de l'empreinte carbone et l'efficacité énergétique).", 
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
            - Réduction des émissions de gaz à effet de serre des sociétés du portefeuille
            - Amélioration des scores de durabilité des bâtiments (efficaicté énergétique, gestion de l'eau et des déchets)
            - Exclusion des secteurs à forte empreinte carbone
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Exclusion d'entreprises impliquées dans des secteurs controversés et ne respectant pas les droits humains
            - Participation à l'amélioration des conditions de vie des populations 
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Exclusion d'entreprises ne respectant pas les principes du Pacte mondial des Nations Unies ou impliquées dans des controverses de corruption ou liées à l'éthique 
            - Soutien à la transparence des informations en matière de durabilité 
            """)

        st.markdown("#### Pourquoi cet actif ?")
        st.info(description1)



# ------------------------------
#   FONDS 
# ------------------------------

elif choix == "Fonds":

    st.markdown("""
### Critères de sélection des Fonds d'investissement

Les fonds de notre portefeuille **Futur de l'Europe** sont gérés par des asset managers reconnus et intégrant une stratégie d'investissement durable. Ils visent à soutenir la **transition énergétique**, à promouvoir l'**économie circulaire** et à favoriser un développement économique européen responsable, avec un focus sur les entreprises contribuant à une croissance durable et à la protection de l'environnement.
Les critères de sélection sont similaires à ceux des ETFs. 

**Méthodologie d’analyse et de sélection :**
- **Critères d’inclusion :** Engagement ferme en faveur de la **transition énergétique** ; soutien à des entreprises et projets européens dynamiques, innovants et en croissance durable, contribuant à la **création d'emplois** et à des **infrastructures vertes**.
- **Critères d’exclusion :** Secteurs polluants, controversés, ou non conformes aux normes environnementales et aux critères de gouvernance durable.
""")


    fonds_EG = {
        "Swiss Life Funds (F) Green Bonds Impact": {
            "ticker": "0P00018AOI.F",
            "description": """Le fonds investit dans des obligations vertes émises par des entreprises et des gouvernements pour financer des projets ayant des bénéfices environnementaux concrets, tels que la transition énergétique, l'efficacité énergétique, et la réduction des émissions de gaz à effet de serre. Il adopte une approche active en sélectionnant des obligations vertes qui respectent des critères ESG stricts, et cherche à maximiser l'impact environnemental tout en générant un rendement attractif pour les investisseurs."""
        },
        "ODDO BHF Génération CR-EUR": {
            "ticker": "0P00000QLH.F",
            "description": """Le fonds vise à investir principalement en actions européennes de toutes capitalisations et tous secteurs, avec une approche de sélection de titres fondée sur des critères de gestion générationelle d'entreprises."""
        },
        "Echiquier Positive Impact Europe I" : {
            "ticker": "0P0001CDVT.F",
            "description": """Le fonds vise des entreprises européennes qui apportent des solutions aux enjeux du développement durable, tout en intégrant des critères environnementaux, sociaux et de gouvernance de manière stricte."""
        },
        "Schroder International Selection Fund Emerging Europe": {
            "ticker": "0P00000AQU.F",
            "description": """Le fonds est géré de façon active et investit au moins deux tiers de ses actifs dans des actions de sociétés d'Europe centrale et d'Europe de l'Est, dont les marchés de l'ex-Union soviétique et les marchés émergents méditerranéens."""
    
        }
        }


   # Sélection du fonds à thématique EG
    choix = st.radio("Sélectionnez un", list(fonds_EG.keys()))
    symbole = fonds_EG[choix]["ticker"]
    description1 = fonds_EG[choix]["description"]

    if choix == "Swiss Life Funds (F) Green Bonds Impact":
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)
 

        # Table Swiss Life Funds (F) Green Bonds Impact
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Activité</b></td>
            <td style="padding: 10px;">Le fonds investit principalement dans des obligations vertes (Green Bonds) émises par des entreprises et institutions engagées dans des projets visant à favoriser la transition énergétique et écologique. </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Approche</b></td>
            <td style="padding: 10px;">La stratégie d'investissement repose sur la sélection de titres obligataires respectant les Green Bond Principles de l'ICMA, avec un objectif d'investissement durable, en privilégiant des émetteurs quasi-publics et privés engagés dans des pratiques de gouvernance responsable.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;"> Le fonds contribue principalement au financement de projets liés à la transition énergétique et écologique. Depuis sa création, le fonds a généré une performance de 10,39%. </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">Le fonds soutient des projets visant à la réduction des émissions de gaz à effet de serre, au financement de la transition énergétique, et à la préservation des ressources naturelles, dans le respect des critères environnementaux stricts.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">Le fonds soutient des projets qui ne nuisent pas aux objectifs sociaux ou environnementaux et favorise des émetteurs ayant des pratiques de bonne gouvernance, tout en respectant les principes du Pacte Mondial de l'ONU.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Le fonds investit un minimum de 80 % de son actif net dans des obligations vertes, et peut allouer jusqu'à 20 % dans des obligations d'entreprises engagées sur une trajectoire vers la neutralité carbone.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">Le fonds est géré activement, avec une sélection rigoureuse des émetteurs, visant à atteindre les objectifs de durabilité tout en maximisant le rendement et en minimisant les risques liés aux critères ESG.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "Label ISR" : "Label garantissant le suivi d'une stratégie d'investissement durable en s'appuyant sur des critères ESG (Environnementaux, Sociaux, de Gouvernance).",
            "Green Bond Principles":"Garantie de traçabilité et de conformité des projets financés aux objectifs environnementaux.",
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
            - Investissements dans des obligations vertes finançant des projets de transition énergétique et écologique
            - Promotion d'entreprises aux pratiques écologiquement responsables 
            - Un minimum de 80% du fonds est alloué à des obligations contribuant directement à la réduction de gaz à effet de serre 
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Exclusions sectorielles et d'entreprises aux pratiques sociales douteuses 
            - Soutien de projets à l'impact social positif 
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Sélection d'entreprises aux pratiques de gouvernances positivement reconnues
            - Exclusion d'entreprises dont la gouvernance n'est pas communiquée de manière transparente 
            - Engagement actif auprès des entreprises pour promouvoir des pratiques durables
            """)

        st.markdown("#### Pourquoi cet actif ?")
        st.info(description1)



    elif choix == "ODDO BHF Génération CR-EUR":
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)
        

        # Table ODDO BHF Génération CR-EUR
        st.markdown("""
                <table style="width:100%; border-collapse: collapse;">
                <tr style="background-color:#f2f2f2;">
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Activité</b></td>
                    <td style="padding: 10px;">Ce fonds investit principalement dans des actions de grandes capitalisations européennes, en ciblant des entreprises dont l'actionnariat est stable et pérenne, souvent contrôlé par des familles​. </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Approche</b></td>
                    <td style="padding: 10px;">La stratégie du fonds repose sur le stock-picking, basé sur l'analyse fondamentale des entreprises pour identifier celles offrant une valorisation attractive et un potentiel de croissance à long terme.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact économique</b></td>
                    <td style="padding: 10px;">Le fonds investit dans des entreprises basées sur une gestion générationelle, contribuant à la croissance économique durable en Europe.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Impact environnemental</b></td>
                    <td style="padding: 10px;">Le fonds maintient une faible exposition aux secteurs fossiles (0%) et se concentre sur les entreprises ayant un impact positif en matière d'environnement, avec 29,5% de son portefeuille lié aux solutions carbone.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact social</b></td>
                    <td style="padding: 10px;">De façon directe, le fonds soutient les entreprises dont la gestion se veut péreine et stable, avec un fort accent sur le développement de long terme (sur plusieurs générations).</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Financement</b></td>
                    <td style="padding: 10px;">Au 28 février 2025, l'actif net du fonds s'élevait à 300 millions d'euros.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Développement</b></td>
                    <td style="padding: 10px;">Le fonds continue de viser un objectif de rentabilité durable, avec une intégration stricte des critères ESG et une note ESG moyenne de 4/5, ce qui reflète un engagement vers des entreprises de plus en plus responsables. </td>
                </tr>

                </table>
                """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels - Récompenses ESG (exemples à adapter ou compléter)
        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 8 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui  intègrent des critères environnementaux, sociaux et de gouvernance dans leurs décisions d'investissement",
            "Label ISR": "Label attribué aux fonds qui respectent des critères ESG rigoureux dans leur processus d'investissement, garantissant un impact positif sur la société et l'environnement",
            "Note ESG": "Note de 4 sur 5 sur l'échelle de notation interne de l'émetteur, avec 1 représentant un risque en terme de durabilité et 5 une opportunité concrète",
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
            - Exposition nulle aux secteurs des énergies fossiles
            - Environ un tiers du portefeuille investi en solutions en matière de transition énergétique 
            - Intensité carbone du fonds 4 fois inférieure à son indice de référence (MSCI EMU Net Return EUR Index)
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Soutien direct aux familles entrepreunariales en Europe 
            - Contribution au renforcement du tissu économique européen (toute taille d'entreprises)
            - Dialogue réguliers avec les entreprises aux faibles scores ESG avec désinvestissement prévu en cas d'inaction 
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Partie importante de l'évaluation ESG du fonds basée sur la gouvernance d'entreprise 
            - Financement d'entreprises à la gouvernance et éthique solides  
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi cet actif ?")
        st.info(description1)
  

    elif choix == "Echiquier Positive Impact Europe I":
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)
        

        # Table Echiquier Positive Impact Europe I
        st.markdown("""
                <table style="width:100%; border-collapse: collapse;">
                <tr style="background-color:#f2f2f2;">
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Activité</b></td>
                    <td style="padding: 10px;">Le fonds investit dans des actions d’entreprises européennes qui apportent des solutions aux enjeux du développement durable, tout en intégrant des critères ESG, et vise à surperformer son indice de référence, le MSCI EUROPE NR​. </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Approche</b></td>
                    <td style="padding: 10px;">La stratégie repose sur un processus de sélection rigoureuse (« stock-picking ») en deux étapes : d'abord, l'analyse de l'univers d'investissement en appliquant des critères ISR, puis une analyse fondamentale des entreprises, incluant leur contribution aux ODD de l'ONU et leur score "Impact".</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact économique</b></td>
                    <td style="padding: 10px;">Le fonds a un objectif de performance à long terme, mais les scénarios de performance varient, avec un rendement potentiel moyen de 7,04% par an sur 5 ans dans un scénario intermédiaire.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Impact environnemental</b></td>
                    <td style="padding: 10px;">Le fonds se concentre sur des entreprises qui génèrent des solutions en matière de durabilité environnementale, en élevant la part de l'investissement dans les solutions aux défis environnementaux et en excluant les secteurs polluants comme le charbon et le pétrole.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact social</b></td>
                    <td style="padding: 10px;">Le fonds évalue les entreprises sur la base de critères sociaux stricts, en se concentrant sur celles ayant des pratiques positives en matière de droits humains, de conditions de travail et de bien-être social.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Financement</b></td>
                    <td style="padding: 10px;">L'encours total du fonds s'élève à environ 486 millions d'euros, début 2025.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Développement</b></td>
                    <td style="padding: 10px;">Le fonds met l'accent sur un processus d’investissement flexible pour capter les opportunités en fonction des évolutions du marché et des pratiques ESG. </td>
                </tr>

                </table>
                """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels - Récompenses ESG (exemples à adapter ou compléter)
        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "Label ISR" : "Label garantissant le suivi d'une stratégie d'investissement durable en s'appuyant sur des critères ESG (Environnementaux, Sociaux, de Gouvernance).",
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
            - Exclusions sectorielles strictes 
            - Contribution favorables aux Objectifs de Développements Durables de l'ONU
            - Analyse de l'impact direct sur les enjeux de durabilité 
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Sélection d'entreprises sur la base de critères sociaux rigoureux 
            - Évaluation de l'impact social, notamment en lien avec la santé, l'éducation et le bien-être des communautés  
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Identification des stratégies d'entreprises durables et claires sur le long terme 
            - Exclusion d'entreprises impliquées dans des controverses non éthiques ou liées à la corruption
            - Désinvestissement dans les entreprises n'effectuant pas d'améliorations substantielles dans un délai prédéfini
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi cet actif ?")
        st.info(description1)
      

    elif choix == "Schroder International Selection Fund Emerging Europe":
    # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
        st.plotly_chart(fig)
        

        # Table Echiquier Positive Impact Europe I
        st.markdown("""
                <table style="width:100%; border-collapse: collapse;">
                <tr style="background-color:#f2f2f2;">
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
                    <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Activité</b></td>
                    <td style="padding: 10px;">Le fonds investit dans des actions de sociétés situées en Europe centrale et orientale, y compris dans les marchés émergents méditerranéens et les anciens pays de l'ex-Union soviétique, avec pour objectif de favoriser la croissance du capital à long terme​. </td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Approche</b></td>
                    <td style="padding: 10px;">Le fonds suit une gestion active, en investissant au moins deux tiers de ses actifs dans des actions de sociétés de la région, et peut également investir dans des titres non actions, des fonds d'investissement et des produits dérivés​.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact économique</b></td>
                    <td style="padding: 10px;">Le fonds ne cible pas un indice de référence précis, mais il est comparé à l'indice MSCI EFM Europe + CIS (E+C) Net Total Return pour évaluer sa performance.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Impact environnemental</b></td>
                    <td style="padding: 10px;">le fonds intègre des facteurs environnementaux dans son processus de sélection des investissements, visant des entreprises qui répondent à des enjeux durables.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Impact social</b></td>
                    <td style="padding: 10px;">Le fonds analyse l'impact social des entreprises dans lesquelles il investit, en privilégiant celles qui ont une gouvernance sociale forte et un engagement envers les communautés locales.</td>
                </tr>

                <tr style="background-color:#f9f9f9;">
                    <td style="padding: 10px;"><b>Financement</b></td>
                    <td style="padding: 10px;">Le fonds permet des rachats quotidiens et est géré avec une exposition entre 60% et 100% en actions, typiquement réparties sur 30 à 50 sociétés​.</td>
                </tr>

                <tr>
                    <td style="padding: 10px;"><b>Développement</b></td>
                    <td style="padding: 10px;">Le fonds est conçu pour capter les opportunités dans les marchés émergents d'Europe, avec une flexibilité d'investissement qui peut évoluer en fonction des opportunités spécifiques dans ces régions​. </td>
                </tr>

                </table>
                """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels - Récompenses ESG (exemples à adapter ou compléter)
        st.subheader("Reconnaissance et Engagement ESG")

        labels = {
            "Article 8 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui  intègrent des critères environnementaux, sociaux et de gouvernance dans leurs décisions d'investissement",
            "EU Taxonomy" : "Alignement avec les activités économiques des les objectifs environnementaux de la taxonomie européenne",
            "MSCI A":"Évalue la performance des entreprises sur les critères Environnementaux, Sociaux et de Gouvernance (ESG).",
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
            - Exclusions sectorielles strictes en matière de pollution
            - Sélection d'entreprises en prenant compte l'imapct environnemental et la mise en place de solutions durables 
            - Comparaison des performances avec un indice de référence pour les critères de durabilité 
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Participation à la réduction d'inégalités sociales au sein de la zone Europe 
            - Analyse sociale se concentrant sur les conditions de travail, les droits humains et les initiatives sociales  
            - Contribution à l'amélioraion des conditions de vie dans les zones où le fonds investit 
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Sélection d'entreprises aux règles de gouvernance solides et au management transparent 
            - Identification d'entreprises en capacité de mettre en place des startégies de développement durable 
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi cet actif ?")
        st.info(description1)





# -------------------------------
#   ACTIONS DURABLES EG
# -------------------------------
elif choix=="Actions Durables":


    st.markdown("""
    ### Critères de sélection des Actions Durables Futur de l'Europe 
    Nous avons sélectionné des actions d'entreprises, principalement européennes, qui, dans leurs objectifs de développement, semblent proposer des solutions innovantes pour la protection de l'environnement en Europe ou qui ont fait récemment des efforts considérables dans les domaines ESG.
    **Méthodologie de sélection :**
    - **Critères d'inclusion** : Initiatives visant à protéger l'environnement en Europe ; Innovations dans les secteurs de la durabilité ; Engagement fort et mesurable dans les domaines ESG (Environnement, Social et Gouvernance) ; Pratiques responsables dans la gestion des ressources naturelles et réduction de l'empreinte carbone
    - **Critères d'exclusion** : Pratiques environnementales controversées ou insuffisantes ; Manque de transparence dans les efforts écologiques ; Greenwashing
    """)

    actions = {
        "Iberdrola": {
            "ticker": "IBE.MC",
            "description": """Iberdrola est un leader mondial dans le secteur de l'énergie, reconnu pour son engagement envers la durabilité et la transition énergétique. L'entreprise se distingue par une empreinte carbone significativement inférieure à la moyenne du secteur, avec 55 grammes de CO₂ par kWh, soit 80 % de moins que ses pairs. Cet engagement se reflète dans ses investissements massifs dans la recherche et le développement, avec 385 millions d'euros consacrés à l'innovation verte. Iberdrola a également été classée en tête du **Sustainability Yearbook 2025** de S&P, obtenant le label Top 1 % pour ses performances environnementales, sociales et de gouvernance (ESG). 
            """
        },
        "OVHcloud": {
            "ticker": "OVH.PA",
            "description": """OVHcloud, acteur majeur du cloud européen, allie innovation technologique et responsabilité environnementale. L'entreprise a récemment rejoint la Coalition pour une IA durable, visant à orienter le développement de l'intelligence artificielle vers des pratiques écoresponsables. OVHcloud se positionne comme un "pionnier du cloud durable", mettant l'accent sur la sobriété énergétique et l'efficacité de ses infrastructures. L'entreprise s'engage à réduire son empreinte carbone et à promouvoir des pratiques respectueuses de l'environnement dans le secteur du cloud computing. """
        },
        "SAP": {
            "ticker": "SAP",
            "description": """SAP, leader mondial des logiciels d'entreprise, s'engage activement en matière de durabilité et de responsabilité sociale (ESG). L'entreprise a lancé des solutions innovantes telles que le SAP Green Ledger, un système de comptabilisation et de reporting carbone qui intègre les données d'émissions dans les systèmes financiers, permettant aux entreprises de suivre et de réduire leur empreinte carbone de manière efficace."""
        },
        "Volvo": {
            "ticker": "VOLV-B.ST",
            "description": """Volvo est un leader dans le secteur automobile, et l'entreprise se distingue par son engagement en matière de durabilité, particulièrement dans le domaine des véhicules électriques. Sa solide stratégie ESG, axée sur l'innovation et la durabilité, en fait une excellente option pour un portefeuille tourné vers les enjeux environnementaux et sociaux.
            """
        },
        "Carrefour": {
            "ticker":"CAP.PA",
            "description":"""Carrefour, acteur majeur de la grande distribution, met en œuvre des initiatives RSE ambitieuses pour répondre aux enjeux environnementaux et sociaux. L'entreprise a récemment adapté sa stratégie pour lutter contre le gaspillage alimentaire, en supprimant la mention de la date de durabilité minimale sur certains produits non périssables. Carrefour soutient également l'innovation durable à travers un fonds de capital-risque de 80 millions d'euros et un programme d'accélération pour les start-up dans la transition alimentaire."""
        },
        "Enel":{
            "ticker": "ENEL.MI",
            "description":"""Enel est une entreprise multinationale italienne spécialisée dans la production, la distribution et la vente d'électricité et de gaz naturel, présente dans environ 30 pays et leader mondial des énergies renouvelables en termes de capacité installée."""
        },
        }


    # Sélection de l'action à thématique eau
    choix = st.radio("Sélectionnez un actif", list(actions.keys()))
    symbole = actions[choix]["ticker"]
    description1 = actions[choix]["description"]

    if choix == "Iberdrola":
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
            <td style="padding: 10px;">Iberdrola est une entreprise espagnole leader dans la production et la distribution d'énergie, principalement à partir de sources renouvelables comme l'éolien, le solaire et l'hydroélectrique.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">L'entreprise utilise des technologies avancées telles que la gestion intelligente des réseaux et des systèmes de stockage d'énergie pour optimiser l'efficacité et la fiabilité de la distribution d'énergie.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">Iberdrola joue un rôle clé dans l'économie en générant des milliers d'emplois et en investissant massivement dans la transition énergétique.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;"> L'entreprise réduit les émissions de CO2 en augmentant la part des énergies renouvelables dans le mix énergétique mondial. </td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;"> Iberdrola soutient l'accès à l'énergie durable dans les communautés locales et mène des projets de responsabilité sociale d'entreprise dans les zones vulnérables.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Iberdrola est cotée à la Bourse de Madrid (BME).</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">Un facteur clé pour l'avenir est l'investissement en R&D (à hauteur de 385 millions d'euros en 2023), notamment pour optimiser le stockage d'énergie et la digitalisation de ses infrastructures pour améliorer l'efficacité des réseaux et l'intégration des énergies renouvelables.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Évaluation ESG d'Iberdrola")

        labels = {
        "ISO 14001": "La norme ISO 14001 est un standard international qui spécifie les exigences relatives à un système de management environnemental (SME) efficace.",
        "ISO 50001": "La norme ISO 50001 est une norme internationale qui spécifie les exigences relatives à un système de management de l'énergie efficace, visant à améliorer la performance énergétique.",
        "CDP A List (Climat)": "Iberdrola figure sur la liste A du CDP, reflétant ses efforts exceptionnels pour la gestion et la transparence de ses émissions de gaz à effet de serre.",
        "Climate Action 100+": "Iberdrola est reconnue pour ses efforts significatifs dans la réduction des émissions de gaz à effet de serre et son alignement avec les objectifs de l'Accord de Paris.",
        "Dow Jones Sustainability Index (DJSI)": "L'inclusion dans cet indice reflète la performance exceptionnelle d'Iberdrola en matière de durabilité et de responsabilité sociale.",
        "FTSE4Good Index": "L'appartenance à l'indice FTSE4Good certifie qu'Iberdrola respecte des normes élevées de responsabilité sociale et environnementale.",
        "Carbon Trust Standard": "Iberdrola a reçu cette certification pour sa gestion efficace des émissions de carbone et sa réduction de l'empreinte écologique.",
        "Global Compact des Nations Unies": "Iberdrola est membre du Global Compact, respectant les dix principes relatifs aux droits de l'homme, aux normes du travail, à l'environnement et à la lutte contre la corruption.",
        "ISO 45001": "La norme ISO 45001 certifie qu'Iberdrola met en place un système efficace de gestion de la santé et de la sécurité au travail (SST), garantissant la sécurité de ses employés.",
        "Empresa Familiarmente Responsable": "Ce label est décerné à Iberdrola pour son engagement à promouvoir la conciliation entre vie professionnelle et personnelle de ses collaborateurs."
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
            - Politique de biodiversité incluant un objectif de zéro déforestation d'ici 2025
            - Développement massif des énergies renouvelables par le bias d'un travail intense de recherche et développement
            - Réduction de 18% de ses émissions de CO2 par rapport à 2019
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Programmes de bénévolat d'entreprise pour travailler sur des projets sociaux et environnementaux 
            - Formations de personnes sans emploi dans les secteurs durables 
            - Intensification des échanges avec les communautés où des projets s'implantent pour minimiser les impacts négatifs  
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Transparence sur les activités et code de conduite aligné avec les principes des Nations unies sur les droits de l'homme 
            - Gestion et évaluation des risques ESG, notamment liés à la biodiversité et aux écosystèmes 
            - Exigence dans le choix de ses fournisseurs 
            """)

        # Pourquoi ce projet ?
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

        
    # -------------------------------
    elif choix == "OVHcloud":

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
            <td style="padding: 10px;">OVHcloud est un fournisseur européen de services cloud, offrant des solutions d'infrastructure et de plateforme adaptées aux besoins des entreprises en matière de cloud privé, public et hybride.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">L'entreprise se distingue par son utilisation des technologies open source comme OpenStack et Kubernetes, permettant une flexibilité maximale et une interopérabilité totale entre les différents environnements cloud.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">OVHcloud soutient l'économie avec un chiffre d'affaires de 993 millions d'euros en 2024, en fournissant des solutions fiables à plus de 1,6 million de clients dans 140 pays, et en créant un écosystème dynamique de partenaires et de fournisseurs.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">'entreprise s'engage à réduire son empreinte carbone avec 100% d'énergie bas carbone pour ses infrastructures et des innovations continues pour améliorer l'efficacité énergétique de ses datacenters.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">OVHcloud favorise la diversité et l'inclusion au sein de son équipe, avec des programmes de bien-être des employés et un engagement social marqué par des actions de bénévolat et d'insertion numérique.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">OVHcloud est cotée en bourse depuis 2021 sur Euronext Paris.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">OVHcloud met un fort accent sur la volonté de créer un cloud durable, avec une gestion responsable des données et un engagement à minimiser l'impact environnemental tout en répondant aux besoins de souveraineté numérique de ses clients.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Evaluation ESG d'OVHcloud")

        labels = {
        "ISO 50001": "La norme ISO 50001 est une norme internationale qui spécifie les exigences relatives à un système de management de l'énergie efficace, visant à améliorer la performance énergétique.",
        "Code of Conduct for Energy Efficiency in Data Centres": "OVHcloud participe à ce code de conduite européen, démontrant son engagement à améliorer l'efficacité énergétique de ses centres de données.",
        "Climate Neutral Data Center Pact": "En adhérant à ce pacte, OVHcloud s'engage à rendre ses centres de données climatiquement neutres d'ici 2030, contribuant ainsi à la réduction des émissions de gaz à effet de serre.",
        "VMware Zero Carbon Committed Initiative": "Cette initiative reconnaît l'engagement d'OVHcloud à réduire l'empreinte carbone de ses opérations de centres de données en optimisant l'utilisation des infrastructures informatiques et en utilisant des énergies renouvelables.",
        "PUE (Power Usage Effectiveness)": "Cet indicateur mesure l'efficacité énergétique des centres de données d'OVHcloud, avec un PUE proche de 1 indiquant une utilisation efficace de l'énergie.",
        "WUE (Water Usage Effectiveness)": "Cet indicateur évalue l'efficacité de la consommation d'eau dans les centres de données d'OVHcloud, reflétant l'engagement de l'entreprise à minimiser l'utilisation de l'eau.",
        "CUE (Carbon Usage Effectiveness)": "Cet indicateur mesure les émissions de carbone liées aux opérations des centres de données d'OVHcloud, avec des valeurs plus faibles indiquant une meilleure performance environnementale.",
        "REF (Renewable Energy Factor)": "Le REF indique la proportion d'énergie renouvelable utilisée par OVHcloud dans ses centres de données, reflétant l'engagement de l'entreprise envers l'énergie verte.",
        "Reused Components Ratio": "Ce ratio montre qu'OVHcloud réutilise 27% de ses composants, prolongeant leur durée de vie et réduisant l'impact environnemental lié à la fabrication de nouveaux équipements."
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
            - Réduction continuelle de l'empreinte carbone grâce à des services cloud performants 
            - Engagement à alimenter ses infrastructures avec 100% d'énergie bas carbone 
            - Datacenters implantés en zone de friches industrielles rénovées et composants réutilisés 
            """)


        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Fort engagement en matière de conditions de travail saines et du bien-être des employés 
            - Accent porté à l'insertion professionelle des personnes en situation de handicap 
            - Programme de bénévolat d'entreprise, renforçant l'inclusion et les projets en matière d'ESG
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Dialogue social de qualité  
            - Diversité au sein des instances dirigeantes 
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)
    
    # -------------------------------
    elif choix =="SAP":

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
            - <td style="padding: 10px;">SAP est un fournisseur mondial de logiciels de gestion d'entreprise, offrant des solutions cloud et sur site pour aider les entreprises à améliorer leurs performances dans des domaines comme la finance, les ressources humaines, et la gestion de la chaîne d'approvisionnement. </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">SAP intègre des technologies avancées telles que l'IA et le cloud computing pour développer des solutions et outils d'analyse qui permettent aux entreprises de prendre des décisions plus intelligentes et durables.</td>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">SAP a généré des recettes à hauteur de 34,2 milliards d'euros en 2024, tout en soutenant des millions d'entreprises à travers le monde dans leur transformation numérique.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">SAP s'engage à atteindre un objectif de neutralité carbone d'ici 2030, avec des investissements continus dans les énergies renouvelables et des solutions pour aider ses clients à réduire leur empreinte écologique.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">SAP soutient l'inclusion numérique, avec des programmes de formation pour plus de 2,5 millions de personnes dans le monde, et des initiatives pour promouvoir la diversité et l'égalité des chances au sein de ses équipes.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">En Europe, SAP est cotée sur la Bourse de Francfort.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">SAP continue de se concentrer sur l'innovation dans le cloud durable et la gestion des données afin d'aider les entreprises à atteindre leurs objectifs ESG.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Evaluation ESG de SAP")

        labels = {
        "ISO 14001": "La norme ISO 14001 est un standard international qui spécifie les exigences relatives à un système de management environnemental (SME) efficace.",
        "ISO 50001": "La norme ISO 50001 est une norme internationale qui spécifie les exigences relatives à un système de management de l'énergie efficace, visant à améliorer la performance énergétique.",
        "ISO 45001": "La norme ISO 45001 est une norme internationale qui spécifie les exigences relatives à un système de management de la santé et de la sécurité au travail (SST).",
        "ISO 27001": "La norme ISO 27001 est une norme internationale qui spécifie les exigences relatives à un système de management de la sécurité de l'information (SMSI).",
        "ISO 37001": "La norme ISO 37001 est une norme internationale qui spécifie les exigences relatives à un système de management anti-corruption (SMAC).",
        "CDP A List (Climat)": "SAP figure sur la liste A du CDP, montrant son engagement et sa transparence dans la gestion et la réduction de ses émissions de gaz à effet de serre.",
        "Dow Jones Sustainability Index (DJSI)": "SAP est inclus dans cet indice, reflétant sa performance exceptionnelle en matière de durabilité, notamment en matière de gouvernance et de responsabilité environnementale.",
        "FTSE4Good Index": "L'appartenance à l'indice FTSE4Good certifie que SAP respecte des critères rigoureux de responsabilité sociale et environnementale dans ses opérations.",
        "Carbon Disclosure Project (CDP)": "SAP est reconnu par le CDP pour ses efforts visant à réduire son empreinte carbone et à améliorer la transparence de ses actions climatiques.",
        "Global Compact des Nations Unies": "SAP adhère au Global Compact des Nations Unies, s'engageant à respecter les principes relatifs aux droits de l'homme, aux normes du travail, à l'environnement et à la lutte contre la corruption."
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
            - Réduction de 40% de ses émissions de gaz à effet de serre par rapport à 2020
            - Mise en place d'outils sophistiqués tels que Sustainability Control Tower, aidant à mesurer les émissions de CO2 en temps réel 
            - Alimentation des centres de données via de l'électricité renouvelable 
                """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Forte politique d'inclusion (28% de femmes au conseil de surveillance)
            - Grande flexibilité dans les conditions de travail des employés 
            - Promotion de modes de transports durables auprès de ses employés 
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Haute fréquence de réunion du comité de gouvernance pour l'évaluation des progrès des objectifs de durabilité 
            - Mécanisme interne de tarification carbone pour inciter ses employés à des pratiques durables 
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    # -------------------------------
    elif choix == "Volvo":
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
            <td style="padding: 10px;">Volvo Group est un fabricant mondial de poids lourds, de bus, d'équipements de construction, ainsi que de moteurs marins et industriels, et propose des solutions de financement et de services pour ses clients dans près de 180 pays.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">Volvo Group mise sur l'électrification avec des véhicules à batterie, à hydrogène et des moteurs à combustion interne fonctionnant avec des carburants renouvelables.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">Volvo génère des revenus significatifs de 527 milliards SEK en 2024, avec des investissements dans l'innovation et la R&D pour répondre aux besoins d'un marché en transformation vers des solutions durables.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">En 2024, les émissions de CO2 de ses produits ont diminué de 25% par rapport à 2019, avec des solutions telles que les camions électriques et hybrides, qui ont amélioré l'efficacité énergétique de jusqu'à 10% par rapport aux modèles précédents.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">L'entreprise emploie 102 000 personnes, et met en œuvre des moyens considérables dans le domaine de la sécurité de ses véhicules. </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Les actions de Volvo sont cotées à la bourse de Stockholm.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;"> En cohérence avec les tendances actuelles, Volvo mise sur un avenir décarboné où les véhicules électriques sont plus performants et plus sécurisés.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Evaluation ESG de Volvo")

        labels = {
        "CDP A List (Climat)": "Volvo figure sur la liste A du CDP, reflétant ses efforts significatifs pour la gestion et la réduction de ses émissions de gaz à effet de serre.",
        "Dow Jones Sustainability Index (DJSI)": "Volvo est inclus dans cet indice prestigieux, attestant de sa performance exceptionnelle en matière de durabilité et de responsabilité sociale et environnementale.",
        "FTSE4Good Index": "Volvo est inscrit dans l'indice FTSE4Good, ce qui montre qu'elle respecte des critères stricts de durabilité sociale, environnementale et éthique.",
        "Carbon Disclosure Project (CDP)": "Volvo reçoit une reconnaissance du CDP pour sa transparence et ses efforts dans la gestion des risques climatiques et la réduction des émissions de carbone.",
        "Global Compact des Nations Unies": "Volvo adhère aux principes du Global Compact, en s'engageant à respecter les droits de l'homme, les normes du travail, l'environnement et la lutte contre la corruption.",
        "ISO 14001": "La certification ISO 14001 atteste de la mise en place d'un système de management environnemental efficace au sein de Volvo.",
        "ISO 50001": "Volvo est certifiée ISO 50001 pour ses efforts en matière de gestion de l'énergie, visant à réduire la consommation énergétique et les émissions de CO2.",
        "B Corp Certification": "Volvo est certifiée B Corp, attestant de son engagement à respecter des critères élevés de performance sociale et environnementale, de responsabilité et de transparence.",
        "LEED Certification": "Les installations de Volvo respectent les critères de construction durable de la certification LEED, garantissant une performance énergétique et environnementale optimale.",
        "Sustainalytics ESG Risk Rating": "Volvo reçoit une note ESG solide de Sustainalytics, indiquant une gestion efficace des risques ESG avec un score faible en termes de risque global.",
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
            - En 2024, diminution de 25% des émissions de CO2 de la "phase d'utilisation" des produits rapport à 2019.
            - 70% des camions lourds électriques de Volvo en Europe en service
            - Participation à la First Movers Coalition pour dialoguer des secteurs difficiles à décarboner
            """)

        # Contenu pour la colonne 2 - Social
        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Formation en continu sur la sécurité dans les usines 
            - Accès à des services essentiels pour des communautés dans le besoin, améliorant la qualité de vie des habitants.
            - Acquisition de l'activité batterie de Proterra pour 2,2 milliards SEK 
            """)

        # Contenu pour la colonne 3 - Gouvernance
        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Communication claire et transparente sur la sécurité 
            - Normes strictes en matière de sécurité, de santé au travail et de durabilité environnementale
            """)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)


 # -------------------------------
    elif choix =="Carrefour":

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
            <td style="padding: 10px;">Carrefour est une entreprise de distribution multinationale opérant principalement dans le secteur alimentaire et non alimentaire, avec une large gamme de produits de marques propres, ainsi que de services financiers et d'immobilier.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">Carrefour investit dans l’e-commerce et l’économie circulaire, avec des initiatives comme la réduction du gaspillage alimentaire et l’utilisation croissante d'emballages recyclables et réutilisables.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">Carrefour vise à représenter 40 % de son chiffre d’affaires alimentaire via ses marques propres d’ici 2026, et met en place des partenariats avec 50 000 producteurs locaux pour une diversification durable de ses chaînes d’approvisionnement.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">CCarrefour a réduit de 49,7 % le gaspillage alimentaire par rapport à 2016 et augmente l’utilisation de plastiques recyclés dans ses emballages, avec 16,4 % de plastique recyclé en 2024.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">Carrefour s’engage à promouvoir l’inclusion, avec 5 000 nouveaux collaborateurs issus de sa formation interne « École des Leaders » d’ici 2026 et un objectif de 15 000 salariés en situation de handicap d’ici 2026.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Carrefour est cotée sur le marché Euronext Paris.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">Carrefour met en place un programme ambitieux pour une transition alimentaire durable, visant à renforcer la traçabilité et la durabilité de ses produits.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        labels = {
        "Climate Action 100+": "Carrefour est engagée dans cette initiative qui vise à réduire les émissions de gaz à effet de serre, améliorer la gouvernance climatique et renforcer la transparence financière liée au climat.",
        "Moody's ESG Performance": "En décembre 2020, Carrefour affichait une performance ESG avancée, se classant à la 2ᵉ place sur 19 entreprises du secteur des supermarchés selon Moody's.",
        "Eco-Score": "Carrefour a testé l'Eco-Score sur son site marchand, une étiquette évaluant l'impact environnemental des produits alimentaires.",
        "Partenariat avec Too Good To Go": "Depuis 2019, Carrefour collabore avec l'application Too Good To Go pour proposer des paniers de produits proches de leur date de péremption à prix réduit, contribuant à la lutte contre le gaspillage alimentaire.",
        "Marque 'Tous AntiGaspi'": "Lancée en 2015, cette marque vise à écouler les produits avec un aspect irrégulier mais toujours consommables, réduisant ainsi le gaspillage alimentaire.",
        "Fondation d'entreprise Carrefour": "Créée en 2000, elle finance des projets liés à l'alimentation solidaire et à l'aide d'urgence, renforçant l'engagement social de l'entreprise.",
        "Engagement pour le bien-être animal": "Depuis 2019, Carrefour a mis en place des audits dans ses abattoirs et a introduit des caméras de surveillance pour améliorer les conditions de traitement des animaux.",
        "Engagement pour la réduction des émissions de CO₂": "Le groupe s'engage à réduire ses émissions de CO₂ de 40 % entre 2010 et 2025, avec des initiatives telles que l'utilisation de camions roulant au biométhane et l'installation de systèmes de froid écologique.",
        "Certification MSC et ASC pour les produits de la mer": "Carrefour propose des produits de la mer certifiés Marine Stewardship Council (pêche durable) et Aquaculture Stewardship Council (aquaculture responsable), garantissant des pratiques respectueuses de l'environnement.",
        "Engagement pour l'huile de palme durable": "En 2016, Carrefour a atteint son objectif d'utiliser 100 % d'huile de palme issue de la filière RSPO (Roundtable of Sustainable Palm Oil), assurant une production durable.",
        "Partenariat pour la commercialisation de semences paysannes": "En 2017, Carrefour a collaboré avec des producteurs bretons pour proposer des légumes issus de semences paysannes, contribuant à la biodiversité agricole.",
        "Suppression des sacs plastiques en caisse": "Depuis 2020, Carrefour a mis fin à la vente de sacs plastiques en caisse, réduisant ainsi l'utilisation de plastique et son impact environnemental.",
        "Initiatives pour la réduction du gaspillage alimentaire": "Carrefour a mis en place diverses actions, telles que la vente de produits proches de la date de péremption à prix réduit et la proposition de paniers 'Zéro Gaspi', visant à lutter contre le gaspillage alimentaire.",
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


        # ESG Columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - Réduction significative du gaspillage alimentaire (diminution d'environ 50% par rapport à 2016)
            - La moitié des emballages des produits Carrefour sont réutilisables, recyclables ou compostables en 2024
            - Émission d'un emprunt obligataire de 750 millions d'euros lié à des objectifs de réduction de gaz à effet de serre          
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Engagement à augmenter l'emploi des personnes en situation de handicap d'ici 2026
            - Partenariats locaux avec des producteurs français pour sécuriser les approvisionnements et renforcer l'agriculture locale 
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Incitation aux employés à devenir actionnaires via le plan Carrefour Invest 
            - Obtention d'un score de 78/100 auprès de Moody's et intégration du Dow Jones Sustainability Index 
            - Veille éthique des fournisseurs 
            """)

        # Pourquoi ce projet ?
        st.markdown("#### Pourquoi ce projet ?")
        st.info(description1)

    elif choix =="Enel":

        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du cours du fonds
        st.subheader(f"Cours d' {choix}")
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
            <td style="padding: 10px;">Enel est une entreprise multinationale italienne spécialisée dans la production, la distribution et la commercialisation d'électricité et de gaz, opérant dans plus de 30 pays à travers le monde.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Technologie</b></td>
            <td style="padding: 10px;">Enel investit massivement dans l'innovation énergétique, notamment avec Enel X, sa branche qui se concentre sur les solutions numériques, l'intégration des énergies renouvelables et l'infrastructure de recharge pour véhicules électriques.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact économique</b></td>
            <td style="padding: 10px;">Enel est un acteur majeur de l’économie mondiale, contribuant de manière significative à la création de valeur dans le secteur énergétique et soutenant l'économie circulaire grâce à son approche de décarbonation.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Impact environnemental</b></td>
            <td style="padding: 10px;">Enel s'engage à atteindre la neutralité carbone d'ici 2040, en fermant ses centrales à charbon d'ici 2027 et en augmentant considérablement sa capacité de production d'énergie renouvelable, avec une capacité installée de plus de 55,5 GW.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Impact social</b></td>
            <td style="padding: 10px;">Grâce à des solutions toujours plus performantes, Enel fournit aujourd'hui de l'énergie et ses services à plus de 55,2 millions de foyers et entreprises.</td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px;"><b>Financement</b></td>
            <td style="padding: 10px;">Enel est cotée à la Bourse de Milan.</td>
        </tr>

        <tr>
            <td style="padding: 10px;"><b>Développement</b></td>
            <td style="padding: 10px;">Enel poursuit une stratégie de transition énergétique, notamment avec la réduction de son empreinte carbone et l'expansion des énergies renouvelables.</td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        # Séparateur visuel
        st.markdown("---")

        # Section Labels
        st.subheader("Évaluation ESG d'Enel")
        labels = {
            "ISO 14001": "La certification ISO 14001 atteste de l'engagement d'Enel à mettre en place un système de management environnemental efficace, visant à réduire son empreinte écologique.",
            "ISO 50001": "Enel est certifiée ISO 50001, reflétant ses efforts pour améliorer la gestion de l'énergie et promouvoir l'efficacité énergétique au sein de ses opérations.",
            "Dow Jones Sustainability Index (DJSI)": "Enel est incluse dans le Dow Jones Sustainability Index, reconnaissant sa performance exceptionnelle en matière de durabilité et de responsabilité sociale et environnementale.",
            "FTSE4Good Index": "Enel fait partie de l'indice FTSE4Good, reflétant son engagement envers des pratiques commerciales responsables et durables sur les plans environnemental, social et de gouvernance.",
            "Carbon Disclosure Project (CDP) A- List": "Enel a obtenu une note A- du CDP, soulignant ses actions pour réduire les émissions de gaz à effet de serre et sa transparence dans la communication des risques climatiques.",
            "Global Compact des Nations Unies": "Enel adhère au Global Compact des Nations Unies, s'engageant à respecter les principes relatifs aux droits de l'homme, aux normes du travail, à l'environnement et à la lutte contre la corruption.",
            "ISO 22000": "Enel vise à obtenir la certification ISO 22000, démontrant son engagement envers la sécurité alimentaire et la qualité de ses produits et services liés à l'énergie.",
            "S&P Global ESG Score": "Enel a obtenu un score élevé selon l'évaluation ESG de S&P Global, reflétant ses pratiques exemplaires en matière d'environnement, de responsabilité sociale et de gouvernance.",
            "CDP Climate Change Score": "Enel est reconnue pour sa transparence et ses actions en matière de changement climatique, obtenant une note positive dans l'évaluation du CDP.",
            "Just Transition Initiative": "Enel participe à l'Initiative pour une Transition Juste, promouvant des politiques et des actions qui soutiennent les travailleurs et les communautés affectées par la transition énergétique.",
            "Enel X": "Enel X est la branche innovation d'Enel, dédiée au développement de solutions technologiques avancées pour une transition énergétique durable, incluant des projets de mobilité électrique et de smart cities.",
            "Sustainability Yearbook": "Enel est incluse dans le Sustainability Yearbook, reflétant son engagement continu envers des pratiques commerciales durables et responsables.",
            "Innovation Hubs": "Enel a inauguré des Innovation Hubs, tels que ceux à Tel Aviv et à l'Université de Californie à Berkeley, pour favoriser l'innovation technologique et le développement durable dans le secteur de l'énergie.",
        }


        # ESG Columns
        col1, col2, col3 = st.columns(3)
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


        with col1:
            st.markdown("**Environnement**")
            st.markdown("""
            - Réduction significative des émissions de CO2 et volonté de neutralité carbone d'ici 2040
            - Investissement massif dans les énergies renouvelables (4,5 milliards d'euros en 2022)
            - Réduction de la consommation d'eau dans les procédés industriels         
            """)

        with col2:
            st.markdown("**Social**")
            st.markdown("""
            - Contribution à l'inclusion énergétique en fournissant à plus de 2 millions de personnes en 2022
            - Réduction de son taux d'incidents au travail de 10% en 2022 par rapport à l'année précédente grâce à la mise en place de normes 
            """)

        with col3:
            st.markdown("**Gouvernance**")
            st.markdown("""
            - Diversité au sein du conseil d'administration (40% de femmes)
            - Obtention de 100% dans l'indice de transparence fiscale de l'ONG Oxfam
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