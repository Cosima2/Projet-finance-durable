import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Fonds ESG", layout="wide")

# -------------------------------
# TITRE 
# -------------------------------
st.title("Fond d'investissement ESG")
st.markdown("Trouvez ici les explications liés à la composition de notre portefeuille structuré selon les critères ESG." \
"Notre portefeuille dispose d'une partie générale et d'une partie spécifique." \
" La partie générale est composée de 45% d'obligations, de fonds à impact, d'ETF durables et de crypto verte." \
" La partie spécifique est composée de 55% d'actifs projet, d'obligations corporate vertes et d'actions durables sur la thématique de votre choix." )

st.header("Composition de notre fond")

composition_generale = {
    "Obligations (gouvernementales ou vertes)": 15,
    "Fonds à impact": 20,
    "ETF durables": 5,
    "Crypto verte": 5,
    "Actifs Projet": 20,
    "Obligations Corporate Vertes": 10,
    "Fonds à Impact": 5,
    "Actions Durables": 20
}
df_generale = pd.DataFrame(list(composition_generale.items()), columns=["Actif", "Poids (%)"])
fig_generale = px.pie(df_generale, values="Poids (%)", names="Actif", title="Répartition des actifs ")
st.plotly_chart(fig_generale, use_container_width=True)

# -------------------------------
# PARTIE GÉNÉRALE
# -------------------------------
st.header("Partie Générale du Portefeuille (45%)")
st.subheader("Analyse des Actifs")
st.write("Cette section présente la répartition des actifs dans le portefeuille général, qui est composé de 45% d'obligations, de fonds à impact, d'ETF durables et de crypto verte.")

categorie_actifs_generale = ["Obligations (gouvernementales ou vertes)", "Fonds à impact","ETF durables", "Startup verte"]
# Sélection de la catégorie d'actifs
choix = st.radio("Sélectionnez une catégorie d'actifs", categorie_actifs_generale)
st.write(f"Vous avez sélectionné : ### **{choix}**")


# -------------------------------
# Obligations
# -------------------------------

