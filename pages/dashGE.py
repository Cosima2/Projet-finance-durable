import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Fonds ESG", layout="wide")

# -------------------------------
# TITRE 
# -------------------------------
st.title("Fonds d'investissement ESG : Donnez du sens à votre épargne")
st.markdown("Bienvenue dans notre univers d’investissement responsable !\n\n"
    "Découvrez comment notre portefeuille structuré selon des critères **ESG** (Environnement, Social, Gouvernance) vous permet d’allier performance financière et impact positif.\n\n"
    "Notre approche se décline en deux volets complémentaires :\n"
    "- **Une partie générale (45%)** : composée d’obligations, de fonds d'investissement et d’ETFs.\n"
    "- **Une partie spécifique (55%)** : concentrée sur des actifs projet, des obligations corporate, des ETFs et des actions sélectionnées selon la thématique qui vous tient le plus à coeur.\n\n"
    "**Investir autrement, c’est possible. Et ça commence ici.**")

# Données
composition_generale = {
    "Obligations gouvernementales": 20,
    "Fonds d'investissement": 20,
    "ETFs": 7,
    "Partie spécifique": 55,
}

df_generale = pd.DataFrame(list(composition_generale.items()), columns=["Actif", "Poids (%)"])

# Camembert avec style
fig_generale = px.pie(
    df_generale,
    values="Poids (%)",
    names="Actif",
    title="Répartition de notre portefeuille ESG",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Emrld
)

# Options de layout pour un rendu plus élégant
fig_generale.update_traces(textinfo='percent', pull=[0.05, 0.05, 0.05, 0.1])
fig_generale.update_layout(
    title_font_size=20,
    title_x=0.5,
    legend_title="Catégories d’actifs",
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
)

# Affichage
st.plotly_chart(fig_generale, use_container_width=True)

# -------------------------------
# PARTIE GÉNÉRALE
# -------------------------------
st.header("Partie Générale du Portefeuille (45%)")
st.subheader("Analyse des Actifs")
st.warning("Cette section présente la répartition des actifs dans le portefeuille général, qui est composé d'obligations, de fonds et d'ETFs.")

categorie_actifs_generale = ["Obligations gouvernementales", "Fonds d'investissement","ETFs"]
# Sélection de la catégorie d'actifs
choix = st.radio("Sélectionnez une catégorie d'actifs", categorie_actifs_generale)

st.markdown("---") 

# -------------------------------
# Obligations
# -------------------------------

