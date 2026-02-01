import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# --- 1. EMBEDDED STRATEGIC DATA (Top 30 Global Candidates) ---
# Data extracted and cleaned from the Safe_Haven_Dynamic_Dataset
raw_data_json = """
[
    {"City": "Singapore", "Country": "Singapore", "Continent": "Asia", "Safety": 9.97, "Economy": 8.75, "Housing": 2.50, "Health": 8.90, "Internet": 9.10, "Cost": 3.10},
    {"City": "Tallinn", "Country": "Estonia", "Continent": "Europe", "Safety": 9.43, "Economy": 5.87, "Housing": 7.80, "Health": 9.10, "Internet": 9.50, "Cost": 7.20},
    {"City": "Doha", "Country": "Qatar", "Continent": "Asia", "Safety": 9.49, "Economy": 9.39, "Housing": 2.13, "Health": 7.43, "Internet": 3.25, "Cost": 6.18},
    {"City": "Taipei", "Country": "Taiwan", "Continent": "Asia", "Safety": 9.54, "Economy": 5.81, "Housing": 6.90, "Health": 8.80, "Internet": 8.10, "Cost": 6.90},
    {"City": "Munich", "Country": "Germany", "Continent": "Europe", "Safety": 9.05, "Economy": 6.97, "Housing": 4.20, "Health": 9.20, "Internet": 7.50, "Cost": 4.50},
    {"City": "Zurich", "Country": "Switzerland", "Continent": "Europe", "Safety": 9.33, "Economy": 8.99, "Housing": 1.10, "Health": 9.50, "Internet": 8.90, "Cost": 2.10},
    {"City": "Tokyo", "Country": "Japan", "Continent": "Asia", "Safety": 9.20, "Economy": 7.20, "Housing": 4.00, "Health": 9.50, "Internet": 8.80, "Cost": 4.00},
    {"City": "Dubai", "Country": "UAE", "Continent": "Asia", "Safety": 9.15, "Economy": 9.00, "Housing": 3.50, "Health": 8.10, "Internet": 4.20, "Cost": 5.50},
    {"City": "Copenhagen", "Country": "Denmark", "Continent": "Europe", "Safety": 9.10, "Economy": 6.50, "Housing": 4.00, "Health": 9.30, "Internet": 9.20, "Cost": 3.90},
    {"City": "Seoul", "Country": "South Korea", "Continent": "Asia", "Safety": 8.90, "Economy": 7.80, "Housing": 3.20, "Health": 9.40, "Internet": 9.80, "Cost": 4.50},
    {"City": "Cluj-Napoca", "Country": "Romania", "Continent": "Europe", "Safety": 9.15, "Economy": 5.10, "Housing": 8.50, "Health": 7.80, "Internet": 9.10, "Cost": 8.20},
    {"City": "Oslo", "Country": "Norway", "Continent": "Europe", "Safety": 8.85, "Economy": 6.40, "Housing": 4.10, "Health": 9.20, "Internet": 9.00, "Cost": 3.20},
    {"City": "Eindhoven", "Country": "Netherlands", "Continent": "Europe", "Safety": 8.85, "Economy": 6.12, "Housing": 4.50, "Health": 8.90, "Internet": 8.80, "Cost": 5.10},
    {"City": "Abu Dhabi", "Country": "UAE", "Continent": "Asia", "Safety": 9.30, "Economy": 8.80, "Housing": 3.80, "Health": 8.00, "Internet": 4.50, "Cost": 5.90},
    {"City": "Helsinki", "Country": "Finland", "Continent": "Europe", "Safety": 9.00, "Economy": 5.90, "Housing": 5.20, "Health": 9.40, "Internet": 9.10, "Cost": 4.80},
    {"City": "Vienna", "Country": "Austria", "Continent": "Europe", "Safety": 8.70, "Economy": 6.40, "Housing": 6.10, "Health": 9.30, "Internet": 8.50, "Cost": 5.40},
    {"City": "Hong Kong", "Country": "Hong Kong", "Continent": "Asia", "Safety": 8.50, "Economy": 8.90, "Housing": 1.00, "Health": 8.80, "Internet": 8.90, "Cost": 2.50},
    {"City": "Ottawa", "Country": "Canada", "Continent": "N. America", "Safety": 8.92, "Economy": 5.88, "Housing": 5.10, "Health": 8.70, "Internet": 8.50, "Cost": 5.20},
    {"City": "Stockholm", "Country": "Sweden", "Continent": "Europe", "Safety": 8.40, "Economy": 6.80, "Housing": 3.90, "Health": 9.10, "Internet": 9.30, "Cost": 4.20},
    {"City": "Tartu", "Country": "Estonia", "Continent": "Europe", "Safety": 9.10, "Economy": 5.20, "Housing": 8.20, "Health": 8.80, "Internet": 9.40, "Cost": 7.90}
]
"""
data = json.loads(raw_data_json)
df = pd.DataFrame(data)