if choix == "Obligations (gouvernementales ou vertes)":

    st.markdown("""
    Objectif :
    Créer un ensemble d'obligations souveraines basé sur :
    - **Critères d'inclusion** : bonne gouvernance, énergie renouvelable, climat des affaires, croissance.
    - **Critères d'exclusion** : usage d’énergies fossiles, prime de risque excessive.
    - des décisions de sélection finale via **volatilité obligataire** et **rendement 2024**.

    Pour décider des Etats dans lesquels investir, nous avons pris en compte différents critères :  \
    des critères de la banque mondiale liées à la qualité ESG des pays ainsi que les rendements obligataires. \
    Pour plus de simplicité nous avons sélectionné les pays de l'OCDE uniquement. Concernant les critères de la banque mondiale,  \
    nous avons sélectionné les indicateurs suivants :
            - "IC.BUS.EASE.XQ": "Ease of doing business rank (1=most business-friendly regulations)",
            - "EG.FEC.RNEW.ZS": "Renewable energy (% of total energy)",
            - "CC.EST": "Control of corruption",
            - "NY.GDP.PCAP.KD.ZG": "GDP per capita growth (annual %)",
            - "EG.USE.COMM.FO.ZS": "Fossil fuel energy consumption (% of total)",
            - "FR.INR.RISK": "Risk premium on lending (lending rate minus treasury bill rate, %)
    """)

    st.code("""
        # Liste des pays de l'OCDE (codes ISO3)
        oecd_countries = [
            "AUS", "AUT", "BEL", "CAN", "CHL", "COL", "CRI", "CZE", "DNK", "EST",
            "FIN", "FRA", "DEU", "GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN",
            "KOR", "LVA", "LTU", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT",
            "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA"
        ]
        """, language="python")

    # ----------- ESG DATAFRAME
    st.subheader("Données ESG - Banque Mondiale")

    try:
        df_esg = pd.read_csv("esg_oecd_worldbank.csv")
        st.dataframe(df_esg)
    except:
        st.warning("Le fichier 'esg_oecd_worldbank.csv' est introuvable. Veuillez exécuter le script de récupération des données.")

    # ----------- SDR AVERAGE SCORE
    st.subheader("Scores SDR (2000-2023)")
    try:
        df_sdr = pd.read_csv("SDR-2024-overall-score.csv")
        st.dataframe(df_sdr.head(10))
    except:
        st.warning("Le fichier 'sdr_scores_avg.csv' est introuvable.")


    # ----------- PAYS INCLUS / EXCLUS
    #CODE A METTRE 
    st.subheader("Résultat de la sélection ESG")

    pays_inclus = ["Greece", "Costa Rica", "Sweden", "Norway", "Finland", "Denmark", "Iceland", "Latvia", "Luxembourg", "Colombia", "France", "Germany", "United Kingdom", "Canada"]
    pays_exclus = ["Hungary", "Australia", "United States", "Czech Republic", "New Zealand", "Israel", "Netherlands", "Japan", "Mexico", "Poland"]

    col1, col2 = st.columns(2)
    with col1:
        st.success("Pays retenus")
        st.write(pays_inclus)
    with col2:
        st.error("Pays exclus")
        st.write(pays_exclus)


    # ------------------------------------------------------------
    # ANALYSE DES TAUX ET VOLATILITÉS
    # ------------------------------------------------------------
    st.header("Analyse macro des obligations souveraines")

    # Rendements 2024
    st.subheader("Top 5 pays par rendement obligataire (déc. 2024)")
    try:
        df_yield = pd.read_csv("macro_data/obli_souveraines.csv", parse_dates=[0], index_col=0)
        df_2024 = df_yield[df_yield.index.year == 2024]
        derniers_taux = df_2024.iloc[-1]
        top5_yield = derniers_taux.sort_values(ascending=False).head(5)
        st.dataframe(top5_yield)
    except:
        st.warning("Erreur lors du chargement du fichier 'obli_souveraines.csv' pour les rendements.")

    # Volatilité
    st.subheader("Pays avec la volatilité obligataire la plus faible depuis 2000")
    try:
        volatilites = df_yield.std().sort_values()
        st.dataframe(volatilites.head(5))
    except:
        st.warning("Erreur lors du calcul de la volatilité obligataire.")

    # ------------------------------------------------------------
    # CONCLUSION
    # ------------------------------------------------------------
    st.header("Conclusion et sélection finale")
    st.markdown("""
    À partir de l’analyse croisée ESG et macro :
    - **Pays retenus** :  Canada, Costa Rica, Iceland, UK, Norway, Colombia car erformants sur les critères ESG **et** attractifs en termes de **rendement ou de stabilité des taux**.
    - L’objectif est de combiner **impact durable** et **performance financière mesurée**.
    """)

    obligations = {
        "Costa Rica": {
            "ticker": "CRIIRLTLT01STM",
            "description": """Le Costa Rica émerge comme un choix de plus en plus populaire pour les investisseurs, particulièrement dans une perspective ESG. Le pays est un modèle 
            en matière de développement durable et de réduction de la dépendance aux énergies fossiles, avec plus de 80% de son énergie provenant de sources renouvelables. 
            Le Costa Rica a également un excellent classement en termes de facilité de faire des affaires, ce qui témoigne de son environnement économique stable et favorable. 
            Le pays enregistre une croissance solide du PIB par habitant, avec une forte priorité donnée à la biodiversité et à la protection de l'environnement. 
            Le Costa Rica possède aussi une faible corruption, créant un environnement de confiance pour les investisseurs. Avec une prime de risque relativement faible et une politique ouverte à l'international, 
            il constitue une option idéale pour un portefeuille cherchant à maximiser les rendements tout en respectant les critères ESG, en particulier pour les investisseurs soucieux de la préservation de l’environnement."""
        },
        "Canada" : {
            "ticker": "IRLTLT01CAM156N",
            "description": """Le Canada se positionne comme un leader d'investissement avec un environnement économique stable et un système financier robuste. Le pays bénéficie d'une note favorable pour la facilité de faire des affaires 
            (classement 72) et offre une forte gouvernance en matière de contrôle de la corruption, avec un système judiciaire fiable et transparent. En matière de croissance du PIB par habitant, le Canada présente des chiffres solides, 
            bien que plus modérés que certains autres pays. En matière d'énergie renouvelable, le pays a fait d'importants progrès, bien que l'usage de l'énergie fossile reste élevé, ce qui limite l'impact écologique de certains investissements. 
            Cependant, les engagements du Canada envers les objectifs climatiques et l'infrastructure de l'énergie verte en font un acteur clé dans la transition énergétique. Le Canada possède également une faible prime de risque sur ses emprunts, 
            indiquant une stabilité économique appréciable. L'investissement dans des obligations canadiennes constitue ainsi un choix pertinent pour un portefeuille ESG, en particulier en raison de son respect des normes éthiques et environnementales, 
            et de sa stabilité politique et économique.
            """
        },
        "Iceland": {
            "ticker": "IRLTLT01ISM156N",
            "description": """L'Islande se distingue par son engagement environnemental avec un usage massif des énergies renouvelables, notamment l'hydroélectricité et la géothermie, représentant plus de 80% de son énergie totale. 
            Ce pays affiche un classement élevé en matière de contrôle de la corruption et d’éthique des affaires, ce qui en fait une destination attractive pour les investisseurs cherchant des actifs fiables et stables. 
            L’Islande a su maintenir une croissance soutenue du PIB et un environnement propice aux affaires durables. Bien que le pays ait une taille économique plus modeste comparé à des géants comme le Canada, ses efforts pour 
            développer une économie circulaire et son faible impact environnemental en font un investissement cohérent pour des stratégies ESG. La faible volatilité des rendements des obligations souveraines combinée à des normes élevées en 
            matière de gouvernance et d'impact environnemental font de l'Islande une valeur sûre pour un portefeuille aligné avec des objectifs ESG.
            """     
        },
        "United Kingdom": {
            "ticker": "IRLTLT01GBM156N",
            "description": """Le Royaume-Uni demeure une puissance économique mondiale et continue de présenter un environnement stable pour les investisseurs. Bien que le pays ait été confronté à des défis liés au Brexit, ses réformes économiques 
            et son marché financier dynamique restent des atouts majeurs. Le Royaume-Uni a un système réglementaire robuste pour les affaires et une gouvernance très transparente. En matière de croissance du PIB par habitant, le pays affiche une stabilité positive. 
            L'UK est également très impliqué dans la transition énergétique, avec des engagements forts en matière d'énergie verte. Son marché des obligations reste attractif, offrant une faible volatilité et des rendements intéressants. Pour un portefeuille ESG, 
            le Royaume-Uni reste une destination privilégiée grâce à ses réformes structurelles en matière d'environnement et de gouvernance.
            """
        },
        "Norway": {
            "ticker": "IRLTLT01NOM156N",
            "description": """La Norvège est un modèle de durabilité et d'engagement pour l'environnement. Le pays possède l'une des plus hautes proportions d'énergie renouvelable en Europe, représentant environ 61% de sa consommation totale d'énergie. 
            La Norvège affiche un très faible niveau de corruption et a un système économique transparent et stable. La croissance du PIB par habitant est robuste et soutenue, ce qui témoigne de la solidité de son économie. 
            En tant que l'un des plus grands producteurs de pétrole au monde, la Norvège s'efforce de diversifier son économie vers des investissements verts et des technologies durables. De plus, le pays maintient une faible prime de risque et une grande stabilité économique. 
            Dans le cadre d'un portefeuille ESG, la Norvège est un choix stratégique qui offre à la fois des rendements solides et une responsabilité environnementale exemplaire.
            """
        },
        "Colombia": {
            "ticker": "COLIRLTLT01STM",
            "description": """La Colombie représente un marché émergent intéressant avec un grand potentiel de croissance économique. Avec une forte croissance du PIB par habitant (environ 4,62% par an), le pays connaît une expansion rapide de son secteur 
            des énergies renouvelables. Bien que la Colombie soit un pays en développement, il a réussi à créer un environnement d'affaires relativement favorable avec un classement honorable en matière de facilité de faire des affaires. 
            En outre, la Colombie a effectué d'importants progrès dans la lutte contre la corruption. Ce pays offre une prime de risque faible, ce qui en fait un choix attractif pour les investisseurs cherchant à diversifier leur portefeuille. 
            Les obligations souveraines colombiennes présentent un bon compromis entre rendement élevé et stabilité, tout en soutenant les objectifs ESG grâce à un environnement réglementaire en amélioration continue.
            """
        },
    }
    # Sélection de l'obligation
    choix = st.radio("Sélectionnez une obligation", list(obligations.keys()))
    symbole = obligations[choix]["ticker"]
    description = obligations[choix]["description"]

    # Récupération des données financières
    csv_file = "macro_data/obli_souveraines.csv"
    df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
    df_plot = df[[symbole]].dropna().reset_index()
    df_plot.columns = ["Date", "Taux"]

        # Affichage du cours de l'obligation 10 ans
    st.subheader(f"Cours de Long-Term Government Bond Yields: 10-Year de {choix}")
    fig = px.line(df_plot, x="Date", y="Taux", title=f"{choix} - Rendement obligataire 10 ans")
    st.plotly_chart(fig)
        # Affichage de la description ESG
    st.markdown("#### Pourquoi ce pays ?")
    st.info(description)


