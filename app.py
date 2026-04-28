import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Natural Disasters Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Google Fonts ─── */
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

/* ─── Global ─── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="collapsedControl"],
button[kind="header"] {
    display: none !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}

/* ─── Metric Cards ─── */
[data-testid="metric-container"] {
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 16px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.10);
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Merriweather', serif;
    font-size: 1.7rem;
    font-weight: 900;
}

/* ─── Section Headers ─── */
.section-header {
    font-family: 'Merriweather', serif;
    font-size: 1.3rem;
    font-weight: 900;
    border-left: 4px solid #3b5998;
    padding-left: 14px;
    margin: 28px 0 16px 0;
    letter-spacing: -0.01em;
}

/* ─── Student Card ─── */
.student-card {
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 12px 0 20px 0;
    text-align: center;
    background: rgba(128,128,255,0.05);
}
.student-card .name {
    font-family: 'Merriweather', serif;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 2px;
}
.student-card .sid {
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    opacity: 0.8;
}
.student-card .module {
    font-size: 0.7rem;
    margin-top: 4px;
    opacity: 0.6;
}

/* ─── Executive / Info Cards ─── */
.exec-card {
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 18px;
    padding: 24px 26px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    background: rgba(128,128,255,0.03);
}
.exec-card:hover {
    border-color: #3b5998;
    box-shadow: 0 4px 16px rgba(59,89,152,0.12);
}
.exec-card h4 {
    font-family: 'Merriweather', serif;
    font-size: 1rem;
    margin-bottom: 10px;
}
.exec-card p {
    font-size: 0.92rem;
    line-height: 1.7;
}
.exec-card .highlight {
    color: #3b82f6 !important;
    font-weight: 600;
}

/* ─── Insight Pills ─── */
.insight-pill {
    display: inline-block;
    border: 1px solid rgba(99,102,241,0.4);
    color: #818cf8 !important;
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.82rem;
    margin: 4px 3px;
    background: rgba(99,102,241,0.1);
}
.insight-pill-warn {
    border-color: rgba(239,68,68,0.4);
    color: #f87171 !important;
    background: rgba(239,68,68,0.08);
}
.insight-pill-ok {
    border-color: rgba(34,197,94,0.4);
    color: #4ade80 !important;
    background: rgba(34,197,94,0.08);
}

/* ─── Divider ─── */
.fancy-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(128,128,200,0.3), transparent);
    margin: 28px 0;
}

