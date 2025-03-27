import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import random

st.title("Data Ingestion")

# Simple introduction
st.markdown("""
Upload submission documents or view your submission inbox.
Quickly process documents and check for duplicates before sending to triage.
""")

# Create tabs for different ingestion methods
tab1, tab2, tab3 = st.tabs(["New Submissions", "Upload Documents", "Submissions Backlog"])

# TAB 1: NEW SUBMISSIONS INBOX
with tab1:
    # Header section with action buttons and filter
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        st.subheader("New Submissions")
        st.markdown('<span style="color:#666;">6 unprocessed submissions</span>', unsafe_allow_html=True)
    
    with col2:
        fetch_button = st.button("Fetch New Submissions", use_container_width=True)
    
    with col3:
        process_all = st.button("Process Selected", type="primary", use_container_width=True)
    
    # Add LOB filter
    st.markdown("### Filters")
    lob_options = ["All Lines of Business", "Property D&F", "Professional Indemnity", "Cyber", "Marine Cargo", "Energy"]
    selected_lob = st.selectbox("Line of Business", lob_options)
    
    # Simulate fetching new submissions
    if fetch_button:
        with st.spinner("Checking for new submissions..."):
            time.sleep(1.5)
        st.success("3 new submissions found and added to inbox")
    
    # Create a dataframe of simulated submissions in the inbox
    def generate_inbox():
        now = datetime.now()
        submissions = [
            {
                "id": "SUB-2024-0123",
                "client": "ABC Property Holdings",
                "broker": "Marsh",
                "type": "Property D&F",
                "received": now - timedelta(hours=2),
                "status": "New",
                "source": "Email"
            },
            {
                "id": "SUB-2024-0122",
                "client": "TechPro Solutions",
                "broker": "Aon",
                "type": "Cyber",
                "received": now - timedelta(hours=5),
                "status": "New",
                "source": "Broker Portal"
            },
            {
                "id": "SUB-2024-0121",
                "client": "Global Architects Inc",
                "broker": "WTW",
                "type": "Professional Indemnity",
                "received": now - timedelta(hours=8),
                "status": "New",
                "source": "Email"
            },
            {
                "id": "SUB-2024-0120",
                "client": "Marine Shipping Co",
                "broker": "Miller",
                "type": "Marine Cargo",
                "received": now - timedelta(hours=12),
                "status": "New",
                "source": "Broker Portal"
            },
            {
                "id": "SUB-2024-0119",
                "client": "Luxury Hotel Group",
                "broker": "BMS",
                "type": "Property D&F",
                "received": now - timedelta(hours=18),
                "status": "New",
                "source": "Email"
            },
            {
                "id": "SUB-2024-0118",
                "client": "Energy Solutions Ltd",
                "broker": "Lockton",
                "type": "Energy",
                "received": now - timedelta(hours=24),
                "status": "New",
                "source": "API"
            }
        ]
        return pd.DataFrame(submissions)
    
    inbox_df = generate_inbox()
    
    # Apply LOB filter
    if selected_lob != "All Lines of Business":
        inbox_df = inbox_df[inbox_df["type"] == selected_lob]
    
    # Format the received time
    inbox_df['received_fmt'] = inbox_df['received'].apply(
        lambda x: f"{(datetime.now() - x).seconds // 3600}h ago" if (datetime.now() - x).seconds < 86400 
        else f"{(datetime.now() - x).days}d ago"
    )
    
    # Display inbox with checkboxes
    st.markdown("### Submission Inbox")
    
    # Add select all checkbox
    select_all = st.checkbox("Select All", key="select_all")
    
    # Show the inbox with checkboxes
    for i, row in enumerate(inbox_df.itertuples()):
        # Create checkbox for each row
        checkbox_val = select_all
        
        col1, col2, col3, col4 = st.columns([0.5, 3, 1.5, 1])
        
        with col1:
            st.checkbox("", value=checkbox_val, key=f"check_{i}")
        
        with col2:
            st.markdown(f"""
            <div>
                <strong>{row.client}</strong><br>
                <span style="color:#666;">{row.id} | {row.type}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div>
                <span style="color:#666;">{row.broker}</span><br>
                <span style="color:#666;">{row.received_fmt}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="text-align:right;">
                <span style="color:#666;">Source: {row.source}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a separator
        st.markdown('<hr style="margin:5px 0; opacity:0.3;">', unsafe_allow_html=True)
    
    # Process button clicked
    if process_all:
        with st.spinner("Processing submissions and checking for duplicates..."):
            time.sleep(2)
        
        # Show duplicate check results
        st.markdown("### Duplicate Check Results")
        
        # Simulate some duplicates for demo purposes
        duplicate_found = False
        for i, row in enumerate(inbox_df.itertuples()):
            if st.session_state.get(f"check_{i}", False) or select_all:
                # Randomly determine if we have a duplicate (for demo)
                is_duplicate = False
                if row.client == "TechPro Solutions" or (random.random() < 0.2 and not duplicate_found):
                    is_duplicate = True
                    duplicate_found = True  # Ensure we don't show too many duplicates
                
                # Show the appropriate status
                if is_duplicate:
                    # Show as duplicate
                    with st.expander(f"**{row.client}** ({row.id} | {row.type})", expanded=True):
                        st.markdown("""<div style="background-color:#f8d7da; color:#721c24; padding:10px; border-radius:5px; margin-bottom:10px;">
                        <strong>⚠️ Potential Duplicate Detected</strong>
                        </div>""", unsafe_allow_html=True)
                        
                        # Show the duplicate details
                        st.markdown("##### Duplicate Details")
                        
                        # Create a simple DataFrame for the duplicate info
                        dupe_data = {
                            "Existing Submission": [f"SUB-2024-0092"],
                            "Client Name": [row.client],
                            "Broker": ["Willis Towers Watson"],  # Different broker
                            "Received": ["10 days ago"],
                            "Status": ["In Triage"]
                        }
                        
                        dupe_df = pd.DataFrame(dupe_data)
                        st.dataframe(dupe_df, hide_index=True, use_container_width=True)
                        
                        # Duplicate resolution actions
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button(f"Mark as Unique", key=f"unique_{i}")
                        with col2:
                            st.button(f"Link to Existing", key=f"link_{i}", type="primary")
                else:
                    # Show as unique
                    with st.expander(f"**{row.client}** ({row.id} | {row.type})", expanded=True):
                        st.markdown("""<div style="background-color:#d4edda; color:#155724; padding:10px; border-radius:5px; margin-bottom:10px;">
                        <strong>✓ No Duplicates Found</strong>
                        </div>""", unsafe_allow_html=True)
                        
                        # Show completion message
                        st.markdown("##### Key Information Extracted")
                        
                        # Summary info based on submission type
                        if row.type == "Property D&F":
                            info = {
                                "Client": [row.client],
                                "Locations": ["3 locations in UK"],
                                "Total Value": ["£320,500,000"],
                                "Primary Occupancy": ["Office Buildings"]
                            }
                        elif row.type == "Cyber":
                            info = {
                                "Client": [row.client],
                                "Industry": ["Technology Services"],
                                "Revenue": ["$450M"],
                                "Coverages": ["Data Breach, Ransomware, Business Interruption"]
                            }
                        else:
                            info = {
                                "Client": [row.client],
                                "Coverage Type": [row.type],
                                "Estimated Premium": ["£175,000"],
                                "Renewal Date": ["01/05/2024"]
                            }
                        
                        info_df = pd.DataFrame(info)
                        st.dataframe(info_df, hide_index=True, use_container_width=True)
                        
                        # Add action button
                        st.button(f"Send to Triage", key=f"triage_{i}", type="primary")
        
        # Add bulk action button
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Process Unique Submissions", type="primary")
        with col2:
            st.button("Review All Duplicates")

# TAB 2: UPLOAD SUBMISSIONS
with tab2:
    st.subheader("Upload Submission Documents")
    
    # File uploader with a clear label
    uploaded_files = st.file_uploader(
        "Drag and drop files here",
        type=["pdf", "xlsx", "xls", "csv", "zip"],
        accept_multiple_files=True,
        help="Supports PDF, Excel, CSV, and ZIP formats"
    )
    
    # Only one sample document option
    st.markdown("### Or use a sample document")
    
    st.markdown("""
    <div style="border:1px solid #ddd; border-radius:5px; padding:15px; text-align:center; max-width:250px;">
        <p style="margin:0; font-weight:bold;">Property Schedule</p>
        <div style="font-size:36px; margin:10px 0;">📊</div>
        <p style="margin:0; color:#666;">Commercial Property Portfolio</p>
    </div>
    """, unsafe_allow_html=True)
    use_sample = st.checkbox("Use this sample document")
    
    # Process button - only show if files are uploaded or sample selected
    if uploaded_files or use_sample:
        files_to_process = len(uploaded_files) if uploaded_files else 0
        files_to_process += 1 if use_sample else 0
        
        st.markdown(f"**{files_to_process} file{'s' if files_to_process > 1 else ''} selected for processing**")
        process_button = st.button("Process Selected", type="primary")
        
        if process_button:
            with st.spinner(f"Processing and checking for duplicates..."):
                time.sleep(2)
            
            st.success("Processing complete!")
            
            # Show duplicate check result for the sample
            st.markdown("### Duplicate Check Results")
            
            # Sample is not a duplicate
            with st.expander("**Commercial Property Portfolio** (Property D&F)", expanded=True):
                st.markdown("""<div style="background-color:#d4edda; color:#155724; padding:10px; border-radius:5px; margin-bottom:10px;">
                <strong>✓ No Duplicates Found</strong>
                </div>""", unsafe_allow_html=True)
                
                # Show extracted information
                st.markdown("##### Key Information Extracted")
                
                sample_info = {
                    "Client": ["ABC Property Holdings Ltd"],
                    "Broker": ["Willis Towers Watson"],
                    "Locations": ["12 locations across UK"],
                    "Total Value": ["£550,628,219"],
                    "Renewal Date": ["01/06/2024"]
                }
                
                sample_df = pd.DataFrame(sample_info)
                st.dataframe(sample_df, hide_index=True, use_container_width=True)
                
                # Add action button
                st.button("Send to Triage", key="sample_triage", type="primary")
            
            # Add navigation buttons
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.button("Process More Documents")
            with col2:
                st.button("Go to Triage", type="primary")

# TAB 3: PENDING SUBMISSIONS
with tab3:
    st.subheader("Submissions Backlog")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox(
            "Status Filter",
            ["All in Backlog", "Awaiting Info", "Duplicate Check", "Needs Review"]
        )
    
    with col2:
        date_filter = st.selectbox(
            "Date Range",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All Time"]
        )
    
    # Generate some pending submissions
    def generate_pending():
        now = datetime.now()
        submissions = [
            {
                "id": "SUB-2024-0115",
                "client": "Regional Property Trust",
                "broker": "Aon",
                "type": "Property D&F",
                "received": now - timedelta(days=3),
                "status": "Duplicate Check",
                "notes": "Checking for potential duplicate"
            },
            {
                "id": "SUB-2024-0112",
                "client": "Global Tech Services",
                "broker": "Marsh",
                "type": "Cyber",
                "received": now - timedelta(days=5),
                "status": "Needs Review",
                "notes": "Awaiting additional info from broker"
            },
            {
                "id": "SUB-2024-0108",
                "client": "European Hospitality Group",
                "broker": "WTW",
                "type": "Property D&F",
                "received": now - timedelta(days=7),
                "status": "Awaiting Info",
                "notes": "Missing values for 3 locations"
            },
            {
                "id": "SUB-2024-0103",
                "client": "Maritime Logistics Co",
                "broker": "Miller",
                "type": "Marine Cargo",
                "received": now - timedelta(days=10),
                "status": "Duplicate Check",
                "notes": "Similar submission identified"
            },
        ]
        return pd.DataFrame(submissions)
    
    pending_df = generate_pending()
    
    # Apply filters
    if status_filter != "All Pending":
        pending_df = pending_df[pending_df["status"] == status_filter]
    
    if date_filter == "Last 7 days":
        pending_df = pending_df[pending_df["received"] >= datetime.now() - timedelta(days=7)]
    elif date_filter == "Last 30 days":
        pending_df = pending_df[pending_df["received"] >= datetime.now() - timedelta(days=30)]
    elif date_filter == "Last 90 days":
        pending_df = pending_df[pending_df["received"] >= datetime.now() - timedelta(days=90)]
    
    # Format the received time
    pending_df['received_fmt'] = pending_df['received'].apply(
        lambda x: f"{(datetime.now() - x).days}d ago"
    )
    
    # Display pending submissions
    st.markdown("### Pending Submissions List")
    
    # Add select all checkbox
    pending_select_all = st.checkbox("Select All", key="pending_select_all")
    
    # Show the pending submissions with checkboxes
    for i, row in enumerate(pending_df.itertuples()):
        # Create checkbox for each row
        checkbox_val = pending_select_all
        
        # Get appropriate status color and HTML
        if row.status == "Awaiting Info":
            status_html = f"""<span style="background-color:#ffc107; color:white; padding:2px 8px; border-radius:10px; font-size:12px;">{row.status}</span>"""
        elif row.status == "Needs Review":
            status_html = f"""<span style="background-color:#17a2b8; color:white; padding:2px 8px; border-radius:10px; font-size:12px;">{row.status}</span>"""
        elif row.status == "Duplicate Check":
            status_html = f"""<span style="background-color:#6610f2; color:white; padding:2px 8px; border-radius:10px; font-size:12px;">{row.status}</span>"""
        else:
            status_html = f"""<span style="background-color:#6c757d; color:white; padding:2px 8px; border-radius:10px; font-size:12px;">{row.status}</span>"""
        
        col1, col2, col3, col4 = st.columns([0.5, 3, 2, 1])
        
        with col1:
            st.checkbox("", value=checkbox_val, key=f"pending_check_{i}")
        
        with col2:
            st.markdown(f"""
            <div>
                <strong>{row.client}</strong><br>
                <span style="color:#666;">{row.id} | {row.type}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(status_html, unsafe_allow_html=True)
            st.caption(f"{row.notes}")
        
        with col4:
            st.markdown(f"""
            <div style="text-align:right;">
                <span style="color:#666;">{row.broker}</span><br>
                <span style="color:#666;">{row.received_fmt}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a separator
        st.markdown('<hr style="margin:5px 0; opacity:0.3;">', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        resume_button = st.button("Resume Processing Selected", type="primary", use_container_width=True)
    with col2:
        archive_button = st.button("Archive Selected", use_container_width=True)
    
    if resume_button:
        st.success("Selected submissions have been sent for processing")
    
    if archive_button:
        st.info("Selected submissions have been archived")