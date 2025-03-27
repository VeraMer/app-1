import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
from datetime import datetime, timedelta
import random

# Add custom CSS for the decline button at the top of the app
st.markdown("""
<style>
.red-button {
    background-color: #dc3545 !important;
    color: white !important; 
    border-color: #dc3545 !important;
}
</style>
""", unsafe_allow_html=True)

# Simple introduction
st.markdown("""
Review submissions, see AI recommendations, and make decisions on which to accept, decline, or move to backlog.
""")

# Create filter section - keep it simple with just the most important filters
st.markdown("### Filters")
col1, col2, col3 = st.columns(3)

with col1:
    lob_filter = st.selectbox(
        "Line of Business",
        ["All Lines of Business", "Property D&F", "Professional Indemnity", "Cyber", "Marine Cargo", "Energy"]
    )

with col2:
    broker_filter = st.multiselect(
        "Broker",
        ["Marsh", "Aon", "WTW", "Howden", "BMS", "Miller", "Gallagher"],
        default=[]
    )

with col3:
    recommendation_filter = st.multiselect(
        "AI Recommendation",
        ["Accept", "Decline", "Needs Review"],
        default=["Accept", "Needs Review", "Decline"]
    )

# Generate sample submissions data
def generate_submissions(n=10):
    now = datetime.now()
    lobs = ["Property D&F", "Professional Indemnity", "Cyber", "Marine Cargo", "Energy"]
    brokers = ["Marsh", "Aon", "WTW", "Howden", "BMS", "Miller", "Gallagher"]
    clients = [
        "ABC Property Holdings", "TechPro Solutions", "Global Architects Inc", 
        "Marine Shipping Co", "Luxury Hotel Group", "Energy Solutions Ltd",
        "European Manufacturing", "UK Retail Chain", "Global Financial Services"
    ]
    
    submissions = []
    
    # Ensure we have at least one of each recommendation type
    recommendations = ["Accept", "Needs Review", "Decline"]
    
    for i in range(n):
        # Base data
        client = random.choice(clients)
        lob = random.choice(lobs)
        broker = random.choice(brokers)
        received_days = random.randint(0, 14)
        
        # Deadline info
        deadline_days = random.randint(5, 21)
        days_remaining = max(1, deadline_days - received_days)
        
        # Risk metrics
        risk_appetite = random.randint(50, 95)
        estimated_premium = random.randint(50, 500) * 1000
        
        # AI recommendation
        # For the first 3 records, force one of each recommendation type
        if i < 3:
            ai_recommendation = recommendations[i]
            confidence = random.randint(70, 95)
        else:
            if risk_appetite >= 75:
                ai_recommendation = "Accept"
                confidence = random.randint(80, 95)
            elif risk_appetite <= 60:
                ai_recommendation = "Decline"
                confidence = random.randint(75, 90)
            else:
                ai_recommendation = "Needs Review"
                confidence = random.randint(60, 75)
        
        # Template match (simplified)
        template_match = random.random() > 0.3  # 70% chance of template match
        
        submissions.append({
            "id": f"SUB-2024-{1000 + i}",
            "client": client,
            "broker": broker,
            "lob": lob,
            "days_remaining": days_remaining,
            "risk_appetite": risk_appetite,
            "estimated_premium": estimated_premium,
            "ai_recommendation": ai_recommendation,
            "confidence": confidence,
            "template_match": template_match
        })
    
    return pd.DataFrame(submissions)

# Generate data
submissions_df = generate_submissions(9)

# Apply filters
if lob_filter != "All Lines of Business":
    submissions_df = submissions_df[submissions_df["lob"] == lob_filter]

if broker_filter:
    submissions_df = submissions_df[submissions_df["broker"].isin(broker_filter)]

if recommendation_filter:
    submissions_df = submissions_df[submissions_df["ai_recommendation"].isin(recommendation_filter)]

# Define a mapping for recommendation priority (for sorting)
recommendation_priority = {
    "Accept": 1,
    "Needs Review": 2,
    "Decline": 3
}

# Add a priority column for sorting by recommendation
submissions_df["recommendation_priority"] = submissions_df["ai_recommendation"].map(recommendation_priority)

# Apply fixed sort: recommended action first, then premium
submissions_df = submissions_df.sort_values(["recommendation_priority", "estimated_premium"], ascending=[True, False])

# Prepare data for pie chart
recommendation_counts = submissions_df["ai_recommendation"].value_counts().reset_index()
recommendation_counts.columns = ["Recommendation", "Count"]

