import streamlit as st

POSTS_PER_PAGE = 10
BLOCK_SIZE = 5


def get_current_page():
    return int(st.query_params.get("page", 1))


def get_pagination_range(current_page, total_pages):
    current_block = (current_page - 1) // BLOCK_SIZE
    start_page = current_block * BLOCK_SIZE + 1
    end_page = min(start_page + BLOCK_SIZE - 1, total_pages)
    return start_page, end_page


def show(db):
    st.title("FAQ")
    columns = ["title", "content"]
    table = "faq"
    all_posts = db.get_data(columns=columns, table=table)

    total_posts = len(all_posts)
    total_pages = (total_posts - 1) // POSTS_PER_PAGE + 1
    current_page = get_current_page()
    st.session_state.page = current_page

    start_idx = (current_page - 1) * POSTS_PER_PAGE
    end_idx = start_idx + POSTS_PER_PAGE
    page_posts = all_posts[start_idx:end_idx]

    for post in page_posts:
        with st.expander(post["title"]):
            st.markdown(post["content"])

    start_page, end_page = get_pagination_range(current_page, total_pages)
    num_buttons = end_page - start_page + 1
    button_cols = st.columns(num_buttons + 2)

    if start_page > 1:
        with button_cols[0]:
            if st.button("«"):
                st.query_params.update(page=start_page - 1)
                st.rerun()

    for idx, i in enumerate(range(start_page, end_page + 1), start=1):
        with button_cols[idx]:
            label = f"**{i}**" if i == current_page else str(i)
            if st.button(label, key=f"page-{i}"):
                st.query_params.update(page=i)
                st.rerun()

    if end_page < total_pages:
        with button_cols[-1]:
            if st.button("»"):
                st.query_params.update(page=end_page + 1)
                st.rerun()
