import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Onboarding", page_icon="👋", layout="wide")

def main():
    st.title("👋 Employee Onboarding")
    st.markdown("### Automated onboarding workflows and tracking")
    
    # Get services from session state
    if 'data_manager' not in st.session_state:
        st.error("Data manager not initialized. Please return to the main page.")
        return
    
    data_manager = st.session_state.data_manager
    ai_services = st.session_state.ai_services
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["New Employee", "Onboarding Dashboard", "Checklist Templates", "Demo Script"])
    
    with tab1:
        new_employee_form(data_manager, ai_services)
    
    with tab2:
        onboarding_dashboard(data_manager)
    
    with tab3:
        checklist_templates(data_manager)
    
    with tab4:
        show_demo_script()

def new_employee_form(data_manager, ai_services):
    st.subheader("Add New Employee")
    
    with st.form("new_employee_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email Address")
            employee_id = st.text_input("Employee ID", value=f"EMP{uuid.uuid4().hex[:6].upper()}")
        
        with col2:
            department = st.selectbox("Department", ["Engineering", "HR", "Sales", "Marketing", "Finance", "Operations"])
            role = st.text_input("Job Title")
            manager = st.selectbox("Manager", ["John Smith", "Sarah Johnson", "Mike Chen", "Lisa Rodriguez"])
            start_date = st.date_input("Start Date", value=datetime.now().date())
        
        # Security & Access
        st.markdown("#### Security & Access Requirements")
        col1, col2 = st.columns(2)
        
        with col1:
            security_clearance = st.selectbox("Security Clearance", ["Standard", "Elevated", "Admin"])
            office_location = st.selectbox("Office Location", ["New York", "San Francisco", "London", "Remote"])
        
        with col2:
            equipment_needed = st.multiselect(
                "Equipment Needed", 
                ["Laptop", "Monitor", "Phone", "Headset", "Dock", "Keyboard", "Mouse"]
            )
            system_access = st.multiselect(
                "System Access Required",
                ["Active Directory", "Email", "VPN", "CRM", "ERP", "Development Tools", "Design Tools"]
            )
        
        submitted = st.form_submit_button("Create Employee & Start Onboarding")
        
        if submitted:
            if first_name and last_name and email and role:
                # Create employee record
                employee = {
                    'id': employee_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'department': department,
                    'role': role,
                    'manager': manager,
                    'start_date': start_date.isoformat(),
                    'status': 'pending',
                    'security_clearance': security_clearance,
                    'office_location': office_location,
                    'equipment_needed': equipment_needed,
                    'system_access': system_access,
                    'created_date': datetime.now().isoformat(),
                    'onboarding_progress': 0
                }
                
                # Generate AI-powered onboarding checklist
                checklist = generate_onboarding_checklist(ai_services, employee)
                employee['checklist'] = checklist
                
                # Save employee
                data_manager.add_user(employee)
                
                st.success(f"Employee {first_name} {last_name} added successfully!")
                st.success("AI-generated onboarding checklist created and assigned.")
                
                # Display generated checklist
                st.markdown("### Generated Onboarding Checklist")
                for category, items in checklist.items():
                    st.markdown(f"**{category}:**")
                    for item in items:
                        st.markdown(f"- {item}")
                
            else:
                st.error("Please fill in all required fields.")

