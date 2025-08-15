import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

class WorkflowEngine:
    """Core workflow execution engine for CrossPilot"""
    
    def __init__(self):
        self.active_workflows = {}
        self.workflow_history = []
    
    def execute_workflow(self, workflow: Dict[str, Any], trigger_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a workflow with the given trigger data"""
        
        execution_id = str(uuid.uuid4())
        execution_context = {
            'id': execution_id,
            'workflow_id': workflow['id'],
            'workflow_name': workflow['name'],
            'started_at': datetime.now().isoformat(),
            'status': 'running',
            'current_step': 0,
            'trigger_data': trigger_data or {},
            'step_results': [],
            'variables': {}
        }
        
        try:
            # Add to active workflows
            self.active_workflows[execution_id] = execution_context
            
            # Execute each step
            for i, step in enumerate(workflow['steps']):
                execution_context['current_step'] = i
                step_result = self.execute_step(step, execution_context)
                execution_context['step_results'].append(step_result)
                
                # Check for step failure
                if not step_result.get('success', True):
                    execution_context['status'] = 'failed'
                    execution_context['error'] = step_result.get('error', 'Step execution failed')
                    break
            
            # Mark as completed if all steps succeeded
            if execution_context['status'] == 'running':
                execution_context['status'] = 'completed'
            
            execution_context['completed_at'] = datetime.now().isoformat()
            
        except Exception as e:
            execution_context['status'] = 'error'
            execution_context['error'] = str(e)
            execution_context['completed_at'] = datetime.now().isoformat()
        
        finally:
            # Move to history and remove from active
            self.workflow_history.append(execution_context.copy())
            if execution_id in self.active_workflows:
                del self.active_workflows[execution_id]
        
        return execution_context
    
    def execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        
        step_type = step.get('type', 'unknown')
        step_config = step.get('config', {})
        
        try:
            if step_type == 'Send Email':
                return self.execute_email_step(step_config, context)
            elif step_type == 'Create Ticket':
                return self.execute_ticket_step(step_config, context)
            elif step_type == 'Assign Task':
                return self.execute_task_step(step_config, context)
            elif step_type == 'API Call':
                return self.execute_api_step(step_config, context)
            elif step_type == 'Approval':
                return self.execute_approval_step(step_config, context)
            elif step_type == 'Wait':
                return self.execute_wait_step(step_config, context)
            elif step_type == 'Condition':
                return self.execute_condition_step(step_config, context)
            else:
                return {
                    'success': False,
                    'error': f'Unknown step type: {step_type}',
                    'executed_at': datetime.now().isoformat()
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Step execution failed: {str(e)}',
                'executed_at': datetime.now().isoformat()
            }
    
    def execute_email_step(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute email sending step"""
        
        to_email = config.get('to', '')
        subject = config.get('subject', '')
        template = config.get('template', '')
        
        # In a real implementation, this would integrate with an email service
        # For now, we'll simulate the email sending
        
        # Replace variables in template
        processed_template = self.replace_variables(template, context)
        processed_subject = self.replace_variables(subject, context)
        
        # Simulate email sending
        email_result = {
            'to': to_email,
            'subject': processed_subject,
            'body': processed_template,
            'sent_at': datetime.now().isoformat(),
            'message_id': f'msg_{uuid.uuid4().hex[:8]}'
        }
        
        return {
            'success': True,
            'result': email_result,
            'executed_at': datetime.now().isoformat()
        }
    
    def execute_ticket_step(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ticket creation step"""
        
        ticket_type = config.get('ticket_type', 'General')
        priority = config.get('priority', 'Medium')
        assign_to = config.get('assign_to', '')
        
        # Create ticket record
        ticket = {
            'id': f'TKT{datetime.now().strftime("%Y%m%d")}{uuid.uuid4().hex[:4].upper()}',
            'type': ticket_type,
            'priority': priority,
            'assigned_to': assign_to,
            'created_by': 'CrossPilot Workflow',
            'created_at': datetime.now().isoformat(),
            'status': 'open',
            'workflow_execution_id': context['id']
        }
        
        return {
            'success': True,
            'result': ticket,
            'executed_at': datetime.now().isoformat()
        }
    
    def execute_task_step(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task assignment step"""
        
        assign_to = config.get('assign_to', '')
        task_description = config.get('description', '')
        due_date = config.get('due_date', '')
        
        # Create task record
        task = {
            'id': f'TSK{uuid.uuid4().hex[:8].upper()}',
            'assigned_to': assign_to,
            'description': task_description,
            'due_date': due_date,
            'created_at': datetime.now().isoformat(),
            'status': 'assigned',
            'workflow_execution_id': context['id']
        }
        
        return {
            'success': True,
            'result': task,
            'executed_at': datetime.now().isoformat()
        }
    
    def execute_api_step(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API call step"""
        
        url = config.get('url', '')
        method = config.get('method', 'GET')
        headers = config.get('headers', {})
        payload = config.get('payload', {})
        
        # In a real implementation, this would make actual HTTP requests
        # For now, we'll simulate the API call
        
        api_result = {
            'url': url,
            'method': method,
            'status_code': 200,
            'response': {'success': True, 'message': 'API call simulated'},
            'called_at': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'result': api_result,
            'executed_at': datetime.now().isoformat()
        }
    
    def execute_approval_step(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute approval step"""
        
        approver = config.get('approver', '')
        approval_type = config.get('type', 'manual')
        
        # For demo purposes, we'll auto-approve
        # In reality, this would create an approval request
        
        approval = {
            'id': f'APP{uuid.uuid4().hex[:8].upper()}',
            'approver': approver,
            'type': approval_type,
            'status': 'approved',
            'approved_at': datetime.now().isoformat(),
            'workflow_execution_id': context['id']
        }
        
        return {
            'success': True,
            'result': approval,
            'executed_at': datetime.now().isoformat()
        }
    
    def execute_wait_step(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute wait/delay step"""
        
        duration = config.get('duration', 0)  # in seconds
        reason = config.get('reason', 'Workflow delay')
        
        # In a real implementation, this would schedule the workflow to resume later
        # For demo purposes, we'll just log the wait
        
        wait_result = {
            'duration': duration,
            'reason': reason,
            'waited_at': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'result': wait_result,
            'executed_at': datetime.now().isoformat()
        }
    
    def execute_condition_step(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute conditional logic step"""
        
        condition = config.get('condition', '')
        true_action = config.get('true_action', {})
        false_action = config.get('false_action', {})
        
        # Evaluate condition (simplified for demo)
        condition_result = self.evaluate_condition(condition, context)
        
        # Execute appropriate action
        if condition_result:
            action_result = true_action
        else:
            action_result = false_action
        
        return {
            'success': True,
            'result': {
                'condition': condition,
                'evaluation': condition_result,
                'action_taken': action_result
            },
            'executed_at': datetime.now().isoformat()
        }
    
    def evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a condition string"""
        
        # Simplified condition evaluation
        # In a real implementation, this would be more sophisticated
        
        variables = context.get('variables', {})
        trigger_data = context.get('trigger_data', {})
        
        # Replace variables in condition
        processed_condition = self.replace_variables(condition, context)
        
        # For demo, return True for most conditions
        return True
    
    def replace_variables(self, text: str, context: Dict[str, Any]) -> str:
        """Replace variables in text with actual values"""
        
        if not text:
            return text
        
        variables = context.get('variables', {})
        trigger_data = context.get('trigger_data', {})
        
        # Replace common variables
        replacements = {
            '{{workflow_id}}': context.get('workflow_id', ''),
            '{{execution_id}}': context.get('id', ''),
            '{{started_at}}': context.get('started_at', ''),
            **variables,
            **trigger_data
        }
        
        for key, value in replacements.items():
            text = text.replace(key, str(value))
        
        return text
    
    def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """Get the status of a workflow execution"""
        
        if execution_id in self.active_workflows:
            return self.active_workflows[execution_id]
        
        # Search in history
        for execution in self.workflow_history:
            if execution['id'] == execution_id:
                return execution
        
        return {'error': 'Workflow execution not found'}
    
    def get_active_workflows(self) -> List[Dict[str, Any]]:
        """Get all currently active workflow executions"""
        return list(self.active_workflows.values())
    
    def get_workflow_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        return self.workflow_history[-limit:]
