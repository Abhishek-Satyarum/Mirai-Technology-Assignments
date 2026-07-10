import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

st.title("Multiverse Chatbot")
personality = st.selectbox("Select anyone", ["A.P.J Abdul kalam", "An expert Hacker", "Donald Trump", "Sherlock Holmes", "Albert Einstein", "Elon Musk", "Stand-up Comedian", "Friendly Teacher", "Motivational Coach", "Angry HOD"])

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_message = st.text_input("Say something : ")
if st.button("SEND"):
    if user_message:
        ai_instructions= f"You are acting as {personality}.Respond to the message sent by the user staying completely in character: {user_message} "

        with st.spinner("Connecting Multiverse...."):
            response = client.models.generate_content(
                model= "gemini-2.5-flash",
                contents=ai_instructions
            )
            st.success("Message received!")
            st.write(response.text)

    else :
        st.warning("Please type a message first")
