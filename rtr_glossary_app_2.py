import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="RtR/RPI/SAA Glossary",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("RtR/RPI/SAA Glossary")
st.markdown("""
Welcome to the RtR/RPI/SAA Glossary App –  
Use the sidebar to filter entries by **Source** via the radio buttons below, and use the keyword search dropdown to quickly find specific definitions or titles. 
""")

@st.cache_data
def load_glossary(sheet_name="Sheet1"):
    file_path_glossary = "rtr_glossary_official_info.xlsx"
    if not os.path.exists(file_path_glossary):
        st.error(f"El archivo '{file_path_glossary}' no se encontró. Asegúrate de que esté subido en el repositorio.")
        st.stop()
    return pd.read_excel(file_path_glossary, sheet_name=sheet_name)

df_glossary = load_glossary(sheet_name="Glossary")

# Sidebar: Filter Options
st.sidebar.header("Filters")
sources = sorted(df_glossary["Source"].unique())
selected_source = st.sidebar.radio("Filter by Source:", options=["All Sources"] + sources, index=0)

# Filtering logic
if selected_source != "All Sources":
    df_source_filtered = df_glossary[df_glossary["Source"] == selected_source]
else:
    df_source_filtered = df_glossary

# Keyword search implemented as a dropdown based on available Category values.
categories = sorted(df_source_filtered["Category"].unique())
search_keyword = st.selectbox("Search:", options=["None"] + categories)

# Filter the DataFrame.
filtered_df = df_glossary.copy()
if selected_source != "All Sources":
    filtered_df = filtered_df[filtered_df["Source"] == selected_source]
if search_keyword != "None":
    filtered_df = filtered_df[
        filtered_df["Definition"].str.contains(search_keyword, case=False, na=False) |
        filtered_df["Source"].str.contains(search_keyword, case=False, na=False) |
        filtered_df["Category"].str.contains(search_keyword, case=False, na=False)
    ]

st.subheader("Glossary Search Results")

# If no filters are selected, show an info message and full table checkbox.
if selected_source == "All Sources" and search_keyword == "None":
    st.info("No filters selected. Please choose a Source from the sidebar to see filtered results.")
    if st.checkbox("Show full data table", key="full_table_none"):
        st.dataframe(df_glossary)
# If filters are applied, show the card-style results and a checkbox for the dynamic table.
else:
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            link_html = f" | <a href='{row['Link']}' target='_blank'>Learn more</a>" if pd.notnull(row['Link']) else ""
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
