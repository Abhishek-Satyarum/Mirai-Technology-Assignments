import streamlit as st
import requests
import random

st.caption("Generate stunning AI images powered by Pollinations AI")

st.title("The AI Image Studio")
st.sidebar.header("Generation Settings")
art_style = st.sidebar.selectbox("Select Art Style", ["Photorealistic", "Water world", "Cartoon", "Sketch", "3D Render"])

width=st.sidebar.slider("Image width",min_value=256,max_value=1024,value=768)
height=st.sidebar.slider("Image height",min_value=256,max_value=1024,value=768)
magic = st.sidebar.checkbox("✨ Enable Magic Enhance")

user_prompt=st.text_input("Decribe the image you want to generate")
random_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon drinking tea in a cafe",
    "A futuristic underwater city",
    "A cat piloting a spaceship"
]

if st.button("Generate Image"):
    if user_prompt:
        with st.spinner("Rendering the image"):
            
            full_prompt = f"{user_prompt}, {art_style} style"

            if magic:
                full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

            url=f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}" # Called as Query
            response=requests.get(url)

            if response.status_code==200:
                st.success("Image Generated")
                # st.write(response)
                # Convert the binary into pixels or an actual image
                st.image(response.content,caption=full_prompt)
                st.download_button(
                    label="Download content",
                    data= response.content,
                    file_name =f"{art_style}_image.png",
                    mime= "image/png" #image/* for option in type
                )
            else:
                st.error("API is not working")
    else:
        st.warning("please add an image description")
        
if st.button("🎲 Surprise Me!"):
    full_prompt = random.choice(random_prompts)

    url = f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}"

    response = requests.get(url)

    if response.status_code == 200:
        st.image(response.content, caption=full_prompt)

        st.download_button(
            "Download Image",
            response.content,
            file_name="surprise_image.png",
            mime="image/png"
        )