if choix == "Obligations gouvernementales":

    st.markdown("""
    ### Critères de sélection des obligations souveraines

    Pour déterminer les États dans lesquels investir, nous avons appliqué une méthodologie rigoureuse basée sur deux grands axes : la qualité ESG des pays (selon des indicateurs de la Banque mondiale) et les rendements obligataires.

    Afin de simplifier l’univers d’investissement, seuls les pays membres de l’OCDE ont été retenus.

    **Indicateurs ESG de la Banque mondiale sélectionnés :**
    - **IC.BUS.EASE.XQ** : *Ease of doing business rank (1 = réglementations les plus favorables aux entreprises)*
    - **EG.FEC.RNEW.ZS** : *Part des énergies renouvelables (% de l'énergie totale)*
    - **CC.EST** : *Contrôle de la corruption*
    - **NY.GDP.PCAP.KD.ZG** : *Croissance annuelle du PIB par habitant (%)*
    - **EG.USE.COMM.FO.ZS** : *Consommation d’énergies fossiles (% de l’énergie totale)*
    - **FR.INR.RISK** : *Prime de risque sur les prêts (% au-dessus du taux des bons du Trésor)*

    **Méthodologie de construction du portefeuille souverain :**
    - **Critères d’inclusion** : bonne gouvernance, usage significatif d’énergies renouvelables, climat des affaires favorable, croissance stable.
    - **Critères d’exclusion** : forte dépendance aux énergies fossiles, prime de risque excessive (indiquant un risque de défaut élevé).
    - **Décision finale** : sélection des obligations souveraines avec le meilleur rendement fin 2024 et la volatilité la plus faible sur la période 2000–2024.
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
    st.markdown("Le Sustainable Development Report Score est un indicateur composite qui mesure les progrès d’un pays vers les " \
    "Objectifs de Développement Durable (ODD) définis par l’ONU. Il évalue la performance globale sur des critères environnementaux, sociaux et économiques, " \
    "avec un score allant de 0 à 100 — 100 représentant l’atteinte complète des ODD.")
    try:
        df_sdr = pd.read_csv("SDR-2024-overall-score.csv")
        st.dataframe(df_sdr.head(10))
    except:
        st.warning("Le fichier 'sdr_scores_avg.csv' est introuvable.")


    # ----------- PAYS INCLUS / EXCLUS
    st.subheader("Résultats de la sélection")
    st.markdown ("Choix des fichiers ayant les meilleures résultats sur les critères ESG et les rendements obligataires.")

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
    st.subheader("Analyse macro des obligations souveraines")

    # Rendements 2024
    st.markdown("Top 5 pays par rendement obligataire (déc. 2024)")
    try:
        df_yield = pd.read_csv("macro_data/obli_souveraines.csv", parse_dates=[0], index_col=0)
        df_2024 = df_yield[df_yield.index.year == 2024]
        derniers_taux = df_2024.iloc[-1]
        top5_yield = derniers_taux.sort_values(ascending=False).head(5)
        st.dataframe(top5_yield)
    except:
        st.warning("Erreur lors du chargement du fichier 'obli_souveraines.csv' pour les rendements.")

    # Volatilité
    st.markdown("Pays avec la volatilité obligataire la plus faible depuis 2000")
    try:
        volatilites = df_yield.std().sort_values()
        st.dataframe(volatilites.head(5))
    except:
        st.warning("Erreur lors du calcul de la volatilité obligataire.")

    # ------------------------------------------------------------
    # CONCLUSION
    # ------------------------------------------------------------
    st.subheader("Conclusion et sélection finale")
    st.markdown("""
    À partir de l’analyse croisée ESG et macro :
    - **Pays retenus** :  Canada, Costa Rica, Iceland, UK, Norway, Colombia car erformants sur les critères ESG **et** attractifs en termes de **rendement ou de stabilité des taux**.
    - L’objectif est de combiner **impact durable** et **performance financière mesurée**.
    """)

    obligations = {
        "Costa Rica": {
            "ticker": "CRIIRLTLT01STM",
            "description": """ Le Costa Rica est un modèle 
            en matière de développement durable et de réduction de la dépendance aux énergies fossiles, avec plus de 80% de son énergie provenant de sources renouvelables. 
            Le Costa Rica a également un excellent classement en termes de facilité de faire des affaires, ce qui témoigne de son environnement économique stable et favorable. 
            Le pays enregistre une croissance solide du PIB par habitant, avec une forte priorité donnée à la biodiversité et à la protection de l'environnement. 
            Le Costa Rica possède aussi une faible corruption, créant un environnement de confiance pour les investisseurs. Avec une prime de risque relativement faible et une politique ouverte à l'international."""
        },
        "Canada" : {
            "ticker": "IRLTLT01CAM156N",
            "description": """Le Canada se positionne comme un leader d'investissement avec un environnement économique stable et un système financier robuste. Le pays bénéficie d'une note favorable pour la facilité de faire des affaires 
            (classement 72) et offre une forte gouvernance en matière de contrôle de la corruption, avec un système judiciaire fiable et transparent. En matière de croissance du PIB par habitant, le Canada présente des chiffres solides, 
            bien que plus modérés que certains autres pays. En matière d'énergie renouvelable, le pays a fait d'importants progrès, bien que l'usage de l'énergie fossile reste élevé, ce qui limite l'impact écologique de certains investissements. 
            Cependant, les engagements du Canada envers les objectifs climatiques et l'infrastructure de l'énergie verte en font un acteur clé dans la transition énergétique. Le Canada possède également une faible prime de risque sur ses emprunts, 
            indiquant une stabilité économique appréciable.
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
            Le Royaume-Uni est également très impliqué dans la transition énergétique, avec des engagements forts en matière d'énergie verte. Son marché des obligations reste attractif, offrant une faible volatilité et des rendements intéressants.
            """
        },
        "Norway": {
            "ticker": "IRLTLT01NOM156N",
            "description": """La Norvège est un modèle de durabilité et d'engagement pour l'environnement. Le pays possède l'une des plus hautes proportions d'énergie renouvelable en Europe, représentant environ 61% de sa consommation totale d'énergie. 
            La Norvège affiche un très faible niveau de corruption et a un système économique transparent et stable. La croissance du PIB par habitant est robuste et soutenue, ce qui témoigne de la solidité de son économie. 
            En tant que l'un des plus grands producteurs de pétrole au monde, la Norvège s'efforce de diversifier son économie vers des investissements verts et des technologies durables. De plus, le pays maintient une faible prime de risque et une grande stabilité économique. 
            """
        },
        "Colombia": {
            "ticker": "COLIRLTLT01STM",
            "description": """La Colombie représente un marché émergent intéressant avec un grand potentiel de croissance économique. Avec une forte croissance du PIB par habitant (environ 4,62% par an), le pays connaît une expansion rapide de son secteur 
            des énergies renouvelables. Bien que la Colombie soit un pays en développement, elle a réussi à créer un environnement d'affaires relativement favorable avec un classement honorable en matière de facilité de faire des affaires. 
            En outre, la Colombie a effectué d'importants progrès dans la lutte contre la corruption. Ce pays offre une prime de risque faible, ce qui en fait un choix attractif pour les investisseurs cherchant à diversifier leur portefeuille. 
            Les obligations souveraines colombiennes présentent un bon compromis entre rendement élevé et stabilité, tout en soutenant les objectifs ESG grâce à un environnement réglementaire en amélioration continue.
            """
        },
    }

    st.markdown("---") 

    # Sélection de l'obligation
    st.warning("Choisissez un pays parmi la liste ci-dessous pour une analyse plus détaillée de l'obligation souveraine.")
    choix = st.radio("Sélectionnez une obligation", list(obligations.keys()))
    symbole = obligations[choix]["ticker"]
    description = obligations[choix]["description"]

    # Récupération des données financières
    csv_file = "macro_data/obli_souveraines.csv"
    df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
    df_plot = df[[symbole]].dropna().reset_index()
    df_plot.columns = ["Date", "Taux"]

        # Affichage du cours de l'obligation 10 ans
    st.subheader(f"Obligation souveraine du {choix}")
    fig = px.line(df_plot, x="Date", y="Taux", title=f"{choix} - Rendement obligataire 10 ans")
    st.plotly_chart(fig)
        # Affichage de la description ESG
    st.markdown("#### Pourquoi ce pays ?")
    st.info(description)


