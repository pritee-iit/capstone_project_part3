# Heart Disease Dataset - Streamlit Dashboard

An interactive Dashoboard build using Streamlit

# Project Overview
 This Dashbaord allows users to explore heart disease patterns by selecting an age group. Selected age group changes all three charts and data table.

# Dashboard Features
- interactive selectbox for age group
- Three charts
1. Heart disease rate by sex
2. Heart disease rate by age
3. Heart disease vs. no heart disease distribution
- Live API shows current temperature and wind speed.

# Dataset
- Dataset shape : [302 rows x 14 columns]
- The main clinical columns used are:

- `age`
- `sex`
- `cp`
- `trestbps`
- `chol`
- `fbs`
- `restecg`
- `thalach`
- `exang`
- `oldpeak`
- `slope`
- `ca`
- `thal`
- `target`
- The target is interpreted as:

- `0` = No Heart Disease
- `1` = Heart Disease

## External REST API

- The dashboard integrates the **Open-Meteo** weather API.
- JSON response diaplay current temperature and wind speed on dashboard.
- No API key,signup required.
- Weather data by Open-Meteo.com (CC BY 4.0).


## 5. Run requirements.txt

1) install dependencies:
```bash
pip install -r requirements.txt
streamlit run app.py
```
## 6. Streamlit dashboard link
https://capstoneprojectpart3-xcmuwzdc6d3vslydqclqnh.streamlit.app/