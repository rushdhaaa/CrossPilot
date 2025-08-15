import streamlit as st
import json
import pandas as pd
from datetime import datetime
import uuid

st.set_page_config(page_title="Workflow Builder", page_icon="🔧", layout="wide")

def main():
    st.title("🔧 Workflow Builder")
    st.markdown("### Create and manage automated workflows")
    
    # Get data manager from session state
    if 'data_manager' not in st.session_state:
        st.error("Data manager not initialized. Please return to the main page.")
        return
    
    data_manager = st.session_state.data_manager
    
    # Tabs for different actions
    tab1, tab2, tab3 = st.tabs(["Create Workflow", "Manage Workflows", "Demo Script"])
    
    with tab1:
        create_workflow_form(data_manager)
    
    with tab2:
        manage_workflows(data_manager)
    
    with tab3:
        show_demo_script()

def create_workflow_form(data_manager):
    st.subheader("Create New Workflow")
    
    # Basic Information
    st.markdown("#### Basic Information")
    
    with st.form("workflow_form"):
        name = st.text_input("Workflow Name", placeholder="e.g., New Employee Onboarding")
        description = st.text_area("Description", placeholder="Describe what this workflow accomplishes")
        category = st.selectbox("Category", ["Onboarding", "Incident Management", "Reporting", "General"])
        
        # Triggers
        st.markdown("#### Triggers")
        trigger_type = st.selectbox("Trigger Type", ["Manual", "Scheduled", "Event-based", "API Call"])
        
        schedule = None
        event = None
        if trigger_type == "Scheduled":
            schedule = st.selectbox("Schedule", ["Daily", "Weekly", "Monthly", "Custom"])
        elif trigger_type == "Event-based":
            event = st.text_input("Event", placeholder="e.g., user.created, incident.submitted")
        
        # Submit form
        submitted = st.form_submit_button("Create Workflow")
    
    # Steps management outside of form
    st.markdown("#### Workflow Steps")
    
    # Initialize steps in session state
    if 'workflow_steps' not in st.session_state:
        st.session_state.workflow_steps = []
    
    # Add step button
    if st.button("Add Step"):
        st.session_state.workflow_steps.append({
            'id': str(uuid.uuid4()),
            'name': '',
            'type': 'Send Email',
            'config': {}
        })
        st.rerun()
    
    # Display and edit steps
    for i, step in enumerate(st.session_state.workflow_steps):
        with st.expander(f"Step {i+1}: {step.get('name', 'Unnamed Step')}", expanded=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                step_name = st.text_input(f"Step Name", value=step.get('name', ''), key=f"step_name_{i}")
                step_type = st.selectbox(
                    f"Step Type", 
                    ["Send Email", "Create Ticket", "Assign Task", "API Call", "Approval", "Wait", "Condition"],
                    index=["Send Email", "Create Ticket", "Assign Task", "API Call", "Approval", "Wait", "Condition"].index(step.get('type', 'Send Email')) if step.get('type') in ["Send Email", "Create Ticket", "Assign Task", "API Call", "Approval", "Wait", "Condition"] else 0,
                    key=f"step_type_{i}"
                )
                
                # Step-specific configuration
                if step_type == "Send Email":
                    to_email = st.text_input("To Email", value=step.get('config', {}).get('to', ''), key=f"email_to_{i}")
                    subject = st.text_input("Subject", value=step.get('config', {}).get('subject', ''), key=f"email_subject_{i}")
                    template = st.text_area("Email Template", value=step.get('config', {}).get('template', ''), key=f"email_template_{i}")
                    
                    step['config'] = {
                        'to': to_email,
                        'subject': subject,
                        'template': template
                    }
                
                elif step_type == "Create Ticket":
                    ticket_type = st.selectbox("Ticket Type", ["IT Support", "HR Request", "Facilities"], key=f"ticket_type_{i}")
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key=f"ticket_priority_{i}")
                    assign_to = st.text_input("Assign To", value=step.get('config', {}).get('assign_to', ''), key=f"ticket_assign_{i}")
                    
                    step['config'] = {
                        'ticket_type': ticket_type,
                        'priority': priority,
                        'assign_to': assign_to
                    }
                
                # Update step
                step['name'] = step_name
                step['type'] = step_type
            
            with col2:
                if st.button("Remove", key=f"remove_step_{i}"):
                    st.session_state.workflow_steps.pop(i)
                    st.rerun()
    # Handle form submission
    if submitted:
        if name and description:
            workflow = {
                'id': str(uuid.uuid4()),
                'name': name,
                'description': description,
                'category': category,
                'trigger': {
                    'type': trigger_type,
                    'config': {}
                },
                'steps': st.session_state.workflow_steps,
                'created_date': datetime.now().isoformat(),
                'status': 'active',
                'version': '1.0'
            }
            
            # Add schedule or event config
            if trigger_type == "Scheduled" and schedule:
                workflow['trigger']['config']['schedule'] = schedule
            elif trigger_type == "Event-based" and event:
                workflow['trigger']['config']['event'] = event
            
            data_manager.save_workflow(workflow)
            st.success(f"Workflow '{name}' created successfully!")
            st.session_state.workflow_steps = []  # Reset steps
            st.rerun()
        else:
            st.error("Please fill in all required fields.")

