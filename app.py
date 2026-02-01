import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CORE ARCHITECTURAL DATASET (Top 50 Global Candidates) ---
data = [
    {"City": "Singapore", "Country": "Singapore", "Continent": "Asia", "Safety": 9.97, "Economy": 8.75, "Housing": 2.50, "Cost": 3.10, "Health": 8.90, "Internet": 9.10},
    {"City": "Tallinn", "Country": "Estonia", "Continent": "Europe", "Safety": 9.43, "Economy": 5.87, "Housing": 7.80, "Cost": 7.20, "Health": 9.10, "Internet": 9.50},
    {"City": "Taipei", "Country": "Taiwan", "Continent": "Asia", "Safety": 9.54, "Economy": 6.64, "Housing": 7.98, "Cost": 5.64, "Health": 5.91, "Internet": 5.23},
    {"City": "Doha", "Country": "Qatar", "Continent": "Asia", "Safety": 9.49, "Economy": 9.39, "Housing": 2.13, "Cost": 6.18, "Health": 7.43, "Internet": 3.25},
    {"City": "Zurich", "Country": "Switzerland", "Continent": "Europe", "Safety": 9.33, "Economy": 8.99, "Housing": 1.10, "Cost": 2.10, "Health": 9.50, "Internet": 8.90},
    {"City": "Tokyo", "Country": "Japan", "Continent": "Asia", "Safety": 9.20, "Economy": 7.20, "Housing": 4.00, "Cost": 4.00, "Health": 9.50, "Internet": 8.80},
    {"City": "Munich", "Country": "Germany", "Continent": "Europe", "Safety": 9.05, "Economy": 6.97, "Housing": 4.20, "Cost": 4.50, "Health": 9.20, "Internet": 7.50},
    {"City": "Helsinki", "Country": "Finland", "Continent": "Europe", "Safety": 9.00, "Economy": 5.90, "Housing": 5.20, "Cost": 4.80, "Health": 9.40, "Internet": 9.10},
    {"City": "Seoul", "Country": "South Korea", "Continent": "Asia", "Safety": 8.90, "Economy": 7.80, "Housing": 3.20, "Cost": 4.50, "Health": 9.40, "Internet": 9.80},
    {"City": "Vienna", "Country": "Austria", "Continent": "Europe", "Safety": 8.70, "Economy": 6.40, "Housing": 6.10, "Cost": 5.40, "Health": 9.30, "Internet": 8.50},
    {"City": "Oslo", "Country": "Norway", "Continent": "Europe", "Safety": 8.85, "Economy": 6.40, "Housing": 4.10, "Cost": 3.20, "Health": 9.20, "Internet": 9.00},
    {"City": "Copenhagen", "Country": "Denmark", "Continent": "Europe", "Safety": 9.10, "Economy": 6.50, "Housing": 4.00, "Cost": 3.90, "Health": 9.30, "Internet": 9.20},
    {"City": "Reykjavik", "Country": "Iceland", "Safety": 9.18, "Economy": 5.20, "Housing": 6.10, "Cost": 4.10, "Health": 8.90, "Internet": 9.30},
    {"City": "Cluj-Napoca", "Country": "Romania", "Continent": "Europe", "Safety": 9.15, "Economy": 5.10, "Housing": 8.50, "Cost": 8.20, "Health": 7.80, "Internet": 9.10},
    {"City": "Eindhoven", "Country": "Netherlands", "Continent": "Europe", "Safety": 8.85, "Economy": 6.12, "Housing": 4.50, "Cost": 5.10, "Health": 8.90, "Internet": 8.80},
    {"City": "Prague", "Country": "Czech Republic", "Safety": 8.60, "Economy": 6.10, "Housing": 7.20, "Cost": 6.80, "Health": 8.50, "Internet": 8.20},
    {"City": "Hong Kong", "Country": "Hong Kong", "Continent": "Asia", "Safety": 8.50, "Economy": 8.90, "Housing": 1.00, "Cost": 2.50, "Health": 8.80, "Internet": 8.90},
    {"City": "Ljubljana", "Country": "Slovenia", "Safety": 8.90, "Economy": 4.80, "Housing": 7.90, "Cost": 7.50, "Health": 8.10, "Internet": 8.40},
    {"City": "Ottawa", "Country": "Canada", "Continent": "N. America", "Safety": 8.92, "Economy": 5.88, "Housing": 5.10, "Cost": 5.20, "Health": 8.70, "Internet": 8.50},
    {"City": "Stockholm", "Country": "Sweden", "Continent": "Europe", "Safety": 8.40, "Economy": 6.80, "Housing": 3.90, "Cost": 4.20, "Health": 9.10, "Internet": 9.30},
    {"City": "Abu Dhabi", "Country": "UAE", "Continent": "Asia", "Safety": 9.30, "Economy": 8.80, "Housing": 3.80, "Cost": 5.90, "Health": 8.00, "Internet": 4.50},
    {"City": "Luxembourg", "Country": "Luxembourg", "Safety": 8.70, "Economy": 7.50, "Housing": 2.50, "Cost": 3.40, "Health": 9.10, "Internet": 8.80},
    {"City": "Aarhus", "Country": "Denmark", "Safety": 9.32, "Economy": 5.45, "Housing": 4.80, "Cost": 4.10, "Health": 9.40, "Internet": 9.30},
    {"City": "Dubai", "Country": "UAE", "Continent": "Asia", "Safety": 9.15, "Economy": 9.00, "Housing": 3.50, "Cost": 5.50, "Health": 8.10, "Internet": 4.20},
    {"City": "Berne", "Country": "Switzerland", "Safety": 9.40, "Economy": 7.20, "Housing": 2.10, "Cost": 1.90, "Health": 9.60, "Internet": 9.10},
    {"City": "Basel", "Country": "Switzerland", "Safety": 9.20, "Economy": 7.50, "Housing": 1.80, "Cost": 1.70, "Health": 9.50, "Internet": 9.00}
]

