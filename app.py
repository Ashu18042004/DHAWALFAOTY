import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- ARCHITECTURAL DATASET ---
# Derived from the Safe Haven Dynamic Dataset
data = [
    {"City": "Singapore", "Country": "Singapore", "Continent": "Asia", "Safety": 9.97, "Economy": 8.75, "Business": 8.90, "Housing": 2.50, "Cost": 3.10, "Health": 8.90, "Internet": 9.10, "Startups": 8.50},
    {"City": "Tallinn", "Country": "Estonia", "Continent": "Europe", "Safety": 9.43, "Economy": 5.87, "Business": 8.20, "Housing": 7.80, "Cost": 7.20, "Health": 9.10, "Internet": 9.50, "Startups": 7.80},
    {"City": "Taipei", "Country": "Taiwan", "Continent": "Asia", "Safety": 9.54, "Economy": 5.81, "Business": 7.40, "Housing": 6.90, "Cost": 6.90, "Health": 8.80, "Internet": 8.10, "Startups": 6.20},
    {"City": "Munich", "Country": "Germany", "Continent": "Europe", "Safety": 9.05, "Economy": 6.97, "Business": 8.10, "Housing": 4.20, "Cost": 4.50, "Health": 9.20, "Internet": 7.50, "Startups": 7.10},
    {"City": "Doha", "Country": "Qatar", "Continent": "Asia", "Safety": 9.49, "Economy": 9.39, "Business": 7.41, "Housing": 2.13, "Cost": 6.18, "Health": 7.43, "Internet": 3.25, "Startups": 2.69},
    {"City": "Zurich", "Country": "Switzerland", "Continent": "Europe", "Safety": 9.33, "Economy": 8.99, "Business": 9.10, "Housing": 1.10, "Cost": 2.10, "Health": 9.50, "Internet": 8.90, "Startups": 8.20},
    {"City": "Tokyo", "Country": "Japan", "Continent": "Asia", "Safety": 9.20, "Economy": 7.20, "Business": 8.40, "Housing": 4.00, "Cost": 4.00, "Health": 9.50, "Internet": 8.80, "Startups": 7.50},
    {"City": "Cluj-Napoca", "Country": "Romania", "Continent": "Europe", "Safety": 9.15, "Economy": 5.10, "Business": 6.80, "Housing": 8.50, "Cost": 8.20, "Health": 7.80, "Internet": 9.10, "Startups": 4.50},
    {"City": "Helsinki", "Country": "Finland", "Continent": "Europe", "Safety": 9.00, "Economy": 5.90, "Business": 8.10, "Housing": 5.20, "Cost": 4.80, "Health": 9.40, "Internet": 9.10, "Startups": 6.40},
    {"City": "Vienna", "Country": "Austria", "Continent": "Europe", "Safety": 8.70, "Economy": 6.40, "Business": 7.90, "Housing": 6.10, "Cost": 5.40, "Health": 9.30, "Internet": 8.50, "Startups": 6.10}
]

df = pd.DataFrame(data)

# --- MODEL CALCULATION ---
# Applying fixed mathematical weights
df['Security_Score'] = df['Safety'] * 0.40
df['Economic_Score'] = ((df['Economy'] + df['Business'] + df['Startups']) / 3) * 0.25
df['Sustainability_Score'] = ((df['Housing'] + df['Cost']) / 2) * 0.20
df['Infrastructure_Score'] = ((df['Health'] + df['Internet']) / 2) * 0.15
df['Weighted_Index'] = df['Security_Score'] + df['Economic_Score'] + df['Sustainability_Score'] + df['Infrastructure_Score']

# --- INTERFACE CONFIGURATION ---
st.set_page_config(page_title="Safe Haven Analysis", layout="wide")

# Minimalist Slate Theme
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1E293B; color: #F8FAFC; border: 1px solid #334155; }
    .metric-card { background-color: #1E293B; border: 1px solid #334155; padding: 20px; border-radius: 4px; }
    h1, h2, h3 { color: #E2E8F0; font-weight: 300; letter-spacing: -0.5px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("SAFE HAVEN STRATEGIC ANALYSIS")
st.markdown("Quantitative assessment for site selection and long-term integration.")

# --- ANALYTICAL CONTROLS ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Subject Profiling")
    selected_city = st.selectbox("Select Target City for Audit", df['City'].unique())
    city_stats = df[df['City'] == selected_city].iloc[0]
    
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #94A3B8; margin-bottom: 5px;">Strategic Index Score</p>
        <h2 style="margin-top: 0;">{city_stats['Weighted_Index']:.2f}</h2>
        <hr style="border-color: #334155;">
        <p><b>Country:</b> {city_stats['Country']}</p>
        <p><b>Security Rating:</b> {city_stats['Safety']}/10</p>
        <p><b>Economic Integration:</b> {city_stats['Economy']}/10</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Comparative Viability Matrix")
    fig_bar = px.bar(
        df.sort_values('Weighted_Index', ascending=True),
        x='Weighted_Index',
        y='City',
        orientation='h',
        color='Weighted_Index',
        color_continuous_scale='Slatebg',
        labels={'Weighted_Index': 'Index Score'}
    )
    fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- DETAIL ANALYSIS ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("Security vs. Economic Growth")
    fig_scatter = px.scatter(
        df, x="Economy", y="Safety", size="Weighted_Index",
        color="Continent", hover_name="City",
        template="plotly_dark"
    )
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col4:
    st.subheader("Structural Components")
    radar_data = pd.DataFrame(dict(
        r=[city_stats['Security_Score']*2.5, city_stats['Economic_Score']*4, 
           city_stats['Sustainability_Score']*5, city_stats['Infrastructure_Score']*6.6],
        theta=['Security', 'Economy', 'Sustainability', 'Infrastructure']))
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_data['r'],
        theta=radar_data['theta'],
        fill='toself',
        line_color='#60A5FA'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- RAW DATA MATRIX ---
with st.expander("Data Source Verification"):
    st.table(df[['City', 'Country', 'Safety', 'Economy', 'Housing', 'Health', 'Weighted_Index']].sort_values('Weighted_Index', ascending=False))
