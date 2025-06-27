#program by Marcus C. Rodriguez PSYC-3220-U71 06/10/2025
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize session state variables
if 'consent_given' not in st.session_state:
    st.session_state.consent_given = False
if 'spsrq_complete' not in st.session_state:
    st.session_state.spsrq_complete = False
if 'sensitivity' not in st.session_state:
    st.session_state.sensitivity = None
if 'rss_asq_complete' not in st.session_state:
    st.session_state.rss_asq_complete = False
if 'sticker_data' not in st.session_state:
    st.session_state.sticker_data = {}
if 'submit_spsrq' not in st.session_state:
    st.session_state.submit_spsrq = False
if 'submit_rss_asq' not in st.session_state:
    st.session_state.submit_asq = False
if "rss_responses" not in st.session_state:
    st.session_state.rss_responses = {}
if "asq_responses" not in st.session_state:
    st.session_state.asq_responses = {}
if "spsrq_responses" not in st.session_state:
    st.session_state.spsrq_responses = {}

# Initialize name input tracking
if 'consent_name' not in st.session_state:
    st.session_state.consent_name = ""

def get_color(value):
    """Return a CSS color gradient based on Likert scale value."""
    color_map = {
        1: '#b30000',  # Dark red
        2: '#e34a33',
        3: '#fc8d59',
        4: '#fdbb84',  # Orange for Neutral
        5: '#a1d99b',
        6: '#74c476',
        7: '#31a354'   # Green
    }
    return color_map.get(value, 'black')
    
# Set Likert Labels
likert_labels = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Somewhat Disagree",
    4: "Neutral",
    5: "Somewhat Agree",
    6: "Agree",
    7: "Strongly Agree"
}

# Function: Consent Form
def show_consent_form():
    if not st.session_state.consent_given:
        st.image("title.png", use_container_width=True, caption="PSYC-3220-U71: Learning, Program By: Marcus C. Rodriguez www.marcusc.com")
    st.write("The cluttered mobile depicted in the image not only creates the visualization of the operant tension between punishment and reward as reflected in the eyes of the mouse, the cat on one side the cheese the other, it also mirrors the perceptual disarray experienced by individuals with ADHD. For those suffering with impaired executive functioning, the world often presents itself not as a mobile in equilibrium reflecting a balanced hierarchy of incentives and consequences, but rather as a disorganized field of dangling contingencies. The field is constantly shifting, overlapping, and difficult to parse. The exaggerated representation of the Calderesque mobile is a metaphor of the  chaotic reinforcement environment: unpredictable, overstimulating, and difficult to regulate. As a cat might swipe at a mobile in fascination and confusion, the ADHD brain is drawn toward stimuli without clear direction or ability to  readily discriminate consequences. In this mock study/paper, I attempt to use instrumental conditioning not just to shape behavior, but to impose structure onto disorder, clarity onto chaos in an effort to restore the contingencies that are drowned out by the distraction.")

    st.title("Informed Consent Form")

    st.write(""" 
    **Purpose:** To understand individual sensitivity to punishment and reward and explore how different stimuli function as reinforcers or punishers within the context of the Response-Deprivation Hypothesis (RDH) and the proposed corollary Punishment Augmentation Hypothesis (PAH). 
      
    **Procedures:** You will complete the SPSRQ, followed by an RSS or ASQ survey depending on your results.  
    
    **Risks:** Minimal, limited to potential mild discomfort while answering introspective questions.  
    
    **Benefits:** You may learn about your own behavioral tendencies and preferences.  
    
    **Confidentiality:** Your name and responses will be kept private and used only for this session.
      
    **Voluntary Participation:** You may withdraw at any time without consequence.

    By typing your name below and clicking "I Consent", you agree to participate and give electronic consent.
    """)

    st.write("This is a mock project for educational purposes and will involve participation in self-reporting behavior, answering psychological questionnaires, and simulating data relative to receiving behaviorally contingent rewards or punishments.")

    with st.form("consent_form", clear_on_submit=False):
        name = st.text_input("Type your full name to consent:", value=st.session_state.consent_name)
        submitted = st.form_submit_button("I Consent")
        
        if submitted:
            if name.strip():
                st.session_state.consent_name = name.strip()
                st.session_state.participant_name = name.strip()
                st.session_state.consent_given = True
                st.success(f"Consent provided by {name.strip()}.")
            else:
                st.warning("Please enter your full name before submitting.")
