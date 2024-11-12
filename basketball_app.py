import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime


st.set_page_config(page_title = 'basketball', 
                   page_icon = ':basketball:',
                   layout = 'wide')
st.title("Explore NBA player stats")


st.markdown(""" 
This app performs simple webscrapping of MBA player stats details
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
""")


# Sidebar - select year
st.sidebar.header('User input features')
current_year = datetime.now().year
selected_year = st.sidebar.selectbox('Year', list(range(current_year,1950, -1)))


# webscrapping of NBA player stats
# In this website the data is in form of a table, so pandas can easily read this data
# returns a dataframe
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    # pandas can easilt read the data which is in the form of table, which is inside the html file
    table = pd.read_html(url, header = 0)
    df_table = table[0]
    raw = df_table.drop(df_table[df_table.Age == 'Age'].index) # Deletes repeating headers 
    df_fillna = raw.fillna(method ='ffill')
    # we will use the pandas default index and drop the index 'Rk'
    preprocesse_table = df_fillna.drop(['Rk'], axis = 1)
    return preprocesse_table

# selected_year is taking input from dropdown sidebar
playerstats = load_data(selected_year)
print('\n\n*******************playerstats******************\n\n')
print(playerstats)



# Sidebar - select Team to display
# Now select team to display in the dataframe 
playerstats.Team = playerstats.Team.astype(str)
sorted_unique_teams  = sorted(playerstats.Team.unique())
# default selecting all availlable teams
selected_teams = st.sidebar.multiselect('Teams', sorted_unique_teams, sorted_unique_teams)
print('\n\n*******************selected_teams******************\n\n')
print(selected_teams)



# Sidebar - select Team to display
# unique_positions = ['C', 'PF', 'SF', 'PG', 'SG']
sorted_unique_positions = sorted(playerstats.Pos.unique())
selected_positions = st.sidebar.multiselect('Positions', sorted_unique_positions, sorted_unique_positions) 
print('\n\n*******************selected_positions******************\n\n')
print(selected_positions)



# filtering datafame 
selected_df_final_display = playerstats[(playerstats.Team.isin(selected_teams)) & 
                                        (playerstats.Pos.isin(selected_positions))]
selected_df_final_display.reset_index(inplace=True)
print('\n\n*******************selected_df_final_display******************\n\n')
print(selected_df_final_display)



st.header('Display Players stats based on selected variables')
st.dataframe(selected_df_final_display)
st.write('Output table dimension: ' + str(selected_df_final_display.shape[0]) + 
' × ' + str(selected_df_final_display.shape[1]))


# Download NBA player stats as csv file
# https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv
# https://stackoverflow.com/questions/69705832/how-do-i-download-a-pandas-dataframe-to-a-csv-file-in-streamlit
@st.cache_data
def convert_df_to_csv(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')



st.write("")


st.download_button(
  label="Download NBA player stats as .csv file",
  data = convert_df_to_csv(selected_df_final_display),
  file_name = 'NBA_player_stats.csv',
  mime = 'text/csv',
)



st.write("")
st.write("")



if st.button('Correlation heatmap'):
    st.header('Correlation heatmap')

    corr = selected_df_final_display.iloc[:,:10].corr(numeric_only = True)
    # Plotting correlation heatmap
    with sns.axes_style("white"):
        fig, ax = plt.subplots()
        ax = sns.heatmap(corr, cmap = "YlGnBu", annot = True, ax = ax)
    st.pyplot(fig)