/* ─── Page Title ─── */
.dash-title {
    font-family: 'Merriweather', serif;
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.dash-subtitle {
    font-size: 0.9rem;
    margin-top: 4px;
    letter-spacing: 0.02em;
    opacity: 0.6;
}

/* ─── Dataframe ─── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.2);
    overflow: hidden;
}

/* ─── Selectbox & multiselect ─── */
[data-testid="stSelectbox"] > div,
[data-testid="stMultiSelect"] > div {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Plotly light theme ──────────────────────────────────────────────────────
def apply_theme(fig, h=420):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        height=h,
        margin=dict(l=8, r=8, t=44, b=8),
        legend=dict(font=dict(size=10, color="#1a1a2e"), bgcolor="rgba(255,255,255,0.8)"),
        xaxis=dict(gridcolor="rgba(59,89,152,0.1)", zerolinecolor="rgba(59,89,152,0.15)", color="#2d3748"),
        yaxis=dict(gridcolor="rgba(59,89,152,0.1)", zerolinecolor="rgba(59,89,152,0.15)", color="#2d3748"),
        title_font=dict(family="Merriweather, serif", size=15, color="#0d0d1a"),
    )
    return fig

# ── Load Data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("emdat_cleaned.csv")
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Student info
    st.markdown("""
    <div class="student-card">
        <div class="name">Yogaraja Bawadharani</div>
        <div class="sid">UoW ID: w2149494</div>
        <div class="sid">IIT ID: 20233004</div>
        <div class="module">5DATA004C · University of Westminster</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "",
        ["🏠 Overview", "📋 Executive Summary", "🗺️ Geographic Impact",
         "📈 Trends Over Time", "🔍 Distribution Analysis", "🏆 Country Rankings", "📋 Data Table"],
        label_visibility="collapsed"
    )

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown("### 🔎 Filters")

    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())
    year_range = st.slider("📅 Year Range", min_value=year_min, max_value=year_max, value=(2000, 2024))

    all_types = sorted(df["Disaster Type"].dropna().unique().tolist())
    selected_types = st.multiselect("🌪️ Disaster Types", options=all_types, default=all_types)

    all_subgroups = sorted(df["Disaster Subgroup"].dropna().unique().tolist())
    selected_subgroups = st.multiselect("📂 Subgroups", options=all_subgroups, default=all_subgroups)

    all_countries = sorted(df["Country"].dropna().unique().tolist())
    selected_countries = st.multiselect("🌍 Country (optional)", options=all_countries, default=[])

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.caption("📊 Data: EM-DAT – CRED via Humanitarian Data Exchange (HDX)")

# ── Filter ───────────────────────────────────────────────────────────────────
mask = (
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["Disaster Type"].isin(selected_types)) &
    (df["Disaster Subgroup"].isin(selected_subgroups))
)
if selected_countries:
    mask &= df["Country"].isin(selected_countries)
filtered = df[mask].copy()

metric_labels = {
    "Total Deaths": "Deaths",
    "Total Affected": "People Affected",
    "Total Events": "Disaster Count",
    "Total Damage (USD, adjusted)": "Economic Damage (USD)"
}

# ── Page header (persistent) ─────────────────────────────────────────────────
st.markdown("""
<div class="dash-title">🌍 Global Natural Disasters</div>
<div class="dash-subtitle">Interactive Intelligence Dashboard · EM-DAT Dataset · 2000–2026</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ── KPI Strip (always visible) ───────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("🌪️ Disaster Events", f"{int(filtered['Total Events'].sum()):,}")
k2.metric("💀 Total Deaths", f"{int(filtered['Total Deaths'].sum()):,}")
k3.metric("👥 People Affected", f"{filtered['Total Affected'].sum()/1_000_000:.1f}M")
k4.metric("💰 Economic Damage", f"${filtered['Total Damage (USD, adjusted)'].sum()/1_000_000_000:.1f}B")
st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown('<div class="section-header">📌 Dashboard Overview</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="exec-card">
        <h4>About This Dashboard</h4>
        <p>
        This dashboard presents an in-depth analysis of <span class="highlight">global natural disaster data</span>
        sourced from the EM-DAT International Disaster Database (CRED), accessed via the Humanitarian Data Exchange (HDX).
        The dataset spans <span class="highlight">{year_range[0]} to {year_range[1]}</span> and covers
        <span class="highlight">{filtered['Country'].nunique()} countries</span> across
        <span class="highlight">{len(selected_types)} disaster types</span>.
        </p>
        <p style="margin-top:10px">
        It was developed as part of the <span class="highlight">5DATA004C Data Science Project Lifecycle</span>
        module at the University of Westminster, presented in the context of a global sustainability conference.
        The goal is to equip high-level decision-makers, finance professionals, and technology experts
        with actionable insights into the frequency, scale, and economic toll of natural disasters worldwide.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔑 Snapshot Highlights</div>', unsafe_allow_html=True)
    ov1, ov2 = st.columns(2)
    with ov1:
        freq_df = filtered.groupby("Year")["Total Events"].sum().reset_index()
        fig = px.area(freq_df, x="Year", y="Total Events",
                      title="Total Disaster Events Per Year",
                      color_discrete_sequence=["#3b5998"])
        fig.update_traces(fillcolor="rgba(59,89,152,0.15)", line_color="#3b5998")
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with ov2:
        top_type = filtered.groupby("Disaster Type")["Total Deaths"].sum().sort_values(ascending=False).reset_index().head(6)
        fig2 = px.bar(top_type, x="Disaster Type", y="Total Deaths",
                      title="Deaths by Disaster Type (Top 6)",
                      color="Total Deaths", color_continuous_scale=["#bfdbfe","#3b5998","#1e3a8a"])
        fig2.update_layout(coloraxis_showscale=False)
        apply_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <p style="color:#6b7280;font-size:0.78rem;text-align:center;margin-top:8px">
    Analysing <b>{len(filtered):,}</b> records · Filters applied via sidebar · Built with Streamlit & Plotly
    </p>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════════
elif page == "📋 Executive Summary":
    st.markdown('<div class="section-header">📋 Executive Summary</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#4a5568;font-size:0.88rem;margin-bottom:20px">
    This section provides evidence-based answers to the core research questions driving this analysis,
    drawn from the EM-DAT dataset (2000–2026).
    </p>
    """, unsafe_allow_html=True)

    # ── RQ1 ──
    top_death_type = filtered.groupby("Disaster Type")["Total Deaths"].sum().idxmax()
    top_death_val = filtered.groupby("Disaster Type")["Total Deaths"].sum().max()
    st.markdown(f"""
    <div class="exec-card">
        <h4>🔬 RQ1 — Which disaster types cause the most deaths globally?</h4>
        <p>
        Analysis of the EM-DAT dataset reveals that <span class="highlight">{top_death_type}</span> is responsible
        for the highest cumulative death toll among all recorded natural disaster types, accounting for
        <span class="highlight">{int(top_death_val):,} deaths</span> between {year_range[0]} and {year_range[1]}.
        Geophysical disasters such as earthquakes are especially lethal due to their sudden onset, the collapse of
        infrastructure, and limited warning time. Storms are the second major contributor, particularly in
        coastal and low-lying regions. By contrast, droughts and extreme temperature events tend to produce
        slower-onset mortality, often affecting already-vulnerable populations over extended periods.
        </p>
        <p style="margin-top:8px">
        <span class="insight-pill insight-pill-warn">⚠ Earthquakes: highest single-event lethality</span>
        <span class="insight-pill insight-pill-warn">⚠ Storms: highest total frequency globally</span>
        <span class="insight-pill">📌 Climatological events: slower but persistent toll</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── RQ2 ──
    yearly_events = filtered.groupby("Year")["Total Events"].sum()
    trend_pct = ((yearly_events.iloc[-1] - yearly_events.iloc[0]) / yearly_events.iloc[0] * 100) if yearly_events.iloc[0] > 0 else 0
    st.markdown(f"""
    <div class="exec-card">
        <h4>📈 RQ2 — Has the frequency of natural disasters increased over time?</h4>
        <p>
        The data indicates a <span class="highlight">clear upward trend</span> in the frequency of recorded
        natural disaster events from {year_range[0]} to {year_range[1]}.
        Hydrological events — particularly floods — have seen the most consistent growth in frequency,
        likely driven by intensifying precipitation patterns linked to climate change. Meteorological
        disasters such as storms have also increased, reflecting shifting atmospheric conditions.
        The rise in recorded events may also be partially attributed to improved global reporting
        infrastructure, which captures incidents that would previously have gone unrecorded, particularly
        in lower-income nations.
        </p>
        <p style="margin-top:8px">
        <span class="insight-pill insight-pill-warn">📊 Floods: fastest-growing disaster type</span>
        <span class="insight-pill insight-pill-warn">🌡️ Climate signals visible post-2010</span>
        <span class="insight-pill">📡 Improved reporting may amplify apparent growth</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── RQ3 ──
    top_damage_country = filtered.groupby("Country")["Total Damage (USD, adjusted)"].sum().idxmax()
    top_damage_val = filtered.groupby("Country")["Total Damage (USD, adjusted)"].sum().max()
    top_death_country = filtered.groupby("Country")["Total Deaths"].sum().idxmax()
    st.markdown(f"""
    <div class="exec-card">
        <h4>🌍 RQ3 — Which countries are most economically and humanitarianly impacted?</h4>
        <p>
        In terms of <span class="highlight">economic damage</span>, <span class="highlight">{top_damage_country}</span>
        bears the greatest burden, with inflation-adjusted losses exceeding
        <span class="highlight">${top_damage_val/1_000_000_000:.1f}B USD</span> over the study period.
        High-income countries tend to experience greater economic losses due to higher asset values exposed
        to risk, while lower-income nations suffer disproportionately higher death tolls relative to their
        population size. <span class="highlight">{top_death_country}</span> records the highest cumulative
        deaths, highlighting the stark disparity between economic and humanitarian impact.
        </p>
        <p style="margin-top:8px">
        <span class="insight-pill insight-pill-warn">💸 Wealthiest nations: highest absolute economic losses</span>
        <span class="insight-pill insight-pill-warn">⚠️ Developing nations: disproportionate death tolls</span>
        <span class="insight-pill insight-pill-ok">✅ Resilience investment critical for at-risk nations</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── RQ4 ──
    top_affected_type = filtered.groupby("Disaster Type")["Total Affected"].sum().idxmax()
    top_affected_val = filtered.groupby("Disaster Type")["Total Affected"].sum().max()
    st.markdown(f"""
    <div class="exec-card">
        <h4>👥 RQ4 — Which disasters affect the largest number of people?</h4>
        <p>
        <span class="highlight">{top_affected_type}</span> events are the leading cause of mass displacement
        and humanitarian need, affecting approximately <span class="highlight">{top_affected_val/1_000_000:.1f} million people</span>
        over the analysis period. These events are particularly impactful because they cover vast geographic
        areas and are often slow to recede, prolonging the humanitarian crisis. The economic damage from
        droughts and floods also feeds into long-term food insecurity, water scarcity, and infrastructure
        degradation — compounding the humanitarian burden well beyond the initial event.
        </p>
        <p style="margin-top:8px">
        <span class="insight-pill insight-pill-warn">🌊 Floods & Droughts: highest people affected</span>
        <span class="insight-pill">📌 Displacement compounds downstream economic loss</span>
        <span class="insight-pill insight-pill-ok">✅ Early warning systems reduce affected populations</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Takeaways ──
    st.markdown('<div class="section-header">💡 Key Recommendations for Decision-Makers</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        <div class="exec-card">
            <h4>🏛️ Policy</h4>
            <p>Prioritise early-warning systems and climate-resilient infrastructure investment
            in flood and storm-prone regions, particularly across South and Southeast Asia.</p>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="exec-card">
            <h4>💰 Finance</h4>
            <p>Expand parametric insurance and disaster risk financing mechanisms for
            lower-income countries with high humanitarian exposure but limited economic buffers.</p>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="exec-card">
            <h4>💻 Technology</h4>
            <p>Leverage satellite monitoring, AI-driven risk modelling, and open data platforms
            (like EM-DAT) to improve disaster preparedness and resource allocation.</p>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE: GEOGRAPHIC IMPACT
# ════════════════════════════════════════════════════════════════
elif page == "🗺️ Geographic Impact":
    st.markdown('<div class="section-header">🗺️ Geographic Impact & Disaster Type Breakdown</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        map_metric = st.selectbox("Metric for choropleth map:", options=list(metric_labels.keys()), key="map_metric")
        map_df = filtered.groupby(["Country", "ISO"])[map_metric].sum().reset_index()
        fig_map = px.choropleth(
            map_df, locations="ISO", color=map_metric, hover_name="Country",
            hover_data={map_metric: True, "ISO": False},
            color_continuous_scale=["#dbeafe","#93c5fd","#3b82f6","#1d4ed8","#1e3a8a","#172554"],
            labels={map_metric: metric_labels[map_metric]},
            title=f"{metric_labels[map_metric]} by Country ({year_range[0]}–{year_range[1]})"
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="rgba(255,255,255,0)",
            font=dict(color="#1a1a2e"), height=420,
            geo=dict(showframe=False, showcoastlines=True,
                     bgcolor="rgba(0,0,0,0)",
                     coastlinecolor="rgba(128,128,200,0.5)"),
            margin=dict(l=0, r=0, t=44, b=0),
            title_font=dict(family="Merriweather, serif", size=15, color="#0d0d1a"),
            coloraxis_colorbar=dict(tickfont=dict(color="#2d3748"), title=dict(font=dict(color="#2d3748")))
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        bar_metric = st.selectbox("Metric for bar chart:", options=list(metric_labels.keys()), key="bar_metric")
        type_df = filtered.groupby("Disaster Type")[bar_metric].sum().sort_values(ascending=True).reset_index()
        fig_bar = px.bar(
            type_df, x=bar_metric, y="Disaster Type", orientation="h",
            color=bar_metric, color_continuous_scale=["#bfdbfe","#3b82f6","#1e3a8a"],
            title=f"{metric_labels[bar_metric]} by Disaster Type",
            labels={bar_metric: metric_labels[bar_metric], "Disaster Type": ""}
        )
        fig_bar.update_layout(coloraxis_showscale=False)
        apply_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE: TRENDS OVER TIME
# ════════════════════════════════════════════════════════════════
elif page == "📈 Trends Over Time":
    st.markdown('<div class="section-header">📈 Trends Over Time</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        freq_df = filtered.groupby(["Year", "Disaster Type"])["Total Events"].sum().reset_index()
        fig_line = px.line(
            freq_df, x="Year", y="Total Events", color="Disaster Type", markers=True,
            title="Disaster Frequency by Type Over Time",
            labels={"Total Events": "Number of Disasters", "Year": "Year"}
        )
        apply_theme(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)

    with col4:
        econ_df = filtered.groupby("Year")["Total Damage (USD, adjusted)"].sum().reset_index()
        econ_df["Damage (USD Billions)"] = econ_df["Total Damage (USD, adjusted)"] / 1_000_000_000
        fig_area = px.area(
            econ_df, x="Year", y="Damage (USD Billions)",
            title="Total Economic Losses Over Time (Inflation-Adjusted)",
            labels={"Damage (USD Billions)": "Damage (USD Billions)"},
            color_discrete_sequence=["#2563eb"]
        )
        fig_area.update_traces(fillcolor="rgba(37,99,235,0.12)", line_color="#2563eb")
        apply_theme(fig_area)
        st.plotly_chart(fig_area, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        death_df = filtered.groupby(["Year", "Disaster Type"])["Total Deaths"].sum().reset_index()
        fig_death = px.line(
            death_df, x="Year", y="Total Deaths", color="Disaster Type", markers=False,
            title="Deaths by Disaster Type Over Time",
            labels={"Total Deaths": "Deaths", "Year": "Year"}
        )
        apply_theme(fig_death)
        st.plotly_chart(fig_death, use_container_width=True)

    with col6:
        aff_df = filtered.groupby("Year")["Total Affected"].sum().reset_index()
        aff_df["Affected (Millions)"] = aff_df["Total Affected"] / 1_000_000
        fig_aff = px.bar(
            aff_df, x="Year", y="Affected (Millions)",
            title="People Affected Per Year (Millions)",
            color="Affected (Millions)",
            color_continuous_scale=["#dbeafe","#3b82f6","#1e3a8a"]
        )
        fig_aff.update_layout(coloraxis_showscale=False)
        apply_theme(fig_aff)
        st.plotly_chart(fig_aff, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE: DISTRIBUTION ANALYSIS
# ════════════════════════════════════════════════════════════════
elif page == "🔍 Distribution Analysis":
    st.markdown('<div class="section-header">🔍 Distribution & Relationship Analysis</div>', unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        donut_df = filtered.groupby("Disaster Type")["Total Events"].sum().reset_index()
        fig_donut = px.pie(
            donut_df, values="Total Events", names="Disaster Type", hole=0.52,
            title="Share of Disasters by Type",
            color_discrete_sequence=["#1e3a8a","#2563eb","#3b82f6","#60a5fa","#93c5fd","#bfdbfe","#1d4ed8","#1e40af","#172554","#dbeafe"]
        )
        fig_donut.update_traces(textfont_color="white")
        apply_theme(fig_donut)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col8:
        scatter_df = filtered.groupby("Disaster Type").agg(
            Deaths=("Total Deaths", "sum"),
            Affected=("Total Affected", "sum"),
            Events=("Total Events", "sum")
        ).reset_index()
        fig_scatter = px.scatter(
            scatter_df, x="Affected", y="Deaths", size="Events", color="Disaster Type",
            hover_name="Disaster Type", size_max=60,
            title="Deaths vs People Affected (bubble = event count)",
            labels={"Affected": "Total People Affected", "Deaths": "Total Deaths"},
            color_discrete_sequence=["#1e3a8a","#2563eb","#3b82f6","#60a5fa","#93c5fd","#bfdbfe","#1d4ed8","#1e40af"]
        )
        apply_theme(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown('<div class="section-header">📂 Subgroup Breakdown</div>', unsafe_allow_html=True)
    sg1, sg2 = st.columns(2)
    with sg1:
        sg_df = filtered.groupby("Disaster Subgroup")["Total Events"].sum().reset_index()
        fig_sg = px.pie(
            sg_df, values="Total Events", names="Disaster Subgroup", hole=0.45,
            title="Events by Disaster Subgroup",
            color_discrete_sequence=["#1e3a8a","#2563eb","#3b82f6","#60a5fa","#1d4ed8","#172554"]
        )
        fig_sg.update_traces(textfont_color="white")
        apply_theme(fig_sg)
        st.plotly_chart(fig_sg, use_container_width=True)

    with sg2:
        sg_d = filtered.groupby("Disaster Subgroup")["Total Deaths"].sum().sort_values(ascending=True).reset_index()
        fig_sgb = px.bar(
            sg_d, x="Total Deaths", y="Disaster Subgroup", orientation="h",
            title="Deaths by Disaster Subgroup",
            color="Total Deaths", color_continuous_scale=["#bfdbfe","#3b82f6","#1e3a8a"]
        )
        fig_sgb.update_layout(coloraxis_showscale=False)
        apply_theme(fig_sgb)
        st.plotly_chart(fig_sgb, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE: COUNTRY RANKINGS
# ════════════════════════════════════════════════════════════════
elif page == "🏆 Country Rankings":
    st.markdown('<div class="section-header">🏆 Country-Level Analysis</div>', unsafe_allow_html=True)

    col9, col10 = st.columns(2)
    with col9:
        top_metric = st.selectbox("Rank countries by:", options=list(metric_labels.keys()), key="top_metric")
        top_df = filtered.groupby("Country")[top_metric].sum().nlargest(10).sort_values(ascending=True).reset_index()
        fig_top = px.bar(
            top_df, x=top_metric, y="Country", orientation="h",
            color=top_metric, color_continuous_scale=["#dbeafe","#3b82f6","#1e3a8a"],
            title=f"Top 10 Countries by {metric_labels[top_metric]}",
            labels={top_metric: metric_labels[top_metric], "Country": ""}
        )
        fig_top.update_layout(coloraxis_showscale=False)
        apply_theme(fig_top)
        st.plotly_chart(fig_top, use_container_width=True)

    with col10:
        stacked_df = filtered.groupby(["Year", "Disaster Subgroup"])["Total Events"].sum().reset_index()
        fig_stacked = px.bar(
            stacked_df, x="Year", y="Total Events", color="Disaster Subgroup",
            title="Disasters per Year by Subgroup (Stacked)",
            labels={"Total Events": "Number of Disasters", "Disaster Subgroup": "Subgroup"},
            color_discrete_sequence=["#1e3a8a","#2563eb","#3b82f6","#60a5fa","#93c5fd","#bfdbfe"]
        )
        apply_theme(fig_stacked)
        st.plotly_chart(fig_stacked, use_container_width=True)

    st.markdown('<div class="section-header">🌿 Least Affected Countries</div>', unsafe_allow_html=True)
    least_metric = st.selectbox("Metric:", options=list(metric_labels.keys()), key="least_metric")
    least_df = filtered.groupby("Country")[least_metric].sum()
    least_df = least_df[least_df > 0].nsmallest(10).sort_values(ascending=False).reset_index()
    fig_least = px.bar(
        least_df, x="Country", y=least_metric,
        title=f"10 Least-Affected Countries by {metric_labels[least_metric]}",
        color=least_metric, color_continuous_scale=["#d1fae5","#34d399","#065f46"]
    )
    fig_least.update_layout(coloraxis_showscale=False)
    apply_theme(fig_least)
    st.plotly_chart(fig_least, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE: DATA TABLE
# ════════════════════════════════════════════════════════════════
elif page == "📋 Data Table":
    st.markdown('<div class="section-header">📋 Filtered Data Table</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <p style="color:#4a5568;margin-bottom:16px">
    Showing <b>{len(filtered):,}</b> rows based on your current sidebar filters.
    </p>
    """, unsafe_allow_html=True)

    display_cols = ["Year", "Country", "Disaster Type", "Disaster Subtype",
                    "Total Events", "Total Deaths", "Total Affected", "Total Damage (USD, adjusted)"]
    st.dataframe(
        filtered[display_cols].sort_values("Total Deaths", ascending=False).reset_index(drop=True),
        use_container_width=True, height=500
    )

    csv_data = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_disasters.csv",
        mime="text/csv"
    )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
st.markdown("""
<p style="color:#9ca3af;font-size:0.75rem;text-align:center">
📊 Data: EM-DAT – The International Disaster Database | Centre for Research on the Epidemiology of Disasters (CRED)<br>
Accessed via Humanitarian Data Exchange (HDX) | Dashboard built with Streamlit & Plotly<br>
5DATA004C Data Science Project Lifecycle · University of Westminster
</p>
""", unsafe_allow_html=True)