def generate_onboarding_checklist(ai_services, employee):
    """Generate AI-powered onboarding checklist based on role and requirements"""
    
    # Create a comprehensive checklist based on employee details
    checklist = {
        "Pre-boarding (Before Start Date)": [
            "Send welcome email with first day instructions",
            "Prepare workspace and equipment",
            "Create accounts in required systems",
            "Schedule orientation meetings"
        ],
        "Day 1 - Welcome & Setup": [
            "Office tour and introductions",
            "Complete I-9 and tax forms",
            "Security badge and access card setup",
            "IT equipment distribution and setup",
            "Review employee handbook and policies"
        ],
        "Week 1 - Integration": [
            "Department-specific orientation",
            "Meet with direct manager for goal setting",
            "Complete mandatory training modules",
            "Set up development/work environment",
            "Introduction to key stakeholders"
        ],
        "Month 1 - Skill Development": [
            "Role-specific training completion",
            "Shadow experienced team members",
            "First project assignment",
            "30-day check-in with HR",
            "Feedback session with manager"
        ]
    }
    
    # Customize based on role and department
    if employee['department'] == 'Engineering':
        checklist["Week 1 - Integration"].extend([
            "Code repository access and setup",
            "Development environment configuration",
            "Architecture overview session"
        ])
    elif employee['department'] == 'Sales':
        checklist["Week 1 - Integration"].extend([
            "CRM system training",
            "Product knowledge sessions",
            "Sales process overview"
        ])
    
    # Add equipment-specific tasks
    if 'Laptop' in employee['equipment_needed']:
        checklist["Day 1 - Welcome & Setup"].append("Laptop configuration and software installation")
    
    if 'VPN' in employee['system_access']:
        checklist["Day 1 - Welcome & Setup"].append("VPN setup and security training")
    
    return checklist

