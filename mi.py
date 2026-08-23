import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
import urllib.request

st.set_page_config(page_title="Network Pulse Ghana", page_icon="⚡", layout="centered")

st.title("⚡ Network Pulse Ghana")
st.markdown("### The National Mobile Network Experiment")
st.write("An open space for Ghanaians to run live latency tests, audit infrastructure, and talk network solutions.")

# 3 Premium Interactive Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 Network Audit", "⏱️ Live Latency Tester", "💬 Community Forum"])

DATA_FILE = "survey_results.csv"
q1_choices = ["One for MoMo/calls, one for data", "One network dies during Dumsor", "Bad signal indoors", "I use only one SIM"]
q2_choices = ["Slows down every evening", "Full bars but no loading", "Vanishes when it rains", "Burns too quickly"]

# --- TAB 1: THE AUDIT SURVEY ---
with tab1:
    st.write("### Log Your Current Experience")
    with st.form(key="telecom_survey"):
        st.markdown("#### 1. The Multi-SIM Culture 📲")
        q1 = st.radio("Why do you use more than one SIM card?", q1_choices, index=None)
        st.divider()
        
        st.markdown("#### 2. The Internet Struggle ⏳")
        q2 = st.radio("What annoys you most about your connection?", q2_choices, index=None)
        st.divider()

        st.markdown("#### 3. Where are you experiencing this? 📍")
        location = st.text_input("Your Current Region/Neighborhood:", placeholder="e.g., Greater Accra - Madina")

        submit_button = st.form_submit_button(label="Log My Feedback 🔥")

    if submit_button:
        if not (q1 and q2 and location.strip()):
            st.error("Please fill out all fields before submitting!")
        else:
            st.balloons()
            st.success("Thank you! Your feedback has been securely logged.")
            
            clean_loc = location.replace(",", " ").strip()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_data = pd.DataFrame([[timestamp, q1, q2, clean_loc, "No custom topic", 0.0]], columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"])
            
            if not os.path.exists(DATA_FILE):
                new_data.to_csv(DATA_FILE, index=False)
            else:
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

# --- TAB 2: NEW FEATURE! LIVE LATENCY TESTER ---
with tab2:
    st.write("### ⏱️ Regional Latency Check")
    st.write("Click below to test your network's response time (latency). High latency means slow loading, even if you have full 4G bars.")
    
    test_region = st.selectbox("Which Region/Town are you testing from right now?", 
                               ["Greater Accra", "Ashanti (Kumasi)", "Western (Takoradi)", "Northern (Tamale)", "Central (Cape Coast)", "Volta (Ho)", "Eastern (Koforidua)", "Other"])
    
    if st.button("⚡ Run Live Ping Test"):
        with st.spinner("Pinging global server network..."):
            latencies = []
            # Run 3 test pings to measure response stability
            for _ in range(3):
                start_time = time.time()
                try:
                    # Open a lightweight connection to measure time-to-first-byte
                    urllib.request.urlopen('https://google.com', timeout=4)
                    end_time = time.time()
                    latencies.append((end_time - start_time) * 1000) # Convert to milliseconds
                except:
                    pass
                time.sleep(0.2)
            
            if latencies:
                avg_latency = round(sum(latencies) / len(latencies), 1)
                
                # Dynamic visual scoring based on results
                if avg_latency < 80:
                    st.success(f"🟢 Excellent Connection! Latency: {avg_latency} ms")
                elif avg_latency < 200:
                    st.warning(f"🟡 Average Connection. Latency: {avg_latency} ms (Expect light delays)")
                else:
                    st.error(f"🔴 Heavy Lag / Congestion. Latency: {avg_latency} ms (Network is crawling)")
                
                # Save the latency test into your database
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                latency_data = pd.DataFrame([[timestamp, "N/A", "N/A", test_region, "Latency Test Log", avg_latency]], columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"])
                
                if not os.path.exists(DATA_FILE):
                    latency_data.to_csv(DATA_FILE, index=False)
                else:
                    latency_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
                    st.caption(f"Latency successfully saved to regional database map under {test_region}.")
            else:
                st.error("❌ Test Failed. Your connection timed out completely.")

    # Show a plain-language summary if data exists
    if os.path.exists(DATA_FILE):
        st.divider()
        st.write("#### 🗺️ Which Regions Are Fastest?")
        df = pd.read_csv(DATA_FILE)
        # Filter rows that have real logged latency numbers
        latency_df = df[df["Latency"] > 0]
        if not latency_df.empty:
            regional_averages = latency_df.groupby("Location")["Latency"].mean().sort_values()
            st.caption("Lower numbers mean a faster response. Fast: under 80 ms | Okay: 80-199 ms | Slow: 200 ms or more")

            for region, average_latency in regional_averages.items():
                average_latency = round(average_latency, 1)
                if average_latency < 80:
                    status = "🟢 Fast"
                elif average_latency < 200:
                    status = "🟡 Okay"
                else:
                    status = "🔴 Slow"

                region_column, latency_column, status_column = st.columns([2, 1, 1])
                region_column.write(f"**{region}**")
                latency_column.metric("Average", f"{average_latency} ms")
                status_column.write(f"**{status}**")
        else:
            st.caption("No latency logs collected yet. Run a test to see regional results!")

# --- TAB 3: THE COMMUNITY DISCUSSION WALL ---
with tab3:
    st.write("### 📢 Public Discussion Wall")
    
    with st.form(key="discussion_form"):
        user_thought = st.text_area("What is on your mind regarding Ghana networks today?", placeholder="Type your experience or ideas here...")
        user_loc = st.text_input("Your Neighborhood (Optional):", placeholder="e.g., East Legon")
        post_button = st.form_submit_button(label="Post to Wall 🚀")
        
    if post_button:
        if not user_thought.strip():
            st.error("You cannot post an empty thought!")
        else:
            st.success("Your thought has been posted live!")
            clean_thought = user_thought.replace(",", " ").replace("\n", " ").strip()
            clean_uloc = user_loc.replace(",", " ").strip() if user_loc.strip() else "Ghana"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            new_discussion = pd.DataFrame([[timestamp, "N/A", "N/A", clean_uloc, clean_thought, 0.0]], columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"])
            
            if not os.path.exists(DATA_FILE):
                new_discussion.to_csv(DATA_FILE, index=False)
            else:
                new_discussion.to_csv(DATA_FILE, mode='a', header=False, index=False)

    st.divider()
    st.write("#### 💬 Latest Community Thoughts")
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        discussions_df = df[(df["Discussion"] != "No custom topic") & (df["Discussion"] != "N/A") & (df["Discussion"] != "Latency Test Log")]
        
        if not discussions_df.empty:
            for _, row in discussions_df.iloc[::-1].head(15).iterrows():
                st.info(f"📍 **{row['Location']}** ({row['Timestamp']})\n\n\"{row['Discussion']}\"")
        else:
            st.caption("The wall is empty. Be the first to start a conversation!")
