try:
    import streamlit as st
    import pint
    import requests
    import time
except ImportError as e:
    print(f"Import Error: {e}")
    exit(1)

# Initialize unit registry and currency converter
ureg = pint.UnitRegistry()

# Define available categories and units
unit_categories = {
    "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch", "nautical_mile", "light_year", "astronomical_unit", "parsec"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour", "knot", "mach"],
    "Temperature": ["degC", "degF", "kelvin"],
    "Weight": ["gram", "kilogram", "metric_ton", "pound", "ounce", "stone", "carat"],
    "Time": ["second", "minute", "hour", "day", "week", "year"],
    "Area": ["meter^2", "kilometer^2", "mile^2", "yard^2", "foot^2", "inch^2", "hectare", "acre"],
    "Volume": ["liter", "milliliter", "meter^3", "centimeter^3", "gallon", "quart", "pint", "cup", "fluid_ounce"],
    "Energy": ["joule", "kilojoule", "calorie", "kilocalorie", "watt_hour", "kilowatt_hour", "electronvolt", "british_thermal_unit"],
    "Data Storage": ["bit", "byte", "kilobyte", "megabyte", "gigabyte", "terabyte", "petabyte"],
    "Pressure": ["pascal", "kilopascal", "bar", "psi", "atmosphere", "mmHg", "torr"],
    "Currency": ["USD", "EUR", "GBP", "INR", "PKR", "AED", "JPY", "CNY"],
    "Force": ["newton", "kilonewton", "pound_force", "dyne"],
    "Density": ["kilogram/meter^3", "gram/centimeter^3", "pound/foot^3"],
    "Magnetism": ["tesla", "gauss", "weber"],
    "Flow Rate": ["meter^3/second", "liter/second", "gallon/minute"],
    "Radiation": ["becquerel", "curie", "gray", "sievert"],
    "Acceleration": ["meter/second^2", "foot/second^2", "standard_gravity", "gal"],
    "Wind Speed": ["meter/second", "kilometer/hour", "mile/hour", "knot"],
    "Data Transfer Rate": ["bit/second", "kilobit/second", "megabit/second", "gigabit/second"]
}

# Expand the facts dictionaries to cover all categories
did_you_know = {
    "Length": "The longest bridge in the world is the Danyang–Kunshan Grand Bridge in China.",
    "Speed": "The fastest land animal is the cheetah, reaching speeds up to 75 mph.",
    "Temperature": "The coldest temperature ever recorded on Earth was -128.6°F in Antarctica.",
    "Weight": "The heaviest recorded blue whale weighed about 199 tonnes!",
    "Time": "The most accurate clock ever built would neither gain nor lose a second in 14 billion years.",
    "Area": "The largest desert is actually Antarctica, not the Sahara.",
    "Volume": "The volume of all Earth's water could fit into a sphere 860 miles in diameter.",
    "Energy": "Lightning strikes contain enough energy to toast 100,000 slices of bread.",
    "Data Storage": "The first hard drive to store one gigabyte cost $40,000 in 1980.",
    "Pressure": "The pressure at the bottom of the Mariana Trench is over 1,000 times normal atmospheric pressure.",
    "Currency": "The first known currency was created by King Alyattes in Lydia, now Turkey, in 600BC.",
    "Force": "The strongest bite force belongs to the Nile Crocodile at 5,000 pounds of force.",
    "Density": "Neutron stars are so dense that a teaspoon would weigh about 4 billion tons.",
    "Magnetism": "The Earth's magnetic poles have completely reversed many times in history.",
    "Flow Rate": "The Amazon River flows about 209,000 cubic meters of water per second.",
    "Radiation": "Bananas are naturally radioactive due to their potassium content.",
    "Hardness": "Diamond is the hardest natural material, scoring 10 on Mohs scale.",
    "Acceleration": "The fastest human acceleration was experienced by John Stapp at 46.2 G.",
    "Wind Speed": "The fastest wind speed ever recorded was 253 mph in Australia.",
    "Data Transfer Rate": "The fastest internet speed ever recorded was 319 Terabits per second."
}

