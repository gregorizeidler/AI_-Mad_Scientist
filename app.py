import streamlit as st
import openai
import base64
from fpdf import FPDF
import os
import datetime
import json
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import uuid  # Add UUID for custom agent IDs

# Load environment variables
load_dotenv()

# Secure OpenAI API configuration
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_KEY_HERE")

# Page settings
st.set_page_config(
    page_title="AI Mad Scientist",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🧪"
)

# Custom CSS styles
st.markdown("""
<style>
    /* Base styles */
    body {
        color: #333;
    }
    
    /* General text styles */
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, 
    .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #333;
    }
    
    /* Header styles */
    .main-header {
        font-size: 2.5rem;
        color: #FF5757;
        text-align: center;
    }
    .subheader {
        font-size: 1.5rem;
        color: #4B9FE1;
        margin-bottom: 20px;
    }
    
    /* Box styles */
    .info-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #333;
    }
    .success-box {
        background-color: #e6ffe6;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
        color: #333;
    }
    
    /* Button styles */
    .stButton>button {
        background-color: #4B9FE1;
        color: white !important;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3283C2;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    .pdf-button>button {
        background-color: #FF5757;
    }
    .pdf-button>button:hover {
        background-color: #E34545;
    }
    
    /* Temperature indicator styles */
    .temp-low {
        color: #2E86C1;
        font-weight: bold;
    }
    .temp-medium {
        color: #E67E22;
        font-weight: bold;
    }
    .temp-high {
        color: #C0392B;
        font-weight: bold;
    }
    
    /* Layout styles */
    .main-tabs {
        margin-top: 20px;
        margin-bottom: 30px;
    }
    
    /* Card styles */
    .custom-agent-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #4B9FE1;
        color: #333;
    }
    
    /* Ensure all text has proper contrast */
    p, h1, h2, h3, h4, h5, h6, li, span, div {
        color: #333;
    }
    
    /* Override for specific styled elements */
    .main-header, .subheader, .temp-low, .temp-medium, .temp-high {
        color: inherit;
    }
    
    /* Fix for dark backgrounds - make text BRIGHTER WHITE */
    .st-emotion-cache-fblp2m {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    .st-emotion-cache-r421ms {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    .st-emotion-cache-10trblm {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    .st-emotion-cache-16idsys {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    .st-emotion-cache-183lzff {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* Ensure sidebar text is bright white on dark background */
    .st-emotion-cache-1gulkj5 {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* Ensure black background elements have bright white text */
    [data-baseweb="select"] {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* Make all text in black backgrounds bright white */
    .stMarkdown div[style*="background-color: black"] * {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    .stExpander details {
        color: #ffffff !important;
    }
    
    /* For Streamlit's dark theme elements */
    .stApp [data-testid="stSidebar"] {
        color: #ffffff !important;
    }
    
    /* For Streamlit tab content */
    .stTabs [data-baseweb="tab-panel"] {
        color: #ffffff !important;
    }
    
    /* Streamlit text input, selectors, and other input widgets */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Streamlit multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        color: #ffffff !important;
        background-color: #4B9FE1 !important;
    }
    
    /* Streamlit select box */
    .stSelectbox [aria-selected="true"] {
        color: #ffffff !important;
        background-color: #4B9FE1 !important;
    }
    
    /* Dark theme text color override - MAKE TEXT BRIGHTER */
    @media (prefers-color-scheme: dark) {
        .stApp {
            color: #ffffff !important;
        }
        .stMarkdown, .stText, .stCode pre {
            color: #ffffff !important;
        }
        /* For dark mode specific styles */
        .info-box {
            background-color: #1E1E1E;
            color: #ffffff !important;
        }
        .info-box * {
            color: #ffffff !important;
        }
        .custom-agent-card {
            background-color: #1E1E1E;
            color: #ffffff !important;
        }
        .custom-agent-card * {
            color: #ffffff !important;
        }
    }
    
    /* For all black backgrounds - BRIGHT WHITE TEXT */
    *[style*="background-color: #000000"], 
    *[style*="background-color: black"],
    *[style*="background-color: rgb(0, 0, 0)"],
    *[style*="background-color: rgba(0, 0, 0"] {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* Additional dark backgrounds - BRIGHT WHITE TEXT */
    *[style*="background-color: #0E1117"],
    *[style*="background-color: #111"],
    *[style*="background-color: #222"],
    *[style*="background-color: #333"] {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* Streamlit dark mode text colors - BRIGHTER */
    .stApp[data-theme="dark"] p,
    .stApp[data-theme="dark"] span,
    .stApp[data-theme="dark"] div,
    .stApp[data-theme="dark"] h1,
    .stApp[data-theme="dark"] h2,
    .stApp[data-theme="dark"] h3,
    .stApp[data-theme="dark"] h4,
    .stApp[data-theme="dark"] h5,
    .stApp[data-theme="dark"] h6,
    .stApp[data-theme="dark"] li,
    .stApp[data-theme="dark"] .stMarkdown {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* For tabs - ensure selected tab is visible with bright text */
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background-color: #4B9FE1 !important;
        font-weight: bold;
    }
    
    /* For API responses display - BRIGHT GREEN */
    pre {
        color: #00FF00 !important;
        background-color: #0E1117 !important;
        padding: 10px;
        border-radius: 5px;
    }
    
    /* For code blocks - BRIGHT GREEN */
    .stMarkdown code {
        color: #00FF00 !important;
        background-color: #0E1117 !important;
        padding: 2px 5px;
        border-radius: 3px;
    }
    
    /* Extra selectors for dark backgrounds */
    .st-emotion-cache-6qob1r,
    .st-emotion-cache-ue6h4q,
    .st-emotion-cache-1kyxreq,
    .st-emotion-cache-7ym5gk,
    .st-emotion-cache-1erivf3,
    .st-emotion-cache-16txtl3,
    .st-emotion-cache-1dk00sf,
    .st-emotion-cache-lrlib,
    .st-emotion-cache-eczf16,
    .st-emotion-cache-xujd7c,
    .st-emotion-cache-15nt8t8 {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* Additional styles for various dark backgrounds */
    div[style*="background-color: rgb(14, 17, 23)"],
    div[style*="background-color: rgb(30, 30, 30)"],
    div[style*="background-color: rgb(38, 39, 48)"],
    div[style*="background-color: rgb(17, 17, 17)"],
    div[style*="background-color: rgb(0, 0, 0)"],
    div[style*="background-color: rgb(31, 31, 31)"] {
        color: #ffffff !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.2);
    }
    
    /* For Streamlit's built-in dark theme */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
    }
    
    [data-testid="stAppViewContainer"] * {
        color: #ffffff !important;
    }
    
    /* Bright text on Streamlit containers with dark backgrounds */
    .stApp div[data-testid="stBlock"] {
        color: #ffffff !important;
    }
    
    /* Add styling for temperature indicators and general text visibility */
    .temperature-indicator {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        text-shadow: 0 0 2px rgba(0,0,0,0.7);
    }
    .temperature-low {
        background-color: #28a745;
        color: white !important;
    }
    .temperature-medium {
        background-color: #ffc107;
        color: #212529 !important;
    }
    .temperature-high {
        background-color: #dc3545;
        color: white !important;
    }
    
    /* Ensure all text on dark backgrounds is bright */
    .stApp {
        color: #ffffff;
    }
    
    /* Force text in dark mode to be bright white for better visibility */
    .css-6qob1r, .css-10trblm, .css-1oe6wy4, .css-1aehpvj, .css-18ni7ap, 
    .css-1qg05tj, .css-qrbaxs {
        color: #ffffff !important;
        text-shadow: 0 0 2px rgba(0,0,0,0.2);
    }
    
    /* Make all text in black backgrounds bright */
    [data-testid="stMarkdownContainer"] p, 
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #ffffff !important;
    }
    
    /* Additional specificity for dark backgrounds */
    [data-testid="stForm"] label, [data-testid="stForm"] p {
        color: #ffffff !important;
    }
    
    /* Add CSS for temperature spans */
    .temp-low, .temp-medium, .temp-high {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
        color: white !important;
        text-shadow: 0 0 2px rgba(0,0,0,0.7);
    }
    .temp-low {
        background-color: #28a745;
    }
    .temp-medium {
        background-color: #ffc107;
        color: #212529 !important;
    }
    .temp-high {
        background-color: #dc3545;
    }
    
    /* Form controls for better dark mode visibility */
    input, textarea, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        color: #ffffff !important;
        background-color: rgba(35, 39, 47, 0.8) !important;
        border-color: rgba(128, 132, 149, 0.5) !important;
    }
    
    /* Make placeholder text more visible */
    ::placeholder {
        color: rgba(200, 200, 200, 0.7) !important;
        opacity: 1 !important;
    }
    
    /* Improve visibility of labels in dark mode */
    .stSelectbox label, .stSlider label, .stTextInput label, .stTextArea label {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 0 0 2px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='main-header'>🧪 AI Mad Scientist</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Generate bizarre hypotheses, test plausibility, and summarize like a true chaos researcher!</p>", unsafe_allow_html=True)

# Sidebar with settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model options
    st.subheader("Models")
    main_model = st.selectbox(
        "Main model for theory generation",
        ["gpt-4", "gpt-4-turbo", "gpt-4-1106-preview", "gpt-3.5-turbo"],
        index=0
    )
    
    secondary_model = st.selectbox(
        "Secondary model for simple tasks",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0
    )
    
    # Creativity options
    st.subheader("Creativity")
    default_temperature = st.slider(
        "Default temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values = more creative/random responses"
    )
    
    explosive_temperature = st.slider(
        "Temperature for absurd hypotheses",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="The higher, the crazier the theories will be"
    )
    
    # Agent temperature visualization
    st.subheader("Agent Temperatures")
    
    # Define temperatures for each agent
    temperatures = {
        "💣 ExplosiveGPT": explosive_temperature,
        "🧨 EvolutiveGPT": 0.9,
        "📖 NarratorGPT": 0.7,
        "🧠 ConnectorGPT": 0.6,
        "🎤 PitchGPT": 0.6,
        "🔬 TesterGPT": 0.5,
        "👓 CriticGPT": 0.4,
        "💼 ViabilityGPT": 0.4,
        "🧵 SummarizerGPT": 0.3,
        "🔍 ResearcherGPT": 0.4,
        "🛡️ DefenderGPT": 0.7,
        "⚔️ ChallengerGPT": 0.7
    }
    
    # Sort agents by temperature (from most to least creative)
    agents_sorted = sorted(temperatures.items(), key=lambda x: x[1], reverse=True)
    
    # Create DataFrame for visualization
    df_temp = pd.DataFrame(agents_sorted, columns=['Agent', 'Temperature'])
    
    # Add category column
    def categorize_temperature(temp):
        if temp >= 0.8:
            return "High"
        elif temp >= 0.5:
            return "Medium"
        else:
            return "Low"
    
    df_temp['Category'] = df_temp['Temperature'].apply(categorize_temperature)
    
    # Create chart
    fig, ax = plt.subplots(figsize=(4, 3))
    colors = {'High': '#C0392B', 'Medium': '#E67E22', 'Low': '#2E86C1'}
    
    for category, color in colors.items():
        filtered_df = df_temp[df_temp['Category'] == category]
        ax.barh(filtered_df['Agent'], filtered_df['Temperature'], color=color, alpha=0.7)
    
    ax.set_xlim(0, 2.0)
    ax.set_xlabel('Temperature')
    ax.set_title('Agent Creativity Level')
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=colors['High'], lw=4, label='High Creativity'),
        Line2D([0], [0], color=colors['Medium'], lw=4, label='Medium Creativity'),
        Line2D([0], [0], color=colors['Low'], lw=4, label='Low Creativity')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    # Display chart
    st.pyplot(fig)
    
    # Display agent information
    st.subheader("Agent Functions")
    agent_info = {
        "💣 ExplosiveGPT": "Generates absurd hypotheses (temperature <span class='temp-high'>HIGH</span>)",
        "🧨 EvolutiveGPT": "Creates more advanced versions (temperature <span class='temp-high'>HIGH</span>)",
        "📖 NarratorGPT": "Transforms into sci-fi (temperature <span class='temp-medium'>MEDIUM</span>)",
        "🧠 ConnectorGPT": "Connects disciplines (temperature <span class='temp-medium'>MEDIUM</span>)",
        "🎤 PitchGPT": "Creates pitch for investors (temperature <span class='temp-medium'>MEDIUM</span>)",
        "🔬 TesterGPT": "Evaluates scientific plausibility (temperature <span class='temp-medium'>MEDIUM</span>)",
        "👓 CriticGPT": "Makes critical review (temperature <span class='temp-low'>LOW</span>)",
        "💼 ViabilityGPT": "Analyzes practical viability (temperature <span class='temp-low'>LOW</span>)",
        "🧵 SummarizerGPT": "Summarizes in thread format (temperature <span class='temp-low'>LOW</span>)",
        "🔍 ResearcherGPT": "Generates serious research questions (temperature <span class='temp-low'>LOW</span>)",
        "🛡️ DefenderGPT": "Defends the theory with strong arguments (temperature <span class='temp-medium'>MEDIUM</span>)",
        "⚔️ ChallengerGPT": "Challenges the theory with critical arguments (temperature <span class='temp-medium'>MEDIUM</span>)"
    }
    
    for agent, info in agents_sorted:
        st.markdown(f"**{agent}**: {agent_info[agent]}", unsafe_allow_html=True)
    
    # PDF options
    st.subheader("PDF Report")
    title_color = st.color_picker("Title color", "#FF5757")
    include_date = st.checkbox("Include date and time", value=True)
    include_footer = st.checkbox("Include custom footer", value=True)
    footer_text = st.text_input("Footer text", "Generated by AI Mad Scientist")
    
    # Button to save settings
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# Improved API call function
def call_gpt(agent_name, prompt, model=None, temperature=None):
    if model is None:
        model = main_model
    if temperature is None:
        temperature = default_temperature
        
    try:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": f"You are the {agent_name} agent, specialized in {agent_name.lower()} in the field of creative science."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return f"Generation error: {str(e)}"

# Improved function to generate PDF
def generate_pdf(theories_dict, theme, include_metadata=True):
    pdf = FPDF()
    pdf.add_page()
    
    # Font and color configuration
    pdf.set_font("Arial", 'B', size=16)
    pdf.set_text_color(int(title_color.lstrip('#')[0:2], 16), 
                      int(title_color.lstrip('#')[2:4], 16), 
                      int(title_color.lstrip('#')[4:6], 16))
    
    # Report title
    pdf.cell(0, 10, f"Crazy Theory about: {theme}", ln=True, align='C')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Date and time
    if include_date:
        pdf.set_font("Arial", 'I', size=10)
        pdf.set_text_color(100, 100, 100)
        current_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pdf.cell(0, 10, f"Generated on: {current_date}", ln=True, align='R')
        pdf.ln(5)
    
    # Content
    pdf.set_text_color(0, 0, 0)
    for title, text in theories_dict.items():
        pdf.set_font("Arial", style='B', size=12)
        pdf.set_text_color(int(title_color.lstrip('#')[0:2], 16), 
                          int(title_color.lstrip('#')[2:4], 16), 
                          int(title_color.lstrip('#')[4:6], 16))
        pdf.multi_cell(0, 10, title)
        
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(0, 0, 0)
        for line in text.split("\n"):
            pdf.multi_cell(0, 7, line)
        pdf.ln(5)
    
    # Footer
    if include_footer:
        pdf.set_y(-15)
        pdf.set_font('Arial', 'I', 8)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 10, footer_text, 0, 0, 'C')
    
    # Save file with name containing theme and timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    theme_name = ''.join(c if c.isalnum() else '_' for c in theme)[:30]
    file_name = f"theory_{theme_name}_{timestamp}.pdf"
    pdf.output(file_name)
    return file_name

# Function to create download link
def download_link(file_name):
    with open(file_name, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{file_name}" class="download-btn">📥 Download PDF Report</a>'
    return href

# Function to save theory history
def save_theory(theme, agents):
    history_path = "theories_history.json"
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = {
        "date": current_date,
        "theme": theme,
        "agents": agents
    }
    
    try:
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []
            
        history.append(new_entry)
        
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        st.error(f"Error saving history: {str(e)}")
        return False

# Add a new page feature with tabs at the top
st.markdown("""
<style>
    .main-tabs {
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .custom-agent-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #4B9FE1;
    }
</style>
""", unsafe_allow_html=True)

# Create tabs for different sections of the app
tab1, tab2 = st.tabs(["🧪 Theory Generator", "🤖 Custom Agents"])

with tab1:
    # Title and description
    st.markdown("<h1 class='main-header'>🧪 AI Mad Scientist</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Generate bizarre hypotheses, test plausibility, and summarize like a true chaos researcher!</p>", unsafe_allow_html=True)
    
    # Initialize agents at tab scope level
    if 'current_agents' not in st.session_state:
        st.session_state.current_agents = {}
    
    # Initialize agents variable - ensure it's defined
    agents = st.session_state.current_agents
    
    # Original content goes here
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.subheader("🔍 Theme for your crazy theory")
    st.markdown("""
    Choose a theme to explore or generate a random idea. Agents with different creativity temperatures 
    will help develop, analyze, and enrich the theory.
    """)
    
    # Text input and examples
    col1, col2 = st.columns([3, 1])
    with col1:
        # If we have a theme in session_state, use it as default value
        theme_default = st.session_state.get('theme', "neuroscience and blockchain")
        theme = st.text_input("Enter a theme to explore:", value=theme_default)

    with col2:
        if st.button("🎲 Theme + Random Idea"):
            random_themes = [
                "trees and cryptography",
                "seahorses and robotics",
                "black holes and nutrition",
                "mushrooms and internet",
                "geology and electronic music",
                "dinosaurs and artificial intelligence",
                "coral reefs and virtual reality",
                "mitochondria and blockchain",
                "bees and cybersecurity",
                "volcanoes and social networks"
            ]
            import random
            random_theme = random.choice(random_themes)
            st.session_state.theme = random_theme
            
            # Also generate an automatic hypothesis using ExplosiveGPT
            with st.spinner(f"🎲 Generating crazy idea about {random_theme}..."):
                try:
                    initial_theory = call_gpt(
                        "ExplosiveGPT", 
                        f"Create a creative, unusual, and absurd scientific hypothesis about: {random_theme}. Be extremely imaginative!",
                        model=main_model,
                        temperature=explosive_temperature + 0.2  # Even more creative
                    )
                    
                    # Store the theory in the session
                    if "initial_theory" not in st.session_state:
                        st.session_state.initial_theory = {}
                    
                    st.session_state.initial_theory[random_theme] = initial_theory
                    
                    # Show the generated idea in an expander
                    with st.expander(f"💣 Crazy idea generated about: {random_theme}", expanded=True):
                        st.markdown(f"**Theme:** {random_theme}")
                        st.markdown("**Generated hypothesis:**")
                        st.write(initial_theory)
                        st.info("This idea is ready to be used when you click 'Generate Crazy Theory'. You can continue with this idea or generate another one.")
                        
                    # Force interface update to show the new theme in the input
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating initial theory: {str(e)}")
                    # Still update the theme
                    theme = random_theme

    # Generation options
    col1, col2 = st.columns(2)
    with col1:
        # Get custom agents from session state if they exist
        if 'custom_agents' not in st.session_state:
            st.session_state.custom_agents = {}
        
        # Include custom agents in the selection
        all_agents = ["💣 ExplosiveGPT", "🔬 TesterGPT", "🧠 ConnectorGPT", "🧵 SummarizerGPT", 
             "🧨 EvolutiveGPT", "👓 CriticGPT", "🎤 PitchGPT", "💼 ViabilityGPT", "📖 NarratorGPT", 
             "🔍 ResearcherGPT", "🛡️ DefenderGPT", "⚔️ ChallengerGPT"]
        
        # Add custom agents to the list
        for agent_id, agent_data in st.session_state.custom_agents.items():
            all_agents.append(f"{agent_data['emoji']} {agent_data['name']}")
        
        selected_agents = st.multiselect(
            "Choose agents to use:",
            all_agents,
            default=["💣 ExplosiveGPT", "🔬 TesterGPT", "🧠 ConnectorGPT", "🧵 SummarizerGPT"]
        )

    with col2:
        mode = st.radio("Generation mode:", ["Standard", "Quick", "Complete", "Debate"])
        if mode == "Quick":
            selected_agents = ["💣 ExplosiveGPT", "🧵 SummarizerGPT"]
        elif mode == "Complete":
            selected_agents = ["💣 ExplosiveGPT", "🔬 TesterGPT", "🧠 ConnectorGPT", "🧵 SummarizerGPT", 
                              "🧨 EvolutiveGPT", "👓 CriticGPT", "🎤 PitchGPT", "💼 ViabilityGPT", "📖 NarratorGPT", "🔍 ResearcherGPT"]
        elif mode == "Debate":
            selected_agents = ["💣 ExplosiveGPT", "🛡️ DefenderGPT", "⚔️ ChallengerGPT", "🧵 SummarizerGPT"]
            
            # Show debate rounds configuration if debate mode is selected
            debate_rounds = st.slider("Number of debate rounds:", min_value=1, max_value=5, value=2)
            st.session_state.debate_rounds = debate_rounds

    st.markdown("</div>", unsafe_allow_html=True)

    # Add a message to show custom agents are being used
    has_custom_agents = False
    for agent in selected_agents:
        emoji_name = agent.split(" ", 1)
        if len(emoji_name) == 2:
            emoji, name = emoji_name
            for agent_id, agent_data in st.session_state.custom_agents.items():
                if f"{agent_data['emoji']} {agent_data['name']}" == agent:
                    has_custom_agents = True
                    break
    
    if has_custom_agents:
        st.info("🤖 You're using custom agents in this generation! Their specific prompts and behaviors will be applied.")

    # Generation button
    if st.button("💥 Generate Crazy Theory", key="generate_btn"):
        # Clear previous agents
        st.session_state.current_agents = {}
        agents = st.session_state.current_agents
        
        # Progress bar
        progress = st.progress(0)
        total_agents = len(selected_agents)
        
        # Model settings based on selections
        model_mapping = {
            "💣 ExplosiveGPT": main_model,
            "🔬 TesterGPT": main_model,
            "🧠 ConnectorGPT": secondary_model,
            "🧵 SummarizerGPT": main_model,
            "🧨 EvolutiveGPT": main_model,
            "👓 CriticGPT": main_model,
            "🎤 PitchGPT": secondary_model,
            "💼 ViabilityGPT": main_model,
            "📖 NarratorGPT": main_model,
            "🔍 ResearcherGPT": main_model,
            "🛡️ DefenderGPT": main_model,
            "⚔️ ChallengerGPT": main_model
        }
        
        # Temperature definition for each agent
        temperature_mapping = {
            "💣 ExplosiveGPT": explosive_temperature,  # High temperature customized by user
            "🧨 EvolutiveGPT": 0.9,                    # High temperature for more daring versions
            "📖 NarratorGPT": 0.7,                     # Medium-high temperature for creative narratives
            "🧠 ConnectorGPT": 0.6,                    # Medium temperature for interdisciplinary connections
            "🎤 PitchGPT": 0.6,                        # Medium temperature for pitches
            "🔬 TesterGPT": 0.5,                       # Medium-low temperature for scientific analysis
            "👓 CriticGPT": 0.4,                       # Low temperature for critical reviews
            "💼 ViabilityGPT": 0.4,                    # Low temperature for viability analysis
            "🧵 SummarizerGPT": 0.3,                   # Even lower temperature for precise summaries
            "🔍 ResearcherGPT": 0.4,                   # Low temperature for serious research questions
            "🛡️ DefenderGPT": 0.7,                     # Medium temperature for persuasive defense
            "⚔️ ChallengerGPT": 0.7                    # Medium temperature for critical challenge
        }
        
        # Start theory generation
        for i, agent_name in enumerate(selected_agents):
            # Check if this is a custom agent
            custom_agent_data = None
            for agent_id, agent_data in st.session_state.custom_agents.items():
                if f"{agent_data['emoji']} {agent_data['name']}" == agent_name:
                    custom_agent_data = agent_data
                    break
            
            if custom_agent_data:
                # This is a custom agent
                with st.spinner(f"{custom_agent_data['emoji']} Processing with {custom_agent_data['name']}..."):
                    # Build dynamic prompt based on the custom agent's purpose
                    if "💣 ExplosiveGPT" in agents:  # Make sure we have a base theory first
                        custom_prompt = f"""You are {custom_agent_data['name']}, a specialized AI with expertise in {custom_agent_data['expertise']}.
                        
Your task is to {custom_agent_data['purpose']} for the following theory:

{agents['💣 ExplosiveGPT']}

{custom_agent_data['instructions']}"""
                        
                        agents[agent_name] = call_gpt(
                            custom_agent_data['name'],
                            custom_prompt,
                            model=main_model,
                            temperature=custom_agent_data['temperature']
                        )
                    else:
                        # This is a custom agent being used as the primary theory generator
                        custom_prompt = f"""You are {custom_agent_data['name']}, a specialized AI with expertise in {custom_agent_data['expertise']}.
                        
Your task is to create an original, creative theory or hypothesis about:

{theme}

{custom_agent_data['instructions']}"""
                        
                        agents[agent_name] = call_gpt(
                            custom_agent_data['name'],
                            custom_prompt,
                            model=main_model,
                            temperature=custom_agent_data['temperature']
                        )
                        
                        # If this is the first agent and it's custom, save it as the primary theory too
                        if "💣 ExplosiveGPT" not in agents:
                            agents["💣 ExplosiveGPT"] = agents[agent_name]
                
            elif agent_name == "💣 ExplosiveGPT":
                with st.spinner(f"💣 Creating absurd hypothesis about {theme}..."):
                    # Check if there's already a pre-generated theory for this theme
                    if hasattr(st.session_state, 'initial_theory') and theme in st.session_state.initial_theory:
                        agents[agent_name] = st.session_state.initial_theory[theme]
                        # Show indicator that the theory was pre-generated
                        st.success("Using the pre-generated crazy idea! 🚀")
                        # Clear the theory from the session to avoid reusing it in future runs
                        del st.session_state.initial_theory[theme]
                    else:
                        # Generate a new theory normally
                        agents[agent_name] = call_gpt(
                            "ExplosiveGPT", 
                            f"Create a creative, unusual, or absurd scientific hypothesis about: {theme}",
                            model=model_mapping[agent_name],
                            temperature=temperature_mapping[agent_name]
                        )
            elif agent_name == "🔬 TesterGPT":
                with st.spinner("🔬 Evaluating scientific plausibility..."):
                    agents[agent_name] = call_gpt(
                        "TesterGPT", 
                        f"""Evaluate the plausibility of the theory below based on real papers and scientific knowledge.

Your response should have two parts:
1. A detailed scientific evaluation of the theory
2. A numerical plausibility score from 0 to 100, where:
   - 0-20: Completely implausible, contradicts established science
   - 21-40: Highly questionable, major scientific obstacles
   - 41-60: Speculative but not impossible
   - 61-80: Plausible with current scientific understanding
   - 81-100: Highly plausible, well-supported by existing science

At the end of your response, include the score in this exact format: "PLAUSIBILITY_SCORE: [number]"

Theory to evaluate:
{agents.get('💣 ExplosiveGPT', 'No base theory available')}""",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
                    
                    # Extract plausibility score
                    try:
                        import re
                        score_match = re.search(r"PLAUSIBILITY_SCORE: (\d+)", agents[agent_name])
                        if score_match:
                            plausibility_score = int(score_match.group(1))
                            st.session_state.plausibility_score = min(100, max(0, plausibility_score))
                        else:
                            st.session_state.plausibility_score = 50  # Default if not found
                    except Exception as e:
                        st.error(f"Error extracting plausibility score: {str(e)}")
                        st.session_state.plausibility_score = 50  # Default in case of error
            elif agent_name == "🧠 ConnectorGPT":
                with st.spinner("🧠 Connecting knowledge areas..."):
                    agents[agent_name] = call_gpt(
                        "ConnectorGPT", 
                        f"Connect the idea below with other disciplines in an innovative way:\n\n{agents.get('💣 ExplosiveGPT', 'No base theory available')}",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "🧵 SummarizerGPT":
                with st.spinner("🧵 Summarizing everything in thread/abstract..."):
                    summarizer_prompt = f"Summarize the theory"
                    if "🔬 TesterGPT" in agents:
                        summarizer_prompt += ", tests"
                    if "🧠 ConnectorGPT" in agents:
                        summarizer_prompt += " and connections"
                    summarizer_prompt += " below as a viral Twitter thread or scientific paper abstract:\n\nIdea: "
                    summarizer_prompt += f"{agents.get('💣 ExplosiveGPT', 'No base theory available')}"
                    
                    if "🔬 TesterGPT" in agents:
                        summarizer_prompt += f"\n\nValidation: {agents['🔬 TesterGPT']}"
                    if "🧠 ConnectorGPT" in agents:
                        summarizer_prompt += f"\n\nInterdisciplinary connection: {agents['🧠 ConnectorGPT']}"
                    
                    agents[agent_name] = call_gpt(
                        "SummarizerGPT", 
                        summarizer_prompt,
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "🧨 EvolutiveGPT":
                with st.spinner("🧨 Upgrading theory (version 2.0)..."):
                    agents[agent_name] = call_gpt(
                        "EvolutiveGPT", 
                        f"Based on this idea:\n{agents.get('💣 ExplosiveGPT', 'No base theory available')}\n\nCreate a 2.0 version that's even more daring or technologically advanced.",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "👓 CriticGPT":
                with st.spinner("👓 Reviewing as a critical scientist..."):
                    agents[agent_name] = call_gpt(
                        "CriticGPT", 
                        f"Write a critical review, peer review style, pointing out flaws or exaggerations in this hypothesis:\n\n{agents.get('💣 ExplosiveGPT', 'No base theory available')}",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "🎤 PitchGPT":
                with st.spinner("🎤 Generating 30-second pitch..."):
                    agents[agent_name] = call_gpt(
                        "PitchGPT", 
                        f"Transform this theory into a 30-second pitch for investors:\n\n{agents.get('💣 ExplosiveGPT', 'No base theory available')}",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "💼 ViabilityGPT":
                with st.spinner("💼 Analyzing practical viability..."):
                    agents[agent_name] = call_gpt(
                        "ViabilityGPT", 
                        f"What would be the cost, time, and feasibility of testing or creating a prototype of this idea?\n\n{agents.get('💣 ExplosiveGPT', 'No base theory available')}",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "📖 NarratorGPT":
                with st.spinner("📖 Transforming into science fiction..."):
                    agents[agent_name] = call_gpt(
                        "NarratorGPT", 
                        f"Write a short science fiction story based on the following idea:\n\n{agents.get('💣 ExplosiveGPT', 'No base theory available')}",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "🔍 ResearcherGPT":
                with st.spinner("🔍 Generating serious research questions..."):
                    agents[agent_name] = call_gpt(
                        "ResearcherGPT", 
                        f"""Transform this creative theory into serious scientific research questions that could be investigated in the real world.

For each research question:
1. Make it scientifically rigorous and testable
2. Ensure it connects to existing scientific disciplines
3. Frame it in a way that could attract legitimate academic interest
4. Suggest potential methodologies or approaches to investigate it

Generate 3-5 research questions of varying complexity, from straightforward to ambitious.

Theory to transform:
{agents.get('💣 ExplosiveGPT', 'No base theory available')}""",
                        model=model_mapping[agent_name],
                        temperature=temperature_mapping[agent_name]
                    )
            elif agent_name == "🛡️ DefenderGPT" or agent_name == "⚔️ ChallengerGPT":
                # Skip these agents initially - they'll be handled in a special debate section below
                continue
            
            # Update progress bar
            progress.progress((i + 1) / total_agents)
        
        # Save to history
        save_theory(theme, agents)
        
        # Update session state with current agents
        st.session_state.current_agents = agents
        
        # Show results with enhanced design
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #4B9FE1;'>🚀 Results</h2>", unsafe_allow_html=True)
        
        # Plausibility meter (if TesterGPT was used)
        if "🔬 TesterGPT" in agents and hasattr(st.session_state, 'plausibility_score'):
            st.markdown("<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
            st.markdown("### 🔬 Plausibility Meter")
            score = st.session_state.plausibility_score
            
            # Determine color and category based on score
            if score <= 20:
                color = "#C0392B"  # Red
                category = "Completely Implausible"
            elif score <= 40:
                color = "#E67E22"  # Orange
                category = "Highly Questionable"
            elif score <= 60:
                color = "#F1C40F"  # Yellow
                category = "Speculative"
            elif score <= 80:
                color = "#2ECC71"  # Light green
                category = "Plausible"
            else:
                color = "#27AE60"  # Dark green
                category = "Highly Plausible"
            
            # Create progress bar
            st.markdown(f"<p style='text-align: center; font-weight: bold;'>Theory Plausibility: {score}/100 - {category}</p>", unsafe_allow_html=True)
            st.progress(score/100)
            
            # Add score interpretation
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.markdown("<p style='text-align: center; font-size: 0.8em; color: #C0392B;'>Implausible</p>", unsafe_allow_html=True)
            col3.markdown("<p style='text-align: center; font-size: 0.8em; color: #F1C40F;'>Speculative</p>", unsafe_allow_html=True)
            col5.markdown("<p style='text-align: center; font-size: 0.8em; color: #27AE60;'>Plausible</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Highlighted summary, if available
        if "🧵 SummarizerGPT" in agents:
            st.markdown("<div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; border-left: 5px solid #4B9FE1;'>", unsafe_allow_html=True)
            st.markdown("### 🧵 Theory Summary")
            st.write(agents["🧵 SummarizerGPT"])
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Other results in expanders
        tabs = st.tabs([k.split(" ")[1] for k in agents.keys()])
        for i, (k, v) in enumerate(agents.items()):
            with tabs[i]:
                st.write(v)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download PDF", key="pdf_btn"):
                file = generate_pdf(agents, theme)
                st.markdown(download_link(file), unsafe_allow_html=True)
                st.success(f"PDF '{file}' generated successfully!")
        
        with col2:
            if st.button("🔄 Generate New Version", key="new_version_btn"):
                st.rerun()
        
        st.markdown("<div class='success-box'>", unsafe_allow_html=True)
        st.success("🎉 Complete theory generated successfully!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Update the session state with the current agents
        st.session_state.current_agents = agents

    # History section
    with st.expander("📚 Generated Theories History"):
        history_path = "theories_history.json"
        if os.path.exists(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    
                if history:
                    for i, item in enumerate(reversed(history)):
                        st.markdown(f"### {i+1}. {item['theme']} ({item['date']})")
                        if st.button(f"View details #{i+1}", key=f"view_{i}"):
                            for k, v in item['agents'].items():
                                with st.expander(k):
                                    st.write(v)
                else:
                    st.info("There's no theory history generated yet.")
            except Exception as e:
                st.error(f"Error loading history: {str(e)}")
        else:
            st.info("There's no theory history generated yet.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>Developed for mad scientists and creative thinkers</p>
        <p style="font-size: 0.8em;">Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)

    # After all regular agents have finished processing, handle the debate if in debate mode
    if mode == "Debate" and "💣 ExplosiveGPT" in agents:
        with st.spinner("🎭 Setting up scientific debate..."):
            debate_transcript = []
            
            # Initialize model and temperature mappings for debate if not already set
            if 'model_mapping' not in locals():
                model_mapping = {
                    "🛡️ DefenderGPT": main_model,
                    "⚔️ ChallengerGPT": main_model
                }
            
            if 'temperature_mapping' not in locals():
                temperature_mapping = {
                    "🛡️ DefenderGPT": 0.7,
                    "⚔️ ChallengerGPT": 0.7
                }
            
            # Initial positions
            with st.spinner("🛡️ Preparing defense position..."):
                initial_defense = call_gpt(
                    "DefenderGPT",
                    f"""You are a passionate scientific defender. Your task is to argue in favor of the following theory, 
                    finding its merits and potential scientific value, even if aspects seem implausible:
                    
                    {agents.get('💣 ExplosiveGPT', 'No base theory available')}
                    
                    Provide a strong, convincing defense using scientific principles and creative thinking. 
                    Focus on the most promising aspects of the theory.""",
                    model=main_model,
                    temperature=0.7
                )
                debate_transcript.append(("🛡️ DefenderGPT", initial_defense))
                
            with st.spinner("⚔️ Preparing challenge position..."):
                initial_challenge = call_gpt(
                    "ChallengerGPT",
                    f"""You are a critical scientific challenger. Your task is to challenge the following theory,
                    pointing out its flaws, logical inconsistencies, and scientific implausibilities:
                    
                    {agents.get('💣 ExplosiveGPT', 'No base theory available')}
                    
                    Provide a rigorous, evidence-based critique. Focus on the most problematic aspects of the theory.
                    
                    Also respond to this defense of the theory:
                    {initial_defense}""",
                    model=main_model,
                    temperature=0.7
                )
                debate_transcript.append(("⚔️ ChallengerGPT", initial_challenge))
            
            # Debate rounds
            debate_rounds = st.session_state.debate_rounds
            for round_num in range(1, debate_rounds):
                with st.spinner(f"🛡️ Defender response (round {round_num+1})..."):
                    defense_response = call_gpt(
                        "DefenderGPT",
                        f"""Continue defending the theory by responding to the critique below. 
                        Counter the challenger's arguments with evidence and creative thinking.
                        
                        Original theory:
                        {agents.get('💣 ExplosiveGPT', 'No base theory available')}
                        
                        Challenger's critique:
                        {initial_challenge if round_num == 1 else debate_transcript[-1][1]}
                        
                        Provide a strong counterargument to each point raised by the challenger.""",
                        model=main_model,
                        temperature=0.7
                    )
                    debate_transcript.append(("🛡️ DefenderGPT", defense_response))
                
                with st.spinner(f"⚔️ Challenger response (round {round_num+1})..."):
                    challenge_response = call_gpt(
                        "ChallengerGPT",
                        f"""Continue challenging the theory by responding to the defense below.
                        Identify new flaws and counter the defender's arguments with scientific reasoning.
                        
                        Original theory:
                        {agents.get('💣 ExplosiveGPT', 'No base theory available')}
                        
                        Defender's latest argument:
                        {defense_response}
                        
                        Provide a rigorous critique that addresses the defender's points.""",
                        model=main_model,
                        temperature=0.7
                    )
                    debate_transcript.append(("⚔️ ChallengerGPT", challenge_response))
            
            # Store the debate transcript in the agents dictionary
            agents["🛡️ DefenderGPT"] = debate_transcript[0][1]  # Initial defense
            agents["⚔️ ChallengerGPT"] = debate_transcript[1][1]  # Initial challenge
            
            # Store the full debate transcript in session state
            st.session_state.debate_transcript = debate_transcript
            
    # Process summarizer after debate if needed
    if mode == "Debate" and "🧵 SummarizerGPT" in selected_agents and "💣 ExplosiveGPT" in agents:
        with st.spinner("🧵 Summarizing debate and theory..."):
            # Build debate text from transcript
            debate_text = ""
            for agent, text in st.session_state.debate_transcript:
                debate_text += f"\n\n{agent}:\n{text}"
            
            summarizer_prompt = f"""Summarize both the original theory and the scientific debate that followed.
            Highlight key points from both sides of the debate, and provide a balanced conclusion about the theory's merits and problems.
            Present this as a concise academic summary.
            
            Original theory:
            {agents.get('💣 ExplosiveGPT', 'No base theory available')}
            
            Debate transcript:
            {debate_text}"""
            
            # Ensure model_mapping exists
            if 'model_mapping' not in locals():
                model_mapping = {"🧵 SummarizerGPT": main_model}
            elif "🧵 SummarizerGPT" not in model_mapping:
                model_mapping["🧵 SummarizerGPT"] = main_model
            
            # Ensure temperature_mapping exists
            if 'temperature_mapping' not in locals():
                temperature_mapping = {"🧵 SummarizerGPT": 0.3}
            elif "🧵 SummarizerGPT" not in temperature_mapping:
                temperature_mapping["🧵 SummarizerGPT"] = 0.3
            
            agents["🧵 SummarizerGPT"] = call_gpt(
                "SummarizerGPT",
                summarizer_prompt,
                model=model_mapping["🧵 SummarizerGPT"],
                temperature=temperature_mapping["🧵 SummarizerGPT"]
            )

    # After the highlighted summary, add a special debate view if in debate mode
    if mode == "Debate" and hasattr(st.session_state, 'debate_transcript'):
        st.markdown("<div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        st.markdown("### 🎭 Scientific Debate")
        
        # Create debate tabs for each round
        round_tabs = []
        debate_transcript = st.session_state.debate_transcript
        
        # Determine number of rounds
        num_rounds = len(debate_transcript) // 2
        for round_num in range(num_rounds):
            round_tabs.append(f"Round {round_num+1}")
        
        debate_view = st.tabs(round_tabs)
        
        # Fill each tab with the debate content
        for round_num in range(num_rounds):
            with debate_view[round_num]:
                idx = round_num * 2
                if idx < len(debate_transcript):
                    st.markdown(f"**{debate_transcript[idx][0]}**")
                    st.markdown(debate_transcript[idx][1])
                    st.markdown("---")
                if idx+1 < len(debate_transcript):
                    st.markdown(f"**{debate_transcript[idx+1][0]}**")
                    st.markdown(debate_transcript[idx+1][1])
        
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    # Custom Agents Tab
    st.markdown("<h1 class='main-header'>🤖 Custom Agents</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Create your own specialized agents with custom expertise and behavior</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
    <h3>Create Your Own AI Agents</h3>
    <p>Design specialized agents that can contribute unique perspectives to your theories. 
    Custom agents can focus on specific disciplines, thought processes, or analytical approaches.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize custom agents dictionary in session state if it doesn't exist
    if 'custom_agents' not in st.session_state:
        st.session_state.custom_agents = {}
    
    # Form for creating new agents
    with st.form(key="create_agent_form"):
        st.subheader("Create New Agent")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            emoji = st.text_input("Agent Emoji:", value="🧠", max_chars=1)
        with col2:
            name = st.text_input("Agent Name:", value="CustomGPT", 
                                placeholder="e.g., EnvironmentalistGPT, PhilosopherGPT")
        
        col1, col2 = st.columns(2)
        with col1:
            expertise = st.text_input("Area of Expertise:", placeholder="e.g., environmental science, ancient philosophy")
        with col2:
            temperature = st.slider("Temperature (Creativity):", 0.1, 1.5, 0.7, 0.1,
                                   help="Lower values are more deterministic, higher values are more creative")
            
            # Display the temperature with a visual indicator
            if temperature < 0.4:
                temp_class = "temperature-low"
                temp_label = "Low"
            elif temperature < 0.8:
                temp_class = "temperature-medium"
                temp_label = "Medium"
            else:
                temp_class = "temperature-high"
                temp_label = "High"

            st.markdown(f"""
            <p style="color: #ffffff !important;">Selected temperature: 
            <span class="temperature-indicator {temp_class}">{temp_label} ({temperature:.1f})</span>
            </p>
            """, unsafe_allow_html=True)
        
        purpose = st.text_input("Agent's Purpose:", placeholder="e.g., analyze environmental impact, explore philosophical implications")
        
        instructions = st.text_area("Special Instructions:", 
                                   placeholder="Provide detailed instructions for how this agent should analyze or transform theories",
                                   height=100)
        
        submit_button = st.form_submit_button(label="Create Agent")
        
        if submit_button and name and purpose:
            # Generate a unique ID for the agent
            agent_id = str(uuid.uuid4())
            
            # Ensure emoji is actually an emoji
            if not emoji or len(emoji.strip()) == 0:
                emoji = "🤖"  # Default emoji
            
            # Store agent data
            st.session_state.custom_agents[agent_id] = {
                "emoji": emoji,
                "name": name,
                "expertise": expertise if expertise else "General knowledge",
                "temperature": temperature,
                "purpose": purpose,
                "instructions": instructions if instructions else "Analyze the theory and provide insights."
            }
            
            st.success(f"Agent {emoji} {name} created successfully!")
    
    # Display and manage existing custom agents
    if st.session_state.custom_agents:
        st.subheader("Your Custom Agents")
        
        for agent_id, agent_data in list(st.session_state.custom_agents.items()):
            with st.container():
                st.markdown(f"""
                <div class="custom-agent-card" style="color: #ffffff !important; background-color: rgba(14, 17, 23, 0.8); border-left: 5px solid #4B9FE1;">
                    <h4 style="color: #ffffff !important; font-weight: bold;">{agent_data['emoji']} {agent_data['name']}</h4>
                    <p style="color: #ffffff !important;"><strong style="color: #ffffff !important;">Expertise:</strong> {agent_data['expertise']}</p>
                    <p style="color: #ffffff !important;"><strong style="color: #ffffff !important;">Temperature:</strong> {agent_data['temperature']}</p>
                    <p style="color: #ffffff !important;"><strong style="color: #ffffff !important;">Purpose:</strong> {agent_data['purpose']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add a delete button for each agent
                if st.button(f"Delete {agent_data['name']}", key=f"delete_{agent_id}"):
                    del st.session_state.custom_agents[agent_id]
                    st.rerun()
    else:
        st.info("You haven't created any custom agents yet. Use the form above to create your first agent!")
    
    st.markdown("""
    <div class='info-box' style="color: #ffffff !important; background-color: rgba(14, 17, 23, 0.7);">
    <h3 style="color: #ffffff !important; font-weight: bold;">🧪 Ideas for Custom Agents</h3>
    <ul style="color: #ffffff !important; margin-bottom: 10px;">
        <li style="color: #ffffff !important;">🌱 <strong style="color: #ffffff !important;">EnvironmentalistGPT</strong>: <span style="color: #ffffff !important;">Analyzes environmental implications of theories</span></li>
        <li style="color: #ffffff !important;">🧘 <strong style="color: #ffffff !important;">PhilosopherGPT</strong>: <span style="color: #ffffff !important;">Explores philosophical dimensions and ethical questions</span></li>
        <li style="color: #ffffff !important;">🏛️ <strong style="color: #ffffff !important;">HistorianGPT</strong>: <span style="color: #ffffff !important;">Connects theories to historical contexts and precedents</span></li>
        <li style="color: #ffffff !important;">🎨 <strong style="color: #ffffff !important;">ArtistGPT</strong>: <span style="color: #ffffff !important;">Visualizes and describes theories in artistic terms</span></li>
        <li style="color: #ffffff !important;">🔮 <strong style="color: #ffffff !important;">FuturistGPT</strong>: <span style="color: #ffffff !important;">Projects long-term implications and societal impacts</span></li>
        <li style="color: #ffffff !important;">🧩 <strong style="color: #ffffff !important;">PsychologistGPT</strong>: <span style="color: #ffffff !important;">Analyzes psychological or behavioral aspects</span></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
