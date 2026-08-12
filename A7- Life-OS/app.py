import streamlit as st
import pandas as pd
import requests
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_client() :
    return genai.Client(api_key= os.getenv("GEMINI_API_KEY"))
client = get_client()

st.set_page_config(
    page_title="Life-OS",
    page_icon="📱",
    layout="wide"
)

st.title("Life-OS")
st.caption("Your AI Powered Digital Wellbeing Dashboard")
df = pd.read_csv("screentime.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("Dashboard Controls")
selected_date =st.sidebar.selectbox(
    "Select Date",
    sorted(df["Date"].dt.strftime("%Y-%m-%d").unique())
)
daily_goal = st.sidebar.slider(
    "Daily Screen Time Goal (minutes)",
    min_value=60,
    max_value=600,
    value=240,
    step=30
)
today_df = df[df["Date"].dt.strftime("%Y-%m-%d") == selected_date]

#KPI Cards

total_time = today_df["Minutes_Used"].sum()
most_used_app = today_df.loc[
    today_df["Minutes_Used"].idxmax(),
    "App_Name"
]
difference = total_time - daily_goal

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "📱 Total Screen Time",
        f"{total_time} min"
    )

with col2:
    st.metric(
        "🔥 Most Used App",
        most_used_app
    )

with col3:
    st.metric(
        "🎯 Goal Status",
        f"{difference:+} min",     #{difference:+} shows the sign
        delta_color="inverse"
    )

#Line chart
st.divider()

st.subheader("14-Day Screen Time Trend")

daily_usage = (
    df.groupby("Date")["Minutes_Used"]
      .sum()
      .sort_index()
)

st.line_chart(daily_usage)

#Bargraph
col1, col2 = st.columns(2)

with col1:
    st.subheader("App Usage")

    app_usage = (
        today_df.groupby("App_Name")["Minutes_Used"]
        .sum()
    )

    st.bar_chart(app_usage)

with col2:
    st.subheader("Category Usage")

    category_usage = (
        today_df.groupby("Category")["Minutes_Used"]
        .sum()
    )

    st.bar_chart(category_usage)

def summarize_day(data):

    summary = (
        data.groupby("Category")["Minutes_Used"]
        .sum()
        .reset_index()
    )
    return summary.to_string(index = False)

if "ai_advice" not in st.session_state:
    st.session_state.ai_advice = None

if "avatar_image" not in st.session_state:
    st.session_state.avatar_image = None
summary = summarize_day(today_df)

col1, col2 = st.columns([2,1])

if st.button("Analyze My Digital Life", use_container_width=True):
    with col1:
            prompt = f"""
        You are Life-OS.

        You are an honest but supportive productivity and wellbeing coach.

        Today's screen time summary is:

        {summary}

        Analyze this data.

        Do NOT simply tell the user to reduce screen time.

        Instead:

        - Identify unhealthy patterns.
        - Identify productive habits.
        - Suggest physical real-world replacements.
        - Mention fitness, reading, hobbies, sleep or social life whenever appropriate.
        - Give practical advice.
        - Keep the response under 200 words.
        """

            with st.spinner("Analyzing your digital habits..."):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                st.session_state.ai_advice = response.text
                advice = response.text
                if total_time > daily_goal:
                    st.warning(advice)
                else:               
                    st.info(advice)

    with col2:
            avatar_prompt = f"""
            You are an AI image prompt engineer.

            Today's screen time summary:

            {summary}

            Generate ONLY one image prompt.

            Rules:
            - If the user's habits are unhealthy, create a symbolic scene (e.g. a tired zombie addicted to a glowing phone, dark room, exhausted eyes).
            - If the habits are balanced, create a motivated character (e.g. focused warrior, productive student, healthy lifestyle).
            - Make it cinematic and highly detailed.
            - Do not explain anything.
            Return only the image prompt.
            """

            avatar = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=avatar_prompt
            )
            image_prompt = avatar.text.strip()
            image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"

            try:
                response= requests.get(image_url, timeout=15)

                if response.status_code== 200:
                    st.session_state.avatar_image = response.content
                    
                    st.image(
                        response.content,
                        caption="AI Reflection",
                        width= 400,
                            # use_container_width= True
                    )
                else:
                    st.toast("Avatar server is busy")

            except Exception:
                st.toast("Unable to generate the avatar.")

score = max(0, 100 - int((total_time/daily_goal)*40))

st.progress(score/100)

st.metric(
    "🌱 Wellness Score",
    f"{score}/100"
)

st.divider()

st.markdown(
"""
### 🌿 Remember

> **Technology should empower your life, not control it.**

Small daily improvements create lasting habits.
Stay mindful. Stay productive.
"""
)

st.markdown("---")
st.caption(
    "Built with ❤️ using Streamlit • Gemini AI • Pandas • Pollinations AI"
)