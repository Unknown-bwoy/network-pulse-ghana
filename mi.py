import streamlit as st
import pandas as pd
import json
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
q2_choices = ["Frequent disconnections", "Slow loading speeds", "High latency / lag", "I don't have connection issues"]

# --- TAB 1: THE AUDIT SURVEY ---
with tab1:
    st.write("### Log Your Current Experience")
    with st.form(key="telecom_survey"):
        st.markdown("#### 1. The Multi-SIM Culture 📲")
        q1 = st.pills(
            "Why do you use more than one SIM card?",
            q1_choices,
            selection_mode="single",
            default=None,
            key="audit_q1_pill",
        )
        st.divider()

        st.markdown("#### 2. The Internet Struggle ⏳")
        q2 = st.pills(
            "What annoys you most about your connection?",
            q2_choices,
            selection_mode="single",
            default=None,
            key="audit_q2_pill",
        )
        st.divider()

        st.markdown("#### 3. Financial Pain Points💡")
        q3 = st.pills(
            "What is your biggest financial pain point with mobile networks?",
            ["High data costs", "Frequent top-up failures", "Unfair MoMo charges", "I don't have a financial pain point"],
            selection_mode="single",
            default=None,
            key="audit_q3_pill",
        )
        st.divider()

        st.markdown("#### 4. Your Main Network 📡")
        primary_network = st.pills(
            "Which network do you use most often?",
            ["MTN", "Telecel", "AirtelTigo", "More than one", "Other / Not sure"],
            selection_mode="single",
            default=None,
            key="audit_network_pill",
        )

        st.markdown("#### 5. Connection Reliability 🔁")
        reliability = st.pills(
            "How often does your connection stop working unexpectedly?",
            ["Daily", "A few times a week", "Sometimes", "Rarely", "Never"],
            selection_mode="single",
            default=None,
            key="audit_reliability_pill",
        )

        st.markdown("#### 6. The Biggest Improvement 🚀")
        improvement = st.pills(
            "What should mobile networks improve first?",
            ["Coverage", "Speed", "Affordability", "Reliability", "Fraud protection"],
            selection_mode="single",
            default=None,
            key="audit_improvement_pill",
        )

        st.markdown("#### 7. Where are you experiencing this? 📍")
        location = st.text_input("Your Current Region/Neighborhood:", placeholder="e.g., Greater Accra - Madina")

        submit_button = st.form_submit_button(label="Log My Feedback 🔥")

    if submit_button:
        if not all([q1, q2, q3, primary_network, reliability, improvement, location.strip()]):
            st.error("Please answer every question and add your location before submitting!")
        else:
            st.balloons()
            st.success("Thank you! Your feedback has been securely logged.")

            clean_loc = location.replace(",", " ").strip()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            audit_details = (
                f"Audit Details | Network: {primary_network} | Reliability: {reliability} | "
                f"Priority: {improvement}"
            )
            new_data = pd.DataFrame(
                [[timestamp, q1, q2, clean_loc, audit_details, 0.0]],
                columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"],
            )

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

    st.divider()
    st.write("### 🚀 Live Network Speed")
    st.write("Measure how quickly data can be downloaded and uploaded from the app server.")
    st.caption("This is a real internet speed test. Results depend on the connection and location of the machine running this app.")

    if st.button("🚀 Test Download and Upload Speed"):
        download_url = "https://speed.cloudflare.com/__down?bytes=2000000"
        upload_url = "https://speed.cloudflare.com/__up"
        test_bytes = b"0" * 1_000_000

        with st.spinner("Measuring download and upload speed..."):
            try:
                download_start = time.perf_counter()
                download_request = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(download_request, timeout=10) as response:
                    downloaded_bytes = len(response.read())
                download_seconds = time.perf_counter() - download_start

                upload_start = time.perf_counter()
                upload_request = urllib.request.Request(
                    upload_url,
                    data=test_bytes,
                    headers={"User-Agent": "Mozilla/5.0"},
                    method="POST",
                )
                with urllib.request.urlopen(upload_request, timeout=10):
                    pass
                upload_seconds = time.perf_counter() - upload_start

                download_speed = round((downloaded_bytes * 8 / download_seconds) / 1_000_000, 2)
                upload_speed = round((len(test_bytes) * 8 / upload_seconds) / 1_000_000, 2)

                download_column, upload_column = st.columns(2)
                download_column.metric("Download", f"{download_speed} Mbps")
                upload_column.metric("Upload", f"{upload_speed} Mbps")

                speed_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                speed_data = pd.DataFrame(
                    [[speed_timestamp, "N/A", "N/A", test_region, f"Speed Test Log | Download: {download_speed} Mbps | Upload: {upload_speed} Mbps", 0.0]],
                    columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"],
                )
                if not os.path.exists(DATA_FILE):
                    speed_data.to_csv(DATA_FILE, index=False)
                else:
                    speed_data.to_csv(DATA_FILE, mode="a", header=False, index=False)
                st.success(f"Speed test saved for {test_region}.")
            except Exception:
                st.error("Speed test failed. Please check the connection and try again.")

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

    st.write("### 🛡️ Help Shape a Safer Network")
    st.caption("Never share your PIN, password, one-time code, or account details here.")
    with st.form(key="fraud_safety_poll"):
        st.write("Do you think fraud through calls, messages, or mobile money is a serious problem on mobile networks?")
        fraud_vote = st.pills(
            "Your view:",
            ["Yes", "No"],
            selection_mode="single",
            default=None,
            key="fraud_vote_pill",
        )
        vote_button = st.form_submit_button(label="Vote on Network Fraud 🗳️")

    if vote_button:
        if not fraud_vote:
            st.error("Choose Yes or No before submitting your vote.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            vote_data = pd.DataFrame(
                [[timestamp, "N/A", "N/A", "Ghana", f"Fraud Protection Vote: {fraud_vote}", 0.0]],
                columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"],
            )

            if not os.path.exists(DATA_FILE):
                vote_data.to_csv(DATA_FILE, index=False)
            else:
                vote_data.to_csv(DATA_FILE, mode="a", header=False, index=False)
            st.success("Your vote has been counted. Thanks for helping shape safer networks!")

    if os.path.exists(DATA_FILE):
        poll_data = pd.read_csv(DATA_FILE)
        vote_counts = poll_data["Discussion"].astype(str).str.extract(
            r"Fraud Protection Vote: (Yes|No)", expand=False
        ).value_counts()
        if not vote_counts.empty:
            yes_votes = int(vote_counts.get("Yes", 0))
            no_votes = int(vote_counts.get("No", 0))
            st.write(f"**Community vote:** ✅ Yes: {yes_votes}  |  ❌ No: {no_votes}")

    st.write("#### 🚨 Share a Fraud Experience or Safety Tip")
    st.caption("Tell the community what happened or what people should do. Do not name victims or include private account details.")
    with st.form(key="fraud_report_form"):
        report_type = st.selectbox(
            "What would you like to share?",
            ["Scam attempt", "I was scammed", "Suspicious call or message", "Safety advice"],
        )
        fraud_experience = st.text_area(
            "Your experience or advice:",
            placeholder="Example: I received a message asking for my MoMo PIN. I ignored it and reported the number.",
        )
        report_location = st.text_input("Region or neighborhood (Optional):", placeholder="e.g., Kumasi")
        report_button = st.form_submit_button(label="Share with the Community 🤝")

    if report_button:
        if not fraud_experience.strip():
            st.error("Please describe the experience or advice before sharing.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            clean_experience = fraud_experience.replace("\n", " ").strip()
            clean_location = report_location.strip() if report_location.strip() else "Ghana"
            report_data = pd.DataFrame(
                [[timestamp, "N/A", "N/A", clean_location, f"Fraud Report | {report_type}: {clean_experience}", 0.0]],
                columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"],
            )

            if not os.path.exists(DATA_FILE):
                report_data.to_csv(DATA_FILE, index=False)
            else:
                report_data.to_csv(DATA_FILE, mode="a", header=False, index=False)
            st.success("Your experience has been shared to help others stay alert.")

    st.write("### 🎭 Network Lounge")
    st.caption("Post a thought, drop a meme, or reply to someone. Keep it respectful and never share private account details.")
    meme_query = st.text_input(
        "Search for a meme category or keyword:",
        placeholder="Try: funny, work, reaction, celebration, network",
        key="meme_query",
    )
    if st.button("🔎 Search Meme Templates"):
        try:
            meme_request = urllib.request.Request(
                "https://api.imgflip.com/get_memes",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(meme_request, timeout=10) as response:
                meme_payload = json.loads(response.read().decode("utf-8"))
            all_meme_templates = meme_payload.get("data", {}).get("memes", [])
            search_terms = meme_query.strip().lower().split()
            matching_templates = [
                meme for meme in all_meme_templates
                if not search_terms or all(term in meme.get("name", "").lower() for term in search_terms)
            ]
            st.session_state["meme_search_results"] = matching_templates
            st.session_state["meme_template_choice"] = None
            st.session_state.pop("selected_meme_url", None)
            if matching_templates:
                st.success(f"Found {len(matching_templates)} meme templates. Choose one below.")
            else:
                st.warning("No templates matched that search. Try a broader keyword such as funny or reaction.")
        except Exception:
            st.error("The meme gallery is unavailable right now. Please try again later.")

    meme_results = st.session_state.get("meme_search_results", [])
    if meme_results:
        meme_options = {meme["name"]: meme for meme in meme_results}
        chosen_meme_name = st.pills(
            "Select a template:",
            list(meme_options),
            selection_mode="single",
            default=None,
            key="meme_template_choice",
        )
        if chosen_meme_name:
            chosen_meme = meme_options[chosen_meme_name]
            st.session_state["selected_meme_url"] = chosen_meme["url"]
            st.session_state["selected_meme_name"] = chosen_meme["name"]

    selected_meme_url = st.session_state.get("selected_meme_url", "")
    if selected_meme_url:
        st.image(selected_meme_url, caption=st.session_state.get("selected_meme_name", "Community meme template"))
        st.markdown("[Browse more public meme templates on Imgflip](https://imgflip.com/memetemplates)")

    with st.form(key="discussion_form"):
        post_kind = st.selectbox("What are you sharing?", ["Thought or question", "Meme"], key="post_kind")
        user_thought = st.text_area(
            "Your message or meme caption:",
            placeholder="Example: When the network comes back after disappearing for an hour...",
        )
        meme_url = selected_meme_url
        user_loc = st.text_input("Your Neighborhood (Optional):", placeholder="e.g., East Legon")
        post_button = st.form_submit_button(label="Share with the Lounge 🚀")

    if post_button:
        if not user_thought.strip() or (post_kind == "Meme" and not meme_url.strip()):
            st.error("Add a caption, and load a meme template when sharing a meme.")
        else:
            st.success("Your thought has been posted live!")
            clean_thought = user_thought.replace(",", " ").replace("\n", " ").strip()
            clean_uloc = user_loc.replace(",", " ").strip() if user_loc.strip() else "Ghana"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            discussion_text = clean_thought
            if post_kind == "Meme":
                discussion_text = f"MEME | {clean_thought} | {meme_url.strip()}"
            new_discussion = pd.DataFrame(
                [[timestamp, "N/A", "N/A", clean_uloc, discussion_text, 0.0]],
                columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"],
            )

            if not os.path.exists(DATA_FILE):
                new_discussion.to_csv(DATA_FILE, index=False)
            else:
                new_discussion.to_csv(DATA_FILE, mode='a', header=False, index=False)

    st.write("#### 🗨️ Join the Conversation")
    st.caption("Say hello, ask a question, or respond to what someone shared. Your message is posted as Anonymous.")
    chat_text = st.chat_input("Write a message to the community...")
    if chat_text and chat_text.strip():
        chat_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        chat_data = pd.DataFrame(
            [[chat_timestamp, "N/A", "N/A", "Ghana", f"Chat | {chat_text.strip()}", 0.0]],
            columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"],
        )
        if not os.path.exists(DATA_FILE):
            chat_data.to_csv(DATA_FILE, index=False)
        else:
            chat_data.to_csv(DATA_FILE, mode="a", header=False, index=False)
        st.success("Your message is now part of the conversation.")

    lounge_data = pd.read_csv(DATA_FILE) if os.path.exists(DATA_FILE) else pd.DataFrame()
    lounge_posts = lounge_data[
        lounge_data["Discussion"].notna()
        & ~lounge_data["Discussion"].astype(str).str.startswith(("Fraud Protection Vote:", "Speed Test Log |", "Reply |"))
    ] if not lounge_data.empty else pd.DataFrame()

    if not lounge_posts.empty:
        st.write("#### 💬 Community Conversations")
        st.caption("Open a conversation to read the post and join the discussion.")
        recent_posts = lounge_posts.iloc[::-1].head(20)
        post_options = {
            f"Post {number}: {str(row['Discussion']).split(' | ')[0][:60]}": row
            for number, (_, row) in enumerate(recent_posts.iterrows(), start=1)
        }
        with st.form(key="reply_form"):
            selected_post = st.pills("Open a conversation:", list(post_options), default=None, key="conversation_picker")
            if selected_post:
                parent = post_options[selected_post]
                parent_text = str(parent["Discussion"])
                st.markdown(f"**{parent['Location']}**  ·  {parent['Timestamp']}")
                if parent_text.startswith("MEME | "):
                    _, caption, image_url = parent_text.split(" | ", 2)
                    st.write(caption)
                    st.image(image_url, caption="Community meme")
                else:
                    st.write(parent_text)
                reply_text = st.text_input("Your reply:", placeholder="Add your voice to this conversation...")
            else:
                reply_text = ""
                st.info("Select a conversation above to reply.")
            reply_button = st.form_submit_button(label="Reply to Conversation 🤝", disabled=not bool(selected_post))

        if reply_button:
            if not reply_text.strip():
                st.error("Write a reply before posting.")
            else:
                parent = post_options[selected_post]
                reply_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                reply_data = pd.DataFrame(
                    [[reply_timestamp, "N/A", "N/A", "Ghana", f"Reply | {parent['Timestamp']} | {reply_text.replace(chr(10), ' ').strip()}", 0.0]],
                    columns=["Timestamp", "Q1", "Q2", "Location", "Discussion", "Latency"],
                )
                reply_data.to_csv(DATA_FILE, mode="a", header=False, index=False)
                st.success("Your reply has been posted.")

        if selected_post:
            parent = post_options[selected_post]
            conversation_replies = lounge_data[
                lounge_data["Discussion"].astype(str).str.startswith(f"Reply | {parent['Timestamp']} |")
            ]
            if not conversation_replies.empty:
                st.write("**Replies in this conversation**")
                for _, reply in conversation_replies.iterrows():
                    reply_text = str(reply["Discussion"]).split(" | ", 2)[-1]
                    with st.chat_message("user"):
                        st.caption(f"Anonymous · {reply['Timestamp']}")
                        st.write(reply_text)

    st.info("🌟 Community Challenge: Share one simple tip that helps people avoid mobile money scams.")

    st.divider()
    st.write("#### 💬 Latest Community Thoughts")

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        discussions_df = df[
            (df["Discussion"] != "No custom topic")
            & (df["Discussion"] != "N/A")
            & (df["Discussion"] != "Latency Test Log")
            & ~df["Discussion"].astype(str).str.startswith("Speed Test Log |")
            & ~df["Discussion"].astype(str).str.startswith("Fraud Protection Vote:")
        ]

        if not discussions_df.empty:
            for _, row in discussions_df.iloc[::-1].head(15).iterrows():
                discussion = str(row["Discussion"])
                if discussion.startswith("Reply | "):
                    _, parent_timestamp, reply_text = discussion.split(" | ", 2)
                    with st.chat_message("user"):
                        st.caption(f"Reply to {parent_timestamp}")
                        st.write(reply_text)
                elif discussion.startswith("Chat | "):
                    with st.chat_message("user"):
                        st.caption(f"Anonymous · {row['Timestamp']}")
                        st.write(discussion.removeprefix("Chat | "))
                elif discussion.startswith("MEME | "):
                    _, caption, image_url = discussion.split(" | ", 2)
                    st.info(f"📍 **{row['Location']}** ({row['Timestamp']})\n\n{caption}")
                    st.image(image_url, caption="Community meme")
                else:
                    st.info(f"📍 **{row['Location']}** ({row['Timestamp']})\n\n\"{discussion}\"")
        else:
            st.caption("The wall is empty. Be the first to start a conversation!")
