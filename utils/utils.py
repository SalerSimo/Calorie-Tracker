import streamlit as st
from sqlalchemy import create_engine,text
from datetime import date, timedelta
import datetime
import pandas as pd

"""Raccoglie le principali funzioni condivise dalle varie pagine"""

def DateToInt(date: str):
    year, month, day = date.split("/")
    return int(year)*10000 + int(month)*100 + int(day)

def IntToDate(number: int):
    year = number//10000
    number = number%10000
    month = number//100
    day = number%100
    year = str(year)
    if month<10:
        month = '0' + str(month)
    else:
        month = str(month)
    if day<10:
        day = '0' + str(day)
    else:
        day = str(day)
    date = year + '/' + month + '/' + day
    return date

def getDateFromString(string):

    date = datetime.datetime.strptime(string, "%Y/%m/%d").date()
    #date = str(date).replace('-', '/')
    return date

def stringFromDate(date: date):
    return str(date).replace('-', '/')

IntToDate(DateToInt("2024/09/17"))

today = "2024/09/02".replace("/", '')
today = datetime.datetime.strptime(today, "%Y%m%d").date()
print(today - timedelta(days=10))