# frontend/app.py

import streamlit as st
import requests

st.set_page_config(page_title="SQL Agent", page_icon="")

st.title("SQL Agent")
st.markdown(
    "Ask any question about your **orders database** and get real-time insights using GPT + SQL."
)

query = st.text_input(
    "🔍 Your question", placeholder="e.g. How many orders were placed in June 2024?"
)
submit = st.button("🔎 Ask")

if submit and query:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                "http://backend:8000/query",
                json={"question": query},
                timeout=30,  # increased timeout
            )
            if response.status_code == 200:
                result = response.json()["response"]

                if result.lower().startswith("error"):
                    st.error(f"❌ {result}")
                else:
                    st.success("Answer:")
                    st.markdown(f"### {result}")
            else:
                st.error(f"⚠️ Server error: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<small>Built using LangChain, OpenAI, FastAPI, and Streamlit</small>",
    unsafe_allow_html=True,
)
