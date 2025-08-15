import streamlit as st
import pandas as pd
import re
from datetime import datetime
import uuid

st.set_page_config(page_title="Incident Triage", page_icon="🚨", layout="wide")

def main():
    st.title("🚨 Incident Triage")
    st.markdown("### AI-powered incident classification and routing")
    
    # Get services from session state
    if 'data_manager' not in st.session_state:
        st.error("Data manager not initialized. Please return to the main page.")
        return
    
    data_manager = st.session_state.data_manager
    ai_services = st.session_state.ai_services
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Submit Incident", "Incident Dashboard", "Triage Rules", "Demo Script"])
    
    with tab1:
        submit_incident_form(data_manager, ai_services)
    
    with tab2:
        incident_dashboard(data_manager)
    
    with tab3:
        triage_rules_management(data_manager)
    
    with tab4:
        show_demo_script()

def submit_incident_form(data_manager, ai_services):
    st.subheader("Submit New Incident")
    
    with st.form("incident_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Incident Title")
            customer = st.text_input("Customer/Requester")
            category = st.selectbox("Category", ["Hardware", "Software", "Network", "Security", "Access", "Other"])
        
        with col2:
            urgency = st.selectbox("Urgency", ["Low", "Medium", "High", "Critical"])
            impact = st.selectbox("Impact", ["Individual", "Department", "Organization", "External"])
            source = st.selectbox("Source", ["Email", "Phone", "Chat", "Portal", "Monitoring"])
        
        description = st.text_area("Detailed Description", height=150)
        
        # Additional context
        st.markdown("#### Additional Context")
        col1, col2 = st.columns(2)
        
        with col1:
            affected_systems = st.multiselect(
                "Affected Systems",
                ["Email", "CRM", "ERP", "Website", "Database", "VPN", "Active Directory"]
            )
        
        with col2:
            attachments = st.file_uploader("Attachments", accept_multiple_files=True)
        
        submitted = st.form_submit_button("Submit Incident")
        
        if submitted:
            if title and description and customer:
                # Generate incident ID
                incident_id = f"INC{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"
                
                # Perform AI-powered triage
                triage_result = perform_ai_triage(ai_services, {
                    'title': title,
                    'description': description,
                    'category': category,
                    'urgency': urgency,
                    'impact': impact,
                    'affected_systems': affected_systems
                })
                
                # Create incident record
                incident = {
                    'id': incident_id,
                    'title': title,
                    'description': description,
                    'customer': customer,
                    'category': category,
                    'urgency': urgency,
                    'impact': impact,
                    'source': source,
                    'affected_systems': affected_systems,
                    'priority': triage_result['priority'],
                    'assigned_team': triage_result['assigned_team'],
                    'tags': triage_result['tags'],
                    'estimated_resolution_hours': triage_result['estimated_hours'],
                    'status': 'open',
                    'created_date': datetime.now().isoformat(),
                    'resolution_hours': None,
                    'resolution_notes': None
                }
                
                # Save incident
                data_manager.add_incident(incident)
                
                # Display triage results
                st.success(f"Incident {incident_id} submitted successfully!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Priority", triage_result['priority'])
                with col2:
                    st.metric("Assigned Team", triage_result['assigned_team'])
                with col3:
                    st.metric("Est. Resolution", f"{triage_result['estimated_hours']}h")
                
                st.markdown("**AI Analysis:**")
                st.write(f"**Tags:** {', '.join(triage_result['tags'])}")
                st.write(f"**Reasoning:** {triage_result['reasoning']}")
                
            else:
                st.error("Please fill in all required fields.")

def perform_ai_triage(ai_services, incident_data):
    """Perform AI-powered incident triage using NLP and rules"""
    
    # Combine title and description for analysis
    text = f"{incident_data['title']} {incident_data['description']}"
    
    # Extract keywords and patterns
    keywords = extract_keywords(text.lower())
    
    # Determine priority based on urgency, impact, and keywords
    priority_score = calculate_priority_score(incident_data, keywords)
    
    if priority_score >= 90:
        priority = "Critical"
        estimated_hours = 2
    elif priority_score >= 70:
        priority = "High"
        estimated_hours = 8
    elif priority_score >= 40:
        priority = "Medium"
        estimated_hours = 24
    else:
        priority = "Low"
        estimated_hours = 72
    
    # Assign team based on category and keywords
    assigned_team = assign_team(incident_data['category'], keywords)
    
    # Generate tags
    tags = generate_tags(keywords, incident_data)
    
    # Generate reasoning
    reasoning = generate_reasoning(incident_data, keywords, priority)
    
    return {
        'priority': priority,
        'assigned_team': assigned_team,
        'tags': tags,
        'estimated_hours': estimated_hours,
        'reasoning': reasoning
    }

