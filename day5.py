import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from add_data import db_execute_fetch

st.set_page_config(page_title="Day 5", layout="wide")

def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df

def selectHashTag():
    df = loadData()
    hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)


def selectLocAndAuth():
    df = loadData()
    location = st.multiselect("choose tweets based on aurthor", list(df['place_coordinate'].unique()))
    lang = st.multiselect("choose Language of tweets", list(df['language'].unique()))

    if location and not lang:
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    elif lang and not location:
        df = df[np.isin(df, lang).any(axis=1)]
        st.write(df)
    elif lang and location:
        location.extend(lang)
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)

def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)

def wordCloud():
    df = loadData()
    cleanText = ''
    for text in df['hashtags']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='blue', min_font_size=5).generate(cleanText)
    st.title("Hashtags Word Cloud")
    st.image(wc.to_array())

def stBarChart():
    df = loadData()
    dfCount = pd.DataFrame({'Friends_count': df.groupby(['original_author'])['friends_count'].count()}).reset_index()
    dfCount["original_author"] = dfCount["original_author"].astype(str)
    dfCount = dfCount.sort_values("Friends_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 10)
    title = f"Top {num} Ranking By Number of Friends"
    barChart(dfCount.head(num), title, "original_author", "Friends_count")    


def langPie():
    df = loadData()
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['language'])['clean_text'].count()}).reset_index()
    dfLangCount["language"] = dfLangCount["language"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
    st.title(" Tweets Language pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count', names='language', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.beta_columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)


st.title("Fumbani Dashboard :chart_with_upwards_trend: :chart_with_downwards_trend: :bar_chart:")
st.header("Data Visualizations")
bar_graph = st.button('Bar Graph')
pie_chart = st.button('Pie Chart')
with st.beta_expander("Show More Graphs"):
    wordCloud()
    selectHashTag()
    selectLocAndAuth()


if bar_graph:
    stBarChart()        
elif pie_chart:
    langPie()
else:
    st.write('Want to see visuals:thinking_face: Click on any of the buttons')


