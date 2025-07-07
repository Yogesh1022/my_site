
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

class ProjectPlanner:
    """Generates detailed project implementation plans from research analysis"""
    
    def __init__(self):
        self.phase_templates = self._load_phase_templates()
    
    def generate_plan(self, paper_analysis: Dict[str, Any], project_settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive project implementation plan
        
        Args:
            paper_analysis: Analysis results from AI
            project_settings: Project configuration settings
            
        Returns:
            Complete project implementation plan
        """
        # Extract domain and complexity
        domain = paper_analysis.get('domain', 'Computer Science')
        complexity = paper_analysis.get('complexity', 'Intermediate')
        duration = project_settings.get('duration', 20)
        team_size = project_settings.get('team_size', 5)
        
        # Generate phases based on domain and complexity
        phases = self._generate_phases(paper_analysis, duration, complexity)
        
        # Create technical stack
        tech_stack = self._generate_tech_stack(paper_analysis)
        
        # Generate architecture
        architecture = self._generate_architecture(paper_analysis)
        
        # Create resource requirements
        resources = self._generate_resource_requirements(paper_analysis, team_size)
        
        # Generate risks and mitigation
        risks = self._generate_risks(paper_analysis, complexity)
        
        # Create success metrics
        metrics = self._generate_success_metrics(paper_analysis)
        
        project_plan = {
            "project_overview": {
                "title": f"{paper_analysis.get('title', 'Research Implementation')} - Project Plan",
                "domain": domain,
                "complexity": complexity,
                "estimated_duration": f"{duration} months",
                "team_size": team_size,
                "generated_date": datetime.now().isoformat()
            },
            "phases": phases,
            "technical_stack": tech_stack,
            "architecture": architecture,
            "resources": resources,
            "risks": risks,
            "success_metrics": metrics,
            "timeline": self._generate_timeline(phases)
        }
        
        return project_plan
    
    def _load_phase_templates(self) -> Dict[str, Any]:
        """Load phase templates for different domains"""
        return {
            "NLP": [
                {
                    "name": "Foundation and Setup",
                    "base_duration": 3,
                    "objectives": "Establish theoretical understanding and development environment",
                    "core_tasks": [
                        "Set up development environment",
                        "Literature review",
                        "Dataset preparation",
                        "Basic NLP understanding"
                    ]
                },
                {
                    "name": "Core Component Development",
                    "base_duration": 6,
                    "objectives": "Build fundamental NLP processing capabilities",
                    "core_tasks": [
                        "Text preprocessing pipeline",
                        "Basic NLP models",
                        "Feature extraction",
                        "Initial testing"
                    ]
                },
                {
                    "name": "Advanced Implementation",
                    "base_duration": 4,
                    "objectives": "Implement state-of-the-art approaches",
                    "core_tasks": [
                        "Neural network implementation",
                        "Advanced model training",
                        "Optimization",
                        "Performance tuning"
                    ]
                },
                {
                    "name": "Application Development",
                    "base_duration": 4,
                    "objectives": "Create practical applications",
                    "core_tasks": [
                        "User interface development",
                        "Application logic",
                        "Integration testing",
                        "User experience optimization"
                    ]
                },
                {
                    "name": "Evaluation and Deployment",
                    "base_duration": 3,
                    "objectives": "Testing, optimization, and deployment",
                    "core_tasks": [
                        "Comprehensive evaluation",
                        "Performance optimization",
                        "Documentation",
                        "Deployment"
                    ]
                }
            ],
            "Computer Vision": [
                {
                    "name": "Environment and Data Setup",
                    "base_duration": 3,
                    "objectives": "Prepare development environment and datasets",
                    "core_tasks": [
                        "Development environment setup",
                        "Image dataset collection",
                        "Data preprocessing",
                        "Baseline model research"
                    ]
                },
                {
                    "name": "Model Development",
                    "base_duration": 6,
                    "objectives": "Implement core computer vision models",
                    "core_tasks": [
                        "Image preprocessing pipeline",
                        "CNN architecture implementation",
                        "Model training",
                        "Initial evaluation"
                    ]
                },
                {
                    "name": "Advanced Techniques",
                    "base_duration": 4,
                    "objectives": "Implement advanced computer vision techniques",
                    "core_tasks": [
                        "Transfer learning",
                        "Data augmentation",
                        "Advanced architectures",
                        "Performance optimization"
                    ]
                },
                {
                    "name": "Application Integration",
                    "base_duration": 4,
                    "objectives": "Build practical applications",
                    "core_tasks": [
                        "Real-time processing",
                        "User interface",
                        "API development",
                        "System integration"
                    ]
                },
                {
                    "name": "Testing and Deployment",
                    "base_duration": 3,
                    "objectives": "Final testing and deployment",
                    "core_tasks": [
                        "Performance testing",
                        "User acceptance testing",
                        "Production deployment",
                        "Monitoring setup"
                    ]
                }
            ],
            "Machine Learning": [
                {
                    "name": "Data and Environment Preparation",
                    "base_duration": 3,
                    "objectives": "Setup and data understanding",
                    "core_tasks": [
                        "Environment configuration",
                        "Data collection and exploration",
                        "Feature engineering",
                        "Data quality assessment"
                    ]
                },
                {
                    "name": "Model Development",
                    "base_duration": 6,
                    "objectives": "Develop and train ML models",
                    "core_tasks": [
                        "Algorithm selection",
                        "Model implementation",
                        "Training and validation",
                        "Hyperparameter tuning"
                    ]
                },
                {
                    "name": "Advanced Modeling",
                    "base_duration": 4,
                    "objectives": "Implement advanced ML techniques",
                    "core_tasks": [
                        "Ensemble methods",
                        "Deep learning integration",
                        "Model optimization",
                        "Cross-validation"
                    ]
                },
                {
                    "name": "System Integration",
                    "base_duration": 4,
                    "objectives": "Build production system",
                    "core_tasks": [
                        "API development",
                        "Database integration",
                        "Real-time prediction",
                        "System architecture"
                    ]
                },
                {
                    "name": "Production and Monitoring",
                    "base_duration": 3,
                    "objectives": "Deploy and monitor system",
                    "core_tasks": [
                        "Production deployment",
                        "Performance monitoring",
                        "Model maintenance",
                        "Documentation"
                    ]
                }
            ]
        }
    
    def _generate_phases(self, analysis: Dict[str, Any], duration: int, complexity: str) -> List[Dict[str, Any]]:
        """Generate project phases based on analysis"""
        domain = analysis.get('domain', 'Machine Learning')
        
        # Get appropriate template
        if 'NLP' in domain.upper() or 'NATURAL LANGUAGE' in domain.upper():
            template_key = 'NLP'
        elif 'VISION' in domain.upper() or 'IMAGE' in domain.upper():
            template_key = 'Computer Vision'
        else:
            template_key = 'Machine Learning'
        
        base_phases = self.phase_templates.get(template_key, self.phase_templates['Machine Learning'])
        
        # Adjust durations based on complexity and total duration
        complexity_multiplier = {
            'Beginner': 0.8,
            'Intermediate': 1.0,
            'Advanced': 1.3,
            'Expert': 1.6
        }.get(complexity, 1.0)
        
        # Calculate phase durations
        total_base_duration = sum(phase['base_duration'] for phase in base_phases)
        duration_multiplier = duration / total_base_duration
        
        phases = []
        current_month = 1
        
        for i, phase_template in enumerate(base_phases):
            adjusted_duration = max(1, round(
                phase_template['base_duration'] * duration_multiplier * complexity_multiplier
            ))
            
            # Customize tasks based on analysis
            customized_tasks = self._customize_phase_tasks(
                phase_template['core_tasks'], 
                analysis, 
                phase_template['name']
            )
            
            phase = {
                "name": phase_template['name'],
                "duration": f"{adjusted_duration} months",
                "start_month": current_month,
                "end_month": current_month + adjusted_duration - 1,
                "objectives": phase_template['objectives'],
                "tasks": customized_tasks,
                "deliverables": self._generate_phase_deliverables(phase_template['name'], analysis),
                "success_criteria": self._generate_success_criteria(phase_template['name'], analysis)
            }
            
            phases.append(phase)
            current_month += adjusted_duration
        
        return phases
    
    def _customize_phase_tasks(self, base_tasks: List[str], analysis: Dict[str, Any], phase_name: str) -> List[str]:
        """Customize phase tasks based on paper analysis"""
        customized_tasks = base_tasks.copy()
        
        # Add domain-specific tasks
        key_concepts = analysis.get('key_concepts', [])
        tech_requirements = analysis.get('technical_requirements', {})
        
        # Add concept-specific tasks
        for concept in key_concepts[:3]:  # Top 3 concepts
            if concept.lower() not in ' '.join(customized_tasks).lower():
                customized_tasks.append(f"Implement {concept} functionality")
        
        # Add framework-specific tasks
        frameworks = tech_requirements.get('frameworks', [])
        for framework in frameworks[:2]:  # Top 2 frameworks
            if framework.lower() not in ' '.join(customized_tasks).lower():
                customized_tasks.append(f"Integrate {framework} framework")
        
        return customized_tasks
    
    def _generate_phase_deliverables(self, phase_name: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate deliverables for each phase"""
        base_deliverables = {
            "Foundation and Setup": [
                "Development environment setup",
                "Literature review document",
                "Dataset preparation report",
                "Technical specification document"
            ],
            "Core Component Development": [
                "Core processing pipeline",
                "Basic model implementations",
                "Initial testing results",
                "Performance baseline report"
            ],
            "Advanced Implementation": [
                "Advanced model implementations",
                "Optimization results",
                "Performance improvement report",
                "Technical documentation"
            ],
            "Application Development": [
                "User interface prototype",
                "Application backend",
                "Integration testing report",
                "User documentation"
            ],
            "Evaluation and Deployment": [
                "Final evaluation report",
                "Optimized production system",
                "Deployment documentation",
                "User manual"
            ]
        }
        
        # Get base deliverables for phase
        deliverables = base_deliverables.get(phase_name, ["Phase deliverables"])
        
        # Add domain-specific deliverables
        domain = analysis.get('domain', '')
        if 'NLP' in domain.upper():
            if 'Core' in phase_name:
                deliverables.append("Text preprocessing pipeline")
                deliverables.append("Language model implementation")
        elif 'Vision' in domain.upper():
            if 'Core' in phase_name:
                deliverables.append("Image preprocessing pipeline")
                deliverables.append("Computer vision model")
        
        return deliverables
    
    def _generate_success_criteria(self, phase_name: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate success criteria for each phase"""
        base_criteria = {
            "Foundation and Setup": [
                "Functional development environment",
                "Complete dataset preparation",
                "Clear project roadmap"
            ],
            "Core Component Development": [
                "Working core components",
                "Baseline performance achieved",
                "Successful initial testing"
            ],
            "Advanced Implementation": [
                "Improved model performance",
                "Optimization targets met",
                "Advanced features implemented"
            ],
            "Application Development": [
                "Functional user interface",
                "Complete application features",
                "User acceptance testing passed"
            ],
            "Evaluation and Deployment": [
                "Performance targets achieved",
                "Successful deployment",
                "Complete documentation"
            ]
        }
        
        criteria = base_criteria.get(phase_name, ["Phase objectives met"])
        
        # Add domain-specific criteria
        complexity = analysis.get('complexity', 'Intermediate')
        if complexity == 'Advanced':
            criteria.append("Advanced performance benchmarks achieved")
        elif complexity == 'Expert':
            criteria.append("State-of-the-art performance achieved")
        
        return criteria
    
    def _generate_tech_stack(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical stack recommendations"""
        tech_requirements = analysis.get('technical_requirements', {})
        domain = analysis.get('domain', '')
        
        # Base stack
        stack = {
            "programming_languages": ["Python"],
            "core_libraries": ["NumPy", "Pandas", "Matplotlib"],
            "development_tools": ["Jupyter Notebook", "Git", "VS Code"],
            "testing": ["Pytest", "Unit Testing"],
            "deployment": ["Docker", "Flask/FastAPI"]
        }
        
        # Add domain-specific technologies
        if 'NLP' in domain.upper():
            stack["ml_frameworks"] = ["TensorFlow", "PyTorch", "Transformers (Hugging Face)"]
            stack["nlp_libraries"] = ["spaCy", "NLTK", "Gensim"]
        elif 'Vision' in domain.upper():
            stack["ml_frameworks"] = ["TensorFlow", "PyTorch", "OpenCV"]
            stack["cv_libraries"] = ["PIL", "scikit-image", "albumentations"]
        else:
            stack["ml_frameworks"] = ["Scikit-learn", "TensorFlow", "PyTorch"]
        
        # Add frameworks from analysis
        frameworks = tech_requirements.get('frameworks', [])
        if frameworks:
            if "ml_frameworks" not in stack:
                stack["ml_frameworks"] = []
            stack["ml_frameworks"].extend(frameworks[:3])
            stack["ml_frameworks"] = list(set(stack["ml_frameworks"]))  # Remove duplicates
        
        return stack
    
    def _generate_architecture(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate system architecture description"""
        domain = analysis.get('domain', '')
        
        if 'NLP' in domain.upper():
            return {
                "data_layer": "Text preprocessing and tokenization pipeline",
                "model_layer": "Neural language models and transformers",
                "application_layer": "NLP applications and APIs",
                "interface_layer": "Web interface and user interaction"
            }
        elif 'Vision' in domain.upper():
            return {
                "data_layer": "Image preprocessing and augmentation pipeline",
                "model_layer": "Convolutional neural networks and vision models",
                "application_layer": "Computer vision applications and APIs",
                "interface_layer": "Image upload interface and visualization"
            }
        else:
            return {
                "data_layer": "Data preprocessing and feature engineering",
                "model_layer": "Machine learning models and algorithms",
                "application_layer": "Prediction services and APIs",
                "interface_layer": "Dashboard and user interface"
            }
    
    def _generate_resource_requirements(self, analysis: Dict[str, Any], team_size: int) -> Dict[str, str]:
        """Generate resource requirements"""
        complexity = analysis.get('complexity', 'Intermediate')
        
        # Base requirements
        resources = {
            "team": f"{team_size} team members (developers, data scientists, researchers)",
            "development_environment": "Modern development machines with good specifications"
        }
        
        # Adjust based on complexity
        if complexity in ['Advanced', 'Expert']:
            resources["hardware"] = "GPU workstations (8GB+ VRAM), 32GB+ RAM, SSD storage"
            resources["cloud_resources"] = "Cloud GPU instances for training (AWS/GCP/Azure)"
        else:
            resources["hardware"] = "Standard development machines, GPU recommended"
            resources["cloud_resources"] = "Basic cloud services for deployment"
        
        # Add domain-specific requirements
        domain = analysis.get('domain', '')
        if 'NLP' in domain.upper():
            resources["data_storage"] = "Large text corpora and pre-trained models"
        elif 'Vision' in domain.upper():
            resources["data_storage"] = "Image datasets and pre-trained vision models"
        
        return resources
    
    def _generate_risks(self, analysis: Dict[str, Any], complexity: str) -> List[Dict[str, str]]:
        """Generate project risks and mitigation strategies"""
        base_risks = [
            {
                "risk": "Technical complexity exceeding team capabilities",
                "mitigation": "Provide comprehensive training and consider external consultants"
            },
            {
                "risk": "Data quality and availability issues",
                "mitigation": "Establish data quality checks and backup data sources"
            },
            {
                "risk": "Performance not meeting requirements",
                "mitigation": "Set realistic benchmarks and implement iterative improvements"
            },
            {
                "risk": "Timeline delays due to unforeseen challenges",
                "mitigation": "Build buffer time into schedule and prioritize core features"
            }
        ]
        
        # Add complexity-specific risks
        if complexity in ['Advanced', 'Expert']:
            base_risks.extend([
                {
                    "risk": "High computational resource requirements",
                    "mitigation": "Secure adequate cloud resources and optimize algorithms"
                },
                {
                    "risk": "Keeping up with rapidly evolving research",
                    "mitigation": "Establish continuous learning and update procedures"
                }
            ])
        
        # Add domain-specific risks
        challenges = analysis.get('challenges', [])
        for challenge in challenges[:2]:  # Top 2 challenges
            base_risks.append({
                "risk": challenge,
                "mitigation": "Implement targeted solutions and monitoring"
            })
        
        return base_risks
    
    def _generate_success_metrics(self, analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate success metrics"""
        domain = analysis.get('domain', '')
        
        metrics = {
            "technical_metrics": [
                "Model accuracy > 85%",
                "System response time < 2 seconds",
                "Code coverage > 80%",
                "Performance benchmarks achieved"
            ],
            "project_metrics": [
                "On-time delivery",
                "Budget adherence",
                "Quality standards met",
                "Stakeholder satisfaction > 4.0/5.0"
            ]
        }
        
        # Add domain-specific metrics
        if 'NLP' in domain.upper():
            metrics["technical_metrics"].extend([
                "BLEU score > 25 (for translation tasks)",
                "F1-score > 0.85 (for classification)",
                "ROUGE score > 0.7 (for summarization)"
            ])
        elif 'Vision' in domain.upper():
            metrics["technical_metrics"].extend([
                "Image classification accuracy > 90%",
                "Object detection mAP > 0.5",
                "Real-time processing capability"
            ])
        
        return metrics
    
    def _generate_timeline(self, phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate project timeline"""
        total_duration = max(phase['end_month'] for phase in phases)
        
        timeline = {
            "total_duration": f"{total_duration} months",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "estimated_end_date": (datetime.now() + timedelta(days=total_duration * 30)).strftime("%Y-%m-%d"),
            "milestones": []
        }
        
        # Generate milestones
        for phase in phases:
            timeline["milestones"].append({
                "name": f"{phase['name']} Completion",
                "month": phase['end_month'],
                "description": f"Complete {phase['name']} with all deliverables"
            })
        
        return timeline
    
    def generate_markdown_report(self, project_plan: Dict[str, Any], paper_analysis: Dict[str, Any]) -> str:
        """Generate markdown report for download"""
        report = f"""# Project Implementation Plan

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Paper Overview
- **Title:** {paper_analysis.get('title', 'N/A')}
- **Authors:** {paper_analysis.get('authors', 'N/A')}
- **Domain:** {paper_analysis.get('domain', 'N/A')}
- **Complexity:** {paper_analysis.get('complexity', 'N/A')}

## Project Summary
- **Duration:** {project_plan['project_overview']['estimated_duration']}
- **Team Size:** {project_plan['project_overview']['team_size']}
- **Domain:** {project_plan['project_overview']['domain']}

## Implementation Phases

"""
        
        # Add phases
        for i, phase in enumerate(project_plan['phases'], 1):
            report += f"""### Phase {i}: {phase['name']}
**Duration:** {phase['duration']}
**Objectives:** {phase['objectives']}

**Key Tasks:**
"""
            for task in phase['tasks']:
                report += f"- {task}\n"
            
            report += f"""
**Deliverables:**
"""
            for deliverable in phase['deliverables']:
                report += f"- {deliverable}\n"
            
            report += f"""
**Success Criteria:**
"""
            for criterion in phase['success_criteria']:
                report += f"- {criterion}\n"
            
            report += "\n"
        
        # Add technical stack
        report += """## Technical Stack

"""
        for category, items in project_plan['technical_stack'].items():
            report += f"**{category.replace('_', ' ').title()}:** {', '.join(items) if isinstance(items, list) else items}\n\n"
        
        # Add risks
        report += """## Risk Mitigation

"""
        for risk in project_plan['risks']:
            report += f"**Risk:** {risk['risk']}\n"
            report += f"**Mitigation:** {risk['mitigation']}\n\n"
        
        return report
