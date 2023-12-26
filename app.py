import google.generativeai as genai
import os
import streamlit as st
#Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science.
from dotenv import load_dotenv
load_dotenv()
# Reads the key,value pair from .env and adds them to environment variable. It is great of managing app settings during development and in production using 12-factor principles.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Gemini pro model and get response

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

#Intialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
input = st.text_input("Input: ",key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    ##Add user query and response to session chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The response is")
    
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))
        
st.subheader("The chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
    