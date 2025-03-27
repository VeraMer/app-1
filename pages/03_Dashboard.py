import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page config for a cleaner look
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)

# Add some custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #1E3A8A;
        margin-top: 1rem;
    }
    .kpi-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .ai-insights {
        background-color: #f0f7ff;
        border-left: 4px solid #3366cc;
        border-radius: 5px;
        padding: 1.25rem;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard title
st.markdown('<div class="main-header">Executive Dashboard</div>', unsafe_allow_html=True)
st.markdown("A comprehensive view of submissions performance and operational metrics")

# Top filter section
st.markdown("### Filters")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    date_range = st.selectbox(
        "Date Range",
        ["Last Quarter", "Last 6 Months", "Year to Date", "Last 12 Months"]
    )

with col2:
    comparison = st.selectbox(
        "Comparison",
        ["vs Previous Period", "vs Same Period Last Year", "vs Target"]
    )

with col3:
    lob_filter = st.multiselect(
        "Line of Business",
        ["All", "Property D&F", "Professional Indemnity", "Cyber", "Marine Cargo", "Energy"],
        default=["All"]
    )

# Generate sample data
def generate_kpi_data():
    return {
        "submissions": {
            "value": random.randint(450, 550),
            "trend": random.uniform(0.05, 0.15),
        },
        "triage_time": {
            "value": random.uniform(0.8, 1.5),
            "trend": random.uniform(-0.1, -0.02),
        },
        "quality_score": {
            "value": random.uniform(7.2, 8.5),
            "trend": random.uniform(0.02, 0.08),
        },
        "processing_rate": {
            "value": random.uniform(0.85, 0.95),
            "trend": random.uniform(0.01, 0.05),
        }
    }

def generate_submissions_data():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_month = datetime.now().month
    recent_months = months[max(0, current_month - 7):current_month]
    
    data = []
    for month in recent_months:
        received = random.randint(140, 220)
        processed = int(received * random.uniform(0.85, 0.98))
        aligned = int(processed * random.uniform(0.5, 0.7))
        not_aligned = processed - aligned
        backlog = received - processed
        
        data.append({
            "month": month,
            "Received": received,
            "Processed": processed,
            "Aligned with Appetite": aligned,
            "Not Aligned": not_aligned,
            "Backlog": backlog
        })
    
    return pd.DataFrame(data)

def generate_lob_data():
    lobs = ["Property D&F", "Professional Indemnity", "Cyber", "Marine Cargo", "Energy"]
    data = []
    
    for lob in lobs:
        submission_count = random.randint(80, 180)
        aligned_pct = random.uniform(0.5, 0.8)
        avg_triage_time = random.uniform(0.7, 2.0)
        data_quality = random.uniform(60, 95)
        
        if lob == "Cyber":
            data_quality = 65  # Intentionally lower for insights
        
        data.append({
            "lob": lob,
            "submission_count": submission_count,
            "aligned_pct": aligned_pct,
            "avg_triage_time": avg_triage_time,
            "data_quality": data_quality
        })
    
    return pd.DataFrame(data)

def generate_broker_data():
    brokers = ["Marsh", "Aon", "WTW", "Howden", "BMS", "Miller", "Gallagher"]
    data = []
    
    for broker in brokers:
        submission_count = random.randint(40, 120)
        aligned_pct = random.uniform(0.4, 0.85)
        avg_triage_time = random.uniform(0.8, 2.2)
        data_quality = random.uniform(65, 95)
        
        if broker == "Howden":  # Make one broker noticeably different for insights
            aligned_pct = 0.82  # High alignment
        elif broker == "Miller":
            aligned_pct = 0.45  # Low alignment
            
        data.append({
            "broker": broker,
            "submission_count": submission_count,
            "aligned_pct": aligned_pct,
            "avg_triage_time": avg_triage_time,
            "data_quality": data_quality
        })
    
    return pd.DataFrame(data)

# Generate the data
kpi_data = generate_kpi_data()
submissions_df = generate_submissions_data()
lob_df = generate_lob_data()
broker_df = generate_broker_data()

# Sparkle emoji with header
st.markdown('<h2 style="font-size: 1.5rem;">✨ Key Insights & Action Items</h2>', unsafe_allow_html=True)

# Use expanders for each insight/action pair
with st.expander("**Submissions backlog** has decreased by **12%** this quarter", expanded=True):
    st.markdown("📍 **Action:** Share workflow improvements with all triage teams.")

with st.expander("**Aviation** submissions have **65%** data completeness score, significantly below other lines", expanded=True):
    st.markdown("📍 **Action:** Work with brokers to improve data quality for Aviation submissions.")

with st.expander("**Howden** is sending the highest proportion of submissions that align with our risk appetite (**82%**)", expanded=True):
    st.markdown("📍 **Action:** Analyse Howden's submission patterns to improve broker guidance.")
# KPI Section
st.markdown('<div class="sub-header">Key Performance Indicators</div>', unsafe_allow_html=True)
kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.markdown(f"""
    <div class="kpi-card">
        <p style="font-size: 1.8rem; font-weight: 700; color: #1E3A8A; margin: 0;">{kpi_data['submissions']['value']}</p>
        <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">Total Submissions</p>
        <p style="font-size: 0.8rem; color: #28a745; margin-top: 0.25rem;">
            +{kpi_data['submissions']['trend']:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown(f"""
    <div class="kpi-card">
        <p style="font-size: 1.8rem; font-weight: 700; color: #1E3A8A; margin: 0;">{kpi_data['triage_time']['value']:.1f} days</p>
        <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">Avg Triage Time</p>
        <p style="font-size: 0.8rem; color: #28a745; margin-top: 0.25rem;">
            {kpi_data['triage_time']['trend']:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""
    <div class="kpi-card">
        <p style="font-size: 1.8rem; font-weight: 700; color: #1E3A8A; margin: 0;">{kpi_data['quality_score']['value']:.1f}/10</p>
        <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">Data Quality Score</p>
        <p style="font-size: 0.8rem; color: #28a745; margin-top: 0.25rem;">
            +{kpi_data['quality_score']['trend']:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown(f"""
    <div class="kpi-card">
        <p style="font-size: 1.8rem; font-weight: 700; color: #1E3A8A; margin: 0;">{kpi_data['processing_rate']['value']:.0%}</p>
        <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">Processing Rate</p>
        <p style="font-size: 0.8rem; color: #28a745; margin-top: 0.25rem;">
            +{kpi_data['processing_rate']['trend']:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Submission Flow Section
st.markdown('<div class="sub-header">Submission Flow</div>', unsafe_allow_html=True)

# Create the visualization for submission flow
fig = px.bar(
    submissions_df,
    x="month",
    y=["Received", "Processed", "Aligned with Appetite", "Not Aligned", "Backlog"],
    title="Submission Volume by Month",
    barmode="group",
    color_discrete_map={
        "Received": "#36A2EB",
        "Processed": "#4BC0C0",
        "Aligned with Appetite": "#3CB371",
        "Not Aligned": "#FF6384",
        "Backlog": "#FFB347"
    }
)
fig.update_layout(
    height=400,
    legend_title_text="",
    xaxis_title="",
    yaxis_title="Number of Submissions",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# Broker Analysis Section
st.markdown('<div class="sub-header">Broker Submission Analysis</div>', unsafe_allow_html=True)

# Sort brokers by alignment percentage
broker_df_sorted = broker_df.sort_values("aligned_pct", ascending=False)

# Create a horizontal bar chart for broker alignment
broker_fig = px.bar(
    broker_df_sorted,
    y="broker",
    x="aligned_pct",
    orientation="h",
    title="Broker Submission Alignment with Risk Appetite",
    text=broker_df_sorted["aligned_pct"].apply(lambda x: f"{x:.0%}"),
    color="aligned_pct",
    color_continuous_scale="Blues",
    hover_data=["submission_count", "data_quality"]
)
broker_fig.update_layout(
    height=400,
    xaxis_title="Alignment with Risk Appetite (%)",
    yaxis_title="",
    coloraxis_showscale=False
)
st.plotly_chart(broker_fig, use_container_width=True)

# Team Performance Section 
st.markdown('<div class="sub-header">Triage Analysis by LoB</div>', unsafe_allow_html=True)
efficiency_col1, efficiency_col2 = st.columns(2)

with efficiency_col1:
    # Create a funnel chart for the submission triage process
    latest_month = submissions_df.iloc[-1]
    
    funnel_labels = ["Received", "Initial Screening", "Processed", "Aligned with Appetite"]
    funnel_values = [
        latest_month["Received"], 
        int(latest_month["Received"] * 0.95),  # Assume 95% pass initial screening
        latest_month["Processed"],
        latest_month["Aligned with Appetite"]
    ]
    
    funnel_fig = go.Figure(go.Funnel(
        y=funnel_labels,
        x=funnel_values,
        textinfo="value+percent initial",
        marker=dict(color=["#36A2EB", "#FFB347", "#4BC0C0", "#3CB371"])
    ))
    
    funnel_fig.update_layout(
        title_text="Current Month Submission Funnel",
        height=400,
        margin=dict(t=50, b=0, l=30, r=30)
    )
    
    st.plotly_chart(funnel_fig, use_container_width=True)

 # Submission distribution
pie_fig = px.pie(
        lob_df,
        values="submission_count",
        names="lob",
        title="Submission Distribution by Line of Business",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
pie_fig.update_traces(textposition='inside', textinfo='percent+label')
pie_fig.update_layout(
        height=400,
        margin=dict(t=30, b=0, l=0, r=0),
        showlegend=False
    )
st.plotly_chart(pie_fig, use_container_width=True)

# Create horizontal bar chart for data quality
quality_fig = px.bar(
    lob_df.sort_values("data_quality"),
    y="lob",
    x="data_quality",
    orientation="h",
    title="Data Completeness Score by Line of Business (%)",
    text=lob_df["data_quality"].apply(lambda x: f"{x:.0f}%"),
    color="data_quality",
    color_continuous_scale=["#dc3545", "#ffc107", "#28a745"],
    range_color=[60, 100]
)
quality_fig.update_layout(
    height=400,
    xaxis_title="Data Completeness Score (%)",
    yaxis_title="",
    coloraxis_showscale=False
)
st.plotly_chart(quality_fig, use_container_width=True)

# Export options
st.markdown('<div class="sub-header">Export Report</div>', unsafe_allow_html=True)
export_col1, export_col2 = st.columns(2)

with export_col1:
    st.download_button(
        "Export Dashboard (PDF)",
        "Example PDF Report",
        file_name="executive_dashboard_report.pdf",
        mime="application/pdf"
    )

with export_col2:
    st.download_button(
        "Export Data (Excel)",
        "Example Excel Data Export",
        file_name="executive_dashboard_data.xlsx",
        mime="application/vnd.ms-excel"
    )

# Footer with last update time
st.markdown(f"""
<div style="text-align: right; color: #6c757d; font-size: 0.8rem; margin-top: 3rem;">
    Dashboard last updated: {datetime.now().strftime('%d %b %Y, %H:%M')}
</div>
""", unsafe_allow_html=True)