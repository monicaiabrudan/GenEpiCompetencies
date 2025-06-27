import streamlit as st
import pandas as pd
import io

# Load and clean data
df = pd.read_csv("Pathogen Genomics Competencies.csv")
df.columns = df.columns.str.strip()  # Clean column names

# Automatically rename the first column to 'Topic'
if df.columns[0] != "Topic":
    df = df.rename(columns={df.columns[0]: "Topic"})

# Drop empty unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]  

# Final check
if 'Topic' not in df.columns:
    st.error("The input file must have a first column with the competency titles.")
    st.stop()

st.set_page_config(page_title="Pathogen Genomics Competencies", layout="wide")
st.title("🧬 Pathogen Genomics Competencies Viewer")
st.markdown("Select your current level of knowledge for each topic based on Bloom's taxonomy.")

# Create a dictionary to collect user selections
selections = {}

# Bloom's taxonomy levels
bloom_levels = ['Unfamiliar', 'Remember', 'Understand', 'Apply', 'Analyse', 'Evaluate', 'Create']

# Display each competency with radio buttons for Bloom's levels
for i, row in df.iterrows():
    topic = str(row.get('Topic', f"Competency {i+1}")).strip()
    st.markdown(f"### {topic}")
    st.markdown(f"<span style='color:blue'><em>{row.get('Short description', '')}</em></span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:blue'><em>{row.get('Description', '')}</em></span>", unsafe_allow_html=True)

    # Prepare options with descriptions
    options = []
    for level in bloom_levels:
        if pd.notna(row.get(level)):
            options.append(f"{level}: {row[level]}")
        else:
            options.append(f"{level}: (no description)")

    # Show radio buttons
    choice = st.radio(
        label="Select your competency level:",
        options=options,
        index=None,
        key=f"radio_{i}"
    )

    # Save selection in dictionary
    if choice:
        selected_level = choice.split(":")[0]
        selections[topic] = selected_level

# Option to download selections
if selections:
    st.markdown("---")
    st.subheader("📥 Download Your Competency Selections")

    # Convert to DataFrame
    result_df = pd.DataFrame(list(selections.items()), columns=["Topic", "Selected Bloom Level"])

    # Create CSV in memory
    csv = result_df.to_csv(index=False)
    st.download_button(
        label="Download Selections as CSV",
        data=csv,
        file_name="selected_bloom_levels.csv",
        mime="text/csv"
    )
