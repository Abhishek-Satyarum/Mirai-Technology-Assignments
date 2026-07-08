import streamlit as st
st.title("The Echo Interface")
st.write("Enter your name and message, then click Send.")

user_name = st.text_input("Enter your name")
user_message = st.text_input("Enter your Message")

if st.button("Send"):
    if user_name == "" :
        st.error("Please provide your name")
    elif user_message == "" :
        st.warning("Please type a message to transmit.")
    else :
        characters = len(user_message)
        token_count = characters/4

        st.info(f"System Check: Your message will consume approximately {token_count} tokens from our context window.")
        st.success(f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}")
