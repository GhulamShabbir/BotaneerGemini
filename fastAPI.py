from time import sleep
import streamlit as st
import google.generativeai as genai
# from dotenv import load_dotenv
import os
from typing import Dict



with st.sidebar:
    chat_api_key = os.getenv("GEN_AI_KEY") or st.text_input("Makersuite API Key", key="chatbot_api_key", type="password")

    if 'phone' not in st.session_state:
        st.session_state["phone"] = st.text_input("Your Phone Number", key="phone1",placeholder="Your phone number")

    if os.getenv("GEN_AI_KEY"):
        st.success("Key was auto set")

    # add  personal info to the sidebar. Do not use inputs. Use text instead
    st.header("Personal :blue[Info]")
    st.text("👋 Hello, I am Dr. Ghulam Shabbir")
    st.text("👨‍💻 I am a Data Scientist")
    st.text("📧 Email: ghulamshabbir@gmail.com")


st.header("💬 :violet[Botaneer] 🤖", divider='rainbow')

st.caption("🚀 A chatbot powered by Gemini")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": ":blue[What are you looking for ?]"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not chat_api_key:
        st.info("Please add your Chat API key to continue.")
        st.stop()
    if 'phone' not in st.session_state:
        st.info("Please Enter your phone number to continue.")
        st.stop()
    
    try:
        genai.configure(api_key=chat_api_key)
        model = genai.GenerativeModel('gemini-pro')
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = model.generate_content(prompt, stream=True)
        msg = ""
        bucket = st.chat_message("assistant").empty()

        for cha in response:
            sleep(0.07)
            msg += cha.text
            bucket.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        st.error(e.args[0])