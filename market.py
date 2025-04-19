import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
from decoy import gemini_api_key

# --- Gemini Setup ---
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Graphs ---
def show_engagement_chart():
    platforms = ["Instagram", "LinkedIn", "Twitter", "Facebook", "YouTube"]
    engagement = [78, 65, 50, 45, 70]

    fig, ax = plt.subplots(figsize=(6, 4))  # Smaller size
    ax.bar(platforms, engagement, color="#1A1A1A")
    ax.set_title("Estimated Engagement by Platform", fontsize=14)
    ax.set_ylabel("Engagement (%)", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)


def show_audience_pie():
    labels = ["Gen Z", "Millennials", "Gen X", "Boomers"]
    sizes = [35, 40, 15, 10]

    fig, ax = plt.subplots(figsize=(5, 5))  # Smaller size
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=["#FF7F50", "#FFD580", "#FFB347", "#FFF5E6"],
        textprops={'fontsize': 10}
    )
    ax.axis("equal")
    st.pyplot(fig)


# --- Prompt Function ---
def generate_strategy(industry, goal, mood):
    prompt = f"""
You are an expert AI assistant for marketing agencies.

Create a tailored marketing strategy for a client in the **{industry}** sector.
Primary goal: **{goal}**
Preferred campaign tone: **{mood}**

Include digital channel suggestions, content ideas, KPI tracking methods, and anything creative using Generative AI.
"""
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit UI ---
st.set_page_config(page_title="GenAI for Marketing", layout="wide")

st.markdown("<h1 style='color:#1A1A1A;'>GenAI Marketing Planner</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
.stApp {
    background-color: #FFA55D;
}
h1 {
    color: #1A1A1A;
    font-size: 48px;
    text-align: center;
}
label, .st-bc {
    color: #1A1A1A !important;
    font-size: 20px !important;
}
input[type="text"] {
    background-color: #FFF5E6;
    color: #1A1A1A;
    font-size: 18px;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
}
.stButton>button {
    background-color: #FF7F50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 18px;
}
.stButton>button:hover {
    background-color: #e0663c;
    color: white;
}
</style>
""", unsafe_allow_html=True)

industry = st.text_input("Industry (e.g., fashion, fintech, healthcare):")
goal = st.text_input("Primary marketing goal (e.g., increase followers, generate leads):")
mood = st.text_input("Preferred tone (e.g., edgy, professional, playful):")

if st.button("Generate Strategy"):
    with st.spinner("Generating plan using Generative AI..."):
        strategy = generate_strategy(industry, goal, mood)
        st.success("Here's your marketing strategy:")
        st.write(strategy)

        st.markdown("### 📊 Marketing Insights")
        show_engagement_chart()
        show_audience_pie()
