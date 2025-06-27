import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Competency Comparison", layout="wide")
st.title("📊 Competency Level Comparison Across Files")

# Define Bloom's level ranking for comparison
bloom_levels = ['Unfamiliar', 'Remember', 'Understand', 'Apply', 'Analyse', 'Evaluate', 'Create']
bloom_rank = {level: i for i, level in enumerate(bloom_levels)}
reverse_bloom_rank = {i: level for level, i in bloom_rank.items()}

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
    chart_data['Bloom Label'] = chart_data['Bloom Index'].map(reverse_bloom_rank)

    # Plot grouped bar chart using Altair with Bloom's levels on Y-axis and full Topic on X-axis
    st.markdown("### 📊 Bloom's Level Comparison (Grouped Bar Chart)")
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Topic:N', sort=None, axis=alt.Axis(labelAngle=90, labelLimit=500)),
        y=alt.Y('Bloom Index:Q', scale=alt.Scale(domain=[-0.5, 6.5]), title="Bloom's Level",
               axis=alt.Axis(values=list(reverse_bloom_rank.keys()), 
                             labelExpr='{"0": "Unfamiliar", "1": "Remember", "2": "Understand", "3": "Apply", "4": "Analyse", "5": "Evaluate", "6": "Create"}[datum.label]')),
        color=alt.Color('File:N', scale=alt.Scale(range=['#99cfff', '#3399ff', '#0055aa'])),
        tooltip=['Topic', 'File', 'Bloom Level'],
        xOffset='File:N'
    ).properties(width=1000, height=600).configure_axis(labelFontSize=12).configure_view(stroke=None)

    st.altair_chart(chart, use_container_width=True)

    # Download option
    csv = merged.to_csv(index=False)
    st.download_button("Download Comparison CSV", csv, "competency_comparison.csv", "text/csv")
else:
    st.info("Please upload all 3 competency CSV files one by one to generate the comparison.")
