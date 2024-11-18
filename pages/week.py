import streamlit as st
import datetime
import pandas as pd
import numpy as np
import altair as alt
from utils import utils
from utils.utils import stringFromDate

selectedDay = st.sidebar.date_input("Select a week")
week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekDay = selectedDay.weekday()
startWeek = selectedDay - datetime.timedelta(days=weekDay)
query = f"SELECT COUNT(*) as Num, SUM(TotalCarbo*4) as Carb, SUM(TotalProtein*4) as Pro, SUM(TotalFat*9) as Fat FROM MealByDay WHERE Day >= '{stringFromDate(startWeek)}' and Day <= '{stringFromDate(startWeek + datetime.timedelta(days=6))}'"
weekDF = pd.read_sql(query, st.session_state.db)

totCal = weekDF['Carb'] + weekDF['Pro'] + weekDF['Fat']
length = weekDF['Num'][0]
if weekDF['Num'][0] == 0:
    totCal = 0
    length = 1

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

year, month, day = stringFromDate(startWeek).split('/')
date1 =  months[int(month)] + ' ' + day
year, month, day = stringFromDate(startWeek + datetime.timedelta(days=6)).split('/')
date2 = months[int(month)] + ' ' + day
today = datetime.date.today()
if today >= startWeek and today <= startWeek + datetime.timedelta(days=6):
    title = "<b class='date'>This week</b> you ate:"
else:
    title = f"The week from <b class='date'>{stringFromDate(date1)}</b> to <b class='date'>{stringFromDate(date2)}</b> you ate:"

string = f"""
    <p class="Today"> {title} </p>
    <style>
    .date(
        border-radius: 5px;
        color: #FFFF80;
    )
    .Today(
        font-size: 2rem; 
        width: 100%; 
        height: 100%; 
        margin-top: 0px; 
        text-align: left;
        margin: 0px 0px 0px;
    )</style>""".replace('(', '{').replace(')', '}')
st.markdown(string, unsafe_allow_html=True)
st.write('')
#col1, col2 = st.columns([1, 2])
string = f"""
    <div class="Line">
        <div style='display: inline-block; background-color: #FFFFFF00; border-radius: 10px;'>
            <p class="tot"> <b> {int(totCal)} </b> </p>
            <p class="cal"> <b> KCal </b> </p>
        </div>
        <p style='display: inline-block; font-size: 1.5rem; margin-right: 20px;'>in <b style='font-size: 2rem'>{weekDF['Num'][0]} days</b>, averaging</p> 
        <div style='display: inline-block; background-color: #FFFFFF00; border-radius: 10px;'>
            <p class='tot'><b> {int(totCal/length)} </b></p>
            <p class="cal"> <b> KCal </b></p>
        </div>
        <p style='display: inline-block; font-size: 1.5rem;'>per day</p> 
    </div>
    <style>
    .tot(
        font-size: 7rem;  
        height: 100%; 
        display:inline-block;
        margin-bottom: 0px;
        margin-left: 0px;
        color: #FFFF80;
    )
    .cal(
        font-size: 2.5rem; 
        margin-right: 20px;
        height: 100%; 
        margin-top: 0px; 
        display: inline-block;
    )</style>""".replace('(', '{').replace(')', '}')
st.markdown(string, unsafe_allow_html=True)

domain = ['Carb', 'Pro', 'Fat']
colors = ['#FAB600', '#00D5F5', '#FFB4D0']  #carb, protein, fat
query = f"SELECT Day, TotalCarbo*4 as Carb, TotalProtein*4 as Pro, TotalFat*9 as Fat FROM MealByDay WHERE Day >= '{stringFromDate(startWeek)}' and Day <= '{stringFromDate(startWeek + datetime.timedelta(days=6))}'"
boh = pd.read_sql(query, st.session_state.db)
for i in range(0, 7):
    date = startWeek + datetime.timedelta(days=i)
    date = stringFromDate(date)
    year, month, day = date.split('/')
    if date not in np.array(boh['Day']):
        boh.loc[len(boh)] = [date, 0, 0, 0]
    week[i] = week[i] + ' - ' + month + '/' + day
boh = boh.sort_values('Day')
boh.insert(1, 'Week day', week)
boh = boh.drop(columns=["Day"], axis=1).rename(columns={'Week day': 'Day'})
if np.sum(np.array(boh.melt('Day', var_name='Macro', value_name='KCal')['KCal'])) > 0:
    chart = alt.Chart(boh.melt('Day', var_name='Macro', value_name='KCal'), height=200).mark_bar().encode(
            alt.X('Macro', axis=alt.Axis(title='', labelFontSize=15, labelAngle=0), sort=['Carb', 'Pro', 'Fat'], ),
            alt.Y('KCal', axis=alt.Axis(title='KCal', grid=True, labelFontSize=15, titleFontSize=20, titlePadding=0)),
            color=alt.Color('Macro', sort=['Carb', 'Protein', 'Fat'], scale=alt.Scale(domain=domain, range=colors), ),
            column=alt.Column('Day', sort=week, ),
        ).configure_legend(
            labelFontSize=15, titleFontSize=20
        ).configure_headerColumn(
            labelFontSize=15, titleFontSize=20
        ).configure_mark(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
    st.header('')
    col1 = st.columns([1, 8])[0]
    col1.altair_chart((chart), use_container_width=True)