# Add premium by broker
premium_by_broker = submissions_df.groupby("broker")["estimated_premium"].sum().reset_index()
premium_by_broker.columns = ["Broker", "Premium"]
premium_by_broker = premium_by_broker.sort_values("Premium", ascending=True)

# Total premium
total_premium = submissions_df["estimated_premium"].sum()

# Display submissions overview with pie chart
st.markdown("### Submissions Overview")
col1, col2 = st.columns([2, 3])

with col1:
    # Create the pie chart - no legend, consistent title
    fig = px.pie(
        recommendation_counts, 
        values="Count", 
        names="Recommendation",
        color="Recommendation",
        color_discrete_map={
            "Accept": "#28a745",
            "Decline": "#dc3545",
            "Needs Review": "#ffc107"
        }
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        margin=dict(t=30, b=0, l=0, r=0), 
        height=250,
        showlegend=False,
        title={
            'text': f"Total Submissions: {len(submissions_df)}",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Premium by broker - no legend, consistent title
    broker_fig = px.bar(
        premium_by_broker,
        x="Premium",
        y="Broker",
        orientation="h",
        color="Broker",
        text=premium_by_broker["Premium"].apply(lambda x: f"£{x:,.0f}")
    )
    broker_fig.update_layout(
        margin=dict(t=30, b=0, l=0, r=0), 
        height=250,
        showlegend=False,
        title={
            'text': f"Total Est. Premium: £{total_premium:,.0f}",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    broker_fig.update_yaxes(title="")
    broker_fig.update_xaxes(title="")
    st.plotly_chart(broker_fig, use_container_width=True)

# Submissions queue with select all below the header
st.markdown("### Submissions Queue")
st.markdown("🔄 **Sorted by:** Recommended Action, then Premium (highest to lowest)")
select_all = st.checkbox("Select All")

selection = []

# Display each submission
for i, row in enumerate(submissions_df.iterrows()):
    index, data = row
    
    # Set checkbox value based on select all
    checkbox_value = select_all
    
    # Create columns for each row - one small for checkbox, one large for data
    col1, col2 = st.columns([0.5, 11.5])
    
    with col1:
        selected = st.checkbox("", value=checkbox_value, key=f"select_{i}")
        if selected:
            selection.append(data["id"])
    
    with col2:
        # Apply conditional formatting to AI recommendation with LARGER buttons
        if data["ai_recommendation"] == "Accept":
            recommendation_html = '<span style="background-color:#28a745; color:white; padding:4px 12px; border-radius:10px; font-size:14px; font-weight:bold;">Accept</span>'
        elif data["ai_recommendation"] == "Decline":
            recommendation_html = '<span style="background-color:#dc3545; color:white; padding:4px 12px; border-radius:10px; font-size:14px; font-weight:bold;">Decline</span>'
        else:
            recommendation_html = '<span style="background-color:#ffc107; color:white; padding:4px 12px; border-radius:10px; font-size:14px; font-weight:bold;">Needs Review</span>'
        
        # Template match indicator (simple)
        template_html = '<span style="color:#28a745;">✓ Template Match</span>' if data["template_match"] else '<span style="color:#6c757d;">No Template</span>'
        
        # Create a simple row display with LARGER confidence display
        st.markdown(f"""
        <div style="padding:15px; background-color:#f8f9fa; border-radius:4px; margin-bottom:15px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <div>
                    <strong style="font-size:16px;">{data["client"]}</strong> - {data["id"]}
                </div>
                <div>
                    {recommendation_html} <span style="margin-left:8px; font-size:14px; font-weight:bold;">({data["confidence"]}% confidence)</span>
                </div>
            </div>
            <div style="display:flex; gap:30px; flex-wrap:wrap; margin-top:5px;">
                <div><span style="color:#666;">LOB:</span> {data["lob"]}</div>
                <div><span style="color:#666;">Broker:</span> {data["broker"]}</div>
                <div><span style="color:#666;">Est. Premium:</span> £{data["estimated_premium"]:,.0f}</div>
                <div><span style="color:#666;">Days Left:</span> {data["days_remaining"]}</div>
                <div>{template_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add view button functionality
        view_button = st.button(f"View Details {i+1}", key=f"view_{i}")
        
        if view_button:
            st.session_state[f"view_submission_{i}"] = True
        
        # Show detailed view if button was clicked
        if st.session_state.get(f"view_submission_{i}", False):
            with st.expander("Submission Details", expanded=True):
                # Tabs for different aspects of the submission
                detail_tab1, detail_tab2, detail_tab3 = st.tabs(["Overview", "Field Mapping", "Risk Analysis"])
                
                with detail_tab1:
                    # Two columns layout
                    dcol1, dcol2 = st.columns(2)
                    
                    with dcol1:
                        st.markdown("##### Client Information")
                        st.markdown(f"""
                        **Client:** {data["client"]}  
                        **Line of Business:** {data["lob"]}  
                        **Broker:** {data["broker"]}  
                        **Submission ID:** {data["id"]}  
                        **Days Remaining:** {data["days_remaining"]}  
                        """)
                    
                    with dcol2:
                        st.markdown("##### AI Assessment")
                        st.markdown(f"""
                        **AI Recommendation:** {data["ai_recommendation"]}  
                        **Confidence:** {data["confidence"]}%  
                        **Risk Appetite Match:** {data["risk_appetite"]}%  
                        **Estimated Premium:** £{data["estimated_premium"]:,.0f}  
                        **Template Match:** {"Yes" if data["template_match"] else "No"}
                        """)
                    
                    # Add view source file button
                    st.markdown("##### Source Document")
                    st.button("View Source File", key=f"source_{i}")
                    
                    # Submission notes
                    st.markdown("##### Notes")
                    notes = st.text_area("", placeholder="Add notes about this submission...", key=f"notes_{i}")
                
                with detail_tab2:
                    # Just field mapping, no source preview
                    st.markdown("##### Field Mapping")
                    
                    # Simplified mapping display
                    if data["template_match"]:
                        st.success("Mapped using existing template")
                        template_name = f"{data['broker']} {data['lob']} Template"
                        st.info(f"Template: **{template_name}**")
                    else:
                        st.warning("No template match - review mappings")
                    
                    # Simple mapping table - focus on just a few critical fields
                    mapping_data = {
                        "Source Field → Target Field": [
                            "Client Name → Insured",
                            "Property Value → TIV" if data["lob"] == "Property D&F" else "Limit → Policy Limit",
                            "Location → Address" if data["lob"] == "Property D&F" else "Profession → Industry",
                            "Construction → Building Type" if data["lob"] == "Property D&F" else "Expiry → Policy End Date",
                            "Occupancy → Building Use" if data["lob"] == "Property D&F" else "Currency → Payment Currency"
                        ],
                        "Confidence": [
                            "High ✓",
                            "Medium !" if not data["template_match"] else "High ✓",
                            "High ✓",
                            "Medium !" if not data["template_match"] else "High ✓",
                            "High ✓"
                        ]
                    }
                    
                    mapping_df = pd.DataFrame(mapping_data)
                    st.dataframe(mapping_df, hide_index=True, use_container_width=True)
                    
                    # Simple template management
                    if not data["template_match"]:
                        st.button(f"Save as New Template", key=f"save_template_{i}")
                
                with detail_tab3:
                    # Simple risk analysis
                    st.markdown("##### Key Risk Indicators")
                    
                    # Just the most important risk indicators
                    risk_data = {
                        "Indicator": ["Sanctions Check", "Within Authority", "Exposure Limit"],
                        "Status": [
                            "Clear ✓",
                            "Yes ✓" if data["risk_appetite"] > 70 else "Referral Required !",
                            "Within Limits ✓" if random.random() > 0.2 else "Near Threshold !"
                        ]
                    }
                    
                    # Create DataFrame
                    risk_df = pd.DataFrame(risk_data)
                    st.dataframe(risk_df, hide_index=True, use_container_width=True)
                
                # Decision buttons - use simple colored buttons
                st.markdown("---")
                st.markdown("##### Decision")
                
                decision_col1, decision_col2, decision_col3 = st.columns(3)
                
                # Simple colored buttons
                with decision_col1:
                    st.button("Accept", key=f"accept_{i}", type="primary")
                
                with decision_col2:
                    st.button("Move to Backlog", key=f"backlog_{i}")
                
                with decision_col3:
                    st.button("Decline", key=f"decline_{i}", help="Decline this submission")

# If any submissions are selected, show batch actions
if selection:
    st.markdown("---")
    st.markdown(f"### Batch Actions ({len(selection)} selected)")
    
    # Use 3 even columns for buttons
    batch_col1, batch_col2, batch_col3 = st.columns(3)
    
    # Accept button (green using Streamlit primary)
    with batch_col1:
        st.button("Accept Selected", type="primary", key="batch_accept")
    
    # Decline button (using a different key)
    with batch_col2:
        st.button("Decline Selected", key="batch_decline")
    
    # Move to backlog (using a different key)
    with batch_col3:
        st.button("Move Selected to Backlog", key="batch_backlog")
else:
    # Show disabled batch actions
    st.markdown("---")
    st.markdown("### Batch Actions (0 selected)")
    st.info("Select submissions to enable batch actions")