# Function: SPSRQ Questionnaire 
def run_spsrq():
    st.header("Sensitivity to Punishment and Sensitivity to Reward Questionnaire (SPSRQ)")
    st.markdown("""
    <div class='likert-legend'>
        <b>Likert Scale</b>: 
        <span style='color:#b30000;'>1</span>, 
        <span style='color:#e34a33;'>2</span>, 
        <span style='color:#fc8d59;'>3</span>, 
        <span style='color:#fdbb84;'>4</span>, 
        <span style='color:#a1d99b;'>5</span>, 
        <span style='color:#74c476;'>6</span>, 
        <span style='color:#31a354;'>7</span> <br>
        <hr style='height:5px;border:none;background:linear-gradient(to right, yellow, orange); border-radius:5px;'>
        <i>1 = Strongly Disagree &nbsp;&nbsp;&nbsp; 2 = Disagree &nbsp;&nbsp;&nbsp; 3 = Somewhat Disagree &nbsp;&nbsp;&nbsp; <br> 4 = Neutral <br> 5 = Somewhat Agree &nbsp;&nbsp;&nbsp; 6 = Agree &nbsp;&nbsp;&nbsp; 7 = Strongly Agree</i>
    </div>
    """, unsafe_allow_html=True)
    # Load SPSRQ questions if not already loaded
    if "spsrq_df" not in st.session_state:
        try:
            spsrq_df = pd.read_csv("spsrq_questions.csv")
            st.session_state.spsrq_df = spsrq_df
        except FileNotFoundError:
            st.error("SPSRQ questions file not found. Please ensure 'spsrq_questions.csv' is in the app directory.")
            return

    responses = {}

    for _, row in st.session_state.spsrq_df.iterrows():    	
        st.markdown("<hr style='height:3px;border:none;background:linear-gradient(to right, red, orange, yellow, green); border-radius:5px;'>", unsafe_allow_html=True)
        question = row["question"]
        qid = f"Q{row['id']}"
        value = st.slider(
            f"{qid}. {question}",
            min_value=1,
            max_value=7,
            value=4,
            key=qid,
            label_visibility="visible"
        )
        responses[qid] = value
        color = get_color(value)
        label = likert_labels.get(value, "Invalid value")
        st.markdown(
            f"<div style='padding:6px; border-radius:5px; background-color:{color}; color:black; margin-bottom:5px;'>"
            f"<b>Your response:</b> {label}</div>",
            unsafe_allow_html=True
        )

    if st.button("Submit SPSRQ"):
        st.session_state.spsrq_responses = responses
        st.session_state.spsrq_complete = True
        process_spsrq_results(responses)
        
    
# Function to compute SPSRQ scores and branch to the next questionnaire
def process_spsrq_results(spsrq_responses):
    reward_score = 0
    punishment_score = 0

    for qid, value in spsrq_responses.items():
        q_type = st.session_state.spsrq_df.loc[st.session_state.spsrq_df['id'] == int(qid[1:]), 'type'].values[0]
        if q_type == 'reward':
            reward_score += value
        elif q_type == 'punishment':
            punishment_score += value

    # Store for later reference
    st.session_state.spsrq_reward = reward_score
    st.session_state.spsrq_punishment = punishment_score

    st.markdown("---")
    st.subheader("SPSRQ Results Summary")
    st.write(f"**Total Sensitivity to Reward (SR):** {reward_score}")
    st.write(f"**Total Sensitivity to Punishment (SP):** {punishment_score}")

    # Decide dominant sensitivity
    if reward_score > punishment_score:
        st.success("Based on your profile, we will proceed with the **Reinforcement Survey Schedule (RSS)**.")
        st.session_state.sensitivity = "rss"
    elif punishment_score > reward_score:
        st.warning("Based on your profile, we will proceed with the **Aversive Stimuli Questionnaire (ASQ)**.")
        st.session_state.sensitivity = "asq"
    else:
        # Tie-breaker: default to reward
        st.info("Scores are equal. Defaulting to **RSS** as per positive conditioning preference.")
        st.session_state.sensitivity = "rss"

    # Trigger button to continue
    if st.button("Continue to Next Questionnaire"):
        st.session_state.spsrq_complete = True

