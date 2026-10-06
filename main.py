import string
from pathlib import Path
import streamlit as st
from st_keyup_custom import st_keyup
# cd "C:\Users\KP\OneDrive\Desktop\Python\Projects\Password Strength Checker"

# Check if user inputs a common password
@st.cache_data
def load_common_passwords():
    password_file = Path(__file__).with_name('100k-most-used-passwords-NCSC.txt')
    if password_file.exists():
        with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
            return set(f.read().splitlines())
    return set()

def check_common_password(password):
    return password in load_common_passwords()

def check_length(password):
    return len(password) >= 12

def check_uppercase(password):
    return any(c.isupper() for c in password)

def check_lowercase(password):
    return any(c.islower() for c in password)

def check_number(password):
    return any(c.isdigit() for c in password)

def check_special_char(password):
    return any(c in string.punctuation for c in password)

def calculate_strength(password):
    if check_common_password(password):
        return "Weak", 0

    score = 0
    if check_length(password):
        score += 1
    if check_uppercase(password):
        score += 1
    if check_lowercase(password):
        score += 1
    if check_number(password):
        score += 1
    if check_special_char(password):
        score += 1

    if score <= 2:
        rating = "Weak"
    elif score <= 4:
        rating = "Moderate"
    else:
        rating = "Strong"

    return rating, score

def give_feedback(password):
    if check_common_password(password):
        return ["This password is found in a list of commonly used passwords, choose something unique."]
    tips = []

    if not check_length(password):
        tips.append("Password must be at least 12 characters long.")
    if not check_uppercase(password):
        tips.append("Password must contain 1 uppercase letter.")
    if not check_lowercase(password):
        tips.append("Password must contain 1 lowercase letter.")
    if not check_number(password):
        tips.append("Password must contain 1 number.")
    if not check_special_char(password):
        tips.append("Password must contain 1 special character (eg. ! @ # $ % ).")

    if not tips:
        tips.append("Password meets all criteria.")
    return tips

def estimate_crack_time(password):
    if check_common_password(password):
        return "Instantly ⚠️"

    charset = 0
    if check_lowercase(password):
        charset += 26
    if check_uppercase(password):
        charset += 26
    if check_number(password):
        charset += 10
    if check_special_char(password):
        charset += 32
    if charset == 0:
        charset = 26

    length = len(password)
    combinations = charset ** length
    seconds = combinations / 10000000000

    if seconds < 1:
        return "Instantly ⚠️"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds // 86400)} days"

    years = seconds / 31536000
    if years < 1000:
        return f"{int(years)} years"
    elif years < 1000000:
        return f"{int(years // 1000)} thousand years"
    elif years < 1000000000:
        return f"{int(years // 1000000)} million years"
    else:
        return "Billions of Years...."

# --- UI DISPLAY ---
st.markdown("""
    <style>
    /* Import Cyberpunk Fonts from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&display=swap');

    /* Main Title - Orbitron Font + Pink & Cyan Neon Glow */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00F0FF !important;
        text-shadow: 0 0 8px #00F0FF, 0 0 15px #FF007F !important;
        letter-spacing: 2px;
    }

    /* Section Headers (Feedback Header) */
    h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        color: #FF007F !important;
        text-shadow: 0 0 8px #FF007F !important;
    }

    /* Metric Label & Value (Estimated Crack Time) */
    [data-testid="stMetricLabel"] {
        font-family: 'Share Tech Mono', monospace !important;
        color: #E6EDF3 !important;
        font-size: 1.1rem !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #00F0FF !important;
        text-shadow: 0 0 10px #00F0FF !important;
        font-size: 2.2rem !important;
    }

    /* Feedback List Items & General Text */
    .stMarkdown p {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.05rem !important;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Ties it all together: get input, run checks, print result
st.title("Password Strength Checker")

password = st_keyup(
    "Enter a password to check",
    type="password",
    key="pwd",
)

if password:
    rating, score = calculate_strength(password)
    tips = give_feedback(password)

    st.markdown("---")

    # Single metric display for crack time
    st.metric(label="Estimated Crack Time", value=estimate_crack_time(password))

    # Coloured alert based on score rating
    if rating == "Weak":
        st.error("Weak Password ⚠️")
    elif rating == "Moderate":
        st.warning("Moderate Password ⚠️")
    else:
        st.success("Strong Password ✅")

    st.progress(score / 5)

    st.write("### Feedback")
    for tip in tips:
        if "meets all criteria" in tip:
            st.write(f"✅ {tip}")
        else:
            st.write(f"❌ {tip}")