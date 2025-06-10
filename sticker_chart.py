#program by Marcus C. Rodriguez PSYC-3220-U71 06/10/2025
import streamlit as st
import pandas as pd
import datetime
import os
import random # Import random module

# --- Configuration and Data Loading ---
sticker_path = "Ronda_Montelli_sticker_data.csv"
behavior_path = "target_behaviors.csv"

# Load behavior and reinforcer/punisher data
if os.path.exists(sticker_path) and os.path.exists(behavior_path):
    reinforcer_df = pd.read_csv(sticker_path)
    target_df = pd.read_csv(behavior_path)
else:
    st.error("Required data files are missing. Please ensure 'Ronda_Montelli_sticker_data.csv' and 'target_behaviors.csv' are in the same directory.")
    st.stop()

# Process reinforcer data
reinforcer_df['label'] = reinforcer_df['qid'].apply(lambda x: "Reward" if x.startswith("RSS") else "Punisher")
reinforcer_type = reinforcer_df['label'].iloc[0]
reinforcer_list = reinforcer_df['qid'].tolist()

# Assuming a 'description' column in Ronda_Montelli_sticker_data.csv for display
if 'question' in reinforcer_df.columns:
    reinforcer_description_map = dict(zip(reinforcer_df['qid'], reinforcer_df['question']))
else:
    reinforcer_description_map = {qid: qid for qid in reinforcer_df['qid']} # Fallback to QID if no description

# Map target behaviors to modified behaviors (for display purposes)
behavior_map = dict(zip(target_df['target_behavior'], target_df['modified_behavior']))
behaviors = target_df['target_behavior'].tolist() # Use target behaviors for the sticker chart index

# --- Session State Initialization ---
if 'phase' not in st.session_state:
    st.session_state.phase = "Phase I"
if 'week_counter' not in st.session_state:
    st.session_state.week_counter = 0 # Initialize week counter

# Initialize schedule and variable ratio threshold
if 'selected_schedule' not in st.session_state:
    st.session_state.selected_schedule = "Continuous" # Default schedule
if 'variable_ratio_threshold' not in st.session_state:
    st.session_state.variable_ratio_threshold = 0 # Will be set dynamically

# Initialize sticker_data for weekly tracking if not already present
if "sticker_data" not in st.session_state:
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # Initialize DataFrame with False values
    st.session_state.sticker_data = pd.DataFrame(False, index=target_df['modified_behavior'].tolist(), columns=days_of_week)

# --- Streamlit App Layout ---
st.title("🎯 Digital Sticker Chart Tracker")

st.subheader("📌 Current Program Phase")
st.markdown(f"**Phase:** {st.session_state.phase}")
st.markdown("---")

# Show Target Behavior Map
st.subheader("🧭 Target Behaviors and Goals")
for tb, mb in behavior_map.items():
    st.markdown(f"- **{tb}** → _{mb}_")

st.markdown("---")
st.subheader("📅 Log Weekly Behavior")
st.markdown("""
Use the checkboxes below to track completion of daily behaviors for the week.
Each checkmark represents a "sticker" earned for completing a task on that day.
""")

# Form for weekly progress submission
with st.form("weekly_sticker_form"):
    for behavior in st.session_state.sticker_data.index:
        st.markdown(f"**{behavior}**")
        cols = st.columns(len(st.session_state.sticker_data.columns))
        for i, day in enumerate(st.session_state.sticker_data.columns):
            # Ensure unique key for each checkbox using current behavior, day, and a stable identifier
            key = f"checkbox_{behavior}_{day}_{st.session_state.week_counter}"
            current_value = st.session_state.sticker_data.at[behavior, day]
            # Update the DataFrame directly with the checkbox state
            st.session_state.sticker_data.at[behavior, day] = cols[i].checkbox(day, value=current_value, key=key)
    submitted = st.form_submit_button("Save Weekly Progress")

if submitted:
    st.success("✅ Weekly progress updated!")

# --- Phase & Schedule Controls ---
st.markdown("---")
col1, col2 = st.columns(2) # Keep layout for consistency, though one button is removed

with col1:
    if st.button("🔄 Advance Phase"):
        st.session_state.phase = "Phase II" if st.session_state.phase == "Phase I" else "Phase I"
        st.rerun() # Rerun to apply phase change immediately

with col2:
    # Dropdown for Schedule Selection
    schedule_options = ["Continuous", "Fixed Ratio", "Variable Ratio"]
    current_schedule_index = schedule_options.index(st.session_state.selected_schedule) if st.session_state.selected_schedule in schedule_options else 0
    
    selected_schedule_new = st.selectbox(
        "Choose Reinforcement Schedule:",
        options=schedule_options,
        index=current_schedule_index,
        key="schedule_selector"
    )

    # Update session state if schedule changed via dropdown
    if selected_schedule_new != st.session_state.selected_schedule:
        st.session_state.selected_schedule = selected_schedule_new
        # If Variable Ratio is selected, generate a new random threshold
        if st.session_state.selected_schedule == "Variable Ratio":
            st.session_state.variable_ratio_threshold = random.randint(15, 30)
        else:
            st.session_state.variable_ratio_threshold = 0 # Reset for non-variable schedules
        st.rerun() # Rerun to apply schedule change immediately

# --- Dynamic REWARD_THRESHOLD based on selected_schedule ---
REWARD_THRESHOLD = 0 # Initialize

if st.session_state.selected_schedule == "Continuous":
    REWARD_THRESHOLD = 1
    st.markdown(f"**Current Schedule: {st.session_state.selected_schedule} (Weekly Goal: {REWARD_THRESHOLD} sticker)**")
