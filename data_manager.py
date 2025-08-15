import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataManager:
    """Data management service for CrossPilot - handles all data operations"""
    
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        self.initialize_sample_data()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def initialize_sample_data(self):
        """Initialize with sample data if files don't exist"""
        
        # Initialize users data
        users_file = os.path.join(self.data_dir, "users.csv")
        if not os.path.exists(users_file):
            self.create_sample_users()
        
        # Initialize incidents data
        incidents_file = os.path.join(self.data_dir, "incidents.csv")
        if not os.path.exists(incidents_file):
            self.create_sample_incidents()
        
        # Initialize roles data
        roles_file = os.path.join(self.data_dir, "roles.csv")
        if not os.path.exists(roles_file):
            self.create_sample_roles()
        
        # Initialize metrics data
        metrics_file = os.path.join(self.data_dir, "metrics.csv")
        if not os.path.exists(metrics_file):
            self.create_sample_metrics()
        
        # Initialize workflows data
        workflows_file = os.path.join(self.data_dir, "workflows.json")
        if not os.path.exists(workflows_file):
            self.create_sample_workflows()
    
    def create_sample_users(self):
        """Create sample users data"""
        users_data = [
            {
                'id': 'EMP001',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.johnson@company.com',
                'department': 'Engineering',
                'role': 'Senior Software Engineer',
                'manager': 'John Smith',
                'start_date': '2024-01-15',
                'status': 'completed',
                'security_clearance': 'Standard',
                'office_location': 'San Francisco',
                'equipment_needed': '["Laptop", "Monitor", "Headset"]',
                'system_access': '["Active Directory", "Email", "VPN", "Development Tools"]',
                'created_date': '2024-01-10T09:00:00',
                'onboarding_progress': 100,
                'checklist': '{}'
            },
            {
                'id': 'EMP002',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'email': 'michael.chen@company.com',
                'department': 'Sales',
                'role': 'Account Executive',
                'manager': 'Lisa Rodriguez',
                'start_date': '2024-02-01',
                'status': 'in_progress',
                'security_clearance': 'Standard',
                'office_location': 'New York',
                'equipment_needed': '["Laptop", "Phone", "Headset"]',
                'system_access': '["Active Directory", "Email", "CRM"]',
                'created_date': '2024-01-25T14:30:00',
                'onboarding_progress': 75,
                'checklist': '{}'
            },
            {
                'id': 'EMP003',
                'first_name': 'Emily',
                'last_name': 'Davis',
                'email': 'emily.davis@company.com',
                'department': 'HR',
                'role': 'HR Business Partner',
                'manager': 'David Wilson',
                'start_date': '2024-02-15',
                'status': 'pending',
                'security_clearance': 'Elevated',
                'office_location': 'Remote',
                'equipment_needed': '["Laptop", "Monitor", "Phone"]',
                'system_access': '["Active Directory", "Email", "HRIS"]',
                'created_date': '2024-02-10T11:15:00',
                'onboarding_progress': 25,
                'checklist': '{}'
            }
        ]
        
        df = pd.DataFrame(users_data)
        df.to_csv(os.path.join(self.data_dir, "users.csv"), index=False)
    
    def create_sample_incidents(self):
        """Create sample incidents data"""
        incidents_data = [
            {
                'id': 'INC20240201001',
                'title': 'VPN connection timeout issues',
                'description': 'Multiple users reporting VPN connection timeouts when working remotely. Issue started this morning around 9 AM.',
                'customer': 'IT Help Desk',
                'category': 'Network',
                'urgency': 'High',
                'impact': 'Organization',
                'source': 'Monitoring',
                'affected_systems': '["VPN", "Network"]',
                'priority': 'High',
                'assigned_team': 'Network Operations',
                'tags': '["network", "vpn", "connectivity", "remote_work"]',
                'estimated_resolution_hours': 8,
                'status': 'in_progress',
                'created_date': '2024-02-01T09:15:00',
                'resolution_hours': None,
                'resolution_notes': None
            },
            {
                'id': 'INC20240201002',
                'title': 'Email delivery delays',
                'description': 'Several departments reporting delayed email delivery. External emails taking 30+ minutes to arrive.',
                'customer': 'Finance Department',
                'category': 'Software',
                'urgency': 'Medium',
                'impact': 'Department',
                'source': 'Email',
                'affected_systems': '["Email"]',
                'priority': 'Medium',
                'assigned_team': 'Application Support',
                'tags': '["email", "delivery", "performance"]',
                'estimated_resolution_hours': 24,
                'status': 'open',
                'created_date': '2024-02-01T11:30:00',
                'resolution_hours': None,
                'resolution_notes': None
            },
            {
                'id': 'INC20240130001',
                'title': 'Laptop screen flickering',
                'description': 'Employee laptop screen intermittently flickering. Issue started after recent Windows update.',
                'customer': 'Jane Smith',
                'category': 'Hardware',
                'urgency': 'Low',
                'impact': 'Individual',
                'source': 'Portal',
                'affected_systems': '["Laptop"]',
                'priority': 'Low',
                'assigned_team': 'IT Support',
                'tags': '["hardware", "laptop", "display"]',
                'estimated_resolution_hours': 72,
                'status': 'resolved',
                'created_date': '2024-01-30T14:45:00',
                'resolution_hours': 48,
                'resolution_notes': 'Replaced laptop screen'
            }
        ]
        
        df = pd.DataFrame(incidents_data)
        df.to_csv(os.path.join(self.data_dir, "incidents.csv"), index=False)
    
    def create_sample_roles(self):
        """Create sample roles and access data"""
        roles_data = [
            {
                'role': 'Software Engineer',
                'department': 'Engineering',
                'required_systems': '["Active Directory", "Email", "VPN", "Development Tools", "Code Repository"]',
                'provisioning_steps': '["Create AD account", "Add to dev groups", "Setup dev environment", "Grant repo access"]',
                'security_clearance': 'Standard',
                'approval_required': False
            },
            {
                'role': 'Account Executive',
                'department': 'Sales',
                'required_systems': '["Active Directory", "Email", "CRM", "Sales Tools"]',
                'provisioning_steps': '["Create AD account", "Setup CRM access", "Assign territory", "Add to sales team"]',
                'security_clearance': 'Standard',
                'approval_required': False
            },
            {
                'role': 'HR Business Partner',
                'department': 'HR',
                'required_systems': '["Active Directory", "Email", "HRIS", "Payroll System"]',
                'provisioning_steps': '["Create AD account", "Grant HRIS access", "Setup payroll permissions", "Add to HR group"]',
                'security_clearance': 'Elevated',
                'approval_required': True
            }
        ]
        
        df = pd.DataFrame(roles_data)
        df.to_csv(os.path.join(self.data_dir, "roles.csv"), index=False)
    
    def create_sample_metrics(self):
        """Create sample metrics data"""
        metrics_data = [
            {
                'week_ending': '2024-01-26',
                'new_employees': 5,
                'onboarding_completion_rate': 89.2,
                'avg_onboarding_days': 12.3,
                'new_incidents': 23,
                'incidents_resolved': 21,
                'avg_resolution_hours': 18.5,
                'customer_satisfaction': 4.2,
                'workflow_executions': 45,
                'automation_savings_hours': 67
            },
            {
                'week_ending': '2024-02-02',
                'new_employees': 3,
                'onboarding_completion_rate': 92.1,
                'avg_onboarding_days': 11.8,
                'new_incidents': 19,
                'incidents_resolved': 22,
                'avg_resolution_hours': 16.2,
                'customer_satisfaction': 4.4,
                'workflow_executions': 52,
                'automation_savings_hours': 78
            }
        ]
        
        df = pd.DataFrame(metrics_data)
        df.to_csv(os.path.join(self.data_dir, "metrics.csv"), index=False)
    
    def create_sample_workflows(self):
        """Create sample workflows data"""
        workflows_data = [
            {
                'id': 'WF001',
                'name': 'New Employee Onboarding',
                'description': 'Automated onboarding workflow for new employees',
                'category': 'Onboarding',
                'trigger': {
                    'type': 'Event-based',
                    'config': {'event': 'user.created'}
                },
                'steps': [
                    {
                        'id': 'step1',
                        'name': 'Send Welcome Email',
                        'type': 'Send Email',
                        'config': {
                            'to': '{{employee_email}}',
                            'subject': 'Welcome to the Company!',
                            'template': 'Welcome email with first day instructions'
                        }
                    },
                    {
                        'id': 'step2',
                        'name': 'Create IT Ticket',
                        'type': 'Create Ticket',
                        'config': {
                            'ticket_type': 'IT Support',
                            'priority': 'Medium',
                            'assign_to': 'IT Team'
                        }
                    }
                ],
                'created_date': '2024-01-15T10:00:00',
                'status': 'active',
                'version': '1.0'
            }
        ]
        
        with open(os.path.join(self.data_dir, "workflows.json"), 'w') as f:
            json.dump(workflows_data, f, indent=2)
    
    # User management methods
    def get_users(self) -> pd.DataFrame:
        """Get all users"""
        try:
            return pd.read_csv(os.path.join(self.data_dir, "users.csv"))
        except FileNotFoundError:
            return pd.DataFrame()
    
    def add_user(self, user_data: Dict[str, Any]) -> bool:
        """Add a new user"""
        try:
            df = self.get_users()
            new_row = pd.DataFrame([user_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(os.path.join(self.data_dir, "users.csv"), index=False)
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_user_status(self, user_id: str, status: str) -> bool:
        """Update user status"""
        try:
            df = self.get_users()
            df.loc[df['id'] == user_id, 'status'] = status
            df.to_csv(os.path.join(self.data_dir, "users.csv"), index=False)
            return True
        except Exception as e:
            print(f"Error updating user status: {e}")
            return False
    
    def update_user_progress(self, user_id: str, progress: int) -> bool:
        """Update user onboarding progress"""
        try:
            df = self.get_users()
            df.loc[df['id'] == user_id, 'onboarding_progress'] = progress
            df.to_csv(os.path.join(self.data_dir, "users.csv"), index=False)
            return True
        except Exception as e:
            print(f"Error updating user progress: {e}")
            return False
    
    # Incident management methods
    def get_incidents(self) -> pd.DataFrame:
        """Get all incidents"""
        try:
            return pd.read_csv(os.path.join(self.data_dir, "incidents.csv"))
        except FileNotFoundError:
            return pd.DataFrame()
    
    def add_incident(self, incident_data: Dict[str, Any]) -> bool:
        """Add a new incident"""
        try:
            df = self.get_incidents()
            new_row = pd.DataFrame([incident_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(os.path.join(self.data_dir, "incidents.csv"), index=False)
            return True
        except Exception as e:
            print(f"Error adding incident: {e}")
            return False
    
    def update_incident_status(self, incident_id: str, status: str) -> bool:
        """Update incident status"""
        try:
            df = self.get_incidents()
            df.loc[df['id'] == incident_id, 'status'] = status
            df.to_csv(os.path.join(self.data_dir, "incidents.csv"), index=False)
            return True
        except Exception as e:
            print(f"Error updating incident status: {e}")
            return False
    
    # Workflow management methods
    def get_workflows(self) -> List[Dict[str, Any]]:
        """Get all workflows"""
        try:
            with open(os.path.join(self.data_dir, "workflows.json"), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_workflow(self, workflow_data: Dict[str, Any]) -> bool:
        """Save a new workflow"""
        try:
            workflows = self.get_workflows()
            workflows.append(workflow_data)
            with open(os.path.join(self.data_dir, "workflows.json"), 'w') as f:
                json.dump(workflows, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving workflow: {e}")
            return False
    
    # Metrics methods
    def get_metrics(self) -> pd.DataFrame:
        """Get metrics data"""
        try:
            return pd.read_csv(os.path.join(self.data_dir, "metrics.csv"))
        except FileNotFoundError:
            return pd.DataFrame()
    
    def get_roles(self) -> pd.DataFrame:
        """Get roles data"""
        try:
            return pd.read_csv(os.path.join(self.data_dir, "roles.csv"))
        except FileNotFoundError:
            return pd.DataFrame()
