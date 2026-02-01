import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. EMBEDDED DATASET (No Excel Required) ---
# This contains the top-performing cities from your analysis to ensure the app is lightweight.
raw_data = {
    "City": ["Singapore", "Hong Kong", "Tallinn", "Taipei", "Munich", "Aarhus", "Eindhoven", "Ottawa", "Tokyo", "Cluj-Napoca", "Vienna", "Zurich", "Copenhagen", "Amsterdam", "Berlin"],
    "Country": ["Singapore", "Hong Kong", "Estonia", "Taiwan", "Germany", "Denmark", "Netherlands", "Canada", "Japan", "Romania", "Austria", "Switzerland", "Denmark", "Netherlands", "Germany"],
    "Continent": ["Asia", "Asia", "Europe", "Asia", "Europe", "Europe", "Europe", "North America", "Asia", "Europe", "Europe", "Europe", "Europe", "Europe", "Europe"],
    "Safety": [9.97, 9.35, 9.43, 9.54, 9.05, 9.32, 8.85, 8.92, 9.20, 9.15, 8.90, 9.10, 8.80, 8.50, 8.20],
    "Economy": [8.75, 8.11, 5.87, 5.81, 6.97, 5.45, 6.12, 5.88, 7.20, 5.10, 6.40, 7.80, 6.30, 7.10, 6.80],
    "Affordability": [2.50, 3.10, 7.80, 6.90, 4.20, 4.80, 4.50, 5.10, 4.00, 8.50, 5.20, 2.10, 3.80, 3.50, 4.80],
    "Wellness": [8.90, 8.50, 9.10, 8.80, 9.20, 9.40, 8.90, 8.70, 9.50, 7.80, 9.30, 9.60, 9.40, 9.00, 8.70]
}

df = pd.DataFrame(raw_data)

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="Safe Haven Navigator", layout="wide")

# Custom Professional Theme
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS', sans-serif; }
    .stMetric { background-color: #161B22; border: 1px solid #D4AF37; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: STRATEGIC MODEL ---
st.sidebar.title("🛡️ Survival Model")
st.sidebar.markdown("Adjust priorities for your second chance.")

# Strategic Weights
ws = st.sidebar.slider("Security (Avoid Recapture)", 0.0, 1.0, 0.40)
we = st.sidebar.slider("Economic/Tech Integration", 0.0, 1.0, 0.30)
wa = st.sidebar.slider("Sustainability (Affordability)", 0.0, 1.0, 0.20)
ww = st.sidebar.slider("Wellness (Partner Care)", 0.0, 1.0, 0.10)

# Normalize weights
total = ws + we + wa + ww
if total > 0:
    ws, we, wa, ww = ws/total, we/total, wa/total, ww/total

# Continent Filter
continents = st.sidebar.multiselect("Filter Regions", df['Continent'].unique(), default=df['Continent'].unique())

# --- 4. DYNAMIC CALCULATION ---
df['Final_Score'] = (
    df['Safety'] * ws + 
    df['Economy'] * we + 
    df['Affordability'] * wa + 
    df['Wellness'] * ww
)

filtered_df = df[df['Continent'].isin(continents)].sort_values('Final_Score', ascending=False)
top_city = filtered_df.iloc[0]

# --- 5. DASHBOARD UI ---
st.title("STRATEGIC SAFE HAVEN NAVIGATOR")
st.caption("Applied Analytics for Executive Decision-Making under Uncertainty")

# Metric Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Top Selection", top_city['City'])
col2.metric("Safety Rating", f"{top_city['Safety']}/10")
col3.metric("Economic Viability", f"{top_city['Economy']}/10")
col4.metric("Aggregate Score", round(top_city['Final_Score'], 2))

st.markdown("---")

# Visualizations
left_col, right_col = st.columns([2, 1])

with left_col:
    # Quadrant Analysis
    fig_scatter = px.scatter(
        filtered_df, x="Economy", y="Safety", size="Final_Score",
        color="Continent", hover_name="City",
        title="<b>The Sweet Spot: Security vs. Opportunity</b>",
        labels={"Economy": "Tech/Finance Opportunity", "Safety": "Detection Risk (Safety)"},
        color_discrete_sequence=px.colors.qualitative.Antique
    )
    fig_scatter.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)

    # World Map
    fig_map = px.scatter_geo(
        filtered_df, locations="Country", locationmode="country names",
        size="Final_Score", color="Final_Score", hover_name="City",
        projection="natural earth", title="<b>Geographic Site Suitability</b>",
        color_continuous_scale="Viridis"
    )
    fig_map.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with right_col:
    # Ranking Bar
    st.markdown("#### Rank Efficiency")
    fig_bar = px.bar(
        filtered_df.head(10), x='Final_Score', y='City', orientation='h',
        color='Final_Score', color_continuous_scale='Bluered_r'
    )
    fig_bar.update_layout(template="plotly_dark", showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

    # Radar Chart for Top City
    st.markdown(f"#### Profile: {top_city['City']}")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[top_city['Safety'], top_city['Economy'], top_city['Affordability'], top_city['Wellness']],
        theta=['Safety', 'Economy', 'Affordability', 'Wellness'],
        fill='toself', line_color='#D4AF37'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        template="plotly_dark", showlegend=False, height=300
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Data Explorer
with st.expander("🔍 View Raw Survival Metrics"):
    st.dataframe(filtered_df.style.highlight_max(axis=0, subset=['Final_Score']), use_container_width=True)

st.info("Analysis Note: Higher weights on 'Safety' and 'Economy' favor Singapore/Taipei. Higher weights on 'Affordability' favor Tallinn/Cluj-Napoca.")
