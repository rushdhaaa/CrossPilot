import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from utils.data_manager import DataManager
from utils.ai_services import AIServices

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

@st.cache_resource
def init_ai_services():
    return AIServices()

def main():
    st.set_page_config(
        page_title="CrossPilot - AI Workflow Copilot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize services
    data_manager = init_data_manager()
    ai_services = init_ai_services()
    
    # Store in session state for access across pages
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = data_manager
    if 'ai_services' not in st.session_state:
        st.session_state.ai_services = ai_services
    
    # Main page content
    st.title("🤖 CrossPilot - AI-Augmented Workflow Copilot")
    st.markdown("### Enterprise Onboarding, Incident Triage & Reporting Platform")
    
    # Overview cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Workflows",
            value=len(data_manager.get_workflows()),
            delta="3 this week"
        )
    
    with col2:
        users_df = data_manager.get_users()
        pending_onboarding = len(users_df[users_df['status'] == 'pending'])
        st.metric(
            label="Pending Onboarding",
            value=pending_onboarding,
            delta=f"-2 from yesterday"
        )
    
    with col3:
        incidents_df = data_manager.get_incidents()
        open_incidents = len(incidents_df[incidents_df['status'] == 'open'])
        st.metric(
            label="Open Incidents",
            value=open_incidents,
            delta="5 new today"
        )
    
    with col4:
        avg_resolution = incidents_df['resolution_hours'].mean() if not incidents_df.empty else 0
        st.metric(
            label="Avg Resolution (hrs)",
            value=f"{avg_resolution:.1f}",
            delta="-2.3 hrs"
        )
    
    # Quick Actions
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔧 Create New Workflow", use_container_width=True):
            st.switch_page("pages/1_🔧_Workflow_Builder.py")
    
    with col2:
        if st.button("👋 Start Onboarding", use_container_width=True):
            st.switch_page("pages/2_👋_Onboarding.py")
    
    with col3:
        if st.button("🚨 Submit Incident", use_container_width=True):
            st.switch_page("pages/3_🚨_Incident_Triage.py")
    
    # Recent Activity
    st.markdown("### Recent Activity")
    
    # Get recent incidents
    recent_incidents = incidents_df.head(5) if not incidents_df.empty else pd.DataFrame()
    
    if not recent_incidents.empty:
        st.dataframe(
            recent_incidents[['id', 'title', 'priority', 'status', 'created_date', 'assigned_team']],
            use_container_width=True
        )
    else:
        st.info("No recent incidents to display.")
    
    # Navigation Guide
    with st.sidebar:
        st.markdown("## Navigation Guide")
        st.markdown("""
        **🔧 Workflow Builder**
        Create and manage automated workflows
        
        **👋 Onboarding**
        Manage employee onboarding processes
        
        **🚨 Incident Triage**
        AI-powered incident classification and routing
        
        **📊 Reporting**
        Generate insights and executive summaries
        """)
        
        st.markdown("---")
        st.markdown("### Demo Scripts Available")
        st.info("Each module includes guided demo flows for hackathon presentation")

if __name__ == "__main__":
    main()
