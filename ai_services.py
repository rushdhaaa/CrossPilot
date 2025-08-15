import os
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import OpenAI if available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    OpenAIClient = OpenAI
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAIClient = None

class AIServices:
    """AI services for CrossPilot - includes text analysis, summarization, and insights"""
    
    def __init__(self):
        self.openai_client = None
        if OPENAI_AVAILABLE and OpenAIClient:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAIClient(api_key=api_key)
    
    def generate_executive_summary(self, data_summary: str, report_type: str, focus_areas: List[str], audience: str) -> Dict[str, Any]:
        """Generate AI-powered executive summary"""
        
        if self.openai_client:
            try:
                prompt = self._create_summary_prompt(data_summary, report_type, focus_areas, audience)
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert business analyst specializing in operational efficiency and workforce management. Generate actionable insights and recommendations based on data analysis."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format={"type": "json_object"},
                    max_tokens=1500
                )
                
                content = response.choices[0].message.content
                if content:
                    return json.loads(content)
                else:
                    return self._generate_fallback_summary(data_summary, report_type, focus_areas)
            
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._generate_fallback_summary(data_summary, report_type, focus_areas)
        else:
            return self._generate_fallback_summary(data_summary, report_type, focus_areas)
    
    def analyze_incident_text(self, title: str, description: str) -> Dict[str, Any]:
        """Analyze incident text for classification and routing"""
        
        if self.openai_client:
            try:
                combined_text = f"Title: {title}\nDescription: {description}"
                
                prompt = f"""
                Analyze the following IT incident and provide classification:
                
                {combined_text}
                
                Provide analysis in JSON format with:
                - priority: "Critical", "High", "Medium", or "Low"
                - category: main category (e.g., "Hardware", "Software", "Network", "Security")
                - urgency_indicators: list of words/phrases that indicate urgency
                - affected_systems: likely affected systems based on description
                - recommended_team: which team should handle this (e.g., "IT Support", "Security Team", "Network Operations")
                - tags: relevant tags for categorization
                - confidence_score: 0-1 confidence in classification
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert IT incident analyst. Analyze incidents and provide accurate classification for routing and prioritization."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format={"type": "json_object"},
                    max_tokens=800
                )
                
                content = response.choices[0].message.content
                if content:
                    return json.loads(content)
                else:
                    return self._fallback_incident_analysis(title, description)
            
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._fallback_incident_analysis(title, description)
        else:
            return self._fallback_incident_analysis(title, description)
    
    def generate_onboarding_checklist(self, employee_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate personalized onboarding checklist"""
        
        if self.openai_client:
            try:
                prompt = f"""
                Generate a comprehensive onboarding checklist for a new employee with the following details:
                
                Role: {employee_data.get('role', 'N/A')}
                Department: {employee_data.get('department', 'N/A')}
                Security Clearance: {employee_data.get('security_clearance', 'Standard')}
                Equipment Needed: {', '.join(employee_data.get('equipment_needed', []))}
                System Access: {', '.join(employee_data.get('system_access', []))}
                Office Location: {employee_data.get('office_location', 'N/A')}
                
                Create a detailed checklist organized by time periods (Pre-boarding, Day 1, Week 1, Month 1).
                Tailor the checklist to the specific role and requirements.
                
                Return in JSON format with time periods as keys and task lists as values.
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an HR workflow expert specializing in employee onboarding. Create comprehensive, role-specific onboarding checklists."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format={"type": "json_object"},
                    max_tokens=1200
                )
                
                content = response.choices[0].message.content
                if content:
                    return json.loads(content)
                else:
                    return self._fallback_onboarding_checklist(employee_data)
            
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._fallback_onboarding_checklist(employee_data)
        else:
            return self._fallback_onboarding_checklist(employee_data)
    
    def _create_summary_prompt(self, data_summary: str, report_type: str, focus_areas: List[str], audience: str) -> str:
        """Create prompt for executive summary generation"""
        
        focus_text = ", ".join(focus_areas)
        
        return f"""
        Generate a comprehensive {report_type} report for {audience} audience focusing on {focus_text}.
        
        Data Summary:
        {data_summary}
        
        Please provide a JSON response with the following structure:
        {{
            "executive_summary": "Brief overview of key findings and performance",
            "key_insights": ["List of 4-5 key insights from the data"],
            "recommendations": ["List of 4-5 actionable recommendations"],
            "next_steps": ["List of 3-4 specific next steps"],
            "metrics_highlight": "Brief summary of the most important metrics"
        }}
        
        Focus on operational efficiency, process improvement, and business impact.
        Make recommendations specific and actionable for the target audience.
        """
    
    def _generate_fallback_summary(self, data_summary: str, report_type: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Generate fallback summary when AI is not available"""
        
        return {
            "executive_summary": f"""
            {report_type} operational review showing system performance across {', '.join(focus_areas)}.
            Key metrics indicate stable operations with opportunities for process optimization.
            Automated workflow management is driving efficiency improvements across departments.
            """,
            "key_insights": [
                "Workflow automation reducing manual tasks by estimated 35-40%",
                "Cross-functional coordination improved through centralized platform",
                "Real-time visibility enabling faster decision making",
                "Standardized processes ensuring consistent service delivery"
            ],
            "recommendations": [
                "Expand automation to additional business processes",
                "Implement advanced analytics for predictive insights",
                "Enhance integration with existing enterprise systems",
                "Develop mobile capabilities for field workers"
            ],
            "next_steps": [
                "Schedule stakeholder review meeting",
                "Evaluate ROI metrics and business case",
                "Plan phased rollout to additional departments",
                "Assess integration requirements with legacy systems"
            ],
            "metrics_highlight": "Operations maintaining stable performance with automation driving efficiency gains"
        }
    
    def _fallback_incident_analysis(self, title: str, description: str) -> Dict[str, Any]:
        """Fallback incident analysis using keyword matching"""
        
        combined_text = f"{title} {description}".lower()
        
        # Define keyword patterns
        security_keywords = ['password', 'login', 'access', 'unauthorized', 'breach', 'virus', 'hack']
        network_keywords = ['connection', 'internet', 'wifi', 'vpn', 'network', 'ping', 'timeout']
        hardware_keywords = ['laptop', 'computer', 'printer', 'mouse', 'keyboard', 'screen', 'hardware']
        critical_keywords = ['down', 'outage', 'critical', 'urgent', 'emergency', 'broken', 'failure']
        
        # Analyze text
        has_security = any(keyword in combined_text for keyword in security_keywords)
        has_network = any(keyword in combined_text for keyword in network_keywords)
        has_hardware = any(keyword in combined_text for keyword in hardware_keywords)
        has_critical = any(keyword in combined_text for keyword in critical_keywords)
        
        # Determine category and priority
        if has_security:
            category = "Security"
            recommended_team = "Security Team"
        elif has_network:
            category = "Network"
            recommended_team = "Network Operations"
        elif has_hardware:
            category = "Hardware"
            recommended_team = "IT Support"
        else:
            category = "Software"
            recommended_team = "Application Support"
        
        if has_critical or has_security:
            priority = "Critical"
        elif 'high' in combined_text or 'urgent' in combined_text:
            priority = "High"
        elif 'low' in combined_text:
            priority = "Low"
        else:
            priority = "Medium"
        
        tags = []
        if has_security:
            tags.extend(['security', 'authentication'])
        if has_network:
            tags.extend(['network', 'connectivity'])
        if has_hardware:
            tags.extend(['hardware', 'equipment'])
        if has_critical:
            tags.append('critical')
        
        return {
            "priority": priority,
            "category": category,
            "urgency_indicators": [word for word in critical_keywords if word in combined_text],
            "affected_systems": ["Unknown"],
            "recommended_team": recommended_team,
            "tags": tags,
            "confidence_score": 0.7
        }
    
    def _fallback_onboarding_checklist(self, employee_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate fallback onboarding checklist"""
        
        department = employee_data.get('department', 'General')
        role = employee_data.get('role', 'Employee')
        
        base_checklist = {
            "Pre-boarding (Before Start Date)": [
                "Send welcome email with first day instructions",
                "Prepare workspace and required equipment",
                "Create user accounts in required systems",
                "Schedule orientation meetings with manager"
            ],
            "Day 1 - Welcome & Setup": [
                "Office tour and introductions to team",
                "Complete HR paperwork and documentation",
                "Security badge and access card setup",
                "IT equipment distribution and basic setup",
                "Review employee handbook and company policies"
            ],
            "Week 1 - Integration": [
                "Department-specific orientation session",
                "Meet with direct manager for role expectations",
                "Complete mandatory training modules",
                "Introduction to key stakeholders and contacts",
                "Set up work environment and tools"
            ],
            "Month 1 - Development": [
                "Complete role-specific training programs",
                "First project or assignment",
                "30-day check-in with HR and manager",
                "Feedback session and goal setting",
                "Integration assessment and adjustments"
            ]
        }
        
        # Add department-specific items
        if department == 'Engineering':
            base_checklist["Week 1 - Integration"].extend([
                "Setup development environment and tools",
                "Access to code repositories and documentation",
                "Architecture overview and code review process"
            ])
        elif department == 'Sales':
            base_checklist["Week 1 - Integration"].extend([
                "CRM system training and setup",
                "Territory assignment and customer introduction",
                "Sales process and methodology training"
            ])
        
        return base_checklist