import streamlit as st
import os
import json
import requests
import tempfile
from gtts import gTTS
from dotenv import load_dotenv
from google import genai
load_dotenv()


st.title("AI Visual Novel")

st.sidebar.title("Story Settings")
genre = st.sidebar.selectbox("Select any one", ["Adventure", "Sci-fi", "Mythology", "Horror", "Cyberpunk"])
art_style = st.sidebar.selectbox("Select any one", ["Photorealistic", "Sketch", "Waterpaint", "Pixel art", "Anime"])

@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

if st.button("Start Story"):

    prompt = f"""
    You are an AI Visual Novel Engine.

    Generate the beginning of a {genre} story.

    Return ONLY valid JSON.

    Do NOT write any explanation.
    Do NOT use markdown.
    Do NOT wrap the JSON inside ```json.
    Return only the JSON object.

    {{
    "story_text":"...",
    "image_prompt":"...",
    "options":[
    "...",
    "...",
    "..."
    ]
    }}

    The image prompt should describe the scene in {art_style} style.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        clean_text = response.text.strip()

        if clean_text.startswith("```"):
            clean_text = clean_text.replace("```json", "")
            clean_text = clean_text.replace("```", "")
            clean_text = clean_text.strip()

        story = json.loads(clean_text)
        


        if "story_history" not in st.session_state:
            st.session_state.story_history = []

        st.session_state.current_story = story
        st.session_state.story_history.append({
        "role": "assistant",
        "story": story
    })
    except Exception:
        st.error("Unable to generate the story. Please try again.")
        st.stop()

if "current_story" in st.session_state:

    story = st.session_state.current_story

    st.subheader("📖 Story")

    for item in st.session_state.story_history:

        if item["role"] == "assistant":

            st.chat_message("assistant").write(
                item["story"]["story_text"]
            )

            image_prompt = item["story"]["image_prompt"]

            url = f"https://image.pollinations.ai/prompt/{image_prompt}"

            try:
                response = requests.get(
                    url,
                    timeout=10
                    )

                if response.status_code == 200:
                    st.image(
                        response.content,
                        caption="Scene",
                        use_container_width=True
                    )
                else:
                    st.toast("Image server busy, skipping visuals...")

            except Exception:
                st.toast("Image server busy, skipping visuals...")

            story_text = item["story"]["story_text"]

            try:
                tts = gTTS(
                    text=story_text,
                    lang="en"
                )

                temp_audio = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3"
                )

                tts.save(temp_audio.name)

                st.audio(temp_audio.name)

            except Exception:
                st.toast("Audio narration unavailable.")

        else:
            st.chat_message("user").write(
                item["content"]
            )
    st.subheader("🎮 Choose your next move")

    for option in story["options"]:
            if st.button(option):

                next_prompt = f"""
Continue exactly from the previous story.

Do not restart the story.

Maintain consistency.

Genre: {genre}

Art Style: {art_style}

The player selected:

{option}

Return ONLY valid JSON.

Do NOT write any explanation.
Do NOT use markdown.
Do NOT wrap the JSON inside ```json.
Return only the JSON object.

{{
"story_text":"...",
"image_prompt":"...",
"options":[
"...",
"...",
"..."
]
}}
"""
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=next_prompt
                    )
                    
                    clean_text = response.text.strip()

                    if clean_text.startswith("```"):
                        clean_text = clean_text.replace("```json", "")
                        clean_text = clean_text.replace("```", "")
                        clean_text = clean_text.strip()

                    try:
                        story = json.loads(clean_text)
                    except Exception:
                        st.error("The AI returned an invalid response.")
                        st.stop()

                    st.session_state.story_history.append(
                        {
                            "role":"user",
                            "content":option
                        }
                    )

                    st.session_state.story_history.append(
                        {
                            "role":"assistant",
                            "story":story
                        }
                    )

                    st.session_state.current_story = story

                    st.rerun()
                except Exception:
                    st.error("Unable to generate the story. Please try again.")
                    st.stop()