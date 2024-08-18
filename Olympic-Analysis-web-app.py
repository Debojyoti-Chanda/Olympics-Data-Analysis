import streamlit as st 
import pandas as pd 
import preprocessor ,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df= pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocessor(df,region_df)

st.sidebar.title("Olympic Anlysis")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/2880px-Olympic_rings_without_rims.svg.png')
user_menu = st.sidebar.radio(
    'Select A Option',
    ('Medal Tally','Overall Analysis', 'Country-wise Analysis', 'Athlete-Wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.header("Medal Tally")
    county, years = helper.country_year_list(df)
    st.sidebar.header("Medal Tally")
    selected_county = st.sidebar.selectbox("Select Country",county)
    selected_year = st.sidebar.selectbox("Select Years",years)
    medal_tally = helper.fetch_medal(df,selected_year,selected_county)
    if(selected_county == 'Overall' and selected_year == 'Overall'):
        st.title("Overall Tally")
    if selected_county == "Overall" and selected_year != "Overall":
        st.title("Medal Tally in " + str(selected_year))
    if selected_county != "Overall" and selected_year == "Overall":
        st.title("Medal Tally in " + str(selected_county))
    if selected_county != "Overall" and selected_year != "Overall":
        st.title("Medal Tally in " + str(selected_year) + " by country " + str(selected_county))
    st.table(medal_tally)
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Edition")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_overtime = helper.data_over_time(df ,'region')
    fig = px.line(nations_overtime, x='Edition', y='region')
    st.title("Partcipating Nations over the Years")
    st.plotly_chart(fig)
    events_overtime = helper.data_over_time(df ,'Event')
    fig = px.line(events_overtime, x='Edition', y='Event')
    st.title("Events over the Years")
    st.plotly_chart(fig)
    athletes_overtime = helper.data_over_time(df ,'Name')
    fig = px.line(athletes_overtime, x='Edition', y='Name')
    st.title("Atheletes over the Years")
    st.plotly_chart(fig)

    st.title("No of Events Overtime (every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Succesful Athletes")
    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,"Overall")
    selected_sport = st.selectbox("Select a Sport", sports_list)
    x= helper.most_successful(df,selected_sport)
    st.table(x)
if user_menu == "Country-wise Analysis":
    county_list = df['region'].dropna().unique().tolist()
    county_list.sort()
    st.sidebar.title("Countrywise Medal")
    selected_county = st.sidebar.selectbox("Select Country",county_list)
    county_df = helper.yearwise_medal_tally(df,selected_county)
    st.title(selected_county + " Over the year medals")
    fig = px.line(county_df,x='Year',y='Medal')
    
    st.plotly_chart(fig)