df = pd.DataFrame(data)

# --- QUANTITATIVE MODEL ---
df['Sustainability'] = (df['Housing'] + df['Cost']) / 2
df['Infrastructure'] = (df['Health'] + df['Internet']) / 2
df['Weighted_Index'] = (df['Safety'] * 0.45) + (df['Economy'] * 0.25) + (df['Sustainability'] * 0.20) + (df['Infrastructure'] * 0.10)
df = df.sort_values('Weighted_Index', ascending=False)

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="Strategic Site Audit", layout="wide")

# Slate and Midnight Theme
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1E293B; color: #F8FAFC; border: 1px solid #334155; }
    .audit-card { background-color: #1E293B; border: 1px solid #334155; padding: 25px; border-radius: 4px; }
    h1, h2, h3 { color: #E2E8F0; font-weight: 300; letter-spacing: -0.5px; }
    hr { border-color: #334155; }
    </style>
    """, unsafe_allow_html=True)

st.title("SAFE HAVEN STRATEGIC ANALYSIS")
st.markdown("Quantitative assessment for high-risk site selection and professional integration.")

# --- PRIMARY ANALYSIS SECTION ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Site Audit Profile")
    # City selection dropdown
    target_city = st.selectbox("Identify Target City for Audit", df['City'].unique())
    stats = df[df['City'] == target_city].iloc[0]
    
    st.markdown(f"""
    <div class="audit-card">
        <p style="color: #94A3B8; margin-bottom: 5px; font-size: 0.9rem;">Strategic Viability Index</p>
        <h2 style="margin-top: 0; color: #60A5FA; font-size: 2.5rem;">{stats['Weighted_Index']:.2f}</h2>
        <hr>
        <p><b>Jurisdiction:</b> {stats['Country']}</p>
        <p><b>Safety & Anonymity:</b> {stats['Safety']}/10</p>
        <p><b>Market Integration Score:</b> {stats['Economy']}/10</p>
        <p><b>Capital Sustainability:</b> {stats['Sustainability']:.2f}/10</p>
        <p><b>Infrastructure Resilience:</b> {stats['Infrastructure']:.2f}/10</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Comparative Efficiency Ranking")
    fig_bar = px.bar(
        df.head(15).sort_values('Weighted_Index', ascending=True),
        x='Weighted_Index', y='City', orientation='h',
        color='Weighted_Index', color_continuous_scale='Greys',
        labels={'Weighted_Index': 'Viability Index'}
    )
    fig_bar.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- SECONDARY ANALYSIS SECTION ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("Structural Risk-Opportunity Mapping")
    # Scatter plot for Security vs Economy
    fig_scatter = px.scatter(
        df, x="Economy", y="Safety", size="Weighted_Index",
        hover_name="City", color_discrete_sequence=['#64748B'],
        labels={"Economy": "Economic Opportunity", "Safety": "Security & Anonymity"},
        template="plotly_dark"
    )
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col4:
    st.subheader("Pillar Distribution (Audit Target)")
    # Radar chart for multi-dimensional profile
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[stats['Safety'], stats['Economy'], stats['Sustainability'], stats['Infrastructure']],
        theta=['Security', 'Economy', 'Sustainability', 'Infrastructure'],
        fill='toself', line_color='#60A5FA'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], color="#94A3B8")),
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- RAW AUDIT LOG ---
with st.expander("Full Site Matrix Verification"):
    st.table(df[['City', 'Country', 'Weighted_Index', 'Safety', 'Economy', 'Sustainability', 'Infrastructure']])
