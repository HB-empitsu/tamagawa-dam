import pandas as pd
import plotly.express as px

import streamlit as st


@st.cache_data()
def load_data():
    df = pd.read_csv("19710401-20241006.csv", parse_dates=["date"])

    df["year"] = df["date"].dt.year
    df["month_day"] = df["date"].dt.strftime("%m-%d")

    pv = df.pivot(index="month_day", columns="year", values="rate")

    pv["平均"] = pv.iloc[:, :-1].mean(axis=1)

    pv.index = pd.to_datetime(pv.index, format="%m-%d")

    return pv


st.set_page_config(
    page_title="玉川ダム　貯水率", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None
)
st.title("玉川ダム　貯水率")

df = load_data()

options = df.columns.to_list()
default = [1994] + options[-5:]

chois = st.multiselect(
    "年を選んでください", options, default=default, max_selections=10, placeholder="年を選んでください"
)


if chois:
    filtered_df = df[chois].copy()
else:
    filtered_df = df.copy()

fig = px.line(filtered_df)

for date in filtered_df[filtered_df.index.day == 1].index:
    fig.add_vline(x=date, line=dict(color="gray", width=1, dash="dot"), opacity=0.5)


fig.update_layout(
    height=600,
    xaxis_title=None,
    yaxis_title=None,
    xaxis=dict(tickformat="%m/%d", tickmode="auto", ticklabelmode="period"),
    yaxis=dict(
        range=[0, 105],
        tickvals=list(range(10, 105, 10)),
    ),
)

st.plotly_chart(fig, use_container_width=True)
