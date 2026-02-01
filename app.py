import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- ARCHITECTURAL DATASET ---
# Hardcoded data to ensure zero dependence on external files
data = [
    {"City": "Singapore", "Country": "Singapore", "Continent": "Asia", "Safety": 9.97, "Economy": 8.75, "Housing": 2.50, "Cost": 3.10, "Health": 8.90, "Internet": 9.10},
    {"City": "Tallinn", "Country": "Estonia", "Continent": "Europe", "Safety": 9.43, "Economy": 5.87, "Housing": 7.80, "Cost": 7.20, "Health": 9.10, "Internet": 9.50},
    {"City": "Taipei", "Country": "Taiwan", "Continent": "Asia", "Safety": 9.54, "Economy": 5.81, "Housing": 6.90, "Cost": 6.90, "Health": 8.80, "Internet": 8.10},
    {"City": "Munich", "Country": "Germany", "Continent": "Europe", "Safety": 9.05, "Economy": 6.97, "Housing": 4.20, "Cost": 4.50, "Health": 9.20, "Internet": 7.50},
    {"City": "Zurich", "Country": "Switzerland", "Continent": "Europe", "Safety": 9.33, "Economy": 8.99, "Housing": 1.10, "Cost": 2.10, "Health": 9.50, "Internet": 8.90},
    {"City": "Tokyo", "Country": "Japan", "Continent": "Asia", "Safety": 9.20, "Economy": 7.20, "Housing": 4.00, "Cost": 4.00, "Health": 9.50, "Internet": 8.80},
    {"City": "Doha", "Country": "Qatar", "Continent": "Asia", "Safety": 9.49, "Economy": 9.39, "Housing": 2.13, "Cost": 6.18, "Health": 7.43, "Internet": 3.25},
    {"City": "Cluj-Napoca", "Country": "Romania", "Continent": "Europe", "Safety": 9.15, "Economy": 5.10, "Housing": 8.50, "Cost": 8.20, "Health": 7.80, "Internet": 9.10},
    {"City": "Vienna", "Country": "Austria", "Continent": "Europe", "Safety": 8.70, "Economy": 6.40, "Housing": 6.10, "Cost": 5.40, "Health": 9.30, "Internet": 8.50},
    {"City": "Helsinki", "Country": "Finland", "Continent": "Europe", "Safety": 9.00, "Economy": 5.90, "Housing": 5.20, "Cost": 4.80, "Health": 9.40, "Internet": 9.10}
]

df = pd.DataFrame(data)

# --- MATHEMATICAL MODEL ---
df['Sustainability'] = (df['Housing'] + df['Cost']) / 2
df['Infrastructure'] = (df['Health'] + df['Internet']) / 2
df['Weighted_Index'] = (df['Safety'] * 0.45) + (df['Economy'] * 0.25) + (df['Sustainability'] * 0.20) + (df['Infrastructure'] * 0.10)

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Strategic Site Audit", layout="wide")

# Slate and Midnight Theme (Non-AI, Classy Look)
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1E293B; color: #F8FAFC; border: 1px solid #334155; }
    .audit-card { background-color: #1E293B; border: 1px solid #334155; padding: 25px; border-radius: 4px; }
    h1, h2, h3 { color: #E2E8F0; font-weight: 300; letter-spacing: -0.5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("SAFE HAVEN STRATEGIC ANALYSIS")
st.markdown("Quantitative assessment for high-risk site selection.")

# --- TOP SECTION: CITY AUDIT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("City Audit Profile")
    # Dropdown for specific country/city selection
    selected_city = st.selectbox("Select Target City", df['City'].unique())
    city_stats = df[df['City'] == selected_city].iloc[0]
    
    st.markdown(f"""
    <div class="audit-card">
        <p style="color: #94A3B8; margin-bottom: 5px;">Strategic Viability Index</p>
        <h2 style="margin-top: 0; color: #60A5FA;">{city_stats['Weighted_Index']:.2f}</h2>
        <hr style="border-color: #334155;">
        <p><b>Territory:</b> {city_stats['Country']}</p>
        <p><b>Safety & Anonymity:</b> {city_stats['Safety']}/10</p>
        <p><b>Market Opportunity:</b> {city_stats['Economy']}/10</p>
        <p><b>Capital Sustainability:</b> {city_stats['Sustainability']:.2f}/10</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Comparative Index Ranking")
    # Fixed the color scale to 'Greys' for a classy, slate look
    fig_bar = px.bar(
        df.sort_values('Weighted_Index', ascending=True),
        x='Weighted_Index', y='City', orientation='h',
        color='Weighted_Index', color_continuous_scale='Greys',
        labels={'Weighted_Index': 'Viability Index'}
    )
    fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- BOTTOM SECTION: DATA VISUALS ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("Strategic Profile: Multi-Dimensional Analysis")
    # Profile Radar
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[city_stats['Safety'], city_stats['Economy'], city_stats['Sustainability'], city_stats['Infrastructure']],
        theta=['Security', 'Economy', 'Sustainability', 'Infrastructure'],
        fill='toself', line_color='#60A5FA'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col4:
    st.subheader("Risk-Growth Distribution")
    fig_scatter = px.scatter(
        df, x="Economy", y="Safety", size="Weighted_Index",
        color="Continent", hover_name="City",
        color_discrete_sequence=px.colors.qualitative.Muted,
        template="plotly_dark"
    )
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)
