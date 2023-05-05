import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt
import plotly.express as px

st.set_page_config(page_title='Covid Data', page_icon='4.jpg', layout='wide')

c1,c2,c3=st.columns([1,2,1])
c2.title("INTERNATIONAL COVID DATA")
st.write("")
st.write("")
st.write("")
c1.image("4.jpg")
c3.image("3.jpg")
c2.subheader('"This Data is Retreived from a snowflake database"')
# Snowflake connection details
account = 'ot15309.us-central1.gcp'
user = 'sakp7'
password = 'Saketh@2003'
database = 'COVID19_EPIDEMIOLOGICAL_DATA'
schema = 'public'
warehouse = 'COMPUTE_WH'
# Connect to Snowflake
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    database=database,
    schema=schema,
    warehouse=warehouse
)
# Retrieve data from Snowflake
query = 'SELECT * FROM WHO_SITUATION_REPORTS'
df = pd.read_sql(query, conn)
# Set Streamlit theme
st.markdown(
"""
<style>
body {
    background-color: #F0F2F6;
}
</style>
""",
    unsafe_allow_html=True
)

# Display data in a chart
chart = alt.Chart(df).mark_bar().encode(
    x='COUNTRY',
    y='TOTAL_CASES'
).interactive()

st.altair_chart(chart, use_container_width=True)
st.write("")
st.write("")
st.write("")

countries = sorted(df['COUNTRY'].unique())
selected_country = st.selectbox('Select a country', countries,index=150)
query = f"SELECT TOTAL_CASES, TRANSMISSION_CLASSIFICATION, DEATHS FROM WHO_SITUATION_REPORTS WHERE COUNTRY = '{selected_country}' LIMIT 1;"
st.write("")
st.write("")
st.write("")

df = pd.read_sql(query, conn)

combined_df = pd.DataFrame({
    'Cases': ['DEATHS', 'TOTAL_CASES'],
    'Counts': [df['DEATHS'][0], df['TOTAL_CASES'][0]]
})
st.dataframe(df)
fig3 = px.pie(combined_df, values='Counts', names='Cases', title=f"COVID-19 Cases in {selected_country}")

x1,x2,x3=st.columns(3)
x2.plotly_chart(fig3)
