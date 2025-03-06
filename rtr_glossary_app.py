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

# Improved Title and Description
st.title("Race to Resilience Glossary")
st.markdown("""
Welcome to the Race to Resilience Glossary App – your comprehensive guide to the key concepts and definitions driving our campaign. 
Use the sidebar to filter entries by **Source** via the dropdown menu, and use the keyword search dropdown below to quickly find specific definitions or titles. 
Whether you're a climate action professional or simply curious about our work, this app is designed to help you navigate our initiatives.
""")

@st.cache_data
def load_glossary():
    file_path_glossary = "glossary.csv"
    return pd.read_csv(file_path_glossary, sep=';')

df_glossary = load_glossary()

# -------------------------------
# Sidebar: Filter Options & Feedback
# -------------------------------
st.sidebar.header("Filters")

# Dropdown menu to filter by Source with "None" as the default option.
sources = sorted(df_glossary["Source"].unique())
selected_source = st.sidebar.selectbox("Filter by Source:", options=["None"] + sources)

# Apply the source filter to determine available categories for the keyword search.
if selected_source != "None":
    df_source_filtered = df_glossary[df_glossary["Source"] == selected_source]
else:
    df_source_filtered = df_glossary

# -------------------------------
# Main Page: Keyword Search & Results
# -------------------------------
# Keyword search implemented as a dropdown based on available Category values (dependent on selected source).
categories = sorted(df_source_filtered["Category"].unique())
search_keyword = st.selectbox("Search:", options=["None"] + categories)

# Filtering the DataFrame based on the selected filters.
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
        st.markdown(f"**Source:** {row['Source']}")
        st.markdown(f"**Category:** {row['Category']}")
        st.markdown(f"**Definition:** {row['Definition']}")
        if row['Link']:
            st.markdown(f"[Learn more]({row['Link']})")
        st.markdown("---")
else:
    st.write("No results found. Try adjusting your filters or search keywords.")

# -------------------------------
# Sidebar: Expanded Feedback Section
# -------------------------------
def save_feedback(feedback):
    filename = "feedback.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [timestamp, feedback]
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Feedback"])
        writer.writerow(new_row)

st.sidebar.subheader("Feedback")
feedback = st.sidebar.text_area("Your feedback or suggestions:")

if st.sidebar.button("Submit Feedback"):
    if feedback.strip():
        save_feedback(feedback)
        st.sidebar.success("Thank you for your feedback!")
    else:
        st.sidebar.error("Please enter your feedback before submitting.")
