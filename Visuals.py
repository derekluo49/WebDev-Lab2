# This creates the page for displaying data visualizations.
import json
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
with open("data.json", "r") as f: #Loading the data from the data.json file
    jsonData = json.load(f)
dfJson = pd.DataFrame(jsonData["data_points"])#Convert json data into pandas form and sort by visitors
st.subheader("All 63 U.S National Parks Map")
st.write("This map displays the geographic locations of all 63 national parks"
         "Hover over each park to see the amount of visitors.")
parkMap = px.scatter_geo(
    dfJson,
    lat='lat',
    lon='lon',
    size='value',
    color='value',
    hover_name='label',
    scope='usa',
    title='All 63 U.S. National Parks Visitor Map',
    labels={'value': 'Annual Visitors'},
)
parkMap.update_layout(height=600, margin={'r': 0, 't': 40, 'l': 0, 'b': 0})

st.plotly_chart(parkMap)
st.markdown('---')
st.subheader("Interactive Visitor Bar Chart")
st.write("Use the slider to filter the parks by visitor count")
if "minVisitors" not in st.session_state:
    st.session_state.minVisitors = 2000000
allStates = sorted(dfJson["state"].unique())
if "selectedStates" not in st.session_state:
    st.session_state.selectedStates = allStates
minVisitorsLimit = st.slider(
    'Minimum annual visitors:',
    min_value=0,
    max_value=12000000,
    value=2000000,
    step=500000,
    key = "minVisitors",
)

selectedStatesList = st.multiselect('Select state(s):', options=allStates, key="selectedStates")
filteredDf = dfJson[(dfJson["value"] >= st.session_state.minVisitors)&(dfJson["state"].isin(st.session_state.selectedStates))].sort_values(by="value", ascending = False)
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(filteredDf["label"], filteredDf["value"], color="steelblue")
ax1.set_title(f"Parks with at least {minVisitorsLimit:,} Visitors")
ax1.set_xlabel("National Park")
ax1.set_ylabel("Annual Visitors")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig1)

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.markdown("---")
st.title("Favorite Country to Travle to Survey Visualizations")
dfCsv = pd.read_csv("data.csv")
st.subheader("Chart of Survey Responses")
st.write("This chart shows the frequency distribution of survey responses.")
colName = dfCsv.columns[0]
responseCounts = dfCsv[colName].value_counts()
fig2, ax2 = plt.subplots(figsize=(6, 6))
ax2.pie(responseCounts.values,labels=responseCounts.index.astype(str),autopct="%1.1f%%",startangle=90,)
ax2.axis("equal")
ax2.set_title("Survey Responses")
plt.tight_layout()
st.pyplot(fig2)
st.subheader("Survey of Favorite Country to Travel to Filtered by Input Count")
st.write("Use slider to filter data by the number of times each category was inputted.")

categoryCounts = dfCsv[colName].value_counts()
maxFreq = int(categoryCounts.max()) if not categoryCounts.empty else 1

if "minFreq" not in st.session_state:
    st.session_state.minFreq = 1

minFreqLimit = st.slider(
    "Minimum number of inputs required:",
    min_value=1,
    max_value=maxFreq,
    value=1,
    step=1,
    key="minFreq",
)

filteredCounts = categoryCounts[categoryCounts >= st.session_state.minFreq].sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.bar(filteredCounts.index.astype(str), filteredCounts.values, color="seagreen")
ax3.set_title(f"Responses with at least {minFreqLimit} Inputs")
ax3.set_xlabel(colName)
ax3.set_ylabel("Frequency / Total Inputs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig3)

st.subheader("Summary Stats")
if not filteredCounts.empty:
    meanVal = filteredCounts.mean()
    medianVal = filteredCounts.median()
    col1, col2 = st.columns(2)
    col1.metric(label="Mean Frequency", value=f"{meanVal:.2f}")
    col2.metric(label="Median Frequency", value=f"{medianVal:.2f}")
else:
    st.write("No data matches this filter.")
