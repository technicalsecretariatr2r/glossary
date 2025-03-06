import streamlit as st
import pandas as pd
import datetime
import csv
import os

st.set_page_config(
    page_title="RtR/RPI/SAA Glossary",
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
st.title("RtR/RPI/SAA Glossary")
st.markdown("""
Welcome to the RtR/RPI/SAA Glossary App –  
Use the sidebar to filter entries by **Source** via the dropdown menu, and use the keyword search dropdown below to quickly find specific definitions or titles. 
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

# If no filters are selected, show an info message and full table checkbox.
if selected_source == "None" and search_keyword == "None":
    st.info("No filters selected. Please choose a Source from the sidebar to see filtered results. Available sources: " + ", ".join(sources))
    if st.checkbox("Show full data table", key="full_table_none"):
        st.dataframe(df_glossary)
# If filters are applied, show the card-style results and a checkbox for the dynamic table.
else:
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            # Safely build the link string only if valid.
            link_html = ""
            if pd.notnull(row['Link']):
                link_html = " | <a href='" + str(row['Link']) + "' target='_blank'>Learn more</a>"
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
                        {link_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        if st.checkbox("Show full data table", key="full_table_filtered"):
            st.dataframe(filtered_df)
    else:
        st.write("No results found. Try adjusting your filters or search keywords.")
