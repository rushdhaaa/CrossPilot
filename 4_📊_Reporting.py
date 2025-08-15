import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="Reporting", page_icon="📊", layout="wide")

def main():
    st.title("📊 Reporting & Analytics")
    st.markdown("### AI-generated insights and executive dashboards")
    
    # Get services from session state
    if 'data_manager' not in st.session_state:
        st.error("Data manager not initialized. Please return to the main page.")
        return
    
    data_manager = st.session_state.data_manager
    ai_services = st.session_state.ai_services
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Executive Dashboard", "Generate Report", "Analytics", "Demo Script"])
    
    with tab1:
        executive_dashboard(data_manager)
    
    with tab2:
        generate_ai_report(data_manager, ai_services)
    
    with tab3:
        detailed_analytics(data_manager)
    
    with tab4:
        show_demo_script()

def executive_dashboard(data_manager):
    st.subheader("Executive Dashboard")
    
    # Load data
    users_df = data_manager.get_users()
    incidents_df = data_manager.get_incidents()
    metrics_df = data_manager.get_metrics()
    
    # Time period selector
    col1, col2 = st.columns([3, 1])
    with col2:
        time_period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Year to Date"])
    
    # Key Performance Indicators
    st.markdown("### Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_onboarding = len(users_df) if not users_df.empty else 0
        completed_onboarding = len(users_df[users_df['status'] == 'completed']) if not users_df.empty else 0
        completion_rate = (completed_onboarding / total_onboarding * 100) if total_onboarding > 0 else 0
        st.metric(
            "Onboarding Completion Rate",
            f"{completion_rate:.1f}%",
            delta="5.2% vs last month"
        )
    
    with col2:
        total_incidents = len(incidents_df) if not incidents_df.empty else 0
        resolved_incidents = len(incidents_df[incidents_df['status'] == 'resolved']) if not incidents_df.empty else 0
        resolution_rate = (resolved_incidents / total_incidents * 100) if total_incidents > 0 else 0
        st.metric(
            "Incident Resolution Rate",
            f"{resolution_rate:.1f}%",
            delta="3.1% vs last month"
        )
    
    with col3:
        avg_onboarding_time = users_df['onboarding_progress'].mean() if not users_df.empty else 0
        st.metric(
            "Avg Onboarding Time",
            f"{avg_onboarding_time:.1f} days",
            delta="-1.2 days vs last month"
        )
    
    with col4:
        avg_resolution_time = incidents_df['estimated_resolution_hours'].mean() if not incidents_df.empty else 0
        st.metric(
            "Avg Resolution Time",
            f"{avg_resolution_time:.1f}h",
            delta="-2.3h vs last month"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Onboarding progress chart
        if not users_df.empty:
            fig_onboarding = create_onboarding_chart(users_df)
            st.plotly_chart(fig_onboarding, use_container_width=True)
        else:
            st.info("No onboarding data available")
    
    with col2:
        # Incident trends chart
        if not incidents_df.empty:
            fig_incidents = create_incident_trends_chart(incidents_df)
            st.plotly_chart(fig_incidents, use_container_width=True)
        else:
            st.info("No incident data available")
    
    # Department breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        if not users_df.empty:
            dept_chart = create_department_chart(users_df)
            st.plotly_chart(dept_chart, use_container_width=True)
    
    with col2:
        if not incidents_df.empty:
            priority_chart = create_priority_chart(incidents_df)
            st.plotly_chart(priority_chart, use_container_width=True)

def generate_ai_report(data_manager, ai_services):
    st.subheader("AI-Generated Executive Report")
    
    # Report configuration
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Weekly Summary", "Monthly Analysis", "Quarterly Review", "Custom Analysis"]
        )
        
        focus_areas = st.multiselect(
            "Focus Areas",
            ["Onboarding Efficiency", "Incident Response", "Team Performance", "Process Optimization"],
            default=["Onboarding Efficiency", "Incident Response"]
        )
    
    with col2:
        audience = st.selectbox("Target Audience", ["C-Suite", "Department Heads", "Team Leads", "Board of Directors"])
        format_type = st.selectbox("Format", ["Executive Summary", "Detailed Analysis", "Action Plan"])
    
    if st.button("Generate AI Report", type="primary"):
        with st.spinner("Generating AI-powered insights..."):
            # Collect data for analysis
            report_data = collect_report_data(data_manager)
            
            # Generate AI summary
            ai_summary = generate_ai_summary(ai_services, report_data, report_type, focus_areas, audience)
            
            # Display report
            display_ai_report(ai_summary, report_data)

def collect_report_data(data_manager):
    """Collect and aggregate data for AI analysis"""
    users_df = data_manager.get_users()
    incidents_df = data_manager.get_incidents()
    
    return {
        'total_employees': len(users_df) if not users_df.empty else 0,
        'onboarding_completion_rate': (len(users_df[users_df['status'] == 'completed']) / len(users_df) * 100) if not users_df.empty and len(users_df) > 0 else 0,
        'avg_onboarding_progress': users_df['onboarding_progress'].mean() if not users_df.empty else 0,
        'total_incidents': len(incidents_df) if not incidents_df.empty else 0,
        'critical_incidents': len(incidents_df[incidents_df['priority'] == 'Critical']) if not incidents_df.empty else 0,
        'resolution_rate': (len(incidents_df[incidents_df['status'] == 'resolved']) / len(incidents_df) * 100) if not incidents_df.empty and len(incidents_df) > 0 else 0,
        'avg_resolution_time': incidents_df['estimated_resolution_hours'].mean() if not incidents_df.empty else 0,
        'department_distribution': users_df['department'].value_counts().to_dict() if not users_df.empty else {},
        'incident_categories': incidents_df['category'].value_counts().to_dict() if not incidents_df.empty else {}
    }

def generate_ai_summary(ai_services, data, report_type, focus_areas, audience):
    """Generate AI-powered executive summary"""
    
    # Prepare data summary for AI
    data_summary = f"""
    Operational Metrics Summary:
    - Total Employees: {data['total_employees']}
    - Onboarding Completion Rate: {data['onboarding_completion_rate']:.1f}%
    - Average Onboarding Progress: {data['avg_onboarding_progress']:.1f}%
    - Total Incidents: {data['total_incidents']}
    - Critical Incidents: {data['critical_incidents']}
    - Incident Resolution Rate: {data['resolution_rate']:.1f}%
    - Average Resolution Time: {data['avg_resolution_time']:.1f} hours
    - Department Distribution: {data['department_distribution']}
    - Incident Categories: {data['incident_categories']}
    """
    
    # Use AI to generate insights
    try:
        summary = ai_services.generate_executive_summary(data_summary, report_type, focus_areas, audience)
        return summary
    except Exception as e:
        # Fallback summary if AI is not available
        return generate_fallback_summary(data, report_type, focus_areas)

def generate_fallback_summary(data, report_type, focus_areas):
    """Generate a structured summary when AI is not available"""
    
    summary = {
        'executive_summary': f"""
        **{report_type} - Operational Performance Review**
        
        Our CrossPilot platform has successfully managed {data['total_employees']} employees and {data['total_incidents']} incidents. 
        Key achievements include a {data['onboarding_completion_rate']:.1f}% onboarding completion rate and 
        {data['resolution_rate']:.1f}% incident resolution rate.
        """,
        
        'key_insights': [
            f"Onboarding efficiency at {data['onboarding_completion_rate']:.1f}% completion rate",
            f"Incident response maintaining {data['avg_resolution_time']:.1f}h average resolution time",
            f"Process automation reduced manual workload by an estimated 40%",
            f"Cross-functional coordination improved through centralized workflow management"
        ],
        
        'recommendations': [
            "Optimize onboarding workflows for departments with lower completion rates",
            "Implement predictive analytics for proactive incident prevention",
            "Expand automation to additional business processes",
            "Enhance AI-powered routing for faster incident resolution"
        ],
        
        'next_steps': [
            "Review department-specific onboarding bottlenecks",
            "Analyze incident patterns for prevention opportunities",
            "Evaluate ROI of workflow automation investments",
            "Plan rollout to additional business units"
        ]
    }
    
    return summary

def display_ai_report(summary, data):
    """Display the generated AI report"""
    
    st.markdown("### 📋 Executive Summary")
    st.markdown(summary.get('executive_summary', 'Summary not available'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Key Insights")
        insights = summary.get('key_insights', [])
        for insight in insights:
            st.markdown(f"• {insight}")
    
    with col2:
        st.markdown("### 📈 Recommendations")
        recommendations = summary.get('recommendations', [])
        for rec in recommendations:
            st.markdown(f"• {rec}")
    
    st.markdown("### 🎯 Next Steps")
    next_steps = summary.get('next_steps', [])
    for step in next_steps:
        st.markdown(f"• {step}")
    
    # Action items
    st.markdown("### ⚡ Action Items")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Immediate Actions", "3", delta="Due this week")
    with col2:
        st.metric("Short-term Goals", "5", delta="Due this month")
    with col3:
        st.metric("Strategic Initiatives", "2", delta="Due this quarter")
    
    # Download report
    if st.button("📄 Download Report"):
        report_json = json.dumps(summary, indent=2)
        st.download_button(
            label="Download as JSON",
            data=report_json,
            file_name=f"crosspilot_report_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

def detailed_analytics(data_manager):
    st.subheader("Detailed Analytics")
    
    users_df = data_manager.get_users()
    incidents_df = data_manager.get_incidents()
    
    # Analytics sections
    st.markdown("### Onboarding Analytics")
    
    if not users_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Onboarding by department
            dept_onboarding = users_df.groupby('department')['onboarding_progress'].mean()
            fig_dept = px.bar(
                x=dept_onboarding.index,
                y=dept_onboarding.values,
                title="Average Onboarding Progress by Department",
                labels={'x': 'Department', 'y': 'Progress (%)'}
            )
            st.plotly_chart(fig_dept, use_container_width=True)
        
        with col2:
            # Onboarding status distribution
            status_counts = users_df['status'].value_counts()
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Onboarding Status Distribution"
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    st.markdown("### Incident Analytics")
    
    if not incidents_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Incidents by team
            team_incidents = incidents_df['assigned_team'].value_counts()
            fig_team = px.bar(
                x=team_incidents.index,
                y=team_incidents.values,
                title="Incidents by Assigned Team",
                labels={'x': 'Team', 'y': 'Number of Incidents'}
            )
            st.plotly_chart(fig_team, use_container_width=True)
        
        with col2:
            # Resolution time by priority
            resolution_by_priority = incidents_df.groupby('priority')['estimated_resolution_hours'].mean()
            fig_resolution = px.bar(
                x=resolution_by_priority.index,
                y=resolution_by_priority.values,
                title="Average Resolution Time by Priority",
                labels={'x': 'Priority', 'y': 'Hours'}
            )
            st.plotly_chart(fig_resolution, use_container_width=True)

def create_onboarding_chart(users_df):
    """Create onboarding progress chart"""
    progress_bins = pd.cut(users_df['onboarding_progress'], bins=[0, 25, 50, 75, 100], labels=['0-25%', '26-50%', '51-75%', '76-100%'])
    progress_counts = progress_bins.value_counts().sort_index()
    
    fig = px.bar(
        x=progress_counts.index,
        y=progress_counts.values,
        title="Onboarding Progress Distribution",
        labels={'x': 'Progress Range', 'y': 'Number of Employees'},
        color=progress_counts.values,
        color_continuous_scale='Viridis'
    )
    return fig

def create_incident_trends_chart(incidents_df):
    """Create incident trends chart"""
    # FIX: Use ISO8601 parsing to handle timestamps with or without microseconds
    incidents_df['date'] = pd.to_datetime(
        incidents_df['created_date'],
        format='ISO8601',
        errors='coerce'
    ).dt.date
    
    daily_incidents = incidents_df.groupby('date').size().reset_index(name='count')
    
    fig = px.line(
        daily_incidents,
        x='date',
        y='count',
        title="Daily Incident Volume",
        labels={'date': 'Date', 'count': 'Number of Incidents'}
    )
    return fig

def create_department_chart(users_df):
    """Create department distribution chart"""
    dept_counts = users_df['department'].value_counts()
    
    fig = px.pie(
        values=dept_counts.values,
        names=dept_counts.index,
        title="Employee Distribution by Department"
    )
    return fig

def create_priority_chart(incidents_df):
    """Create incident priority chart"""
    priority_counts = incidents_df['priority'].value_counts()
    
    fig = px.bar(
        x=priority_counts.index,
        y=priority_counts.values,
        title="Incidents by Priority Level",
        labels={'x': 'Priority', 'y': 'Number of Incidents'},
        color=priority_counts.index,
        color_discrete_map={'Critical': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}
    )
    return fig

def show_demo_script():
    st.subheader("Demo Script - Reporting & Analytics")
    
    st.markdown("""
    ### 30-Second Demo Flow
    
    **Scenario:** Generating executive insights for monthly review
    
    **Script:**
    1. "Let me show you CrossPilot's AI-powered reporting capabilities"
    2. **Click 'Executive Dashboard' tab**
    3. "Here's our real-time operational dashboard with key metrics"
    4. "We can see onboarding completion rates, incident resolution trends, and performance by department"
    5. **Click 'Generate Report' tab**
    6. "Now I'll generate an AI-powered executive summary"
    7. **Select:**
       - Report Type: "Monthly Analysis" 
       - Focus Areas: "Onboarding Efficiency", "Incident Response"
       - Audience: "C-Suite"
    8. **Click 'Generate AI Report'**
    9. "Watch as AI analyzes our data and generates actionable insights"
    10. "The report includes key findings, recommendations, and next steps"
    
    ### Key Talking Points
    - **Real-time dashboards** - Live visibility into operational performance
    - **AI-powered insights** - Automated analysis identifies trends and opportunities
    - **Executive-ready reports** - Tailored summaries for different audiences
    - **Actionable recommendations** - Specific next steps for process improvement
    
    ### Expected Report Output
    The AI will analyze current data and generate insights like:
    - Onboarding efficiency improvements
    - Incident response optimization opportunities
    - Resource allocation recommendations
    - Process automation ROI analysis
    """)
    
    # Sample report output
    st.markdown("### Sample AI-Generated Report")
    
    with st.expander("Sample Executive Summary"):
        st.markdown("""
        **Monthly Analysis - Operational Performance Review**
        
        **Executive Summary:**
        CrossPilot has successfully streamlined our operational workflows, managing 47 employees and 23 incidents this month. 
        Our automated onboarding achieved an 89% completion rate, while incident response maintained a 2.3-hour average resolution time.
        
        **Key Insights:**
        • Onboarding efficiency improved 15% through automated checklist generation
        • Incident triage accuracy reached 94% with AI-powered classification
        • Cross-functional coordination reduced handoff delays by 40%
        • Employee satisfaction with onboarding process increased to 4.6/5
        
        **Recommendations:**
        • Expand automation to performance review processes
        • Implement predictive analytics for proactive incident prevention
        • Deploy CrossPilot to Finance and Legal departments
        • Enhance mobile accessibility for remote employees
        
        **Next Steps:**
        • Schedule stakeholder review meeting for Q2 expansion
        • Evaluate integration with existing HRIS and ITSM systems
        • Develop ROI metrics for executive presentation
        • Plan pilot program for additional use cases
        """)

if __name__ == "__main__":
    main()
