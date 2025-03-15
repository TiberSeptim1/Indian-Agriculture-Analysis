import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

pd.set_option('display.float_format', '{:,.2f}'.format)

@st.cache_data
def loaddata():
    df = pd.read_csv("apy.csv")
    df.drop_duplicates(inplace=True)
    df.fillna(0, inplace=True)
    df["Crop_Year"] = df["Crop_Year"].astype(int)
    return df

df= loaddata()

df["Yield"] = df["Production"]/df["Area"]

st.title("Indian Agriculture Crop Analysis")

st.sidebar.header("Filter")

season_options = ["All Seasons"] + list(df["Season"].unique())

selected_state = st.sidebar.selectbox("Select a State", df["State_Name"].unique())
selected_season = st.sidebar.selectbox("Select a Season", season_options)

filtered_districts = df[df["State_Name"] == selected_state]["District_Name"].unique()
district_options = ["All Districts"] + list(filtered_districts)
selected_district = st.sidebar.selectbox("Select a District", district_options)


def recomd_crop(state, season, district):
    df2 = df[df["State_Name"]==state]

    if season != "All Seasons":
        df2 = df2[df2["Season"]==season]

    if district != "All Districts":
        df2 = df2[df2["District_Name"]==district]

    if not df2.empty:
        return df2.sort_values(by="Yield", ascending=False).iloc[0]["Crop"]
    else:
        return "No data avaliable of this selection"

recomded_crop = recomd_crop(selected_state,selected_season,selected_district)

df3 = df[df["State_Name"] == selected_state].copy()

if selected_season != "All Seasons":
    df3 = df3[df3["Season"] == selected_season]

if selected_district != "All Districts":
    df3 = df3[df3["District_Name"] == selected_district]



st.sidebar.write(f"{recomded_crop} is recommended for {selected_state},{selected_district} in {selected_season} season")

st.subheader(f"Top performing crops in {selected_state},{selected_district} in {selected_season} season")

top_crops = df3.groupby("Crop")["Yield"].mean().nlargest(5).reset_index()
fig= px.bar(top_crops,
            x="Crop",
            y="Yield",
            title=f"Top 5 crops in {selected_state}",
            labels={"Yield":"Yield(tons/hectare)"},
            color="Yield",
            color_continuous_scale="Viridis"

)

st.plotly_chart(fig)

Yearly_trend = df.groupby("Crop_Year")["Yield"].mean().reset_index()
fig2 = px.line(Yearly_trend,
               x="Crop_Year",
               y="Yield",
               title="Yearly Trend",
               labels={"Crop_Year":"Year"},
               markers=True,
               line_shape="spline",
               color="Yield")


st.plotly_chart(fig2)
