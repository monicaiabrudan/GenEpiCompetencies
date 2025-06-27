import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Competency Comparison", layout="wide")
st.title("📊 Competency Level Comparison Across Files")

# Define Bloom's level ranking for comparison
bloom_levels = ['Unfamiliar', 'Remember', 'Understand', 'Apply', 'Analyse', 'Evaluate', 'Create']
bloom_rank = {level: i for i, level in enumerate(bloom_levels)}

# Upload each file individually
file1 = st.file_uploader("Upload File 1", type="csv", key="file1")
file2 = st.file_uploader("Upload File 2", type="csv", key="file2")
file3 = st.file_uploader("Upload File 3", type="csv", key="file3")

if file1 and file2 and file3:
    # Load and label each file
    df1 = pd.read_csv(file1).rename(columns={"Selected Bloom Level": "File 1"})
    df2 = pd.read_csv(file2).rename(columns={"Selected Bloom Level": "File 2"})
    df3 = pd.read_csv(file3).rename(columns={"Selected Bloom Level": "File 3"})

    # Merge on Topic
    merged = df1.merge(df2, on="Topic").merge(df3, on="Topic")

    # Display table
    st.markdown("### Comparison Table")
    st.dataframe(merged)

    # Prepare chart data
    chart_data = pd.melt(merged, id_vars=['Topic'], value_vars=['File 1', 'File 2', 'File 3'], 
                         var_name='File', value_name='Bloom Level')
    chart_data['Bloom Index'] = chart_data['Bloom Level'].map(bloom_rank)

    # Plot grouped bar chart
    st.markdown("### 📊 Bloom's Level Comparison (Grouped Bar Chart)")
    fig, ax = plt.subplots(figsize=(14, max(6, len(merged) * 0.4)))
    topics = chart_data['Topic'].unique()
    x = range(len(topics))
    width = 0.25
    colors = ['#99cfff', '#3399ff', '#0055aa']  # Three shades of blue

    for i, (file, color) in enumerate(zip(['File 1', 'File 2', 'File 3'], colors)):
        values = [chart_data[(chart_data['Topic'] == topic) & (chart_data['File'] == file)]['Bloom Index'].values[0] for topic in topics]
        ax.bar([pos + i * width for pos in x], values, width=width, label=file, color=color)

    ax.set_xticks([pos + width for pos in x])
    ax.set_xticklabels(topics, rotation=45, ha='right')
    ax.set_ylabel("Bloom's Level")
    ax.set_yticks(range(len(bloom_levels)))
    ax.set_yticklabels(bloom_levels)
    ax.legend()
    st.pyplot(fig)

    # Download option
    csv = merged.to_csv(index=False)
    st.download_button("Download Comparison CSV", csv, "competency_comparison.csv", "text/csv")
else:
    st.info("Please upload all 3 competency CSV files one by one to generate the comparison.")