fun_facts = {
    "Length": "A light-year is about 5.88 trillion miles!",
    "Speed": "A bullet travels faster than the speed of sound.",
    "Temperature": "Venus is hotter than Mercury despite being farther from the Sun.",
    "Weight": "A teaspoon of neutron star material weighs billions of tons.",
    "Time": "One day on Venus is longer than its year!",
    "Area": "Russia is larger than the surface area of Pluto.",
    "Volume": "All planets in our solar system could fit between Earth and the Moon.",
    "Energy": "The Sun produces more energy in one second than humanity has used in all of history.",
    "Data Storage": "The human brain can store about 2.5 petabytes of information.",
    "Pressure": "Jupiter's core pressure is about 50 million times Earth's atmospheric pressure.",
    "Currency": "The most expensive currency in the world is the Kuwaiti Dinar.",
    "Force": "A single hurricane releases more energy than 10,000 nuclear bombs.",
    "Density": "Saturn would float in a giant bathtub because its density is less than water.",
    "Magnetism": "Magnets can temporarily lose their magnetism if heated sufficiently.",
    "Flow Rate": "The Gulf Stream moves more water than all of Earth's rivers combined.",
    "Radiation": "Astronauts see flashes of light when cosmic rays hit their eyes.",
    "Hardness": "The hardest natural material after diamond is wurtzite boron nitride.",
    "Acceleration": "Cheetahs can accelerate faster than most sports cars.",
    "Wind Speed": "Jupiter's Great Red Spot has winds up to 400 mph.",
    "Data Transfer Rate": "Quantum networks could be unhackable and super fast."
}

# Initialize session state for conversion history at the very beginning
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

# Display category at the top
st.title(" Laiqely Converter")
category = st.selectbox("Select a Category", list(unit_categories.keys()))

# Theme selection (default to Dark)
theme = st.sidebar.radio("Select Theme", ["Dark", "Light"], index=0)

