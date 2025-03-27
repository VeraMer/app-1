import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="hx Renew - Submission Triage App",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .card {
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Main home page content
st.title("hx Renew - Submission Triage App")

st.markdown("""
<div class="card">
    <h3>Welcome to your Submissions Triage App</h3>
    <p>This app will help you manage submissions, 
    assess risks, and make better decisions with AI assistance.</p>
</div>
""", unsafe_allow_html=True)

# Overview of available pages
st.subheader("Available Modules")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Data Ingestion**
    - Upload submission documents
    - AI-powered data extraction
    - Structured data preview
    """)
    
    st.markdown("""
    **Submissions Triage**
    - Prioritized submission queue
    - Risk appetite matching
    - Quick action workflow
    """)

with col2:
    st.markdown("""
    **Risk Assessment**
    - Exposure visualization
    - Historical comparison
    - Sanctions checking
    """)
    
    st.markdown("""
    **Executive Dashboard**
    - Portfolio metrics
    - Performance tracking
    - Business intelligence
    """)