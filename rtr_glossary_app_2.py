import streamlit as st
import pandas as pd
import datetime
import csv
import os

st.set_page_config(
    page_title="Race to Resilience Glossary",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state keys before any widget is created.
if "feedback_name" not in st.session_state:
    st.session_state["feedback_name"] = ""
if "feedback_text" not in st.session_state:
    st.session_state["feedback_text"] = ""
if "feedback_error" not in st.session_state:
    st.session_state["feedback_error"] = ""
if "last_feedback" not in st.session_state:
    st.session_state["last_feedback"] = ""

# Title and introductory description.
st.title("Race to Resilience Glossary")
st.markdown("""
Welcome to the Race to Resilience Glossary App – your comprehensive guide to the key concepts and definitions driving our campaign. 
Use the sidebar to filter entries by **Source** via the dropdown menu, and use the keyword search dropdown below to quickly find specific definitions or titles. 
Whether you're a climate action professional or simply curious about our work, this app is designed to help you navigate our initiatives.
""")

# Load glossary data.
@st.cache_data
def load_glossary():
    file_path_glossary = "glossary.csv"
    return pd.read_csv(file_path_glossary, sep=';')

df_glossary = load_glossary()

# -------------------------------
# Sidebar: Filter Options
# -------------------------------
st.sidebar.header("Filters")
sources = sorted(df_glossary["Source"].unique())
selected_source = st.sidebar.selectbox("Filter by Source:", options=["None"] + sources)

# -------------------------------
# Main Page: Keyword Search & Results
# -------------------------------
# Determine available categories based on the source filter.
if selected_source != "None":
    df_source_filtered = df_glossary[df_glossary["Source"] == selected_source]
else:
    df_source_filtered = df_glossary

# Keyword search implemented as a dropdown based on available Category values.
categories = sorted(df_source_filtered["Category"].unique())
search_keyword = st.selectbox("Search:", options=["None"] + categories)

# Filter the DataFrame.
filtered_df = df_glossary.copy()
if selected_source != "None":
    filtered_df = filtered_df[filtered_df["Source"] == selected_source]
if search_keyword != "None":
    filtered_df = filtered_df[
        filtered_df["Definition"].str.contains(search_keyword, case=False, na=False) |
        filtered_df["Source"].str.contains(search_keyword, case=False, na=False) |
        filtered_df["Category"].str.contains(search_keyword, case=False, na=False)
    ]

st.subheader("Glossary Search Results")
if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        st.markdown(
            f"""
            <div style="padding: 15px; background-color: #f9f9f9; border-left: 6px solid #FF37D5; margin-bottom: 15px;">
                <div style="font-size: 20px; font-weight: bold; color: #333;">
                    {row['Category']}
                </div>
                <div style="font-size: 20px; margin-top: 10px; color: #555;">
                    {row['Definition']}
                </div>
                <div style="font-size: 14px; margin-top: 10px; color: #777;">
                    <strong>Source:</strong> {row['Source']}
                    {" | <a href='" + row['Link'] + "' target='_blank'>Learn more</a>" if row['Link'] else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.write("No results found. Try adjusting your filters or search keywords.")

# -------------------------------
# Sidebar: Expanded Feedback Section
# -------------------------------
st.sidebar.subheader("Feedback")

# Feedback inputs.
feedback_name = st.sidebar.text_input("Your Name:", key="feedback_name")
feedback_text = st.sidebar.text_area("Your feedback or suggestions:", key="feedback_text")

def submit_feedback():
    if not st.session_state.feedback_name.strip():
        st.session_state.feedback_error = "Please enter your name before submitting."
        return
    if not st.session_state.feedback_text.strip():
        st.session_state.feedback_error = "Please enter your feedback before submitting."
        return
    # Save the feedback to a CSV file.
    filename = "feedback.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [timestamp, st.session_state.feedback_name, st.session_state.feedback_text]
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Name", "Feedback"])
        writer.writerow(new_row)
    # Prepare a snippet from the feedback.
    snippet = st.session_state.feedback_text[:50] + ("..." if len(st.session_state.feedback_text) > 50 else "")
    st.session_state.last_feedback = f"Thank you, {st.session_state.feedback_name}! Your feedback: {snippet}"
    st.session_state.feedback_error = ""
    # Clear the feedback fields.
    st.session_state.feedback_name = ""
    st.session_state.feedback_text = ""
    # No need to call st.rerun(); Streamlit automatically re-runs the script after the callback.

st.sidebar.button("Submit Feedback", on_click=submit_feedback)

if st.session_state.feedback_error:
    st.sidebar.error(st.session_state.feedback_error)
elif st.session_state.last_feedback:
    st.sidebar.success(st.session_state.last_feedback)
