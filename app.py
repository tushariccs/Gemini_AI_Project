import google.generativeai as genai
import os
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science.
from dotenv import load_dotenv
load_dotenv()
# Reads the key,value pair from .env and adds them to environment variable. It is great of managing app settings during development and in production using 12-factor principles.
genai.configure(api_key="AIzaSyBHd1O33-1ZuNeZSwJbaWAvQB-AkhTdteY")

# function to load Gemini pro model and get response

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

chunk_data = ""
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    # print(response)
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
    # print(response)
    ##Add user query and response to session chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The response is")
    
    for chunk in response:
        st.write(chunk.text)
        # print(chunk.text)
        chunk_data += chunk.text
        print(chunk_data)
        
        # print(st.write(chunk.text))
        st.session_state['chat_history'].append(("Bot",chunk.text))


st.subheader("The chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
    
uri = "mongodb+srv://tusharbhansali2402:Tushariccs@cluster0.vcldeaf.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# ##Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
db = client['GenAI']
collection_create = db["GenAI_Info"]
data = {
    "content":chunk_data
}
collection_create.insert_one(data)