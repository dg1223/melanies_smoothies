import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """
    Choose fruits you want in your custom smoothie.
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table('smoothies.public.FRUIT_OPTIONS').select(col('FRUIT_NAME'),col('SEARCH_ON'))
df = my_dataframe.to_pandas()
# st.dataframe(data=df, use_container_width=True)
# st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for chosen_fruit in ingredients_list:
        ingredients_string += chosen_fruit + ' '
        search_on = df.loc[df['FRUIT_NAME'] == chosen_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', chosen_fruit,' is ', search_on, '.')
        
        smoothiefroot_response = requests.get('https://my.smoothiefroot.com/api/fruit/' + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        

    my_insert_statement = """
        insert into smoothies.public.ORDERS(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """');
    """
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon='✅')