# Function: RSS or ASQ 
def run_rss_or_asq():
    if st.session_state.sensitivity == "rss":
        run_rss()
    else:
        run_asq()

# Function: RSS Questionnaire 
def run_rss():
    st.header("Reinforcement Survey Schedule (RSS)")
    st.markdown("""
    <div class='likert-legend'>
        <b>Likert Scale</b>: 
        <span style='color:#b30000;'>1</span>, 
        <span style='color:#e34a33;'>2</span>, 
        <span style='color:#fc8d59;'>3</span>, 
        <span style='color:#fdbb84;'>4</span>, 
        <span style='color:#a1d99b;'>5</span>, 
        <span style='color:#74c476;'>6</span>, 
        <span style='color:#31a354;'>7</span> <br>
        <hr style='height:5px;border:none;background:linear-gradient(to right, yellow, orange); border-radius:5px;'>
        <i>1 = Strongly Disagree &nbsp;&nbsp;&nbsp; 2 = Disagree &nbsp;&nbsp;&nbsp; 3 = Somewhat Disagree &nbsp;&nbsp;&nbsp; <br> 4 = Neutral <br> 5 = Somewhat Agree &nbsp;&nbsp;&nbsp; 6 = Agree &nbsp;&nbsp;&nbsp; 7 = Strongly Agree</i>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("____________ is important to me.")
# Load RSS questions if not already loaded
    if "rss_df" not in st.session_state:
        try:
            rss_df = pd.read_csv("rss_questions.csv")
            st.session_state.rss_df = rss_df
        except FileNotFoundError:
            st.error("RSS questions file not found. Please ensure 'rss_questions.csv' is in the app directory.")
            return
    responses = {}
    for _, row in st.session_state.rss_df.iterrows():
        st.markdown("<hr style='height:3px;border:none;background:linear-gradient(to right, red, orange, yellow, green); border-radius:5px;'>", unsafe_allow_html=True)
        question = row["question"]
        qid = f"RSS_{row['id']}"
        value = st.slider(
            f"{qid}. {question}",
            min_value=1,
            max_value=7,
            value=4,
            key=qid,
            label_visibility="visible"
        )
        responses[qid] = value
        color = get_color(value)
        label = likert_labels.get(value, "Invalid value")
        
        st.markdown(
            f"<div style='padding:6px; border-radius:5px; background-color:{color}; color:black; margin-bottom:5px;'>"
            f"<b>Your response:</b> {label}</div>",
            unsafe_allow_html=True
        )

    if st.button("Submit RSS"):
        st.session_state.rss_responses = responses
        st.session_state.rss_asq_complete = True
        st.success("RSS Completed. Proceeding to next phase...")
        st.rerun()  # Force rerun to go to summary
 
# Function: Aversive Stimuli Questionnaire (ASQ)
def run_asq():
    st.header("Aversive Stimuli Questionnaire (ASQ)")
    st.markdown("""
    <div class='likert-legend'>
        <b>Likert Scale</b>: 
        <span style='color:#b30000;'>1</span>, 
        <span style='color:#e34a33;'>2</span>, 
        <span style='color:#fc8d59;'>3</span>, 
        <span style='color:#fdbb84;'>4</span>, 
        <span style='color:#a1d99b;'>5</span>, 
        <span style='color:#74c476;'>6</span>, 
        <span style='color:#31a354;'>7</span> <br>
        <hr style='height:5px;border:none;background:linear-gradient(to right, yellow, orange); border-radius:5px;'>
        <i>1 = Strongly Disagree &nbsp;&nbsp;&nbsp; 2 = Disagree &nbsp;&nbsp;&nbsp; 3 = Somewhat Disagree &nbsp;&nbsp;&nbsp; <br> 4 = Neutral <br> 5 = Somewhat Agree &nbsp;&nbsp;&nbsp; 6 = Agree &nbsp;&nbsp;&nbsp; 7 = Strongly Agree</i>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("How unpleasant is ____________?")

    # Load ASQ questions if not already loaded
    if "asq_df" not in st.session_state:
        try:
            asq_df = pd.read_csv("asq_questions.csv")
            st.session_state.asq_df = asq_df
        except FileNotFoundError:
            st.error("ASQ questions file not found. Please ensure 'asq_questions.csv' is in the app directory.")
            return

    responses = {}
    for _, row in st.session_state.asq_df.iterrows():
        st.markdown("<hr style='height:3px;border:none;background:linear-gradient(to right, red, orange, yellow, green); border-radius:5px;'>", unsafe_allow_html=True)
        question = row["question"]
        qid = f"ASQ_{row['id']}"

        value = st.slider(
            f"{qid}. {question}",
            min_value=1,
            max_value=7,
            value=4,
            key=qid,
            label_visibility="visible"
        )
        responses[qid] = value

        color = get_color(value)
        label = likert_labels.get(value, "Invalid value")
        st.markdown(
            f"<div style='padding:6px; border-radius:5px; background-color:{color}; color:black; margin-bottom:5px;'>"
            f"<b>Your response:</b> {label}</div>",
            unsafe_allow_html=True
        )

    if st.button("Submit ASQ"):
        st.session_state.asq_responses = responses
        st.session_state.rss_asq_complete = True
        st.success("ASQ Completed. Proceeding to next phase...")
        st.rerun()  # Force rerun to go to summary

#Function: Final Summary Report & Behavior Modifier Data Pass Through
def render_summary_table(summary_df):
    st.markdown("### Summary Table")
    html = "<table style='width:100%; border-collapse: collapse; font-family: sans-serif;'>"
    # Header
    html += "<thead><tr>" + "".join(
        [f"<th style='padding:8px;border:1px solid #ddd;background:#333333;color:#ffffff;text-align:left;'>{col}</th>"
         for col in summary_df.columns]) + "</tr></thead><tbody>"    
    # Body
    for _, row in summary_df.iterrows():
        html += "<tr>" + "".join([
            f"<td style='padding:8px;border:1px solid #ddd;"
            f"{'font-weight:bold;color:#0072B2;' if str(cell) in ['Reward','Punishment'] else ''}'>"
            f"{cell}</td>"
            for cell in row
        ]) + "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

def plot_bliss_or_distress_point():
    fig, ax = plt.subplots(figsize=(7, 5))
    
    top_question = "Question text not found"
    
    if st.session_state.get("rss_responses"):
        responses = st.session_state.rss_responses
        top_item = max(responses.items(), key=lambda x: x[1])
        top_label = top_item[0]
        top_id = int(top_label.split('_')[1])

        if "rss_df" in st.session_state:
            top_question = st.session_state.rss_df.loc[
                st.session_state.rss_df["id"] == top_id, "question"
            ].values[0]

        x = [1, 2, 3, 4, 5]
        y = [i * 1.5 for i in x]
        ax.plot(x, y, label="Effort vs. Perceived Reward Utility", color="green")
        ax.scatter(2.5, 7.5, color="blue", label="Bliss Point", s=100, zorder=5)
        #ax.text(2.5, 7.8, "Bliss Point", ha='center', fontsize=8)
        ax.set_title(f"Top Reward: {top_question}", fontsize=10)
        ax.set_ylabel("Perceived Reward Utility (PRU)")
        ax.set_xlabel("Required Behavioral Effort (RBE)")
        ax.legend()        
        plt.tight_layout()
        plt.figtext(0.5, 0.01,
            "RDH: When access to a normally high-frequency behavior is restricted below baseline, it becomes a reinforcer.",
            wrap=True, horizontalalignment='center', fontsize=9, style='italic')
        st.pyplot(fig)

    elif st.session_state.get("asq_responses"):
        responses = st.session_state.asq_responses
        top_item = max(responses.items(), key=lambda x: x[1])
        top_label = top_item[0]
        top_id = int(top_label.split('_')[1])

        if "asq_df" in st.session_state:
            top_question = st.session_state.asq_df.loc[
                st.session_state.asq_df["id"] == top_id, "question"
            ].values[0]

        x = [1, 2, 3, 4, 5]
        y = [i * 1.5 for i in x]
        ax.plot(x, y, label="Arousal vs. Perceived Punisher Aversiveness", color="red")
        ax.scatter(2.5, 7.5, color="black", label="Distress Point", s=100, zorder=5)
        #ax.text(3.5, 5.1, "Distress Point", ha='center', fontsize=8)
        ax.set_title(f"Top Punisher: {top_question}", fontsize=10)
        ax.set_ylabel("Perceived Punisher Aversiveness (PPA)")
        ax.set_xlabel("Arousal (Arousal)")
        ax.legend()
        plt.tight_layout()
        plt.figtext(0.5, 0.01,
            "PAH: When exposure to a low-frequency behavior is imposed above baseline, it becomes a punisher.",
            wrap=True, horizontalalignment='center', fontsize=9, style='italic')
        st.pyplot(fig)


def show_summary():
    st.header("Summary of Behavioral Assessment")

    # --- Part 1: Summary Table ---
    st.subheader("1. SPSRQ Scores Summary")
    reward = st.session_state.spsrq_reward
    punishment = st.session_state.spsrq_punishment
    dominant = "Reward" if reward > punishment else "Punishment"
    
    # Assuming SPSRQ has 24 reward and 24 punishment questions
    reward_total = st.session_state.spsrq_reward
    punishment_total = st.session_state.spsrq_punishment
    reward_mean = round(reward_total / 24, 2)
    punishment_mean = round(punishment_total / 24, 2)
    reward_sd = round(st.session_state.spsrq_df[st.session_state.spsrq_df['type'] == 'reward']['id'].apply(lambda x: st.session_state.spsrq_responses.get(f"Q{x}", 0)).std(), 2)
    punishment_sd = round(st.session_state.spsrq_df[st.session_state.spsrq_df['type'] == 'punishment']['id'].apply(lambda x: st.session_state.spsrq_responses.get(f"Q{x}", 0)).std(), 2)
    
    summary_data = {
        "Total Sensitivity to Reward": [reward_total],
        "Mean Reward Score": [reward_mean],
        "Reward Score SD": [reward_sd],
        "Total Sensitivity to Punishment": [punishment_total],
        "Mean Punishment Score": [punishment_mean],
        "Punishment Score SD": [punishment_sd],
        "Dominant Sensitivity": [dominant]
    }
    summary_df = pd.DataFrame(summary_data)
    render_summary_table(summary_df)

    # --- Part 2: Lollipop Chart of Top 5 Stimuli ---
    st.subheader("2. Top 5 Stimuli by Strength of Response")
    
    # Choose data source
    if st.session_state.sensitivity == "rss":
        data_df = st.session_state.rss_df
        responses = st.session_state.rss_responses
        stim_type = "Reinforcer"
    else:
        data_df = st.session_state.asq_df
        responses = st.session_state.asq_responses
        stim_type = "Punisher"

    # Merge responses with questions
    df = data_df.copy()
    df["qid"] = df["id"].apply(lambda x: f"{'RSS' if stim_type=='Reinforcer' else 'ASQ'}_{x}")
    df["response"] = df["qid"].map(responses)
    df = df.dropna(subset=["response"])
    df = df.sort_values("response", ascending=False).head(5)

    # Save to session for export
    st.session_state.sticker_data = df[["qid", "question", "response"]]

    # Plot lollipop chart
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hlines(y=df["question"], xmin=0, xmax=df["response"], color="skyblue")
    ax.plot(df["response"], df["question"], "o")
    ax.set_xlabel("Likert Score (1-7)")
    ax.set_title(f"Top 5 {stim_type}s by Subjective Intensity")
    st.pyplot(fig)
    
    # Plot Bliss Point / Distress Point
    plot_bliss_or_distress_point()

    # --- Part 3: Export to CSV ---
    st.subheader("3. Export for Digital Sticker Chart")

    filename = f"{st.session_state.participant_name.replace(' ', '_')}_sticker_data.csv"
    csv = st.session_state.sticker_data.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

    st.success("Data saved and ready for use in the Digital Sticker Chart App!")


# --- APP FLOW ---
if not st.session_state.consent_given:
    show_consent_form()
elif not st.session_state.spsrq_complete:
    run_spsrq()
elif not st.session_state.rss_asq_complete:
    run_rss_or_asq()
else:
    show_summary()

