import streamlit as st

pages = {
    "Investir avec nous": [
        st.Page("dashGE.py", title="Général"),
        st.Page("dashSG.py", title="Investissement Socialement Responsable : Inclusion et Équité"),
        st.Page("dashES.py", title="Investissement Écologiquement Responsable : Eau"),
        st.Page("dashEG.py", title="Investissement Ethique : Investir en Europe"),
    ]
    #"Resources": [
        #st.Page("learn.py", title="Learn about us"),
        #st.Page("trial.py", title="Try it out"),
    #],
}

pg = st.navigation(pages)
pg.run()