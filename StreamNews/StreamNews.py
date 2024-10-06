import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

st.set_page_config(page_title="네이버 농업 기사 크롤러", page_icon="🌱", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px;
    }
    .stTextInput input {
        border-radius: 5px;
        padding: 10px;
        border: 1px solid #cccccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('🌾 네이버 기사 크롤러')

st.write(
    """
    이 애플리케이션은 네이버 뉴스에서 기사를 검색합니다.
    검색 키워드를 입력하고 버튼을 클릭하여 최신 뉴스를 확인해 보세요!
    """
)

keyword = st.text_input("검색 키워드를 입력하세요:")

start_date = st.date_input("시작 날짜", datetime.date.today() - datetime.timedelta(days=7))
end_date = st.date_input("종료 날짜", datetime.date.today())

if st.button('검색'):
    if keyword:
        search_url = f'https://search.naver.com/search.naver?where=news&query={keyword}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            for item in soup.select('div.news_area'):
                title_tag = item.select_one('a.news_tit')
                if title_tag:
                    title = title_tag.get_text()
                    link = title_tag['href']
                    source = item.select_one('.press').get_text() if item.select_one('.press') else '출처 없음'
                    date_tag = item.select_one('.info_group .info')
                    date = date_tag.get_text() if date_tag else '날짜 없음'
                    articles.append({'제목': title, '출처': source, '날짜': date, '링크': f'[링크 보기]({link})'})

            if articles:
                articles_df = pd.DataFrame(articles)
                st.write(articles_df.to_html(escape=False), unsafe_allow_html=True)

            else:
                st.warning("관련 기사를 찾을 수 없습니다.")
        else:
            st.error("네이버 뉴스에 접근할 수 없습니다. 다시 시도해주세요.")
    else:
        st.warning("키워드를 입력해주세요.")