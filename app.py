import importlib
import streamlit as st
from mysql_client import MysqlClient


st.set_page_config(page_title="test", initial_sidebar_state="collapsed")


@st.cache_resource
def get_db():
    return MysqlClient(
        host=st.secrets["db"]["host"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        database=st.secrets["db"]["database"],
    )


PAGES = {
    "홈": "home",
    "차량 FAQ": "faq"
}

selection = st.sidebar.selectbox("메뉴", list(PAGES.keys()))

module = importlib.import_module(PAGES[selection])
db = get_db()
module.show(db)
