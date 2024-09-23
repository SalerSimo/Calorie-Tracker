import streamlit as st
import pandas as pd

st.title('Insert a new food')
st.header('')

col1, col2, col3, col4 = st.columns(4)

col1.write('Name')
col2.write('Carb')
col3.write('Protein')
col4.write('Fat')

col1, col2, col3, col4 = st.columns(4)
name = col1.text_input('Name', placeholder='Name', label_visibility='collapsed')
carb = col2.number_input('Carb', placeholder='Carb', label_visibility='collapsed', value=None)
pro = col3.number_input('Protein', placeholder='Protein', label_visibility='collapsed', value=None)
fat = col4.number_input('Fat', placeholder='Fat', label_visibility='collapsed', value=None)

if st.button('insert', use_container_width=True, type='primary'):
    query = f"SELECT COUNT(*) as count FROM ValoriNutrizionali WHERE Name = '{name}'"
    x = pd.read_sql(query, st.session_state.db)
    if x['count'][0] == 0:
        query = f"INSERT INTO ValoriNutrizionali(Name, Carbo, Protein, Fat) VALUES('{name}', {carb}, {pro}, {fat})"
        st.session_state.cursor.execute(query)
        st.session_state.cursor.commit()
        st.header('Inserted success')
    else:
        st.header('food already present!!')