# -------------------------------
# Fonds à impact
# -------------------------------
elif choix== "Fonds d'investissement":
    st.markdown("""
    ### Critères de sélection des fonds d'investissement
    Afin de constituer un portefeuille de fonds d'investissement répondant à nos exigences strictes en matière d’investissement responsable, nous avons appliqué la méthode suivante : 
    **Méthodologie appliquée** :
    - **Critères d’inclusion** : Présence de labels reconnus (ISR, Greenfin, etc.), Conformité réglementaire, Classification **Article 9** selon la réglementation **SFDR**
    - **Critères d’exclusion** : Implication dans les énergies fossiles, entreprises controversées, absence de stratégie d’impact claire.
    - **Décision finale** : Sélection fondée sur la pertinence de la stratégie d’impact et la singularité du fonds dans son univers d’investissement.
    """)

    # ----------- Labels DATAFRAME
    st.subheader("Liste des fonds ayant le label Greenfin et le label ISR ")

    try:
        df_labels = pd.read_csv("Fonds_greenfin_ISR.csv")
        st.dataframe(df_labels)
    except:
        st.warning("Le fichier 'esg_oecd_worldbank.csv' est introuvable. Veuillez exécuter le script de récupération des données.")


    # ----------- Fonds INCLUS / EXCLUS
    st.markdown("Bien que possédant des labels ESG, il nous paraissait peu cohérent de sélectionner des fonds émis par des entreprises" \
    "comme Blackrock ou Vanguard qui sont des entreprises qui investissent massivement dans des actifs peu respectueux de l'environnement." \
    
    "Nous avons donc décidé de ne pas sélectionner ces fonds et il paraissait inévitable de chercher manuellement les fonds en épluchant les sites de certaines" \
    "sociétés prometteuses.")

    fonds_exclus = ["Blackrock", "Vanguard","Lyxor", "HSBC", "Natixis", "Société Générale"]
    st.error("Fonds exclus")
    st.write(fonds_exclus)

    fonds = {
        "Mirova Environment Accelerating Capital": {
            "ticker": "none",
            "description": """Le Mirova Environment Accelerating Capital (MEAC) est un fonds de Private Equity axé sur les entreprises innovantes répondants aux défis environnementaux mondiaux.
            Il investit dans des sociétés qui développent des solutions durables dans les domaines de l'énergie, de l'eau, des déchets et de l'agriculture."""
        },
        "Mirova Europe Environnement" : {
            "ticker": "0P0000G6X1.F",
            "description": """Le fonds Mirova Europe Environnement a pour objectif de soutenir des entreprises européennes qui s'engagent dans des solutions et services ayant un impact positif sur l'environnement. 
            Ce fonds s’inscrit dans une démarche d’investissement durable et vise à allouer le capital vers des modèles économiques favorisant les enjeux environnementaux, tout en cherchant à générer des rendements à long terme. 
            Il met l’accent sur des secteurs comme la gestion durable des ressources, l'économie circulaire, les énergies renouvelables et l’efficacité énergétique.
            """
        },
        "Echiquier Health Impact For All A": {
            "ticker": "0P0001IVQQ.F",
            "description": """Le fonds Echiquier Health Impact For All A se distingue par son approche résolument responsable et impactante dans le secteur de la santé. 
            Il s'engage pleinement dans la durabilité et l'impact positif, conformément aux objectifs de développement durable (ODD) des Nations Unies, en particulier en matière de santé et d'inclusion. 
            Ce fonds vise à financer des entreprises et des projets qui améliorent l'accès aux soins de santé, tout en générant un impact mesurable sur la société et l'environnement. Il bénéficie du Label ISR (Investissement Socialement Responsable), témoignant de son engagement à intégrer des critères environnementaux, sociaux et de gouvernance (ESG) dans ses décisions d’investissement.
            """
        },
        "Insertion Emplois Dynamiques Fonds Mirova": {
            "ticker": "0P0000KU3M.F",
            "description": """Le Fonds Insertion Emplois Dynamiques de Mirova, classé Article 9 du SFDR, est un investissement durable axé sur la création d'emplois et l'insertion professionnelle des populations vulnérables. 
            Ce fonds se distingue par son approche thématique, en sélectionnant des entreprises générant de la valeur à long terme tout en favorisant l’inclusion sociale. 
            Il alloue une portion de ses actifs à des entreprises solidaires non cotées, soutenant des initiatives pour l’insertion professionnelle des jeunes et des personnes handicapées.
            """
        },
        "LFR INCLUSION RESPONSABLE ISR": {
            "ticker": "0P0001HZQR.F",
            "description": """Le Fonds Inclusion : LFR Inclusion Responsable ISR est un fonds d'investissement durable classé Article 9 du SFDR. 
            Ce fonds soutient des entreprises promouvant la diversité, l'inclusion des populations défavorisées et l'égalité des chances, notamment pour les personnes handicapées et les jeunes en difficulté.
            Il se distingue par son engagement envers des politiques ESG axées sur l’inclusion sociale, l'égalité des genres et la création de conditions favorables à la participation active dans la société.
            """
        },
        "AXA WF ACT Green Bonds A Capitalisation EUR": {
            "ticker": "0P00016ZNX.F",
            "description": """Le fonds AXA WF ACT Green Bonds A Capitalisation EUR, classé Article 9 du SFDR, est un fonds axé sur la transition écologique. 
            Il investit principalement dans des green bonds et des obligations souveraines européennes, soutenant des projets ayant un impact environnemental positif. 
            Le fonds exclut les secteurs controversés comme les énergies fossiles et se concentre sur des initiatives contribuant à la lutte contre le changement climatique et la préservation de la biodiversité.
            """
        }
        }
    
    st.markdown("---") 

    # Sélection du fonds
    st.warning("Choisissez un fonds parmi la liste ci-dessous pour une analyse plus détaillée.")
    choix = st.radio("Sélectionnez un fonds d'investissement", list(fonds.keys()))
    symbole = fonds[choix]["ticker"]
    description1 = fonds[choix]["description"]

    if choix == "Mirova Environment Accelerating Capital":
        # Récupération des données financières
        st.markdown("Ce fonds étant un fonds de private equity, nous ne disposons pas de données financières en temps réel.")
        # Section labels et stratégie
        st.markdown("""
        ### Présentation du fonds : Mirova Environment Acceleration Capital (MEAC)
        
        Ce fonds étant un fonds de private equity, nous ne disposons pas de données financières en temps réel.

        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Stratégie d’investissement</b></td>
            <td style="padding: 10px;">
            Investit dans des entreprises innovantes apportant des solutions à la transition écologique, notamment dans la gestion des ressources naturelles, les agro-technologies, l'économie circulaire, l'énergie propre et les villes durables.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Investissement dans des entreprises innovantes œuvrant pour la transition énergétique et la durabilité.
            - Entreprises développants des solutions dans des secteurs clés tels que l'agriculture durable, la gestion des déchets, la construction écologique, la mobilité verte, et les technologies pour réduire l'empreinte carbone, avec un fort accent sur 
            l'utilisation de l'intelligence artificielle et de technologies propres.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Actifs sous gestion : 197 millions d'euros fin 2023<br>
            - Investissements réalisés dans cinq pays, avec quatre nouvelles entreprises ajoutées en 2023
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            - Présence dans cinq pays, y compris le Canada et les États-Unis<br>
            - Investissements dans des secteurs tels que l'agro-technologie, l'énergie propre et la gestion des ressources naturelles
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Soutien à des entreprises développant des solutions innovantes pour des défis environnementaux<br>
            - Engagement actif dans la promotion de la finance durable
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par Mirova, société spécialisée dans l’investissement responsable et durable, reconnue pour son approche proactive en matière d'impact.
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)

        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Greenfin": "Label français garantissant la contribution des fonds à la transition énergétique et écologique.",
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "B-Corp": "Certification pour les entreprises conciliant but lucratif et impact sociétal et environnemental positif."
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)

    elif choix=="Mirova Europe Environnement" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Investit dans des entreprises à fort potentiel de croissance< et à impact environnemental positif,
            avec une référence à l’indice MSCI Europe Net TR EUR.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - 90% des investissements sont considérés comme durables<br>
            - 14,5% alignés sur la taxonomie de l’UE<br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance mesurée par rapport à l’indice MSCI Europe<br>
            - Volatilité élevée<br>
            - Indice de risque : 6 sur 7
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
            - 93% des actifs visent à <b>réduire les émissions de gaz à effet de serre<br>
            - Focus sur la biodiversité et l’accès à des services essentiels
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par Mirova.
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


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Greenfin": "Label français garantissant la contribution des fonds à la transition énergétique et écologique.",
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "B-Corp": "Certification pour les entreprises conciliant but lucratif et impact sociétal et environnemental positif."
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")



        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)

    elif choix=="Echiquier Health Impact For All A" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Investit dans des entreprises améliorent l'accès aux soins de santé tout en ayant un impact environnemental positif,
            avec une référence aux indices 66.60% MSCI EUROPE HEALTHCARE NR, 33.40% MSCI WORLD HEALTHCARE NR USD (en EUR).
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - 98,1% des investissements sont considérés comme durables<br>
            - 47,2%des entreprises ont leurs objectifs de réduction des émissions de gaz à effet de serre sont validés par SBTI
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance mesurée par rapport à l’indice 66.60% MSCI EUROPE HEALTHCARE NR, 33.40% MSCI WORLD HEALTHCARE NR USD (en EUR)<br>
            - Volatilité élevée (~13%)<br>
            - Indice de risque : 4 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Santé, technologies (IT), matériaux<br>
            <b>Pays</b> : USA, Allemagne, Suisse, France <br>
            <b>Zone</b> : Mondial
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière d'inclusion sociale</b></td>
            <td style="padding: 10px;">
            - 93% des actifs visent à <b>réduire les émissions de gaz à effet de serre<br>
            - Focus sur la biodiversité et l’accès à des services essentiels
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par la Financière de l'Echéquier, société de Gestion d'actifs responsable</b>.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Frais et commissions</b></td>
            <td style="padding: 10px;">
            - <b>Frais de gestion</b> : 1,81%<br>
            - <b>Commission de souscription</b> : jusqu’à 3%<br>
            - <b>Commission de surperformance</b> : 15%<br>
            - <b>Valorisation quotidienne</b>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.title("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair."
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")



        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)

    elif choix=="Insertion Emplois Dynamiques Fonds Mirova" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "0P0000KU3M.F"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="0P0000KU3M.F", title=f"{choix} - Cours")
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
            Fonds axé sur la création d'emploiset l' insertion professionnelle des populations vulnérables,
            avec une référence aux indices 45% MSCI EUROPE EX FRANCE NET TR LOCAL INDEX 45% SBF 120 (C) DNR € 10% ESTR CAPITALISE.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - 90% des investissements sont considérés comme durables<br>
            - 2,5% alignés sur la taxonomie de l’UE
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance mesurée par rapport à l’indice 45% MSCI EUROPE EX FRANCE NET TR LOCAL INDEX 45% SBF 120 (C) DNR € 10% ESTR CAPITALISE<br>
            - Volatilité élevée (~15%)<br>
            - Indice de risque : 4 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Santé, technologies (IT), matériaux<br>
            <b>Pays</b> : USA, Allemagne, France <br>
            <b>Zone</b> : Mondial
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
                - Approche thématique axée sur les tendances à long terme et la création d'emplois durables<br>
                - Entre 5 % et 10 % du fonds alloués à une poche solidaire, en partenariat avec France Active<br>
                - Sélection d'entreprises ayant un impact social fort, notamment en faveur de l’insertion des personnes vulnérables
            </td>
        </tr>


        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par Mirova, société spécialisée dans l’investissement responsable et durable.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Frais et commissions</b></td>
            <td style="padding: 10px;">
            - <b>Frais de gestion</b> : 1,2%<br>
            - <b>Valorisation quotidienne</b>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.title("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "Finansol": "Le Label Finansol labellise des produits qui investissent dans des entreprises sociales non cotées."
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


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)

    elif choix=="LFR INCLUSION RESPONSABLE ISR" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "0P0001HZQR.F"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="0P0001HZQR.F", title=f"{choix} - Cours")
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
            Investit dans des valeurs de croissance de l'UE engagées en faveur de l'inclusion des personnes en situation de handicap et dans une démarche de développement durable,
            avec une référence à l'indice Euronstoxx 50 DNR.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - 76% des investissements sont signataires du Global Compact<br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance mesurée par rapport à l’indice Euronstoxx 50 DNR<br>
            - Volatilité élevée (~19%)<br>
            - Indice de risque : 5 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Industrie, consommation discrétionnaire, technologie, santé<br>
            <b>Pays</b> : France, Allemagne, Pays-bas <br>
            <b>Zone</b> : Europe
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de d'inclusion sociale</b></td>
            <td style="padding: 10px;">
            - 100% des entreprises ont fait appel à un ergonomiste pour l'accessibilité du lieu de travail <br>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par La Financière Responsable, société spécialisée dans l’investissement responsable et durable.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Frais et commissions</b></td>
            <td style="padding: 10px;">
            - <b>Frais de gestion</b> : 0,5%<br>
            - <b>Commission de souscription</b> : jusqu’à 6%<br>
            - <b>Commission de surperformance</b> : 25%<br>
            - <b>Valorisation quotidienne</b>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair."
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")



        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)

    elif choix=="AXA WF ACT Green Bonds A Capitalisation EUR" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "0P00016ZNX.F"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="0P00016ZNX.F", title=f"{choix} - Cours")
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
            Fonds axé sur la création d'emplois et l' insertion professionnelle des populations vulnérables,
            avec une référence à l'indice 100% ICE BofA Green Bond Hedged EUR.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - 90% des investissements sont considérés comme durables<br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance mesurée par rapport à l’indice 100% ICE BofA Green Bond Hedged EUR<br>
            - Volatilité faible (~5%)<br>
            - Indice de risque : 3 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Financier, industrie, quasi-souverain& gouvernement étranger, services publiques<br>
            <b>Pays</b> : France, Italie, USA <br>
            <b>Zone</b> : Mondial
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - 93% des actifs visent à réduire les émissions de gaz à effet de serre<br>
            - Focus sur la biodiversitéet l’accès à des services essentiels
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par Axa Management, société d'assurance française.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Frais et commissions</b></td>
            <td style="padding: 10px;">
            - <b>Frais de gestion</b> : jusqu'à 0,75%<br>
            - <b>Commission de souscription</b> : jusqu’à 3%<br>
            - <b>Commission de surperformance</b> : 15%<br>
            - <b>Valorisation quotidienne</b>
            </td>
        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Greenfin": "Label français garantissant la contribution des fonds à la transition énergétique et écologique.",
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "Towards Sustainability": "Le label Towards Sustainability garantit que le produit financier respecte des critères environnementaux, sociaux et de gouvernance stricts, tout en excluant certains secteurs controversés, afin d'assurer une approche durable, responsable et transparente de l'investissement."
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")



        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)

# -------------------------------
# ETF durables
# -------------------------------
elif choix== "ETFs":

    st.markdown("""
### Critères de sélection des ETFs

Dans une démarche de diversification de la partie générale de notre portefeuille, il nous a semblé essentiel d'inclure des **ETFs** en complément des fonds traditionnels. Les ETFs ne sont pas des instruments proposés par tous les établissements de gestion. Ainsi, leur disponibilité est plus limitée, notamment lorsqu'on impose des critères **ESG** élevés. 
Toutefois, certains ETFs proposent une concentration sectorielle pertinente ou un engagement particulièrement solide envers un projet durable. 

**Méthodologie appliquée** :

- **Critères d’inclusion** : 
  - Conformité aux **normes ESG** et présence de **labels reconnus** (ISR, Greenfin, etc.)
  - Conformité réglementaire, notamment la **classification Article 9 SFDR**
  - Alignement avec des **objectifs de développement durable** et des thématiques innovantes.

- **Critères d’exclusion** : 
  - **Implication dans les énergies fossiles** et les **secteurs controversés**
  - Absence de stratégie d’impact claire et mesurable.

- **Décision finale** : 
  - Sélection fondée sur l'**alignement stratégique** de l'ETF avec nos objectifs ESG, la **diversification du portefeuille** et la **pertinence de l'impact environnemental et social** visé.

Voici la sélection d'**ETFs** répondant à nos exigences et ayant gagné leur place dans notre portefeuille ESG. 
""")

    fonds = {
        "VanEck Bionic Engineering UCITS ETF": {
            "ticker": "CYBO.SW",
            "description": """Le VanEck Bionic Engineering UCITS ETF est un fonds d’investissement qui se concentre sur des 
            entreprises innovantes dans les secteurs des implants médicaux, des prothèses, de la bioprinting et de la préservation des organes, visant à améliorer la qualité de vie des populations vieillissantes et souffrant de déficiences fonctionnelles."""
        },
        "VanEck VanEck Circular Economy UCITS ETF": {
            "ticker": "REUS.L",
            "description": """L'ETF VanEck Circular Economy UCITS rassemble des entreprises mondiales engagées dans l'économie circulaire, en suivant l'indice MVIS Global Circular Economy ESG."""
        },
        "Invesco Solar Energy UCITS ETF": {
            "ticker": "ISUN.L",
            "description":"""L'Invesco Solar Energy UCITS ETF investit dans des entreprises du secteur de l'énergie solaire à l'échelle mondiale, en suivant la performance de l'indice MAC Global Solar Energy Index."""
        },
        "Invesco MSCI World ESG Climate Paris Aligned UCITS ETF":{
            "ticker": "PAWD.L",
            "description":"""L'Invesco MSCI World ESG Climate Paris Aligned UCITS ETF sélectionne des entreprises des marchés développés qui répondent à des critères environnementaux, sociaux et de gouvernance, en alignement avec les objectifs climatiques de l'Accord de Paris."""
        },
        "UBS ETF Euro Stoxx 50 ESG ECITS":{
            "ticker": "UET5.DE",
            "description": """L'UBS ETF Euro Stoxx 50 ESG UCITS investit dans les 50 principales entreprises de la zone euro, sélectionnées selon des critères environnementaux, sociaux et de gouvernance, en suivant l'indice EURO STOXX 50 ESG."""
        },
        "Franklin Sustainable Euro Green Sovereign UCITS ETF": {
            "ticker": "GSOV.DE",
            "description": "Le fonds a pour objectif d'offrir une exposition aux obligations souveraines vertes libellées en euros, émises par des gouvernements européens engagés dans des projets ayant des avantages environnementaux positifs."
        },
        "Guinness Sustainable Energy UCITS ETF": {
            "ticker": "CLMA.MI",
            "description": """L'ETF Guinness Sustainable Energy UCITS est un fonds activement géré qui vise à offrir une croissance du capital à long terme en investissant dans des entreprises mondiales engagées dans la génération et le stockage d'énergie durable, ainsi que dans l'électrification et l'efficacité énergétique, tout en excluant les sociétés impliquées dans l'extraction de pétrole, de gaz naturel et de charbon."""
        }
        }
        


    st.markdown("---") 
    st.warning("Choisissez un ETF parmi la liste ci-dessous pour une analyse plus détaillée.")
    # Sélection du fonds
    choix = st.radio("Sélectionnez un ETF", list(fonds.keys()))
    symbole = fonds[choix]["ticker"]
    description1 = fonds[choix]["description"]

    if choix=="VanEck Bionic Engineering UCITS ETF" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Investit dans des sociétés à la pointe de la biotechnologie et des technologies médicales, respectant des critères ESG élevés,
            avec une référence à l’indice MVIS Global Bionic Healthcare ESG Index.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - 90% des investissements sont considérés comme durables<br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance mesurée par rapport à l’indice MVIS Global Bionic Healthcare ESG Index<br>
            - Volatilité faible<br>
            - Indice de risque : 6 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : santé, technologies<br>
            <b>Pays</b> : USA, Suisse, Australia <br>
            <b>Zone</b> : Majoritairement USA
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Focus sur les avancées technologiques ayant un impact positif sur la santé et le bien-être des individus
            - Exclusion automatique des entreprises impliquées dans des secteurs controversés<br>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par VanEck, spécialiste des stratégies d'investissement intelligentes et prospectives.
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


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "ISR": "Label Investissement Socialement Responsable pour les fonds intégrant des critères ESG dans leur gestion.",
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)





    elif choix=="VanEck VanEck Circular Economy UCITS ETF" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Le fonds investit dans des entreprises générant au moins 50 % de leurs revenus dans des secteurs liés à l'économie circulaire, tels que le recyclage, la gestion des déchets et la purification de l'eau.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Soutien à des pratiques de production et de consommation durables <br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance en YTD : 0,51% <br>
            - Principaux risques : concentration sectorielle, risque lié au marché actions <br>
            - Indice de risque : 4 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : industrie, matériaux, consommation <br>
            <b>Pays</b> : Diversifié, avec accent sur les États-Unis  <br>
            <b>Zone</b> : Diversifié
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Promotion et engagement vers l'économie circulaire 
            - Objectif d'investissement durable au sens de l'article 9 SFDR <br>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par VanEck, spécialiste des stratégies d'investissement intelligentes et prospectives.
            </td>
        </tr>

        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)




    elif choix=="Invesco Solar Energy UCITS ETF" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Le fonds investit dans des entreprises impliquées dans la production, le stockage et la distribution d'énergie solaire, en répliquant la performance de l'indice MAC Global Solar Energy Index.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Soutien à des pratiques durables de production d'énergie (solaire) <br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance en YTD : -8,86% (en lien avec l'indice de référence) <br>
            - Principaux risques : concentration sectorielle <br>
            - Indice de risque : 6 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : technologies, industrie, services publics <br>
            <b>Pays</b> : Diversifié, avec accent sur les États-Unis  <br>
            <b>Zone</b> : Diversifié
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Contribution à la transition énergétique (éolien)
            - Exclusions sectorielles des secteurs controversés 
            - Prise en compte de facteurs durables au sens de l'article 8 SFDR <br>
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par VanEck, spécialiste des stratégies d'investissement intelligentes et prospectives.
            </td>
        </tr>

        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Article 8 (SFDR)": "Le fonds promeut des caractéristiques environnementales ou sociales.",
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)




    elif choix=="Invesco MSCI World ESG Climate Paris Aligned UCITS ETF" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Le fonds investit dans des entreprises des marchés développés qui répondent à des critères ESG stricts, en suivant l'indice MSCI World ESG Climate Paris Aligned Benchmark Select Index. 
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Suivi strict de l'indice de référence, en accord avec les objectifs de l'Accord de Paris
            - Objectifs de transition énergétiques et de réduction des émissions carbone <br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance en YTD : -2,53% (en lien avec l'indice de référence) <br>
            - Performance depuis la création : 7,5%
            - Principaux risques : risque de marché <br>
            - Indice de risque : 4 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : technologies, services financiers <br>
            <b>Pays</b> : États-Unis  <br>
            <b>Zone</b> : Diversifié
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Contribution à la transition énergétique en lien avec l'Accord de Paris 
            - Engagements durables dans les secteurs financés 
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par Invesco, société de gestion d'investissements reconnue.
            </td>
        </tr>

        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)



    elif choix=="UBS ETF Euro Stoxx 50 ESG ECITS" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Le fonds réplique de manière passive la performance de l'indice EURO STOXX 50® ESG Index (Net Return), qui inclut les 50 principales entreprises de la zone euro, sélectionnées sur la base de critères ESG stricts. 
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Proportion minimale de placements durables 
            - Exclusions sectorielles de secteurs controversés (armement, tabac, charbon thermique) <br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance en YTD : -3,96% (en lien avec l'indice de référence) <br>
            - Principaux risques : risque de marché <br>
            - Indice de risque : 4 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Diversifié <br>
            <b>Pays</b> : Zone Euro  <br>
            <b>Zone</b> : zone Euro
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Prise en compte des scores ESG des entreprises dans la stratégie d'investissement via l'indice référent 
            - Objectif de réplication d'un indice visant des entreprises aux scores ESG meilleurs que l'indice parent    
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par UBS, gestion passive.
            </td>
        </tr>

        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Article 8 (SFDR)": "Le fonds promeut des caractéristiques environnementales ou sociales par l'utilisation d'un indice ESG.",
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)




    elif choix=="Franklin Sustainable Euro Green Sovereign UCITS ETF" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Le Fonds vise à contribuer aux objectifs environnementaux en assurant une exposition principalement au marché européen des obligations souveraines vertes tout en optimisant le rendement total. 
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Financement de projets ayant des implications environnementales positives 
            - Minimum de 90% des actifs nets dans des investissements durables
            - Obligations considérés comme contribuant à réduire ou éliminer les émissions de carbone <br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Performance en YTD : +3,69%  <br>
            - Principaux risques : risque de taux <br>
            - Indice de risque : 3 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : obligations vertes souveraines <br>
            <b>Pays</b> : principalement Allemagne, Autriche  <br>
            <b>Zone</b> : zone Euro
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Intégration des critères ESG dans la sélection des titres (obligations dites "vertes")
            - Exclusions sectorielles des secteurs controversés  
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par Franklin Templeton de façon active.
            </td>
        </tr>

        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
            "Towards Sustainability" : "Label de la Central Labelling Agency (CLA) en Belgique, certifiant le respect de critères stricts en matière de durabilité, et s'assurant des bénéfices environnementaux positifs des financements."
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)


    elif choix=="Guinness Sustainable Energy UCITS ETF" :
        # Récupération des données financières
        csv_file = "financial_data/data_actifs.csv"
        df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
        df_plot = df[[symbole]].dropna().reset_index()
        df_plot.columns = ["Date", "Prix"]

            # Affichage du cours du fonds
        st.subheader(f"Cours du fonds {choix}")
        fig = px.line(df_plot, x="Date", y="Prix", title=f"{choix} - Cours")
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
            Ce fonds investit activement dans des entreprises des secteurs de l'énergie durable et des technologies énergétiques, incluant des sociétés impliquées dans le solaire, l'éolien, l'hydroélectrique, la géothermie, les biocarburants et l'efficacité énergétique. 
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            - Financement de la transition vers des systèmes énergétiques durables 
            - Soutien à l'innovation technologique 
            - Contribution au développement des énergies renouvelables <br>
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performance et risque</b></td>
            <td style="padding: 10px;">
            - Volatilité élevée <br>
            - Principaux risques : risque de concentration <br>
            - Indice de risque : 5 sur 7
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Répartition sectorielle et géographique</b></td>
            <td style="padding: 10px;">
            <b>Secteurs</b> : Équipements, véhicules électriques <br>
            <b>Pays</b> : Principalement États-Unis, Europe  <br>
            <b>Zone</b> : Diversifié
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Engagement en matière de développement durable</b></td>
            <td style="padding: 10px;">
            - Soutien aux projets liés à la transition énergétique
            - Contribution à la décarbonation des zones financées 
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Structure et gestion</b></td>
            <td style="padding: 10px;">
            Géré par Guinness Asset Management de façon active.
            </td>
        </tr>

        </tr>

        </table>
        """, unsafe_allow_html=True)


        st.subheader("Labels d'investissement responsable")

        # Dictionnaire des labels avec descriptions
        labels = {
            "Article 9 (SFDR)": "Catégorie de la réglementation SFDR pour les fonds qui ont un objectif d’investissement durable clair.",
        }

        # Initialisation des états de clic
        for label in labels:
            if f"show_{label}" not in st.session_state:
                st.session_state[f"show_{label}"] = False

        # Affichage des boutons et description dynamique
        for label, description in labels.items():
            if st.button(label):
                st.session_state[f"show_{label}"] = not st.session_state[f"show_{label}"]

            if st.session_state[f"show_{label}"]:
                st.success(f"**{label}** : {description}")


        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce fonds ?")
        st.info(description1)


# -------------------------------
# NAVIGATION ENTRE PAGES
# -------------------------------
st.markdown("---")
st.subheader("Choisissez votre thématique d'investissement")

# Options de navigation sans la page générale
options_pages = {
    "Investissement Écologique": "dashEG",  # Correspond à pages/dashEG.py
    "Investissement Social": "dashSG",      # Correspond à pages/dashSG.py
    "Investissement en Europe": "dashES"    # Correspond à pages/dashES.py
}

# Création des colonnes pour organiser les boutons
cols = st.columns(len(options_pages))

for i, (nom_page, fichier_page) in enumerate(options_pages.items()):
    with cols[i]:
        if st.button(nom_page, use_container_width=True):
            st.switch_page(f"pages/{fichier_page}.py")


# -------------------------------
# INFOS FOOTER
# -------------------------------
st.sidebar.info("Ce dashboard présente les performances financières et les évaluations ESG des actifs séléctionnées par notre fonds.")
st.markdown("---")
st.caption("© 2025 - Dashboard ESG_Reghina&Coline&Cosima | Streamlit prototype | Projet Finance Durable")
