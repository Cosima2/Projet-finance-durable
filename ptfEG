import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# TITRE ET INTRODUCTION
# -------------------------------
st.set_page_config(page_title="Partie spécifique thématique EG", layout="wide")

st.title("Fonds d'investissement ESG")
st.markdown(
    "Trouvez ici les explications liées à la composition de notre portefeuille structuré selon les critères ESG. "
    "Notre portefeuille se divise en deux parties : une **partie générale** et une **partie spécifique**. \n\n"
    "- La partie générale est composée de **45%** d'obligations, de fonds à impact, d'ETF durables et de crypto verte.  \n"
    "- La partie spécifique représente **55%** du portefeuille et est composée d'actions, de fonds, d'ETFs et d'actifs projet, "
    "se concentrant sur les thèmes de la **protection de l'environnement et le dynamisme économique à l'échelle européenne.**"
)


# -------------------------------
# VISUALISATION DE LA RÉPARTITION SPÉCIFIQUE
# -------------------------------
st.header("Composition de la partie spécifique liée à la protection de l'environnement et le dynamisme économique à l'échelle européenne")

composition_spe = {
    "Non coté": 3,
    "Obligations Corporate": 2,
    "Fonds à Thématique EG": 7,
    "Actions Durables EG": 6
}
df_generale = pd.DataFrame(list(composition_spe.items()), columns=["Actif", "Poids (%)"])
fig_generale = px.pie(df_generale, values="Poids (%)", names="Actif", title="Répartition des actifs de la partie spécifique")
st.plotly_chart(fig_generale, use_container_width=True)

# -------------------------------
# DÉTAIL DES ACTIFS SPÉCIFIQUES
# -------------------------------
st.header("Analyse détaillée de la partie spécifique (55%)")
st.write(
    "Cette section présente la répartition détaillée des actifs composant la partie spécifique du portefeuille liée à la thématique EG. "
    "Les actifs sont sélectionnés selon leur impact environnemental positif et leur lien direct avec la protection de l'environnement, dans son ensemble, ou la mise en place de mesures efficaces pour soutenir l'économie européenne."
)

categorie_actifs_spe = list(composition_spe.keys())
choix = st.radio("Sélectionnez une catégorie d'actifs", categorie_actifs_spe)


# -------------------------------
#   ‼️ NON COTÉ ‼️
# -------------------------------
if choix == "Non coté":

    entreprises_projet = {
        "Patagonia": {
            "ticker": "?",
            "description": """Patagonia est une entreprise de vêtements et d'équipements de plein air fondée en 1973, reconnue pour son engagement en faveur de l'environnement. Elle se distingue par l'utilisation de matériaux durables et recyclés, comme le polyester recyclé pour ses vestes et le coton organique pour ses vêtements, afin de réduire son empreinte écologique. En parallèle, son programme Worn Wear encourage la réparation et la réutilisation des produits, permettant ainsi d’allonger leur durée de vie et de diminuer la consommation de nouvelles ressources. Cette approche soutient un modèle de consommation circulaire qui s’intègre parfaitement dans une démarche durable, permettent à Patagonia de s’inscrire dans un portefeuille d'investissement éthique et responsable. """
        },
        "Néolithe" : {
            "ticker": "?",
            "description": """Néolithe est une start-up française fondée en 2019, qui révolutionne la gestion des déchets grâce à une innovation de taille : la Fossilisation Accélérée®, un procédé unique qui transforme les déchets non-recyclables en granulats minéraux pour la construction. Cette technique permet de substituer l'enfouissement et l'incinération, deux pratiques fortement polluantes, par une solution durable qui séquestre le carbone. En réutilisant ces granulats dans la fabrication de bétons à faible empreinte carbone, Néolithe contribue activement à la décarbonation du secteur du BTP. Cette approche novatrice ouvre la voie à une gestion des déchets plus écologique et s’inscrit dans un modèle circulaire porteur d’avenir.
            """
       
        },
        "Prometeia": {
            "ticker": "?",
            "description": """Prometeia est une entreprise italienne fondée en 1974, spécialisée dans les services de conseil financier, les solutions technologiques et la recherche économique. Elle accompagne les entreprises dans l'intégration des risques climatiques, en proposant des outils d'analyse avancés pour évaluer l'impact des risques physiques et de transition liés au changement climatique sur leurs activités. Par exemple, l'outil Nature-Retaled Risk (NRR) aide les clients à comprendre comment les bilans de leurs entreprises peuvent être affectés par leurs interactions et dépendances au capital naturel."""
        }
        }

    # Sélection de l'actif projet
    choix = st.radio("Sélectionnez un", list(entreprises_projet.keys()))
    symbole = entreprises_projet[choix]["ticker"]
    description = entreprises_projet[choix]["description"]


