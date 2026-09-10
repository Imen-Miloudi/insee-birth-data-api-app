import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from handler import AppHandler


# Création du handler
handler = AppHandler()


# Titre
st.title("Évolution des naissances par département")


# Récupération des départements
departments = handler.get_departments()


# Sélection du département
dep = st.selectbox(
    "Sélectionnez un département",
    departments
)

dep_code = dep.replace("2025-DEP-", "")


# Récupération des naissances
births = handler.get_births_by_department(dep_code)

df = pd.DataFrame(births)


# Conversion de la période en date
df["period"] = pd.to_datetime(df["period"])

# Tri chronologique
df = df.sort_values("period")


# Affichage du tableau
st.dataframe(df)


# Création du graphique
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["period"],
        y=df["births"],
        mode="lines+markers",
        name="Naissances",
        fill="tozeroy"
    )
)


# Mise en forme
fig.update_layout(
    title=f"Évolution des naissances - département {dep_code}",
    xaxis_title="Période",
    yaxis_title="Nombre de naissances",
    hovermode="x unified",

    xaxis=dict(
        rangeslider=dict(
            visible=True
        )
    )
)


# Affichage dans Streamlit
st.plotly_chart(
    fig,
    use_container_width=True
)