# -------------------------------
# Fonds à impact
# -------------------------------
elif choix== "Fonds à impact":
    st.markdown("""
    Objectif :
    Créer un ensemble de fonds à impact basé sur :
    - **Critères d'inclusion** : labels, respect de la réglementation, article 9 SFDR
    - **Critères d'exclusion** : usage d’énergies fossiles, prime de risque excessive.
    - des décisions de sélection finale via la pertinence et la singularité du fonds.
    """)

    # ----------- Labels DATAFRAME
    st.subheader("Données ESG - Labels")

    try:
        df_labels = pd.read_csv("Fonds_greenfin_ISR.csv")
        st.dataframe(df_labels)
    except:
        st.warning("Le fichier 'esg_oecd_worldbank.csv' est introuvable. Veuillez exécuter le script de récupération des données.")


    # ----------- Fonds INCLUS / EXCLUS
    st.markdown("Bien que possédant des labels ESG, il nous paraissait peu cohérent de sélectionner des fonds émis par des entreprises" \
    "comme Blackrock, Vanguard ou Amundi qui sont des entreprises qui investissent massivement dans des actifs peu respectueux de l'environnement." \
    "Nous avons donc décidé de ne pas sélectionner ces fonds et il paraissait inévitable de chercher manuellement les fonds en épluchant les sites de certaines" \
    "sociétés prometteuses")

    fonds_inclus = ["Mirova", "Ecofi", "La Banque Postale", "Amiral Gestion", "Sycomore"]
    fonds_exclus = ["Blackrock", "Vanguard", "Amundi", "Lyxor", "HSBC", "BNP Paribas", "Natixis", "Société Générale"]
    col1, col2 = st.columns(2)
    with col1:
        st.success("Fonds retenus")
        st.write(fonds_inclus)
    with col2:
        st.error("Fonds exclus")
        st.write(fonds_exclus)

    fonds = {
        "Mirova Environment Accelerating Capital": {
            "ticker": "none",
            "description": """Le Mirova Environment Accelerating Capital (MEAC) est un fonds de private equity axé sur les entreprises innovantes répondant aux défis environnementaux mondiaux.
            Il investit dans des sociétés qui développent des solutions durables dans les domaines de l'énergie, de l'eau, des déchets et de l'agriculture."""
        },
        "Mirova Europe Environnement" : {
            "ticker": "FR0010521575",
            "description": """Le fonds Mirova Europe Environnement a pour objectif de soutenir des entreprises européennes qui s'engagent dans des solutions et services ayant un impact positif sur l'environnement. 
            Ce fonds s’inscrit dans une démarche d’investissement durable et vise à allouer le capital vers des modèles économiques favorisant les enjeux environnementaux, tout en cherchant à générer des rendements à long terme. 
            Il met l’accent sur des secteurs comme la gestion durable des ressources, l'économie circulaire, les énergies renouvelables et l’efficacité énergétique.
            """
        },
        }
    # Sélection de l'obligation
    choix = st.radio("Sélectionnez un", list(fonds.keys()))
    symbole = fonds[choix]["ticker"]
    description = fonds[choix]["description"]

    if choix == "Mirova Environment Accelerating Capital":
        # Récupération des données financières

        # Section labels et stratégie
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Labels et certifications</b></td>
            <td style="padding: 10px;">
            - B-Corp<br>
            - Entreprise à mission<br>
            - Greenfin<br>
            - Article 9 (SFDR)
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Stratégie d'investissement</b></td>
            <td style="padding: 10px;">
            Investit dans des <b>technologies éprouvées</b> pour résoudre des problématiques environnementales telles que :
            <ul>
                <li>Le changement climatique</li>
                <li>La pollution de l'air, de l'eau et des sols</li>
                <li>La gestion des ressources naturelles</li>
            </ul>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Impact ESG</b></td>
            <td style="padding: 10px;">
            Suivi et <b>mesure systématique</b> des contributions :
            <ul>
                <li>Environnementales</li>
                <li>Sociales</li>
                <li>De gouvernance (ESG)</li>
            </ul>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Exemples d'entreprises</b></td>
            <td style="padding: 10px;">
            <ul>
                <li><b>Ombrea</b> : Agriculture durable par gestion intelligente de l’ombre et de la lumière</li>
                <li><b>Tallano Technologies</b> : Technologies de réduction des particules fines liées au freinage</li>
                <li><b>Naïo Technologies</b> : Robots agricoles autonomes et écologiques</li>
            </ul>
            </td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description)

    elif choix=="Mirova Europe Environnement" :
        # Récupération des données financières depuis Yahoo Finance
        yf_data = yf.download(symbole, start="2020-01-01", end="2024-12-31")

        # Extraction de la date et du cours ajusté
        df_plot = yf_data[["Adj Close"]].reset_index()
        df_plot.columns = ["Date", "Prix"]

        # Affichage du graphique
        st.subheader(f"Cours de {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours du fonds")
        st.plotly_chart(fig)

        # Section labels et stratégie
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Stratégie d’investissement</b></td>
            <td style="padding: 10px;">
            Investit dans des entreprises à <b>fort potentiel de croissance</b> et à <b>impact environnemental positif</b>,
            avec une référence à l’indice <b>MSCI Europe Net TR EUR</b>.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Conformité à l’<b>article 9</b> du SFDR<br>
            - <b>90%</b> des investissements sont considérés comme durables<br>
            - <b>14,5%</b> alignés sur la <b>taxonomie de l’UE</b>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance mesurée par rapport à l’indice <b>MSCI Europe</b><br>
            - Volatilité élevée<br>
            - Indice de risque : <b>6 sur 7</b>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Matériaux, industrie, énergie, santé, technologies<br>
            <b>Pays</b> : France, Allemagne, Espagne<br>
            <b>Zone</b> : Majoritairement Europe
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - <b>93%</b> des actifs visent à <b>réduire les émissions de gaz à effet de serre</b><br>
            - Focus sur la <b>biodiversité</b> et l’<b>accès à des services essentiels</b>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par <b>Mirova</b>, société spécialisée dans l’<b>investissement responsable et durable</b>.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Frais et commissions</b></td>
            <td style="padding: 10px;">
            - <b>Frais de gestion</b> : 0,90%<br>
            - <b>Commission de souscription</b> : jusqu’à 3%<br>
            - <b>Commission de surperformance</b> : 20%<br>
            - <b>Valorisation quotidienne</b>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description)

# -------------------------------
# ETF durables
# -------------------------------
#elif choix== "ETF durables":

# -------------------------------
# Startup verte
# -------------------------------

elif choix== "Startup verte":

#elif choix== "ETFs":


# -------------------------------
# INFOS FOOTER
# -------------------------------
st.sidebar.info("Ce dashboard présente les performances financières et les notations ESG des entreprises spécialisées dans le secteur de l'eau.")
st.markdown("---")
st.caption("© 2025 - Dashboard ESG | Streamlit prototype | Données fictives ou publiques.")
