import streamlit as st

API_URL = st.secrets["API_URL"]
cookie = st.session_state.session.cookies.get_dict()

col1, col2 = st.columns(2)

with col1:
    graph_id = st.text_input("Enter Graph Id")
    if st.button("Edit Graph"):
        try:
            if graph_id == "":
                raise ValueError
            response = st.session_state.session.get(f"{API_URL}/user/update/{graph_id}", cookies=cookie)
            if response.status_code == 200:
                st.session_state.graph_update = {"update": True, "graph_id": graph_id}
                st.switch_page("pages/table_page.py")
            elif response.status_code == 404:
                st.error("Graph id does not exist")
            elif response.status_code == 422:
                st.error("Graph please enter a valid graph id")
            else:
                st.error(response.text)
        except ValueError:
            st.error("Please enter a graph id")

with col2:
    graph_id = st.text_input("Enter Graph Id", key="graph_id")
    if st.button("Delete Graph"):
        response = st.session_state.session.delete(f"{API_URL}/graph/{graph_id}", cookies=cookie)
        if response.status_code == 200:
            st.success("successfully deleted graph")
        else:
            st.error(response.text)