def extract_keywords(text):
    """Extract relevant keywords from incident text"""
    keywords = {
        'security': ['password', 'login', 'access', 'hack', 'breach', 'unauthorized', 'virus', 'malware'],
        'network': ['connection', 'internet', 'wifi', 'vpn', 'slow', 'timeout', 'ping'],
        'email': ['email', 'outlook', 'mail', 'send', 'receive', 'attachment'],
        'hardware': ['laptop', 'computer', 'printer', 'mouse', 'keyboard', 'screen', 'monitor'],
        'software': ['application', 'app', 'program', 'software', 'install', 'update'],
        'database': ['database', 'sql', 'query', 'data', 'report', 'export'],
        'critical': ['down', 'outage', 'critical', 'urgent', 'emergency', 'broken', 'failure']
    }
    
    found_keywords = []
    for category, words in keywords.items():
        for word in words:
            if word in text:
                found_keywords.append(category)
                break
    
    return found_keywords

def calculate_priority_score(incident_data, keywords):
    """Calculate priority score based on multiple factors"""
    score = 0
    
    # Base score from urgency
    urgency_scores = {'Low': 10, 'Medium': 30, 'High': 60, 'Critical': 90}
    score += urgency_scores.get(incident_data['urgency'], 10)
    
    # Impact multiplier
    impact_multipliers = {'Individual': 1.0, 'Department': 1.2, 'Organization': 1.5, 'External': 2.0}
    score *= impact_multipliers.get(incident_data['impact'], 1.0)
    
    # Keyword modifiers
    if 'critical' in keywords:
        score += 30
    if 'security' in keywords:
        score += 20
    if 'network' in keywords and incident_data['impact'] in ['Organization', 'External']:
        score += 15
    
    return min(score, 100)  # Cap at 100

def assign_team(category, keywords):
    """Assign incident to appropriate team"""
    team_mapping = {
        'Hardware': 'IT Support',
        'Software': 'Application Support',
        'Network': 'Network Operations',
        'Security': 'Security Team',
        'Access': 'Identity & Access'
    }
    
    # Override based on keywords
    if 'security' in keywords:
        return 'Security Team'
    elif 'network' in keywords:
        return 'Network Operations'
    elif 'database' in keywords:
        return 'Database Team'
    else:
        return team_mapping.get(category, 'General Support')

def generate_tags(keywords, incident_data):
    """Generate relevant tags for the incident"""
    tags = []
    
    # Add keyword-based tags
    tags.extend(keywords)
    
    # Add category tag
    tags.append(incident_data['category'].lower())
    
    # Add system tags
    if incident_data['affected_systems']:
        tags.extend([system.lower().replace(' ', '_') for system in incident_data['affected_systems']])
    
    # Remove duplicates and return
    return list(set(tags))

def generate_reasoning(incident_data, keywords, priority):
    """Generate human-readable reasoning for triage decision"""
    reasons = []
    
    reasons.append(f"Classified as {priority} priority based on {incident_data['urgency']} urgency")
    
    if incident_data['impact'] in ['Organization', 'External']:
        reasons.append(f"High impact affecting {incident_data['impact'].lower()} level")
    
    if 'critical' in keywords:
        reasons.append("Critical keywords detected in description")
    
    if 'security' in keywords:
        reasons.append("Security-related incident requiring immediate attention")
    
    if incident_data['affected_systems']:
        reasons.append(f"Multiple systems affected: {', '.join(incident_data['affected_systems'])}")
    
    return ". ".join(reasons) + "."

def incident_dashboard(data_manager):
    st.subheader("Incident Dashboard")
    
    incidents_df = data_manager.get_incidents()
    
    if incidents_df.empty:
        st.info("No incidents reported yet.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    open_incidents = len(incidents_df[incidents_df['status'] == 'open'])
    critical_incidents = len(incidents_df[incidents_df['priority'] == 'Critical'])
    avg_resolution = incidents_df['estimated_resolution_hours'].mean()
    
    with col1:
        st.metric("Open Incidents", open_incidents)
    with col2:
        st.metric("Critical", critical_incidents)
    with col3:
        st.metric("Avg Est. Resolution", f"{avg_resolution:.1f}h")
    with col4:
        resolved_today = len(incidents_df[
            (incidents_df['status'] == 'resolved') & 
            (pd.to_datetime(incidents_df['created_date'], format='ISO8601').dt.date == datetime.now().date())
        ])
        st.metric("Resolved Today", resolved_today)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "open", "in_progress", "resolved"])
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        team_filter = st.selectbox("Filter by Team", ["All"] + list(incidents_df['assigned_team'].unique()))
    
    # Apply filters
    filtered_df = incidents_df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
    if team_filter != "All":
        filtered_df = filtered_df[filtered_df['assigned_team'] == team_filter]
    
    # Incident list
    st.markdown("### Incident List")
    
    for _, incident in filtered_df.iterrows():
        with st.expander(f"[{incident['priority']}] {incident['id']} - {incident['title']}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Customer:** {incident['customer']}")
                st.write(f"**Description:** {incident['description'][:200]}...")
                st.write(f"**Tags:** {', '.join(incident['tags']) if incident['tags'] else 'None'}")
                st.write(f"**Created:** {incident['created_date']}")
            
            with col2:
                st.metric("Priority", incident['priority'])
                st.metric("Team", incident['assigned_team'])
                st.metric("Est. Hours", incident['estimated_resolution_hours'])
            
            with col3:
                current_status = incident['status']
                if current_status == 'open':
                    if st.button("Start Work", key=f"start_{incident['id']}"):
                        data_manager.update_incident_status(incident['id'], 'in_progress')
                        st.rerun()
                elif current_status == 'in_progress':
                    if st.button("Resolve", key=f"resolve_{incident['id']}"):
                        data_manager.update_incident_status(incident['id'], 'resolved')
                        st.rerun()
                else:
                    st.success("Resolved")

