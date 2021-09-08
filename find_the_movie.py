import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import random
import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
#import plotly.express as px
import seaborn as sns

web_link='https://www.imdb.com/search/title/?genres={}&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=CVAA7839K9RPQBDSK05W&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1'

genres=['action','adventure','animation','biography','comedy','crime','drama','family','fantasy','film-Noir','history','horror','music','Musical','mystery','romance','sci-fi','sport','thriller','war','western']

select_box = st.sidebar.selectbox('Select the genre',genres)


url= web_link.format(select_box)
data= requests.get(url)
soup=BeautifulSoup(data.content,'html.parser')
time.sleep(random.randint(1,5))
full_data=soup.find_all('div', class_='lister-item-content')  


dummy_movie_name=[]
for i in full_data:
        dummy_movie_name.append(i.find('h3',class_="lister-item-header").get_text().strip())
        movie_name=[]
        year=[]
        for i in range(len(dummy_movie_name)):
                    k=re.sub("[^A-Za-zöä ]",'',dummy_movie_name[i])
                    j=dummy_movie_name[i].split('\n')
                    l=j[2]
                    l=re.sub("[^0-9]",'',l)
                    year.append(l)
                    year[i]=year[i].strip()
                    movie_name.append(k)
                    movie_name[i]=movie_name[i].strip()
        ratings_data=soup.find_all('div', class_='ratings-bar')
        dummy_ratings=[]
        for i in ratings_data:
            dummy_ratings.append(i.find('strong'))
            ratings=[]
            for i in range(len(dummy_ratings)):
                    k=re.sub("[^0-9.]",'',str(dummy_ratings[i]))
                    ratings.append(k)
                    ratings[i]=ratings[i].strip()
        income_data=soup.find_all('p',class_='sort-num_votes-visible')
        dummy_income=[]
        for i in income_data:
            dummy_income.append(i.text.strip())
            income=[]

            for i in range(len(dummy_income)):
                try:
                    k=str(dummy_income[i]).split('|')[1]
                    j=re.sub("[^0-9.]",'',str(k))
                    income.append(j)
                except:
                    income.append(np.nan)
        cla=soup.find_all('p')
        dummy_directors=[]
        directors=[]
        i=0
        for j in range(2,201,4):
            try:
                dummy_directors.append(cla[j].text.strip())
                k=dummy_directors[i].split('|')[0]
                m=k.split(':')[1].strip()
                directors.append(m)
                i+=1
            except:
                 directors.append(np.nan)

df = pd.DataFrame ({'Name of Movie' : movie_name, 'Year launched': year,'Ratings': ratings,'Income(Millions)': income, 'Directors': directors})
df[["Year launched", "Ratings", "Income(Millions)"]] = df[["Year launched", "Ratings", "Income(Millions)"]].apply(pd.to_numeric)
df['Income(Millions)']=df['Income(Millions)'].fillna(value= df['Income(Millions)'].mean())
df['Ratings']= df['Ratings'].fillna(value= df['Ratings'].mean())
df['Year launched']= df['Year launched'].fillna(value= df['Year launched'].mode())
st.subheader('Top 50 Movies of Choosen Genre')
st.write(df)
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(df['Name of Movie'],df['Income(Millions)'])
plt.xticks(rotation=90)
plt.show()
st.pyplot(fig)

st.subheader('Correlation Heat Map')
fig, ax = plt.subplots()
sns.heatmap(df.corr(), ax=ax)
st.write(fig)

