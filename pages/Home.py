import streamlit as st
import pyodbc
import pandas as pd
import numpy as np
import datetime
import altair as alt
from utils import utils
from utils.utils import stringFromDate
import os


colors = ['#FAB600', '#00D5F5', '#FFB4D0']  #carb, protein, fat

def makeBarChart(labelNames, calories, grams, column, fontSize):
    sum = 0
    big = calories.max()
    string=f"""
    <style>
    .nonso(
        height: {fontSize*41.6}px;
    )
    .label(
        font-size: {fontSize}rem; 
        width: 8%;
        margin-right: 0.5%; 
        margin-left: 1.5%;
        text-align: right;
    )
    .wrapper(
        border: 2px #FFFFFF20;
        margin-top: 5px;
        border-radius: 10px;
        background-color: #FFFFFF20;
    )</style>""".replace('(', '{').replace(')', '}')
    column.markdown(string, unsafe_allow_html=True)
    for val in calories:
        sum += val
    string= '<div class="wrapper"> '
    css = "<style>"
    for i in range(len(labelNames)):
        val = calories[i]/big
        if calories[i] == 0:
            val = calories[i]/0
        val = val*100
        val = val*0.70
        string = string + f"""
        <div class="line">
            <p class="label" style="display: inline-block" > <b> {labelNames[i].upper()} </b> </p>
            <p class="val{i}" style="display: inline-block"> c</p>
            <p style="display: inline-block; margin-left: 0.5%; font-size: {fontSize}rem;">{round(grams[i], 1)} g  /  {round(calories[i], 1)} KCal</p>
        </div>""".replace('(', '{').replace(')', '}')
        css = css + f"""
        .val{i}(
            font-size: {fontSize}rem;
            height: {fontSize*1.6}rem;
            width: {val}%;
            background-color: {colors[i]};
            border-radius: 5px;
            text-align: right;
            color: #FFFFFF00;
            margin-top: {16*(i==0)}px;
            )""".replace('(', '{').replace(')', '}')
    string = string + "</div>"
    css = css + "</style>"
    #column.markdown(css, unsafe_allow_html=True)
    column.markdown(string + css, unsafe_allow_html=True)
    return None

if 'button' not in st.session_state:
    st.session_state.button = False

def click():
     st.session_state.button = True

val = pd.read_sql("SELECT * FROM ValoriNutrizionali", st.session_state.db)

cursor = st.session_state.cursor
if not st.session_state.button and False:
    st.button("Show table", on_click=click)
if st.session_state.button:
    if st.button('Hide table'):
        st.session_state.button = False
        st.rerun()
    st.write(val)

selectedDay = st.sidebar.date_input("Select a date")

#today = str(datetime.date.today()).replace('-', '/')
#today = '2024/09/15'
query = f"SELECT * FROM MealByDay WHERE Day = '{stringFromDate(selectedDay)}'"
eatToday = pd.read_sql(query, st.session_state.db)
if len(eatToday) == 0:
    eatToday.loc[0] = [stringFromDate(selectedDay), 0, 0, 0, 0]
eatTodayChart = pd.DataFrame({'Macro': ['TotalCarbo', 'TotalProtein', 'TotalFat'], 'Amount': [eatToday['TotalCarbo'][0]*4, eatToday['TotalProtein'][0]*4, eatToday['TotalFat'][0]*9], 'Grams': [eatToday['TotalCarbo'][0], eatToday['TotalProtein'][0], eatToday['TotalFat'][0]]})
#col1.markdown('#### Today you ate')
string = f"""
    <p class="Today"> {stringFromDate(selectedDay)}: </p>
    <style>
    .Today(
        font-size: 2rem; 
        width: 100%; 
        height: 100%; 
        margin-top: 0px; 
        text-align: left;
        margin: 0px 0px 0px;
    )</style>""".replace('(', '{').replace(')', '}')
st.markdown(string, unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])
string = f"""
    <div class="Line">
        <p class="tot"> <b> {int(eatToday['TotalCalories'][0])} </b> </p>
        <p class="cal"> <b> KCal </b> </p>
    </div>
    <style>
    .tot(
        font-size: 7rem;  
        height: 100%; 
        display:inline-block;
    )
    .cal(
        font-size: 2.5rem; 
        width: 30%; 
        height: 100%; 
        margin-top: 0px; 
        display: inline-block;
    )</style>""".replace('(', '{').replace(')', '}')
col1.markdown(string, unsafe_allow_html=True)

