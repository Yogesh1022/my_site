import json
from typing import Dict, Any, List

class VisualizationGenerator:
    """Generates workflow diagrams and visualizations for project plans"""
    
    def __init__(self):
        pass
    
    def generate_diagrams(self, project_plan: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate various project diagrams
        
        Args:
            project_plan: Complete project plan
            
        Returns:
            Dictionary of diagram names and their content
        """
        diagrams = {}
        
        # Generate Gantt chart (Mermaid)
        diagrams['gantt_chart.md'] = self._generate_gantt_chart(project_plan)
        
        # Generate workflow diagram (Mermaid)
        diagrams['workflow_diagram.md'] = self._generate_workflow_diagram(project_plan)
        
        # Generate system architecture (Mermaid)
        diagrams['architecture_diagram.md'] = self._generate_architecture_diagram(project_plan)
        
        # Generate phase flowchart (Mermaid)
        diagrams['phase_flowchart.md'] = self._generate_phase_flowchart(project_plan)
        
        return diagrams
    
    def _generate_gantt_chart(self, project_plan: Dict[str, Any]) -> str:
        """Generate Mermaid Gantt chart"""
        phases = project_plan.get('phases', [])
        
        gantt = """gantt
    title Project Implementation Timeline
    dateFormat  X
    axisFormat %m
    
"""
        
        # Add sections and tasks
        current_section = None
        
        for i, phase in enumerate(phases):
            # Create section for each phase
            section_name = f"Phase {i+1}"
            gantt += f"    section {section_name}\n"
            
            # Add phase as a task
            start_month = phase.get('start_month', 1)
            end_month = phase.get('end_month', start_month + 1)
            duration = end_month - start_month + 1
            
            phase_name = phase.get('name', f'Phase {i+1}').replace(' ', '_')
            gantt += f"    {phase_name} :a{i+1}, {start_month}, {duration}\n"
            
            # Add key tasks as sub-tasks
            tasks = phase.get('tasks', [])
            for j, task in enumerate(tasks[:3]):  # Limit to first 3 tasks
                task_name = task.replace(' ', '_')[:20]  # Truncate long names
                task_duration = max(1, duration // len(tasks))
                task_start = start_month + (j * task_duration)
                gantt += f"    {task_name} :a{i+1}_{j+1}, {task_start}, {task_duration}\n"
            
            gantt += "\n"
        
        return gantt
    
    def _generate_workflow_diagram(self, project_plan: Dict[str, Any]) -> str:
        """Generate workflow diagram using Mermaid"""
        phases = project_plan.get('phases', [])
        
        workflow = """flowchart TD
    Start([Project Start]) --> Phase1
    
"""
        
        # Add phases
        for i, phase in enumerate(phases):
            phase_id = f"Phase{i+1}"
            phase_name = phase.get('name', f'Phase {i+1}')
            
            # Add phase box
            workflow += f"    {phase_id}[\"{phase_name}\"] --> "
            
            # Connect to next phase or end
            if i < len(phases) - 1:
                next_phase_id = f"Phase{i+2}"
                workflow += f"{next_phase_id}\n"
            else:
                workflow += "End([Project Complete])\n"
            
            # Add decision points for major phases
            if i == len(phases) // 2:  # Middle phase
                decision_id = f"Decision{i+1}"
                workflow += f"    {phase_id} --> {decision_id}{{Quality Check}}\n"
                workflow += f"    {decision_id} -->|Pass| Phase{i+2}\n"
                workflow += f"    {decision_id} -->|Fail| {phase_id}\n"
        
        # Add styling
        workflow += """
    classDef phaseBox fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef endpoint fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    
"""
        
        # Apply styles
        for i in range(len(phases)):
            workflow += f"    class Phase{i+1} phaseBox\n"
        
        workflow += "    class Start,End endpoint\n"
        
        return workflow
    
    def _generate_architecture_diagram(self, project_plan: Dict[str, Any]) -> str:
        """Generate system architecture diagram"""
        architecture = project_plan.get('architecture', {})
        
        arch_diagram = """graph TB
    subgraph "System Architecture"
        UI[User Interface Layer]
        API[Application Layer]
        MODEL[Model Layer]
        DATA[Data Layer]
        INFRA[Infrastructure Layer]
    end
    
    UI --> API
    API --> MODEL
    MODEL --> DATA
    API --> INFRA
    
"""
        
        # Add specific components based on architecture
        for component, description in architecture.items():
            component_id = component.upper().replace(' ', '_')
            arch_diagram += f"    {component_id}[\"{component.title()}\"]\n"
        
        # Add styling
        arch_diagram += """
    classDef layer fill:#f9f9f9,stroke:#333,stroke-width:2px
    classDef component fill:#e3f2fd,stroke:#1976d2,stroke-width:1px
    
    class UI,API,MODEL,DATA,INFRA layer
"""
        
        return arch_diagram
    
    def _generate_phase_flowchart(self, project_plan: Dict[str, Any]) -> str:
        """Generate detailed phase flowchart"""
        phases = project_plan.get('phases', [])
        
        flowchart = """flowchart LR
    subgraph "Project Implementation Flow"
        Start([Start])
"""
        
        # Add phases with internal structure
        for i, phase in enumerate(phases):
            phase_id = f"P{i+1}"
            phase_name = phase.get('name', f'Phase {i+1}')
            
            # Create subgraph for each phase
            flowchart += f"""        
        subgraph "{phase_name}"
            {phase_id}_Start([Begin]) --> {phase_id}_Plan[Planning]
            {phase_id}_Plan --> {phase_id}_Exec[Execution]
            {phase_id}_Exec --> {phase_id}_Review[Review]
            {phase_id}_Review --> {phase_id}_End([Complete])
        end
"""
        
        # Connect phases
        flowchart += "\n        Start --> P1_Start\n"
        for i in range(len(phases) - 1):
            flowchart += f"        P{i+1}_End --> P{i+2}_Start\n"
        
        flowchart += f"        P{len(phases)}_End --> Finish([Project Complete])\n"
        flowchart += "    end"
        
        return flowchart
    
    def generate_html_report(self, project_plan: Dict[str, Any], diagrams: Dict[str, str]) -> str:
        """Generate HTML report with embedded diagrams"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Project Implementation Plan</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .diagram {{ margin: 20px 0; }}
        .phase {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
    </style>
</head>
<body>
    <h1>Project Implementation Plan</h1>
    
    <h2>Project Timeline</h2>
    <div class="diagram mermaid">
{diagrams.get('gantt_chart.md', '')}
    </div>
    
    <h2>Workflow Diagram</h2>
    <div class="diagram mermaid">
{diagrams.get('workflow_diagram.md', '')}
    </div>
    
    <h2>System Architecture</h2>
    <div class="diagram mermaid">
{diagrams.get('architecture_diagram.md', '')}
    </div>
    
    <h2>Implementation Phases</h2>
"""
        
        # Add phase details
        phases = project_plan.get('phases', [])
        for i, phase in enumerate(phases, 1):
            html += f"""
    <div class="phase">
        <h3>Phase {i}: {phase.get('name', '')}</h3>
        <p><strong>Duration:</strong> {phase.get('duration', '')}</p>
        <p><strong>Objectives:</strong> {phase.get('objectives', '')}</p>
        <h4>Key Tasks:</h4>
        <ul>
"""
            for task in phase.get('tasks', []):
                html += f"            <li>{task}</li>\n"
            
            html += """        </ul>
    </div>
"""
        
        html += """
    <script>
        mermaid.initialize({startOnLoad:true});
    </script>
</body>
</html>"""
        
        return html
