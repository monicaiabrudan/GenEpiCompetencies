import streamlit as st
import pandas as pd
import altair as alt
import textwrap

st.set_page_config(page_title="Competency Comparison", layout="wide")
st.title("📊 Competency Level Comparison Across Files")

# Define Bloom's level ranking for comparison
bloom_levels = ['Unfamiliar', 'Remember', 'Understand', 'Apply', 'Analyse', 'Evaluate', 'Create']
bloom_rank = {level: i for i, level in enumerate(bloom_levels)}
reverse_bloom_rank = {i: level for level, i in bloom_rank.items()}

# --------------------------
# NEW: Combined File Upload and Radar Plot (Updated for Bloom Levels)
# --------------------------
import matplotlib.pyplot as plt
import numpy as np

st.markdown("### 📁 Or Upload 2 or 3 Files Together for Radar Plot Comparison")
multi_files = st.file_uploader("Upload 2 or 3 CSV files", type=["csv"], accept_multiple_files=True, key="multi")

if multi_files and 2 <= len(multi_files) <= 3:
    dfs = []
    labels = []
    categories = None

    bloom_levels = ['Unfamiliar', 'Remember', 'Understand', 'Apply', 'Analyse', 'Evaluate', 'Create']
    bloom_rank = {level: i for i, level in enumerate(bloom_levels)}

    for file in multi_files:
        df = pd.read_csv(file)
        if "Topic" not in df.columns or "Selected Bloom Level" not in df.columns:
            st.error(f"{file.name} must contain 'Topic' and 'Selected Bloom Level' columns.")
            break

        df["Score"] = df["Selected Bloom Level"].map(bloom_rank)
        df_sorted = df.sort_values("Topic")
        dfs.append(df_sorted)
        labels.append(file.name)
        if categories is None:
            categories = df_sorted["Topic"].tolist()

    if len(dfs) == len(multi_files):
        st.markdown("#### 🕸️ Radar Plot Comparison")
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

        for i, df in enumerate(dfs):
            values = df["Score"].tolist()
            values += values[:1]
            ax.plot(angles, values, color=colors[i % len(colors)], linewidth=2, label=labels[i])
            ax.fill(angles, values, color=colors[i % len(colors)], alpha=0.25)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        wrapped_categories = [textwrap.fill(cat, 20) for cat in categories]
        ax.set_thetagrids(np.degrees(angles[:-1]), wrapped_categories, fontsize=10)
        ax.set_title("Competency Bloom Level Radar Chart", size=14)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        st.pyplot(fig)
        # --------------------------
        # Optional: Grouped Bar Plot (Matplotlib-only)
        # --------------------------
        st.markdown("#### 📊 Grouped Bar Plot")

        # Prepare data for grouped bar plot
        bar_df = pd.DataFrame()
        for i, df in enumerate(dfs):
            temp = df[["Topic", "Score"]].copy()
            temp["File"] = labels[i]
            bar_df = pd.concat([bar_df, temp], ignore_index=True)

        bar_df["Topic"] = bar_df["Topic"].apply(lambda x: textwrap.fill(x, 30))
        topics = bar_df["Topic"].unique()
        files = bar_df["File"].unique()
        x = np.arange(len(topics))
        width = 0.8 / len(files)

        fig, ax = plt.subplots(figsize=(12, 6))
        for idx, file in enumerate(files):
            subset = bar_df[bar_df["File"] == file]
            scores = subset.set_index("Topic").reindex(topics)["Score"].values
            ax.bar(x + idx * width, scores, width, label=file)

        ax.set_xticks(x + width * (len(files) - 1) / 2)
        ax.set_xticklabels(topics, rotation=45, ha="right")
        ax.set_ylabel("Bloom Score")
        ax.set_title("Bloom Level Comparison by Topic")
        ax.legend()
        st.pyplot(fig)

elif multi_files:
    st.warning("Please upload exactly 2 or 3 files.")
