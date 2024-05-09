import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

DATA_URL = (
    "vgssales.csv"
)

st.title("Exploratory Data Analysis: Video Games Sales")

st.sidebar.title("EDA: Video Games Sales")

st.markdown("This application is a Streamlit dashboard used "
            "to analyze Video Games Sales")
st.sidebar.markdown("This application is a Streamlit dashboard used "
            "to analyze Video Games Sales")


@st.cache(persist=True)
def load_data():
    df = pd.read_csv(DATA_URL)
    
    return df

df = load_data()

st.table(df.head())


a = st.sidebar.selectbox('Tasks', ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5', 'Task 6', 'Task 7'], key='2')
if a == 'Task 1':
    alltimesales =round(df.groupby(["Genre"]).mean(),2)
    alltimesales.reset_index(inplace=True)

    fig = px.bar(alltimesales.sort_values('Global_Sales'), 
             x='Global_Sales', y='Genre', title='Average Global Sales(million dollars) across years for different Game Genres'
             , text='Global_Sales', orientation='h')

    st.plotly_chart(fig)
    st.subheader('Observation:\nPlatform Genre has the Highest Sales')

if a == 'Task 2':
    platform=pd.DataFrame(df['Platform'].value_counts())
    platform.reset_index(inplace=True)
    platform.rename(columns={'index':'Platform','Platform':'Number of Games'},inplace=True)

    fig = px.bar(platform.sort_values('Number of Games'), 
             x='Number of Games', y='Platform', title='Number of games across different platforms', 
             text='Number of Games', orientation='h')
    st.plotly_chart(fig)
    st.header('Observations')
    st.subheader('DS platform has the number of games across all the platforms')
    st.subheader('PS3 platform is very close to the highest platform')

if a == 'Task 3':
    yearlyreleases=pd.DataFrame(df['Year'].value_counts())
    yearlyreleases.reset_index(inplace=True)
    yearlyreleases.rename(columns={'index':'Year','Year':'Number of Releases'},inplace=True)
    fig = px.bar(yearlyreleases.sort_values('Year',ascending=True), 
             x='Number of Releases', y='Year', title='Number of games released in each year', 
             text='Number of Releases', orientation='h')
    st.plotly_chart(fig)
    st.header('Observations')
    st.subheader('Most of the Games were released in the 20th Century')
    st.subheader('Number of releases suddenly increased after 2004, and started to decrease after 2011')
    st.subheader('Very few games were released in late 19th Century')

if a == 'Task 4':
    salespergenre=df.groupby('Genre').sum()
    salespergenre['percentagesales']=round(salespergenre['Global_Sales']/(salespergenre['Global_Sales'].sum()),4)*100
    salespergenre.reset_index(inplace=True)
    fig = px.pie(salespergenre, names='Genre', values='percentagesales',template='presentation', title = 'Percentage Share of Each Genre in Global Sales')
    st.plotly_chart(fig)
    st.header('Observations')
    st.subheader('**Action** Genre has contributed most to the Global Sales followed by **Sports** and **Shooter** Genre games')
    st.subheader('**Strategy** and **Puzzle** genre games brought in the lowest sales because most of the people find such games boring. So, to increase Global Sales, a Gaming company should focus on creating more Action, Sports and Shooter games as they bring in the most number of Sales')

if a == 'Task 5':
    fig = px.scatter(df, x="Year", y="Global_Sales", color="Genre", hover_data=['Publisher'])
    st.plotly_chart(fig)
    st.subheader('Observations')
    st.subheader('In the year 2006, **Nintendo** recorded the Highest Global Sales in Sports Genre')
    st.subheader('**Strategy** Genre Games has been consistenly performing very bad')
    st.subheader('**Nintendo** is consistenly bringing in highest Global Sales in the year 2005, 2006, 2008')



platformsales=df[['Platform','Year','Global_Sales']]
platformsales['Netplatformsales']=platformsales.groupby(['Platform','Year'])['Global_Sales'].transform('sum')
desiredplatforms=['PS2','PS','Wii','PSP','PS','PC','XB','GBA']

#desiredplatforms=['PS3','X360']

platformsales=platformsales[(platformsales['Year']>=2005) & (platformsales['Year']<=2015) & (platformsales['Platform'].isin(desiredplatforms))]
platformsales=platformsales.sort_values('Year',ascending=True)
platformsales.drop_duplicates()
platformsales.drop('Global_Sales', axis=1, inplace=True)

if a == 'Task 6':


    fig=px.bar(platformsales,x='Platform', y='Netplatformsales', animation_frame="Year",range_y=[0,220], 
           animation_group='Netplatformsales', hover_name='Platform',color_discrete_sequence=px.colors.qualitative.D3,
          title='Change in Net Sales(million $) across different platforms from 2005 to 2015')
    st.plotly_chart(fig)

if a == 'Task 7':
    publishersales=df[['Publisher','Year','Global_Sales']]
    publishersales['Netpublishersales']=publishersales.groupby(['Publisher','Year'])['Global_Sales'].transform('sum')
    desiredpublisher=['Electronic Arts','Activison','Namco Bandal Games','Ubisoft','Konami Digital Entertainment',
                  'THQ','Nintendo','Sega','Sony Computer Entertainment','Take-Two Interactive']

    publishersales=publishersales[(platformsales['Year']>=2005) & (platformsales['Year']<=2015) & (publishersales['Publisher'].isin(desiredpublisher))]
    publishersales=publishersales.sort_values('Year',ascending=True)
    publishersales.drop_duplicates()
    publishersales.drop('Global_Sales', axis=1, inplace=True)

    fig=px.bar(publishersales,x='Netpublishersales', y='Publisher', animation_frame="Year", 
           animation_group="Netpublishersales", hover_name="Publisher",color_discrete_sequence=px.colors.qualitative.D3,width=1000, height=500
          ,title='Change in Net Sales(million $) of different Publishers from 2005 to 2015')
    st.plotly_chart(fig)