#PATAGONIA 


    if choix == "Patagonia":

        # Section labels et stratégie
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Stratégie de l'entreprise</b></td>
            <td style="padding: 10px;">
             Patagonia adopte une stratégie axée sur la durabilité en utilisant des <b>matériaux recyclés<b>, en soutenant <b>l'économie circulaire<b> et en favorisant la <b>réparabilité<b> de ses produits.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            L'entreprise s'engage à <b>réduire son empreinte carbone<b>, à <b>reverser 1% de ses ventes annuelles à des initiatives environnementales<b> et à promouvoir des pratiques commerciales <b>équitables<b>.
            </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performances et risques</b></td>
            <td style="padding: 10px;">
            En 2022, </b>96 %</b> de ses produits étaient fabriqués sans produits chimiques nocifs et 85 % étaient certifiés commerce équitable.
            Les risques principaux sont liés aux défis de </b>gestion des ressources naturelles</b> dans les chaînes d'approvisionnement.
            </td>
        </tr>
                    
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Actualités</b></td>
            <td style="padding: 10px;">
            "La Terre est maintenant notre seul actionnaire.", Yvon Chouinard, cofondateur de Patagonia, 2022. Cette déclaration, réalisée après avoir cédé l'entreprise à une fondation dédiée à la conservation de la planète, signifie que les profits seront désormais utilisés pour préserver les écosystèmes plutôt que de maximiser les rendements financiers, soulignant le modèle unique et éthique.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Coup de coeur de la gestion</b></td>
            <td style="padding: 10px;">
            Sur son site, Patagonia met en avant et invite à rejoindre des <b>projets de terrain<b> visant à protéger l'environnement et offre la possibilité à ses clients de <b>faire des dons<b> pour soutenir des initiatives écologiques à travers sa fondation.
            </td>
        </tr>
            
        </tr>


        </table>
        """, unsafe_allow_html=True)

        st.title("Labels d'investissement responsable")

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
                st.markdown(f"**{label}** : {description}")

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.write(
        "Patagonia n'est pas seulement une marque de vêtements de plein air, c'est un véritable modèle d'entreprise engagée, alliant performance économique et responsabilité écologique. Son approche innovante, qui intègre la durabilité à chaque étape de la production, ainsi que ses actions concrètes en faveur de la planète, en font un exemple à suivre dans l'industrie. En cédant ses actions à une fondation dédiée à la protection de la Terre et en soutenant des projets de terrain, Patagonia montre qu'il est possible d'être profitable tout en contribuant activement à la préservation de l'environnement. Son modèle, centré sur l'économie circulaire, la transparence et la justice sociale, offre une vision prometteuse pour un avenir plus durable, et c'est cette approche qui justifie qu'on s'y intéresse, bien au-delà de la simple consommation de produits."
        )

    elif choix == "Néolithe":

        # Section labels et stratégie
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Stratégie de l'entreprise</b></td>
            <td style="padding: 10px;">
            Néolithe transforme les déchets non-recyclables en granulats minéraux pour le BTP grâce à son procédé breveté de Fossilisation Accélérée®, offrant une alternative circulaire à l'enfouissement et à l'incinération.            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
            L'entreprise vise à réduire l'empreinte carbone de la gestion des déchets en séquestrant le CO₂ dans ses granulats, contribuant ainsi à la décarbonation du secteur du BTP.             </td>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performances et risques</b></td>
            <td style="padding: 10px;">
            Néolithe a levé plus de 80 millions d'euros pour financer l'industrialisation de sa technologie et prévoit l'ouverture de nouvelles usines en France, avec une capacité de traitement de 100 000 tonnes de déchets par an.            </td>
        </tr>
                    
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Actualités</b></td>
            <td style="padding: 10px;">
            Néolithe a récemment été reconnue parmi les "100 start-up où investir" par le magazine Challenges, soulignant son potentiel d'innovation et d'impact environnemental. ​
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Coup de coeur de la gestion</b></td>
            <td style="padding: 10px;">
            L'innovation technique est au coeur de l'ADN de l'entreprise : Néolithe a été cofondée en 2019 par Nicolas Cruaud, ingénieur diplômé de l'École Polytechnique, et son père William Cruaud, tailleur de pierre de métier.          </td>
        </tr>
            
        </tr>


        </table>
        """, unsafe_allow_html=True)

        st.title("Labels d'investissement responsable")

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
                st.markdown(f"**{label}** : {description}")

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.write(
        "En contribuant à la décarbonation du secteur du BTP, Néolithe ouvre la voie à une économie circulaire et offre une solution concrète aux défis environnementaux. Son modèle prometteur, à la fois rentable et responsable, fait de Néolithe une entreprise à suivre de près et un investissement stratégique pour un avenir durable."        
        )


    elif choix == "Prometeia":

        # Section labels et stratégie
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color:#f2f2f2;">
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Catégorie</th>
            <th style="padding: 10px; text-align:left; border-bottom: 1px solid #ddd;">Détails</th>
        </tr>

        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Stratégie de l'entreprise</b></td>
            <td style="padding: 10px;">
        Prometeia aide les entreprises à intégrer les risques climatiques pour optimiser leur stratégie, performances, conformité et gestion des risques.
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Objectifs durables</b></td>
            <td style="padding: 10px;">
        L'entreprise soutient des initiatives visant à améliorer l'efficacité des ressources et réduire les émissions de CO₂, contribuant aux Objectifs de Développement Durable.        </tr>
        <tr>
            <td style="padding: 10px; vertical-align: top;"><b>Performances et risques</b></td>
            <td style="padding: 10px;">
        En 2023, Prometeia a souligné la résilience de l'industrie italienne, soutenue par des investissements stratégiques et l'innovation, malgré un ralentissement économique.

        </tr>
                    
        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Actualités</b></td>
            <td style="padding: 10px;">
            Prometeia continue de renforcer sa position avec des rapports sectoriels et des initiatives pour soutenir le développement économique durable.
            </td>
        </tr>

        <tr style="background-color:#f9f9f9;">
            <td style="padding: 10px; vertical-align: top;"><b>Coup de coeur de la gestion</b></td>
            <td style="padding: 10px;">
        Prometeia développe ses stratégies de conseil en s'appuyant sur un travail de recherche économique interne approfondi, lui permettant d’offrir des solutions adaptées et innovantes aux entreprises.        </tr>
            
        </tr>


        </table>
        """, unsafe_allow_html=True)

        st.title("Labels d'investissement responsable")

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
                st.markdown(f"**{label}** : {description}")

        # Affichage de la description ESG
        st.markdown("#### Pourquoi ce projet ?")
        st.write(
        "Soutenir Prometeia, c'est parier sur une entreprise qui combine expertise en conseil stratégique, recherche économique interne et capacité à aider les entreprises à naviguer dans les défis financiers et environnementaux, en offrant des solutions durables et adaptées aux enjeux de demain."
        )
