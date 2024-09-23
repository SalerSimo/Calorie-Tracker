import pyodbc
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os

path = os.path.dirname(os.path.realpath(__file__))

def getTable():
    db = pyodbc.connect(rf'Driver=[Microsoft Access Driver (*.mdb, *.accdb)];DBQ= {path}\\db.accdb'.replace('[', '{').replace(']', '}'))
    cursor = db.cursor()
    st.session_state.db = db
    st.session_state.cursor = cursor 
    #query = "SELECT * FROM ValoriNutrizionali"
    #x = pd.read_sql(query, db)
    #st.session_state.ValoriNutrizionali = x
    

st.set_page_config(page_title="Home", layout='wide')
string = """
    <style>
        section[data-testid="stSidebar"] {
            width: 315px !important; # Set the width to your desired value
        }
    </style>
"""
st.markdown(string, unsafe_allow_html=True)
getTable()
home = st.Page("pages\\Home.py", title="Home")
newMeal = st.Page("pages\\newMeal.py", title='Add New Meal')
ins = st.Page("pages\\inserted.py", title=" ")
week = st.Page('pages/week.py', title=' ')
update = st.Page('pages/updateValoriNutrizionali.py', title=' ')

st.navigation([home, newMeal, ins, week, update], position="sidebar").run()