def manage_workflows(data_manager):
    st.subheader("Existing Workflows")
    
    workflows = data_manager.get_workflows()
    
    if workflows:
        for workflow in workflows:
            with st.expander(f"{workflow['name']} ({workflow['category']})"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Description:** {workflow['description']}")
                    st.write(f"**Trigger:** {workflow['trigger']['type']}")
                    st.write(f"**Steps:** {len(workflow['steps'])}")
                    st.write(f"**Status:** {workflow['status']}")
                
                with col2:
                    if st.button("Edit", key=f"edit_{workflow['id']}"):
                        st.info("Edit functionality - would open workflow in edit mode")
                
                with col3:
                    if st.button("Run", key=f"run_{workflow['id']}"):
                        st.success(f"Workflow '{workflow['name']}' executed successfully!")
                
                # Show workflow steps
                if workflow['steps']:
                    st.markdown("**Workflow Steps:**")
                    for i, step in enumerate(workflow['steps'], 1):
                        st.markdown(f"{i}. **{step['name']}** ({step['type']})")
    else:
        st.info("No workflows created yet. Create your first workflow in the 'Create Workflow' tab.")

def show_demo_script():
    st.subheader("Demo Script - Workflow Builder")
    
    st.markdown("""
    ### 30-Second Demo Flow
    
    **Scenario:** Creating an automated onboarding workflow
    
    **Script:**
    1. "Let me show you how to create a workflow in CrossPilot"
    2. **Click 'Create Workflow' tab**
    3. "I'll create an employee onboarding workflow"
    4. **Fill in:** 
       - Name: "New Employee Onboarding"
       - Description: "Automated checklist and access provisioning"
       - Category: "Onboarding"
       - Trigger: "Event-based" → "user.created"
    5. **Add steps by clicking 'Add Step':**
       - Step 1: Send Email → Welcome email to new employee
       - Step 2: Create Ticket → IT access provisioning
       - Step 3: Assign Task → Manager orientation setup
    6. **Click 'Create Workflow'**
    7. "Now this workflow will automatically trigger whenever a new employee is added"
    
    ### Key Talking Points
    - **No-code workflow creation** - Business users can create workflows without technical knowledge
    - **Event-driven automation** - Workflows trigger automatically based on business events
    - **Cross-functional integration** - Connects HR, IT, and management processes
    - **Audit trail** - All workflow executions are logged for compliance
    
    ### Mock Data for Demo
    Use the sample workflow creation above with these realistic examples.
    """)
    
    # Demo data
    st.markdown("### Sample Workflow Steps")
    demo_steps = [
        {"name": "Send Welcome Email", "type": "Send Email", "config": "HR template with company handbook"},
        {"name": "Create IT Ticket", "type": "Create Ticket", "config": "Hardware and software provisioning"},
        {"name": "Schedule Orientation", "type": "Assign Task", "config": "Manager receives task to schedule orientation"},
        {"name": "Add to Systems", "type": "API Call", "config": "Automatically provision Active Directory, email, VPN"}
    ]
    
    for i, step in enumerate(demo_steps, 1):
        st.markdown(f"**{i}. {step['name']}** ({step['type']})")
        st.caption(step['config'])

if __name__ == "__main__":
    main()
