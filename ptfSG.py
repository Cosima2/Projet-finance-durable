import streamlit as st

st.set_page_config(layout="wide")
st.title("Investissement Socialement Responsable : Inclusion et Équité")
st.subheader("Portefeuille SG")

# ------------------ LES PROJETS ------------------
st.header("📌 Les Projets")

projets = [
    {
        "Nom": "I Was A Sari",
        "Description": "Emploi de femmes défavorisées via upcycling textile (Gucci Equilibrium)",
        "Type": "Insertion & Mode responsable",
    },
    {
        "Nom": "Simplon.co",
        "Description": "Formations gratuites aux métiers du numérique pour publics éloignés de l’emploi",
        "Type": "Éducation & Numérique",
    },
    {
        "Nom": "La Varappe",
        "Description": "Chantiers écologiques & BTP pour publics très éloignés de l’emploi",
        "Type": "Insertion sociale",
        "CA 2021": "66,5M€",
        "CA 2022": "87,4M€",
        "CA 2023": "90M€",
    },
    {
        "Nom": "OREADIS PRODUCTIONS",
        "Description": "Cinéma d’impact (ex : *Deux Semaines en Juin*, 2020)",
        "Type": "Culture & Sensibilisation",
    },
    {
        "Nom": "Axsol",
        "Description": "Mobilité & accessibilité pour PMR (CA: 2M€)",
        "Type": "Handicap & Santé",
    },
]

st.subheader("Les projets")
for i in range(0, len(projets), 3):
    cols = st.columns(3)
    for col, projet in zip(cols, projets[i:i+3]):
        with col.container():
            st.markdown(f"### {projet['Nom']}")
            st.caption(projet["Type"])
            with st.expander("Voir plus"):
                st.write(projet["Description"])
                if "CA 2021" in projet:
                    st.write(f"**CA 2021** : {projet['CA 2021']}")
                    st.write(f"**CA 2022** : {projet['CA 2022']}")
                    st.write(f"**CA 2023** : {projet['CA 2023']}")

# ------------------ LES FONDS À IMPACT ------------------
st.header("💼 Les Fonds à Impact")

fonds_impact = [
    {
        "Nom": "Fonds Mirova Insertion Emplois Dynamique",
        "Type": "Insertion & emploi",
        "Lien": "https://www.mirova.com/",
    },
    {
        "Nom": "Mirova Women Leaders and Diversity Equity",
        "Type": "Leadership féminin & diversité",
        "Lien": "https://www.mirova.com/en/funds/shares/3817/mirova-women-leaders-and-diversity-equity",
    },
    {
        "Nom": "Robeco Global Gender Equality Fund",
        "Type": "Égalité de genre mondiale",
        "Lien": "https://www.robeco.com/en-int/products/funds/isin-lu2145459850/robeco-global-gender-equality-ie-eur",
    },
]

for i in range(0, len(fonds_impact), 3):
    cols = st.columns(3)
    for col, fonds in zip(cols, fonds_impact[i:i+3]):
        with col.container():
            st.markdown(f"### {fonds['Nom']}")
            st.caption(fonds["Type"])
            with st.expander("Voir plus"):
                st.markdown(f"[Lien vers le fonds]({fonds['Lien']})")

# ------------------ LES OBLIGATIONS ------------------
st.header("🧾 Les Obligations")

obligations = [
    {
        "Nom": "Candriam Sustainable Bond Euro Corporate",
        "Description": "Fonds obligataire Euro d'entreprises ESG (Art. 9)",
        "Type": "Obligation verte / ESG",
    },
]

cols = st.columns(3)
for col, oblig in zip(cols, obligations):
    with col.container():
        st.markdown(f"### {oblig['Nom']}")
        st.caption(oblig["Type"])
        with st.expander("Voir plus"):
            st.write(oblig["Description"])

# ------------------ LES ACTIONS ------------------
# ------------------ LES ACTIONS ------------------
st.header("📈 Les Actions")

