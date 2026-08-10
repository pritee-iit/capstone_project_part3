import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(
    page_title="Heart Disease Dashboard",
    page_icon="❤️",
    layout="wide"
)

DATA_URL = (
    "clean_data.csv"
)

WEATHER_API = (
    "https://api.open-meteo.com/v1/forecast?latitude=53.3498&longitude=-6.2603&current=temperature_2m,wind_speed_10m"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # Keep original variables for dashbaord
    columns = ['age','sex','cp','trestbps', 'chol', 'fbs', 'restecg', 
               'thalach', 'exang', 'oldpeak', 'slope', 'ca','thal', 'target']

    df = df[columns].copy()

    # Target variable
    df["target_label"] = df['target'].map(
        {0:"No Heart Disease",1:"Heart Disease"}
    )

    # age group
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0,39,49,59,69,float("inf")],
        labels=["<40","40-49","50-59","60-69","70+"]
    )

    return df


@st.cache_data(ttl=600)

def get_weather():
    """Call REST API Live"""
    try:
        response = requests.get(WEATHER_API,timeout=10)
        response.raise_for_status()
        return response.json(),None
    except requests.RequestException as exc:
        return None,str(exc)

df = load_data()

st.title("❤️ Heart Disease Dashboard")
st.write(
    "Interactive exploration of 302-row Cleveland Heart Disease dataset."
)

# Sidebar filter
st.sidebar.header("Dashboard Filter")
age_options = ["All","Under 40","40-49","50-59","60+"]
selected_age = st.sidebar.selectbox("Select age group",age_options)

if selected_age == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["age_group"]==selected_age].copy()

# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Filtered Records",len(filtered_df))

with col2:
    disease_rate = filtered_df["target"].mean() * 100
    st.metric("Heart Disease Rate",f"{disease_rate:.1f}%")

with col1:
    st.metric("Average Age",f"{filtered_df['age'].mean():.1f} years")

st.divider()

# Live API
st.subheader("Live Dublin Weather")

weather_data, weather_error = get_weather()

if weather_data:
    current = weather_data["current"]
    w1,w2 = st.columns(2)

    with w1:
        st.metric(
            "Current Temperature",
            f"{current["temperature_2m"]} °C"
        )

    with w2:
        st.metric(
            "Wind Speed",
            f"{current["wind_speed_10m"]} km/h"
        )
else:
    st.warning(f"Weather API is temporarily unavailable:{weather_error}")

st.caption("Weather data by Open-Meteo.com (CC BY 4.0)")
st.divider()


#-----------------------------------
# Chart 1: Heart Disease Rate by sex
#-----------------------------------
st.subheader("1: Heart Disease Rate by sex")
sex_summary =(
    filtered_df.groupby("sex")["target"]
    .mean()
    .mul(100)
    .rename(index={0: "Female", 1: "Male"})
    .rename("Heart Disease Rate (%)")
)

st.bar_chart(sex_summary)



#-----------------------------------
# Chart 2: Heart Disease Rate by age
#-----------------------------------
st.subheader("1: Heart Disease Rate by sex")
age_summary =(
    filtered_df.groupby("age", observed=True)["target"]
    .mean()
    .mul(100)
    .sort_index()
    .rename("Heart Disease Rate (%)")
)

st.line_chart(age_summary)


#-----------------------------------
# Chart 3: Disease Vs No Disease
#-----------------------------------
st.subheader("1: Heart Disease Distribution")
target_counts =(
    filtered_df["target_label"]
    .value_counts()
    .reindex(["No Heart Disease", "Heart Disease"])
    .fillna(0)
)
fig,ax = plt.subplots(figsize=(6,4))
ax.pie(
    target_counts.values,
    labels=target_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
ax.set_title("Heart Disease vs No Heart Disease")
st.pyplot(fig,use_container_width=True)
plt.close(fig)

st.divider()

# Live filter Table
st.subheader("Filtered Data Table")
st.write(f"showing {len(filtered_df)} records for: **{selected_age}**")

display_columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "target_label"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Dataset : Heart Disease, "
    "using 302 rows"
)