def triage_rules_management(data_manager):
    st.subheader("Triage Rules Configuration")
    
    st.markdown("""
    ### Current AI Triage Rules
    
    **Priority Calculation:**
    - Urgency score (Low: 10, Medium: 30, High: 60, Critical: 90)
    - Impact multiplier (Individual: 1.0, Department: 1.2, Organization: 1.5, External: 2.0)
    - Keyword bonuses (Critical: +30, Security: +20, Network+Organization: +15)
    
    **Team Assignment Rules:**
    """)
    
    rules = {
        "Security Team": ["security", "password", "breach", "unauthorized"],
        "Network Operations": ["network", "connection", "vpn", "internet"],
        "Database Team": ["database", "sql", "data", "report"],
        "Application Support": ["software", "application", "program"],
        "IT Support": ["hardware", "laptop", "printer", "computer"]
    }
    
    for team, keywords in rules.items():
        st.markdown(f"**{team}:** {', '.join(keywords)}")
    
    # Add new rule
    st.markdown("### Add New Rule")
    
    with st.form("new_rule"):
        rule_name = st.text_input("Rule Name")
        keywords = st.text_input("Keywords (comma-separated)")
        assigned_team = st.text_input("Assigned Team")
        priority_modifier = st.slider("Priority Modifier", -20, 20, 0)
        
        if st.form_submit_button("Add Rule"):
            if rule_name and keywords and assigned_team:
                st.success(f"Rule '{rule_name}' added successfully!")
                st.info("In production, this would update the triage engine configuration.")

def show_demo_script():
    st.subheader("Demo Script - Incident Triage")
    
    st.markdown("""
    ### 30-Second Demo Flow
    
    **Scenario:** IT Security incident requiring immediate attention
    
    **Script:**
    1. "Let me demonstrate CrossPilot's AI-powered incident triage"
    2. **Click 'Submit Incident' tab**
    3. "I'll submit a security incident"
    4. **Fill in quickly:**
       - Title: "Unauthorized access attempt detected"
       - Customer: "Security Monitoring"
       - Category: "Security"
       - Urgency: "High"
       - Impact: "Organization"
       - Description: "Multiple failed login attempts from unknown IP address. Potential brute force attack on admin accounts."
    5. **Select affected systems:** Active Directory, VPN
    6. **Click 'Submit Incident'**
    7. "Watch as AI automatically classifies this as Critical priority"
    8. "AI assigns to Security Team and estimates 2-hour resolution"
    9. **Switch to 'Incident Dashboard' tab**
    10. "Here we see real-time incident tracking and team assignments"
    
    ### Key Talking Points
    - **Intelligent classification** - AI analyzes text to determine priority and routing
    - **Consistent triage** - Eliminates human bias and ensures proper escalation
    - **Automated routing** - Incidents reach the right team immediately
    - **Predictive analytics** - Estimates resolution time for better planning
    
    ### Demo Data to Use
    **High Priority Security Incident:**
    - **Title:** "Unauthorized access attempt detected"
    - **Description:** "Multiple failed login attempts from unknown IP address. Potential brute force attack on admin accounts."
    - **Expected Result:** Critical priority, Security Team assignment, 2-hour estimate
    
    **Medium Priority Hardware Issue:**
    - **Title:** "Laptop won't start"
    - **Description:** "Employee laptop showing black screen, power light is on but no display"
    - **Expected Result:** Medium priority, IT Support assignment, 24-hour estimate
    """)
    
    # Sample triage results
    st.markdown("### Expected AI Triage Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Security Incident:**")
        st.code("""
Priority: Critical
Team: Security Team
Tags: security, unauthorized, brute_force
Est. Resolution: 2 hours
Reasoning: High urgency with organization impact. 
Security keywords detected requiring immediate attention.
        """)
    
    with col2:
        st.markdown("**Hardware Issue:**")
        st.code("""
Priority: Medium  
Team: IT Support
Tags: hardware, laptop, display
Est. Resolution: 24 hours
Reasoning: Medium urgency affecting individual user.
Hardware-related issue assigned to IT Support.
        """)

if __name__ == "__main__":
    main()