# --- 2. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Safe Haven Strategic Navigator", layout="wide")

# Theme: Midnight and Gold
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: #161B22; border: 1px solid #D4AF37; padding: 20px; border-radius: 12px; }
    div[data-testid="stMetricValue"] { color: #D4AF37; }
    .stSlider > div > div > div > div { background-color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: DYNAMIC WEIGHTING ENGINE ---
st.sidebar.title("🛡️ Strategic Priorities")
st.sidebar.markdown("Balance the model according to your immediate survival needs.")

w_safety = st.sidebar.slider("Security & Invisibility", 0.0, 1.0, 0.40)
w_econ = st.sidebar.slider("Career & Economic Strength", 0.0, 1.0, 0.25)
w_afford = st.sidebar.slider("Sustainability (Affordability)", 0.0, 1.0, 0.20)
w_health = st.sidebar.slider("Wellness & Digital Infrastructure", 0.0, 1.0, 0.15)

# Normalization
total_w = w_safety + w_econ + w_afford + w_health
if total_w > 0:
    ws, we, wa, wh = w_safety/total_w, w_econ/total_w, w_afford/total_w, w_health/total_w
else:
    ws, we, wa, wh = 0.40, 0.25, 0.20, 0.15

# --- 4. MODEL CALCULATION ---
# Calculate the Dynamic Safe Haven Index
df['Affordability_Score'] = (df['Housing'] + df['Cost']) / 2
df['Wellness_Score'] = (df['Health'] + df['Internet']) / 2
df['Final_Score'] = (
    df['Safety'] * ws + 
    df['Economy'] * we + 
    df['Affordability_Score'] * wa + 
    df['Wellness_Score'] * wh
)

top_data = df.sort_values('Final_Score', ascending=False)
top_city = top_data.iloc[0]

# --- 5. DASHBOARD LAYOUT ---
st.title("GLOBAL SAFE HAVEN COMMAND CENTER")
st.markdown("_Strategic decision-support for high-risk profiles seeking long-term integration._")

# Top Level Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Recommended Haven", top_city['City'])
m2.metric("Safety Rating", f"{top_city['Safety']}/10")
m3.metric("Economic Viability", f"{top_city['Economy']}/10")
m4.metric("Aggregate Score", round(top_city['Final_Score'], 2))

st.markdown("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # 1. Map of Safe Havens
    st.subheader("Geographic Site Suitability")
    fig_map = px.scatter_geo(
        top_data.head(15), locations="Country", locationmode="country names",
        size="Final_Score", color="Final_Score", hover_name="City",
        projection="natural earth", color_continuous_scale="YlOrRd",
        template="plotly_dark"
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

    # 2. Risk vs Opportunity Quadrant
    st.subheader("The Opportunity Quadrant (Security vs. Economy)")
    fig_quad = px.scatter(
        top_data, x="Economy", y="Safety", size="Final_Score",
        color="Continent", hover_name="City",
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="plotly_dark"
    )
    fig_quad.add_hline(y=df['Safety'].median(), line_dash="dash", opacity=0.3)
    fig_quad.add_vline(x=df['Economy'].median(), line_dash="dash", opacity=0.3)
    fig_quad.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_quad, use_container_width=True)

with col_right:
    # 3. Efficiency Ranking
    st.subheader("Top 10 Survival Index")
    fig_bar = px.bar(
        top_data.head(10), x='Final_Score', y='City', orientation='h',
        color='Final_Score', color_continuous_scale='Magma'
    )
    fig_bar.update_layout(template="plotly_dark", yaxis={'categoryorder':'total ascending'}, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

    # 4. Profile Radar for Top City
    st.subheader(f"Profile Profile: {top_city['City']}")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[top_city['Safety'], top_city['Economy'], top_city['Affordability_Score'], top_city['Wellness_Score']],
        theta=['Security', 'Economy', 'Affordability', 'Wellness'],
        fill='toself', line_color='#D4AF37'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 6. DATA EXPLORER ---
with st.expander("🔍 View Comprehensive Risk Matrix"):
    st.dataframe(top_data[['City', 'Country', 'Final_Score', 'Safety', 'Economy', 'Affordability_Score', 'Wellness_Score']], use_container_width=True)

st.sidebar.info("Model Note: Higher weights on Safety favor cities like Singapore and Taipei. Prioritizing Affordability highlights Tallinn and Cluj-Napoca.")
