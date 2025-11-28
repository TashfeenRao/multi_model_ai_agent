import streamlit as st

import requests
from streamlit.elements.lib.layout_utils import Height

from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Multi-AI Agent", page_icon=":robot_face:")
st.title("Multi-AI Agent")

model_options = settings.ALLOWED_MODELS

system_prompt = st.text_area("Enter your system prompt", height=70)
query = st.text_area("Enter your query", height=150)
allow_search = st.checkbox("Allow Search")
selected_model = st.selectbox("Select Model", model_options)

if st.button("Ask Agent") and query.strip():
    try:
        logger.info("sending request to backend")
        response = requests.post("http://localhost:9999/chat", json={
            "model": selected_model,
            "query": query,
            "allow_search": allow_search,
            "system_prompt": system_prompt
        })
        if response.status_code == 200:
            agent_response = response.json()["message"]
            logger.info("successfully recieved response")
            st.subheader("Agent Response")
            st.markdown(agent_response.replace(
                "\n", "<br>"), unsafe_allow_html=True)
        else:
            logger.error("Error in chat: %s", response.json()["detail"])
            st.error(response.json()["detail"])

    except Exception as e:
        logger.error(e)
        st.error(f"Error in chat: {e}")
