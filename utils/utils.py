import streamlit as st
from sqlalchemy import create_engine,text
from datetime import date, timedelta
import datetime
import pandas as pd

def DateToInt(date: str) -> int:
    year, month, day = date.split("/")
    return int(year)*10000 + int(month)*100 + int(day)

def IntToDate(number: int) -> str:
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
    return date

def stringFromDate(date: date) -> str:
    return str(date).replace('-', '/')