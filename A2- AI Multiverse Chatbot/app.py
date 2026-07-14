import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

st.title("Multiverse Chatbot")
personality = st.sidebar.selectbox("Select anyone", ["A.P.J Abdul kalam", "An expert Hacker", "Donald Trump", "Sherlock Holmes", "Albert Einstein", "Elon Musk", "Stand-up Comedian", "Friendly Teacher", "Motivational Coach", "Angry HOD"])

intensity = st.sidebar.slider("Intensity", min_value=1, max_value=10)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_message = st.text_input("Say something : ")
if st.button("SEND"):
    if user_message:
        if personality == "A.P.J Abdul kalam":
            bot_avatar = "🚀"

        elif personality == "An expert Hacker":
            bot_avatar = "💻"

        elif personality == "Donald Trump":
            bot_avatar = "🇺🇸"

        elif personality == "Sherlock Holmes":
            bot_avatar = "🕵️"

        elif personality == "Albert Einstein":
            bot_avatar = "🧠"

        elif personality == "Elon Musk":
            bot_avatar = "🚀"

        elif personality == "Stand-up Comedian":
            bot_avatar = "😂"

        elif personality == "Friendly Teacher":
            bot_avatar = "👨‍🏫"

        elif personality == "Motivational Coach":
            bot_avatar = "💪"

        elif personality == "Angry HOD":
            bot_avatar = "😠"

        else:
            bot_avatar = "🤖"

        ai_instructions= f"You are acting as {personality}.Make sure to maintain the intensity of reply based on {intensity}/10. Respond to the message sent by the user staying completely in character: {user_message} "

        with st.spinner("Connecting Multiverse...."):
            response = client.models.generate_content(
                model= "gemini-2.5-flash",
                contents=ai_instructions
            )
            with st.chat_message("user"):
                st.write(user_message)
            
            with st.chat_message("assistant", avatar= bot_avatar):
                st.write(response.text)

    else :
        st.warning("Please type a message first")