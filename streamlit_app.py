import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """
    Choose fruits you want in your custom smoothie.
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)


session = get_active_session()
my_dataframe = session.table('smoothies.public.FRUIT_OPTIONS').select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''

    for chosen_fruit in ingredients_list:
        ingredients_string += chosen_fruit + ' '

    st.write(ingredients_string)

    my_insert_statement = """
        insert into smoothies.public.ORDERS(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """');
    """
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon='✅')