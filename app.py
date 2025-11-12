# ===============================================
# ⚽ Player Injuries and Team Performance Dashboard
# Mathematics for AI-II | Summative Assessment
# ===============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Player Injuries Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("player_injuries.csv", parse_dates=["Injury_Start", "Injury_End", "Match_Date"])
    df["Injury_Duration"] = (df["Injury_End"] - df["Injury_Start"]).dt.days
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("⚙️ Filters")
teams = st.sidebar.multiselect("Select Team(s)", df["Team"].unique(), default=df["Team"].unique())
positions = st.sidebar.multiselect("Select Position(s)", df["Position"].unique(), default=df["Position"].unique())
df_filtered = df[(df["Team"].isin(teams)) & (df["Position"].isin(positions))]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Average Rating", f"{df_filtered['Performance_Rating'].mean():.2f}")
col2.metric("Average Injury Duration (days)", f"{df_filtered['Injury_Duration'].mean():.1f}")
col3.metric("Average Performance Drop", f"{df_filtered['Performance_Drop'].mean():.2f}")

st.title("⚽ Player Injuries and Team Performance Dashboard")
st.markdown("### Analyze how player injuries affect overall team performance and outcomes.")

# --- Visualization 1: Top Performance Drops ---
st.subheader("Top 10 Players with Highest Performance Drop")
top_players = df_filtered.groupby("Player")["Performance_Drop"].mean().nlargest(10).reset_index()
fig1 = px.bar(top_players, x="Player", y="Performance_Drop", color="Performance_Drop",
              color_continuous_scale="Reds", title="Top 10 Players by Performance Drop")
st.plotly_chart(fig1, use_container_width=True)

# --- Visualization 2: Average Performance by Team ---
st.subheader("Average Pre vs Post-Injury Ratings by Team")
team_perf = df_filtered.groupby("Team")[["Pre_Injury_Rating", "Post_Injury_Rating"]].mean().reset_index()
fig2 = px.bar(team_perf, x="Team", y=["Pre_Injury_Rating", "Post_Injury_Rating"],
              barmode="group", title="Team Performance Comparison (Before vs After Injuries)")
st.plotly_chart(fig2, use_container_width=True)

# --- Visualization 3: Injury Frequency Over Time ---
st.subheader("Monthly Injury Frequency")
df_filtered["Month"] = df_filtered["Injury_Start"].dt.strftime("%b")
monthly = df_filtered.groupby("Month").size().reset_index(name="Injury_Count")
fig3 = px.line(monthly, x="Month", y="Injury_Count", markers=True, title="Injury Frequency by Month")
st.plotly_chart(fig3, use_container_width=True)

# --- Visualization 4: Age vs Performance Drop ---
st.subheader("Player Age vs Performance Drop")
fig4 = px.scatter(df_filtered, x="Age", y="Performance_Drop", color="Position",
                  title="Player Age vs Performance Drop by Position", trendline="ols")
st.plotly_chart(fig4, use_container_width=True)

# --- Visualization 5: Injury Duration Distribution ---
st.subheader("Distribution of Injury Duration")
fig5 = px.histogram(df_filtered, x="Injury_Duration", nbins=20, color="Team",
                    title="Injury Duration Distribution Across Teams")
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("**Created for Mathematics for AI-II Summative Assessment | Generic Dataset | Player Injuries Dashboard**")