actions = [
    {
        "Nom": "Sodexo",
        "Type": "Services & Inclusion",
        "Description": """Leader mondial des services de qualité de vie, Sodexo est reconnu pour son engagement en faveur de l'inclusion et de la diversité.  
En 2023, l'entreprise a maintenu un score élevé de **91,90 %** dans le Workplace Pride Global Benchmark, soulignant ses efforts pour l'inclusion des personnes LGBTQ+.  
De plus, Sodexo a été classé **n°2 en 2019** parmi les sociétés françaises cotées en bourse pour la **mixité de ses équipes dirigeantes**, avec **35 % de femmes** au Comité Exécutif et **60 % au Conseil d'Administration**.
""",
    },
    {
        "Nom": "Capgemini",
        "Type": "Numérique & Inclusion sociale",
        "Description": """Capgemini se distingue comme un acteur engagé en matière d’inclusion sociale, intégrant pleinement la diversité, l’égalité des chances et l’insertion professionnelle dans sa stratégie RSE.  
Le groupe mène de nombreuses initiatives concrètes pour favoriser l’emploi de populations sous-représentées dans le secteur du numérique :
- Programmes de formation et reconversion vers les métiers du digital, souvent en partenariat avec des associations ou des écoles inclusives comme **Simplon.co**
- Politique proactive en faveur de la diversité, avec des **objectifs chiffrés** pour améliorer la représentation des femmes dans les fonctions techniques et managériales
- **Inclusion du handicap**, avec des dispositifs d’accompagnement à l’embauche et au maintien dans l’emploi
""",
    },
    {
        "Nom": "EssilorLuxottica",
        "Type": "Santé visuelle & Formation",
        "Description": """**ESG Risk Rating 16.9 – Low Risk (Morningstar)**  
Chez EssilorLuxottica, inclusion sociale et impact positif sont au cœur de la stratégie du Groupe.

**Quelques initiatives clés :**
- **Eyes on Inclusion** : programme de création d’un environnement professionnel inclusif et formateur
- **Programme Leonardo** : plateforme de formation ouverte à tout le secteur de l’optique, avec **5,5M d’heures de formation** déjà délivrées dans **30 langues**
- **OneSight EssilorLuxottica Foundation** (lancée en 2022) : plus grande fondation mondiale pour l’accès à la santé visuelle, visant à **éliminer les problèmes de vue évitables d’ici 2050**

Investir dans cette entreprise, c’est conjuguer performance économique et impact social, en donnant à des millions de personnes les moyens de mieux voir… et donc de mieux vivre.
""",
    },
    {
        "Nom": "Acer",
        "Type": "Tech inclusive & ESG",
        "Description": """Chez Acer, la performance ne se limite pas à l’innovation technologique. L’entreprise se distingue par un engagement en faveur d’une **croissance inclusive**, d’une **gouvernance exemplaire** et d’un **impact environnemental crédible**.

**Inclusion numérique** :
- Produits pensés pour l’accessibilité : seniors, étudiants défavorisés, personnes en situation de handicap
- Partenariats éducatifs & formations aux compétences numériques, notamment dans les régions sous-équipées

**Gouvernance** :
- Cadre ESG intégré à tous les niveaux décisionnels
- Normes internationales rigoureuses, alignées avec les recommandations de l’OCDE
- Transparence, politiques anticorruption, chaîne de valeur éthique

**Engagement environnemental** :
- Objectif de **neutralité carbone**
- Stratégie d’**éco-conception** et promotion du recyclage
- **Économie circulaire** dans le secteur électronique
""",
    },
    {
        "Nom": "France Active",
        "Type": "Finance solidaire / ESS",
        "Description": """France Active est un **mouvement associatif** qui soutient les entreprises et associations de l’**économie sociale et solidaire**, ainsi que les **entrepreneurs éloignés des banques**, via :
- Financements, accompagnement stratégique, et mise en réseau
- Un créateur / 2 accompagné est une **femme**

**Exemple : Natacha KANCEL**, responsable projet de **Drain’ailes** :  
→ Projet d’**agroforesterie** (cacao, vanille, café…), **agriculture biologique** en permaculture (maraîchage, arbres fruitiers…) et **agro-transformation** (sauces, assaisonnements, jus…)
""",
    },
]

for i in range(0, len(actions), 3):
    cols = st.columns(3)
    for col, action in zip(cols, actions[i:i+3]):
        with col.container():
            st.markdown(f"### {action['Nom']}")
            st.caption(action["Type"])
            with st.expander("Voir plus"):
                st.markdown(action["Description"])

