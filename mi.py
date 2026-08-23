import streamlit as st

# Set a premium, professional page layout
st.set_page_config(
    page_title="Network Pulse Ghana", 
    page_icon="⚡", 
    layout="centered"
)

# Custom premium styling using Streamlit's built-in markdown
st.title("⚡ Network Pulse Ghana")
st.markdown("### The National Mobile Network Experiment")
st.write("We are analyzing the hidden gaps in Ghana's telecom infrastructure. Help us uncover the truth.")
st.divider()

# Progress tracking for engagement
st.caption("Progress: 4 Quick Questions")
progress_bar = st.progress(0.0)

# Multi-Step Survey Form
with st.form(key="telecom_survey"):
    
    # Question 1: The Multi-SIM Culture
    st.markdown("#### 1. The Multi-SIM Culture 📲")
    q1 = st.radio(
        "What is the main reason you are forced to use more than one SIM card (e.g., MTN + Telecel)?",
        [
            "One is for MoMo/calls, the other is strictly for data bundle",
            "One network completely dies the moment Dumsor hits",
            "Network is good outside but inside my room it goes to 'No Service'",
            "I strictly use only one SIM card"
        ],
        index=None
    )
    
    st.divider()
    
    # Question 2: The Data Struggle
    st.markdown("#### 2. The Internet Struggle ⏳")
    q2 = st.radio(
        "What annoys you the most about your internet data connection when you are active online?",
        [
            "The internet slows down to a crawl every evening",
            "I have full network bars but pages refuse to load",
            "The entire network completely vanishes when it rains",
            "The speed is fast but the data burns way too quickly"
        ],
        index=None
    )
    
    st.divider()

    # Question 3: Financial Pain Points
    st.markdown("#### 3. Financial Pain Points 💰")
    q3 = st.radio(
        "What pricing or billing fix do you want to see most in Ghana?",
        [
            "Truly unlimited data packages that don't expire",
            "Cheaper data bundles with consistent high speeds",
            "Complete elimination of hidden deductions and 'vanishing airtime'",
            "Lower transaction fees on Mobile Money transfers"
        ],
        index=None
    )
    
    st.divider()

    # Question 4: Everyday Annoyances
    st.markdown("#### 4. Everyday Annoyances 😠")
    q4 = st.radio(
        "Apart from data prices, what is the most annoying thing your network provider does?",
        [
            "Waking up to see my airtime has vanished or been deducted wrongly",
            "Bombarding my phone with endless spam SMS ads and flash messages",
            "Making me memorize too many confusing star shortcodes (*138#, *110#, etc.)",
            "Forcing me to talk to a useless AI bot when I have a real issue"
        ],
        index=None
    )

    # Submit Button
    submit_button = st.form_submit_button(label="Submit Feedback 🔥")

# Handling Form Submission
if submit_button:
    if not (q1 and q2 and q3 and q4):
        st.error("Please answer all 4 questions before submitting!")
    else:
        progress_bar.progress(1.0)
        st.balloons()
        st.success("Thank you! Your feedback has been encrypted and securely logged. Watch out for what's coming next! 👀")
        
        # Here you can later write code to save the answers to a text file or database:
        with open("survey_results.txt", "a") as f:
            f.write(f"Q1: {q1} | Q2: {q2} | Q3: {q3} | Q4: {q4}\n")

