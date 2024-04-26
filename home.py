import streamlit as st
import pandas as pd
import ScatterPlot
import Goals_Years
import maps
import shots_goalsXG
from logo import laliga_logo
from logo import bundesliga_logo
from logo import ligue1
from logo import prem_logo
from logo import serieA_logo
from logo import ligue2
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import json,time

@st.cache_data 
def load_data(csv):
    df = pd.read_csv(csv)
    return df
@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)
    
@st.cache_resource
def display_animation():
    image_placeholder=st.empty()
    image_placeholder.image('https://cdn.dribbble.com/users/494229/screenshots/1601132/loadingicon14.gif')
    time.sleep(3)
    image_placeholder.empty()
    


display_animation()

main_file=load_data('../StrikerAnalysis.csv')
year=main_file['Year'].unique()
year_chosen=st.sidebar.selectbox('Select a year',year)
league=main_file['League'].unique()
league=['La Liga','Bundesliga','France Ligue 1','Premier League','Serie A','France Ligue 2']
league_chosen=st.sidebar.selectbox('Select the league',league)


if league_chosen=='La Liga':
    laliga_logo.laligaLogo()
elif league_chosen=='Bundesliga':
    bundesliga_logo.bundesligaLogo()
elif league_chosen=='France Ligue 1':
    ligue1.ligue1Logo()
elif league_chosen=='Premier League':
    prem_logo.premLogo()
elif league_chosen=='Serie A':
    serieA_logo.serieALogo()
else:
    ligue2.ligue2Logo()
filtered_data=main_file[main_file['League']==league_chosen]
country=filtered_data['Country'].unique()
st.sidebar.write('Country: ',f'{country[0]}')
top_chosen=st.sidebar.select_slider('Select how many players you want to compare',options=list(range(0,50)),value=15)

# with st.sidebar:
#     selected = option_menu('Welcome', [year_chosen, 'Search','Analyze'], 
#         icons=['play-btn','search','info-circle'],menu_icon='intersect', default_index=0)
#     lottie = load_lottiefile("footballAnimation.json")
#     st_lottie(lottie,key='loc')

main_file=main_file[main_file['Year']==year_chosen]
main_file=main_file[main_file['League']==league_chosen].sort_values(by='Goals',ascending=False)

    
maps.mapsViz(main_file,league_chosen)
st.header('Analysis')
st.altair_chart(ScatterPlot.scatter_plot(main_file.head(top_chosen),'Goals','X G','Goals vs XG'))

Goals_Years.goalsvsyears(main_file,year_chosen)
shots_goalsXG.expectation(main_file)
