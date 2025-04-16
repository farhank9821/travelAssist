import requests
import google.generativeai as genai
from decoy import weather_api_key as x
from decoy import coordinates_api_key as y
from decoy import gemini_api_key as z
import streamlit as st

def get_weather(city: str, api_key: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        visibility = data["visibility"]
        return f"{weather.title()}, {temp}°C, {visibility}"
    else :
        return "weather data not available"
    


def get_coordinates(city, api_key):
    url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        lat = data["features"][0]["properties"]["lat"]
        lon = data["features"][0]["properties"]["lon"]
        return lat, lon
    
    else:
        return None, None
    

#fetching nearby tourist places from given lat, lon, in circle with radius = 5000
def get_top_places(lat, lon,api_key):
    url = f"https://api.geoapify.com/v2/places?categories=tourism.sights&filter=circle:{lon},{lat},5000&limit=10&apiKey={api_key}"
    respnse = requests.get(url)
    if respnse.status_code == 200:
        data = respnse.json()
        places = []
        #getting name of places, using if cause there might be a case where there is no name
        for place in data["features"]:
            if place["properties"].get("name"):
                places.append(place["properties"]["name"])

        return places
    else:
        return []
    


weather_api_key = x
coordinates_api_key = y
gemini_api_key = z



def generate_travel_plan(city, days, mood, weather_api_key, geoapify_key, gemini_key):
    
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    lat, lon = get_coordinates(city, geoapify_key)
    weather = get_weather(city, weather_api_key)
    places = get_top_places(lat, lon, geoapify_key)

    prompt = f"""
You are a friendly and smart travel planner.

Create a {days}-day travel itinerary for {city.title()}.

User preferences: {mood}

Weather forecast: {weather}

Recommended attractions: {', '.join(places)}

Organize the plan day-by-day with variety, suggest food/activities suited to the mood, and be creative but realistic.
"""

    response = model.generate_content(prompt)
    return response.text


st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.markdown("<h1 style='color:#1A1A1A;'>TravelAssist : Your travel planner</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #FFA55D;
    }

    /* Title styling */
    h1 {
        color: #1A1A1A;
        font-size: 48px;
        text-align: center;
    }

    h2 {
       color: #1A1A1A;
       font-size: 35px;
    }

    /* Label styling (text_input, slider) */
    label, .st-bc {
        color: #1A1A1A !important;
        font-size: 20px !important;
    }

    /* Input field (text_input) background and text color */
    input[type="text"] {
        background-color: #FFF5E6;
        color: #1A1A1A;
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }

    /* Slider text */
    .stSlider .css-1m1f8hn {
        color: #1A1A1A !important;
        font-size: 18px !important;
    }

    /* Button styling */
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
    """,
    unsafe_allow_html=True
)


city = st.text_input(" Where do you want to go? ")
days = st.slider("How many days? ", 1,10,3)
mood = st.text_input("Describe your ideal vibe or goal for this trip (e.g., romantic, adventurous, chill, foodie): ")

if st.button("Generate Plan"):
    with st.spinner("Planning your trip..."):
        plan = generate_travel_plan(city, days, mood, weather_api_key, coordinates_api_key, gemini_api_key)
        st.success("Here's your travel itinerary!")
        st.write(plan)




