import streamlit as st
import pandas as pd
import datetime


def insert(food, amounts, date, type):
    cursor = st.session_state.cursor
    MealDb = pd.read_sql("SELECT * FROM Meal", st.session_state.db)
    foodDB = pd.read_sql("SELECT * FROM ValoriNutrizionali", st.session_state.db)
    totCarbo = 0
    totPro = 0
    totFat = 0
    for i in range(len(food)):
        if food[i] != None and amounts[i] != None:
            query = f"INSERT INTO Meal (FoodName, Day, Type, Amount) VALUES ('{food[i]}', '{date}', '{type}', {amounts[i]})"
            cursor.execute(query)
            cursor.commit()
            mult = amounts[i]/100
            foodInfo = foodDB.loc[foodDB['Name'] == food[i]]
            for j, name in enumerate(foodDB['Name']):
                if name == food[i]:
                    index = j
            totCarbo += foodInfo['Carbo'][index]*mult
            totPro += foodInfo['Protein'][index]*mult
            totFat += foodInfo['Fat'][index]*mult
    totCarbo = round(totCarbo, 1) 
    totPro = round(totPro, 1) 
    totFat = round(totFat, 1) 
    x = pd.read_sql(f"SELECT COUNT(*) as cont FROM MealByDayAndType WHERE Type = '{type}' and Day = '{date}'", st.session_state.db)
    if x['cont'][0] == 0:
        query = f"INSERT INTO MealByDayAndType (Day, Type, TotalCarbo, TotalProtein, TotalFat) VALUES ('{date}', '{type}', {totCarbo}, {totPro}, {totFat})"
    else:
        query = f"UPDATE MealByDayAndType SET TotalCarbo = Totalcarbo + {totCarbo}, TotalProtein = TotalProtein + {totPro}, TotalFat = TotalFat + {totFat} WHERE Type = '{type}' and Day = '{date}'"
    cursor.execute(query)
    cursor.commit()
    x = pd.read_sql(f"SELECT COUNT(*) as cont FROM MealByDay WHERE  Day = '{date}'", st.session_state.db)
    if x['cont'][0] == 0:
        query = f"INSERT INTO MealByDay (Day, TotalCarbo, TotalProtein, TotalFat) VALUES ('{date}', {totCarbo}, {totPro}, {totFat})"
    else:
        query = f"UPDATE MealByDay SET TotalCarbo = Totalcarbo + {totCarbo}, TotalProtein = TotalProtein + {totPro}, TotalFat = TotalFat + {totFat} WHERE Day = '{date}'"
    cursor.execute(query)
    cursor.commit()
    

st.title('NEW MEAL')
st.markdown('######')

st.session_state.switchToNewMeal = False

query = "SELECT Name FROM ValoriNutrizionali"
foodName = pd.read_sql(query, st.session_state.db)

food = []
amounts = []
maxNum = 11

col1, col2, col3 = st.columns([2, 2, 1])
date = str(col1.date_input(label='Date', value='today', format="DD/MM/YYYY", max_value=datetime.date.today(), min_value=datetime.date(1111, 11, 11))).replace('-', '/')
type = col2.selectbox(label='', options=('Breakfast', 'Lunch', 'Dinner', 'Snack'), index=None, placeholder='Insert meal type')
num = col3.selectbox(label = 'Number of foods', options=range(1, maxNum), index=0, placeholder='Insert number of foods')
st.write('')
col1, col2, col3 = st.columns([2, 2, 1])
if num != None:
    for i in range(num):
        #col1, col2, col3, col4 = st.columns(4)
        food.append(col1.selectbox(label =' '*i, options=foodName['Name'].sort_values(), index = None, placeholder='Select a food', label_visibility='collapsed'))
        amounts.append(col2.number_input(label=' '*i, placeholder='Insert food amount (in grams)', value=None, label_visibility='collapsed'))

height = num*40 + (num-1)*16
string = f"""
<style>
button[kind='primary'] (
    height: {height}px;
)
</style>
""".replace('(', '{').replace(')', '}')
st.markdown(string,
    unsafe_allow_html=True,
)
#col4.write('')
#col4.write('')
if col3.button('**INSERT**', type='primary', use_container_width=True):
    if date == '1111/11/11':
        st.switch_page('pages/updateValoriNutrizionali.py')
    if type == None:
        st.markdown("## You have to select a meal type!!")
    else:
        insert(food, amounts, date, type)
        st.switch_page('pages/inserted.py')