#x=st.slider('ci', min_value=0.5, max_value=3.0, step=0.1)
makeBarChart(['Carb', 'Protein', 'Fat'], calories=eatTodayChart['Amount'], grams=eatTodayChart['Grams'], fontSize=0.9, column=col2)

domain = ['Carb', 'Pro', 'Fat']
types = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
startWeek = selectedDay - datetime.timedelta(days=6)
startWeek = str(startWeek).replace('-', '/')
query = f"SELECT Type, TotalCarbo*4 as Carb, TotalProtein*4 as Pro, TotalFat*9 as Fat FROM MealByDayAndType WHERE Day = '{stringFromDate(selectedDay)}'"
boh = pd.read_sql(query, st.session_state.db)
if len(boh) > 0:
    chart = alt.Chart(boh.melt('Type', var_name='Macro', value_name='KCal'), height=65).mark_bar().encode(
            y=alt.X('Macro', axis=alt.Axis(title='', labelFontSize=15, labelAngle=0), sort=['Carb', 'Pro', 'Fat'],),
            x=alt.Y('KCal', axis=alt.Axis(title='KCal', grid=True, labelFontSize=15, titleFontSize=20)),
            color=alt.Color('Macro', sort=['Carb', 'Protein', 'Fat'], scale=alt.Scale(domain=domain, range=colors)),
            row=alt.Row('Type', sort=types, title=""),
        ).configure_legend(labelFontSize=15, titleFontSize=20).configure_headerRow(labelFontSize=20, titleFontSize=20, labelAngle=0, labelAlign='left').configure_mark(cornerRadiusBottomRight=5, cornerRadiusTopRight=5, )
    st.header('')
    col1, col2 = st.columns([1, 2, 0.5])[:2]
    col2.altair_chart((chart), use_container_width=True)

typesTable = {}
columns = st.columns(2)
i = 0
for type in types:
    query = f"SELECT Day, Type, FoodName as Food, Amount FROM Meal WHERE Day = '{stringFromDate(selectedDay)}' and Type = '{type}'"
    typesTable[type] = pd.read_sql(query, st.session_state.db)
    if len(typesTable[type]) > 0:
        i += 1
if i == 4:
    columns = st.columns(2)
    st.write('')
    col = st.columns(2)
    columns.append(col[0])
    columns.append(col[1])
elif i>0:
    columns = st.columns(i)    
i = 0
for type in types:
    string = f"""
    <div style="border: 0.1rem solid #FFFFFFBF; border-radius: 5px; margin-bottom: 15px;">
    <div class='tag-container'>
        <p class='tag' style="width: 70%; padding-left: 10px;">Food</p>
        <p class='vertical-line'> c </p>
        <p class='tag'>Amount</p>
    </div>
    <div class='container'>
    """
    if len(typesTable[type]) == 0:
        continue
    string1 = f"""
    <p style="font-size: 2.5rem; margin-top: 10px; margin-bottom: -20px;">{type}</p>
    """
    for food, amount in np.array(typesTable[type][['Food', 'Amount']]):
        html = f"""<p class='linea'>c</p>
        <div>
            <p class='food'>{food}</p>
            <p class='vertical-line'> c </p>
            <p class='amount'>{amount}</p>
            <p class='amount'>g</p>
        </div>
        """
        string = string + html
    string = string + '</div> </div>'
    string = string + """
    <style>
    .tag(
        display: inline-block;
        margin-bottom: 0px;
        margin-top: 5px;
    )
    .container(
        background-color: #FFFFFF20;
        padding-bottom: 5px;
        border: 0.1rem #FFFFFF;
    )
    .food(
        display: inline-block;
        margin-bottom: 0px;
        padding-left: 10px;
        width: 70%;
        font-size: 1.2rem;
    )
    .amount(
        display: inline-block;
        margin-bottom: 0px;
        font-size: 1.2rem;
    )
    .linea(
        background-color: #FFFFFFCF;
        color: #FFFFFF00;
        height: 0.1rem;
        margin-top: 5px;
        margin-bottom: 5px;
    )
    .vertical-line(
        display: inline-block;
        margin-bottom: 0px;
        background-color: #FFFFFFCF;
        width: 0.1rem;
        color: #FFFFFF00;
        margin-right: 1%;
    )
    .st-emotion-cache-uef7qa.e1nzilvr5 > p(
        font-size: 1.2rem;
    )</style>""".replace('(', '{').replace(')', '}')
    
    with col1.expander(label= type):
        st.markdown(string, unsafe_allow_html=True)
    col1.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    i += 1

st.sidebar.write('')
st.sidebar.page_link('pages/week.py', label='Week')