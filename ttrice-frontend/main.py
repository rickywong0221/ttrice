import streamlit as st
import requests
import pandas as pd
from typing import List

API_URL = 'http://backend-service:8000/'


def greetings() -> None:
    response = requests.get(API_URL)
    if response.status_code == 200:
        result = response.json()
        greeting = result.get('Greeting')
        st.write(f'{greeting}')
    else:
        st.error(f'Error: {response.status_code}')


def get_menu() -> (List[str], int):
    day_of_week = st.text_input('今日係星期幾?')

    if day_of_week not in ['1', '2', '3', '4', '5']:
        st.warning('請輸入介於 1 到 5 的數字')

    if day_of_week:
        st.write(f'你的輸入是星期{day_of_week}')

    if day_of_week:
        if day_of_week:
            endpoint = f'menu/{day_of_week}'
            response = requests.get(API_URL + endpoint)
            if response.status_code == 200:
                result = response.json()
                if len(result) > 0:
                    menu_items = [item.get("name") for item in result]
                    df = pd.DataFrame(menu_items, columns=['是日餐單'])
                    print(df)
                    st.table(df)
                    return menu_items, day_of_week
                else:
                    st.write(f'星期{day_of_week}沒有餐點')
            else:
                st.error(f'Error: {response.status_code}')


def create_ricebox(items: List[str], wday: int) -> None:
    selected_menu_items = st.multiselect('選擇餐點加入飯盒', options=items, default=[], max_selections=2)
    st.write('已選擇的餐點:')
    for item in selected_menu_items:
        st.write(f'- {item}')


    if len(selected_menu_items) == 2:
        payload = {
            "dish1": selected_menu_items[0],
            "dish2": selected_menu_items[1],
            "weekday": wday
        }
        endpoint = "create_ricebox"
        try:
            response = requests.post(API_URL + endpoint, data=payload)
            if response.status_code == 200:
                result = response.json()
                message = result.get('message')
                st.success(f'API Response: {message}')
            else:
                st.error(f'Error: {response.status_code}')
        except requests.exceptions.RequestException:
            st.error("An error occurred while creating the ricebox")
    elif len(selected_menu_items) == 1:
        st.warning('請選擇兩個餐點')
    else:
        st.warning('請選擇餐點')


if __name__ == "__main__":
    st.title('兩餸飯！')
    greetings()
    menu_items, wday = get_menu()
    create_ricebox(menu_items, wday)