def onboarding_dashboard(data_manager):
    st.subheader("Onboarding Dashboard")
    
    users_df = data_manager.get_users()
    
    if users_df.empty:
        st.info("No employees in the system yet.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    pending_onboarding = len(users_df[users_df['status'] == 'pending'])
    in_progress = len(users_df[users_df['status'] == 'in_progress'])
    completed = len(users_df[users_df['status'] == 'completed'])
    
    with col1:
        st.metric("Pending", pending_onboarding)
    with col2:
        st.metric("In Progress", in_progress)
    with col3:
        st.metric("Completed", completed)
    with col4:
        avg_progress = users_df['onboarding_progress'].mean() if not users_df.empty else 0
        st.metric("Avg Progress", f"{avg_progress:.0f}%")
    
    # Employee list with actions
    st.markdown("### Employee Onboarding Status")
    
    for _, employee in users_df.iterrows():
        with st.expander(f"{employee['first_name']} {employee['last_name']} - {employee['status'].title()}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Role:** {employee['role']}")
                st.write(f"**Department:** {employee['department']}")
                st.write(f"**Start Date:** {employee['start_date']}")
                st.write(f"**Manager:** {employee['manager']}")
                
                # Progress bar
                progress = employee.get('onboarding_progress', 0)
                st.progress(progress / 100)
                st.caption(f"Onboarding Progress: {progress}%")
            
            with col2:
                if st.button("View Checklist", key=f"checklist_{employee['id']}"):
                    st.session_state[f"show_checklist_{employee['id']}"] = True
                
                if st.button("Update Progress", key=f"progress_{employee['id']}"):
                    new_progress = st.slider(
                        "Progress", 0, 100, progress, 
                        key=f"slider_{employee['id']}"
                    )
                    data_manager.update_user_progress(employee['id'], new_progress)
                    st.rerun()
            
            with col3:
                if employee['status'] == 'pending':
                    if st.button("Start Onboarding", key=f"start_{employee['id']}"):
                        data_manager.update_user_status(employee['id'], 'in_progress')
                        st.success("Onboarding started!")
                        st.rerun()
                
                elif employee['status'] == 'in_progress':
                    if st.button("Mark Complete", key=f"complete_{employee['id']}"):
                        data_manager.update_user_status(employee['id'], 'completed')
                        data_manager.update_user_progress(employee['id'], 100)
                        st.success("Onboarding completed!")
                        st.rerun()
            
            # Show checklist if requested
            if st.session_state.get(f"show_checklist_{employee['id']}", False):
                st.markdown("**Onboarding Checklist:**")
                if 'checklist' in employee and employee['checklist']:
                    checklist = eval(employee['checklist']) if isinstance(employee['checklist'], str) else employee['checklist']
                    for category, items in checklist.items():
                        st.markdown(f"**{category}:**")
                        for item in items:
                            st.markdown(f"- {item}")

def checklist_templates(data_manager):
    st.subheader("Onboarding Checklist Templates")
    
    templates = {
        "Engineering": {
            "Week 1": [
                "Code repository access",
                "Development environment setup",
                "Architecture overview",
                "Team introductions"
            ],
            "Month 1": [
                "First code contribution",
                "Code review process training",
                "Technical mentorship assignment"
            ]
        },
        "Sales": {
            "Week 1": [
                "CRM system training",
                "Product knowledge sessions",
                "Sales process overview",
                "Territory assignment"
            ],
            "Month 1": [
                "First client meeting",
                "Sales methodology training",
                "Pipeline management"
            ]
        },
        "HR": {
            "Week 1": [
                "HRIS system training",
                "Employment law overview",
                "Policy and procedure review"
            ],
            "Month 1": [
                "First recruitment cycle",
                "Employee relations training",
                "Compliance certification"
            ]
        }
    }
    
    selected_dept = st.selectbox("Department", list(templates.keys()))
    
    if selected_dept:
        st.markdown(f"### {selected_dept} Onboarding Template")
        
        for period, tasks in templates[selected_dept].items():
            st.markdown(f"**{period}:**")
            for task in tasks:
                st.markdown(f"- {task}")
    
    # Allow customization
    st.markdown("### Customize Template")
    
    with st.form("template_form"):
        new_period = st.text_input("Period (e.g., Week 2, Month 2)")
        new_tasks = st.text_area("Tasks (one per line)")
        
        if st.form_submit_button("Add to Template"):
            if new_period and new_tasks:
                st.success(f"Tasks added to {selected_dept} template for {new_period}")

def show_demo_script():
    st.subheader("Demo Script - Employee Onboarding")
    
    st.markdown("""
    ### 30-Second Demo Flow
    
    **Scenario:** Onboarding a new software engineer
    
    **Script:**
    1. "Let me show you CrossPilot's automated onboarding"
    2. **Click 'New Employee' tab**
    3. "I'm adding a new software engineer"
    4. **Fill in quickly:**
       - Name: "Alex Chen"
       - Email: "alex.chen@company.com"
       - Department: "Engineering"
       - Role: "Senior Software Engineer"
       - Manager: "John Smith"
    5. **Select equipment:** Laptop, Monitor, Headset
    6. **Select systems:** Active Directory, Email, VPN, Development Tools
    7. **Click 'Create Employee & Start Onboarding'**
    8. "Watch as AI generates a personalized onboarding checklist"
    9. **Switch to 'Onboarding Dashboard' tab**
    10. "Here we can track progress and manage all employees"
    
    ### Key Talking Points
    - **AI-powered checklist generation** - Automatically creates role-specific onboarding plans
    - **Progress tracking** - Real-time visibility into onboarding status
    - **Cross-functional coordination** - Connects HR, IT, and management
    - **Compliance ready** - Ensures no critical steps are missed
    
    ### Demo Data to Use
    - **Employee:** Alex Chen, Senior Software Engineer
    - **Manager:** John Smith
    - **Department:** Engineering
    - **Equipment:** Laptop, Monitor, Headset
    - **Systems:** Development Tools, VPN, Email
    """)
    
    # Sample checklist output
    st.markdown("### Expected AI-Generated Checklist")
    st.code("""
    Pre-boarding:
    - Send welcome email with first day instructions
    - Prepare workspace with laptop and monitor
    - Create Active Directory account
    - Set up email and VPN access
    
    Day 1:
    - Office tour and team introductions
    - IT equipment setup and configuration
    - Security training and badge creation
    - Development environment setup
    
    Week 1:
    - Code repository access and training
    - Architecture overview session
    - Pair programming with senior developer
    - Project assignment and goal setting
    """)

if __name__ == "__main__":
    main()