elif st.session_state.selected_schedule == "Fixed Ratio":
    REWARD_THRESHOLD = 15
    st.markdown(f"**Current Schedule: {st.session_state.selected_schedule} (Weekly Goal: {REWARD_THRESHOLD} stickers)**")
elif st.session_state.selected_schedule == "Variable Ratio":
    # If it's a new week or just selected, generate a new random threshold
    if st.session_state.variable_ratio_threshold == 0: # Only generate if not already set for this session
         st.session_state.variable_ratio_threshold = random.randint(15, 30)
    REWARD_THRESHOLD = st.session_state.variable_ratio_threshold
    st.markdown(f"**Current Schedule: {st.session_state.selected_schedule} (Weekly Goal: Randomly Generated: {REWARD_THRESHOLD} stickers)**")


# --- Summary Section ---
st.markdown("---")
st.subheader("📊 Weekly Behavior Summary")

# Convert boolean DataFrame to integer for display and summation
weekly_summary_df = st.session_state.sticker_data.astype(int)
st.dataframe(weekly_summary_df)

# Total stickers earned per behavior
st.subheader("📈 Stickers Earned per Behavior")
sticker_totals_behavior = weekly_summary_df.sum(axis=1)
st.bar_chart(sticker_totals_behavior)

# Total stickers earned per day
st.subheader("📅 Stickers Earned per Day")
sticker_totals_day = weekly_summary_df.sum(axis=0)
st.line_chart(sticker_totals_day)

# Overall weekly total
total_stickers_this_week = sticker_totals_behavior.sum()
st.markdown(f"**Total Stickers Earned This Week:** {total_stickers_this_week}")

# Reinforcer/Punisher logic based on weekly total (as a system status/goal indicator)
reinforcer_display_text = reinforcer_description_map.get(reinforcer_list[0], reinforcer_list[0])

st.markdown("---")
st.subheader("Outcome Status (Based on Weekly Goal):")
if reinforcer_type == "Reward":
    if total_stickers_this_week >= REWARD_THRESHOLD:
        st.success(f"🎉 **Weekly Reward Goal Met!** ({total_stickers_this_week} / {REWARD_THRESHOLD} stickers). Administrator will review daily for: **{reinforcer_display_text}**")
    else:
        st.info(f"💪 **Weekly Reward Goal In Progress:** {REWARD_THRESHOLD - total_stickers_this_week} more stickers needed for weekly goal ({total_stickers_this_week} / {REWARD_THRESHOLD} stickers). Administrator will review daily. Current Reward/Punishment: **{reinforcer_display_text}**")
elif reinforcer_type == "Punisher":
    if total_stickers_this_week < REWARD_THRESHOLD: # Punisher administered if below threshold
        st.error(f"⚠️ **Weekly Punisher Goal Triggered!** ({total_stickers_this_week} / {REWARD_THRESHOLD} stickers). Administrator will review daily for: **{reinforcer_display_text}**")
    else:
        st.success(f"🙌 **Weekly Punisher Goal Avoided!** ({total_stickers_this_week} / {REWARD_THRESHOLD} stickers). Administrator will review daily for: **{reinforcer_display_text}**")

st.markdown("*(Note: Actual daily consequence administration is handled by the administrator, separate from this weekly tally.)*")


# --- Reset Button and Log Export ---
st.markdown("---")
if st.button("🔁 Reset for New Week and Save Log"):
    # Only increment week counter and save log if current data has been actively submitted
    # (Checking `submitted` flag isn't reliable here as it resets on rerun.
    # Instead, we'll just increment and save when reset is pressed, assuming
    # the user intends to finalize the current week.)
    
    st.session_state.week_counter += 1

    # Prepare data for logging: Add phase and schedule
    log_df = weekly_summary_df.copy() # Make a copy to avoid modifying the displayed DF
    # Add columns for phase, schedule, and total stickers
    log_df['Phase'] = st.session_state.phase
    log_df['Schedule'] = st.session_state.selected_schedule
    log_df['Weekly_Threshold_Goal'] = REWARD_THRESHOLD # Log the goal for this week
    log_df['Total_Stickers_Earned'] = total_stickers_this_week
    # Add a timestamp for the log
    log_df['Log_Timestamp'] = datetime.datetime.now().isoformat()


    # Construct the filename with incremental suffix
    export_filename = f"weekly_behavior_log_week{st.session_state.week_counter}.csv"
    log_df.to_csv(export_filename, index=True)
    st.success(f"Sticker chart reset for the new week! Log saved as **{export_filename}**")

    # Reset sticker data for the new week
    st.session_state.sticker_data[:] = False
    
    # Crucially, if Variable Ratio was selected for the *next* week, generate its new threshold here.
    # This ensures the random threshold is set for the upcoming week immediately after reset.
    if st.session_state.selected_schedule == "Variable Ratio":
        st.session_state.variable_ratio_threshold = random.randint(15, 30)
    else:
        st.session_state.variable_ratio_threshold = 0 # Reset for other schedules

    # Rerun to clear checkboxes and update displayed threshold/schedule for the new week
    st.rerun()

# --- Download Link for the LAST saved log ---
# This link will always point to the most recently saved log file.
# You might want to list all saved logs if historical access is needed.
if st.session_state.week_counter > 0:
    last_saved_filename = f"weekly_behavior_log_week{st.session_state.week_counter}.csv"
    
    if os.path.exists(last_saved_filename):
        with open(last_saved_filename, "rb") as file: # Open in binary read mode
            btn = st.download_button(
                label=f"📂 Download Last Saved Weekly Log ({last_saved_filename})",
                data=file, # Pass the file object
                file_name=last_saved_filename, # Name for the downloaded file
                mime="text/csv" # MIME type for CSV files
            )
    else:
        st.warning(f"Log file '{last_saved_filename}' not found for download. Please ensure it was saved.")
        
        
        
        
        
        
        