if theme == "Dark":
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
        
        /* Main title styling */
        .stApp h1 {
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 3.5rem;
            background: linear-gradient(90deg, #00ff95, #00ffcc, #00f2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,255,149,0.2);
            margin-bottom: 2rem;
            padding: 20px 0;
            text-align: center;
            letter-spacing: 2px;
        }
        
        /* All sidebar headings */
        .stSidebar h2, .stSidebar h3, .stSidebar .stSubheader {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 700;
            background: linear-gradient(90deg, #00ffcc, #00f2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
        }
        
        /* Labels and selectbox headings */
        .stSelectbox label, .stNumberInput label {
            font-family: 'Orbitron', sans-serif;
            font-weight: 500;
            font-size: 1.2rem;
            background: linear-gradient(90deg, #00ff95, #00ffcc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
        }
        
        /* Button text */
        .stButton button {
            font-family: 'Orbitron', sans-serif;
            font-weight: 500;
            font-size: 1.1rem;
            background: linear-gradient(90deg, #00ffcc, #00f2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
            border: 2px solid #00ffcc;
        }
        
        /* Radio buttons styling */
        .stRadio > div[role="radiogroup"] > label {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 500;
            font-size: 1rem;
            color: #ffffff !important;
            background: transparent !important;
            -webkit-text-fill-color: #ffffff !important;
            letter-spacing: 1px;
            margin: 0.5rem 0;
        }
        
        /* Success messages */
        .stSuccess {
            background: linear-gradient(90deg, rgba(0,255,149,0.2), rgba(0,242,255,0.2));
            border: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:  # Light Theme
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
        
        /* Main title styling */
        .stApp h1 {
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 3.5rem;
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            padding: 20px 0;
            text-align: center;
            letter-spacing: 2px;
        }
        
        /* Labels and selectbox headings with gradient */
        .stSelectbox label, .stNumberInput label {
            font-family: 'Orbitron', sans-serif;
            font-weight: 500;
            font-size: 1.2rem;
            background: linear-gradient(90deg, #8B0000, #FF0000) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            letter-spacing: 1px;
        }
        
        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e8e8e8, #f5f5f5) !important;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        }
        
        /* Sidebar headings with gradient */
        .stSidebar h2, .stSidebar h3, .stSidebar .stSubheader {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 700;
            font-size: 1.3rem;
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            letter-spacing: 1px;
        }
        
        /* Regular sidebar text in black */
        .stSidebar p, .stSidebar .stMarkdown,
        .stSidebar .stRadio > div[role="radiogroup"] > label {
            font-family: 'Orbitron', sans-serif !important;
            color: black !important;
            -webkit-text-fill-color: black !important;
            background: none !important;
            letter-spacing: 1px;
        }
        
        /* History box styling */
        .stSidebar code {
            background-color: #e8e8e8 !important;
            color: black !important;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 8px;
            margin: 4px 0;
        }
        
        /* Button text */
        .stButton button {
            font-family: 'Orbitron', sans-serif;
            font-weight: 500;
            font-size: 1.1rem;
            background: linear-gradient(90deg, #4ECDC4, #45B7D1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
            border: 2px solid #4ECDC4;
        }
        
        /* Radio buttons styling */
        .stRadio > div[role="radiogroup"] > label {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 500;
            font-size: 1rem;
            color: #333333 !important;
            background: transparent !important;
            -webkit-text-fill-color: #333333 !important;
            letter-spacing: 1px;
            margin: 0.5rem 0;
        }
        
        /* Success messages */
        .stSuccess {
            background-color: #f8f9fa !important;
            color: black !important;
            border: 1px solid #e9ecef !important;
        }
        
        /* Force black text in success message */
        .stSuccess > div {
            color: black !important;
            -webkit-text-fill-color: black !important;
        }
        
        .stSuccess p {
            color: black !important;
            -webkit-text-fill-color: black !important;
        }
        
        /* Background color */
        .stApp {
            background-color: #ffffff;
        }
        
        /* History box styling */
        .stSidebar code {
            background-color: #e8e8e8 !important;
            color: black !important;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 8px;
            margin: 4px 0;
        }
        
        /* Success message (conversion result) styling */
        div[data-testid="stMarkdownContainer"] > div.stSuccess {
            background-color: #f8f9fa !important;
            color: black !important;
            -webkit-text-fill-color: black !important;
        }
        
        div[data-testid="stMarkdownContainer"] > div.stSuccess > * {
            color: black !important;
            -webkit-text-fill-color: black !important;
        }
        
        div[data-testid="stMarkdownContainer"] > div.stSuccess div {
            color: black !important;
            -webkit-text-fill-color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# Language selection
language = st.sidebar.radio("Select Language", ["English", "Urdu"])
if language == "Urdu":
    st.sidebar.title("ترتیبات")

# Get available units for selected category
units = unit_categories[category]

# User selects units
from_unit = st.selectbox("Convert from", units)
to_unit = st.selectbox("Convert to", units)

# User input
value = st.number_input("Enter value", value=0.0)

# Function to get exchange rate
def get_exchange_rate(from_currency, to_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        return data["rates"][to_currency]
    except:
        return None

# Perform conversion
if st.button("Convert"):
    try:
        if category == "Currency":
            rate = get_exchange_rate(from_unit, to_unit)
            if rate:
                result = value * rate
                formatted_result = f"{value} {from_unit} = {result:.2f} {to_unit}"
            else:
                st.error("Unable to fetch current exchange rates. Please check your internet connection and try again.")
                st.stop()
        else:
            result = ureg.Quantity(value, from_unit).to(to_unit)
            formatted_result = f"{value} {from_unit} = {result}"
        
        # Add to conversion history with styled markdown
        timestamp = time.strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {category}: {formatted_result}"
        
        if 'conversion_history' not in st.session_state:
            st.session_state.conversion_history = []
        st.session_state.conversion_history.append(history_entry)
        
        # Display history with custom styling
        st.sidebar.markdown("---")
        st.sidebar.subheader("Conversion History")
        for item in reversed(st.session_state.conversion_history[-5:]):
            st.sidebar.markdown(f"""
                <div style="
                    background-color: #e8e8e8;
                    color: black;
                    padding: 8px;
                    margin: 4px 0;
                    border: 1px solid #d1d1d1;
                    border-radius: 4px;
                    font-family: monospace;
                ">
                    {item}
                </div>
            """, unsafe_allow_html=True)
              # Using markdown with custom HTML and larger font size only
        st.markdown(f'<div style="padding: 1rem; background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 0.25rem; color: black; font-size: 1.5rem;">{formatted_result}</div>', unsafe_allow_html=True)


    except Exception as e:
        st.error("Currency conversion failed. Please try again later.")
        st.stop()

# Display facts after conversion history
st.sidebar.markdown("---")  # Add a separator
st.sidebar.subheader("Did You Know?")
if category in did_you_know:
    st.sidebar.info(did_you_know[category])

st.sidebar.subheader("Fun Fact")
if category in fun_facts:
    st.sidebar.success(fun_facts[category])
# 🔚 Footer
st.write("---")
st.write("Built with Streamlit | By Laiqa Eman")
