
import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

# Import our custom modules
from pdf_processor import PDFProcessor
from ai_analyzer import AIAnalyzer
from project_planner import ProjectPlanner
from visualization_generator import VisualizationGenerator

# Configure Streamlit page
st.set_page_config(
    page_title="ModelMate - Research to Implementation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ResearchAnalyzerApp:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.ai_analyzer = AIAnalyzer()
        self.project_planner = ProjectPlanner()
        self.viz_generator = VisualizationGenerator()
        
        # Create necessary directories
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = ['uploads', 'outputs', 'diagrams', 'reports']
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    def run(self):
        """Main application runner"""
        st.title("🧠 ModelMate - Research Paper to Implementation Plan")
        st.markdown("---")
        
        # Sidebar configuration
        self.render_sidebar()
        
        # Main content area
        if 'analysis_complete' not in st.session_state:
            st.session_state.analysis_complete = False
        
        # Upload and analysis section
        self.render_upload_section()
        
        # Results section
        if st.session_state.analysis_complete:
            self.render_results_section()
    
    def render_sidebar(self):
        """Render sidebar with configuration options"""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # API Key input
            api_key = st.text_input(
                "Together.AI API Key",
                type="password",
                help="Enter your Together.AI API key"
            )
            
            if api_key:
                os.environ['TOGETHER_API_KEY'] = api_key
                st.success("✅ API Key configured")
            
            # Model selection
            model_options = [
                "meta-llama/Llama-3-8b-chat-hf",
                "meta-llama/Llama-3-70b-chat-hf",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "Qwen/Qwen2-72B-Instruct"
            ]
            
            selected_model = st.selectbox(
                "Select AI Model",
                model_options,
                index=0
            )
            
            st.session_state.selected_model = selected_model
            
            # Project settings
            st.header("📋 Project Settings")
            
            project_duration = st.slider(
                "Project Duration (months)",
                min_value=6,
                max_value=36,
                value=20,
                step=1
            )
            
            team_size = st.slider(
                "Estimated Team Size",
                min_value=1,
                max_value=20,
                value=5,
                step=1
            )
            
            complexity_level = st.select_slider(
                "Project Complexity",
                options=["Beginner", "Intermediate", "Advanced", "Expert"],
                value="Intermediate"
            )
            
            st.session_state.project_settings = {
                'duration': project_duration,
                'team_size': team_size,
                'complexity': complexity_level
            }
    
    def render_upload_section(self):
        """Render file upload and analysis section"""
        st.header("📄 Upload Research Paper")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a research paper in PDF format for analysis"
        )
        
        if uploaded_file is not None:
            # Display file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.2f} KB",
                "File type": uploaded_file.type
            }
            
            st.write("📊 **File Information:**")
            for key, value in file_details.items():
                st.write(f"- **{key}:** {value}")
            
            # Save uploaded file
            upload_path = f"uploads/{uploaded_file.name}"
            with open(upload_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Analysis button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Analyze Paper & Generate Project Plan", use_container_width=True):
                    self.analyze_paper(upload_path, uploaded_file.name)
    
    def analyze_paper(self, file_path, filename):
        """Analyze the uploaded paper and generate project plan"""
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Extract text from PDF
            status_text.text("📖 Extracting text from PDF...")
            progress_bar.progress(20)
            
            extracted_text = self.pdf_processor.extract_text(file_path)
            
            if not extracted_text.strip():
                st.error("❌ Could not extract text from the PDF. Please ensure the file is readable.")
                return
            
            # Step 2: Analyze with AI
            status_text.text("🧠 Analyzing paper with AI...")
            progress_bar.progress(40)
            
            paper_analysis = self.ai_analyzer.analyze_paper(extracted_text)
            
            # Step 3: Generate project plan
            status_text.text("📋 Generating project implementation plan...")
            progress_bar.progress(60)
            
            project_plan = self.project_planner.generate_plan(
                paper_analysis, 
                st.session_state.project_settings
            )
            
            # Step 4: Generate visualizations
            status_text.text("📊 Creating workflow diagrams...")
            progress_bar.progress(80)
            
            diagrams = self.viz_generator.generate_diagrams(project_plan)
            
            # Step 5: Save results
            status_text.text("💾 Saving results...")
            progress_bar.progress(100)
            
            # Store results in session state
            st.session_state.paper_analysis = paper_analysis
            st.session_state.project_plan = project_plan
            st.session_state.diagrams = diagrams
            st.session_state.filename = filename
            st.session_state.analysis_complete = True
            
            status_text.text("✅ Analysis complete!")
            st.success("🎉 Project implementation plan generated successfully!")
            
            # Auto-refresh to show results
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            progress_bar.empty()
            status_text.empty()
    
    def render_results_section(self):
        """Render the analysis results and project plan"""
        st.header("📊 Analysis Results")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📄 Paper Overview", 
            "🗺️ Project Roadmap", 
            "📋 Implementation Plan", 
            "📊 Workflow Diagrams", 
            "📥 Downloads"
        ])
        
        with tab1:
            self.render_paper_overview()
        
        with tab2:
            self.render_project_roadmap()
        
        with tab3:
            self.render_implementation_plan()
        
        with tab4:
            self.render_workflow_diagrams()
        
        with tab5:
            self.render_downloads()
    
    def render_paper_overview(self):
        """Render paper analysis overview"""
        if 'paper_analysis' in st.session_state:
            analysis = st.session_state.paper_analysis
            
            st.subheader("📑 Paper Summary")
            
            # Basic information
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Title:**", analysis.get('title', 'N/A'))
                st.write("**Authors:**", analysis.get('authors', 'N/A'))
                st.write("**Domain:**", analysis.get('domain', 'N/A'))
            
            with col2:
                st.write("**Publication Year:**", analysis.get('year', 'N/A'))
                st.write("**Research Type:**", analysis.get('research_type', 'N/A'))
                st.write("**Complexity Level:**", analysis.get('complexity', 'N/A'))
            
            # Abstract/Summary
            st.subheader("📝 Abstract")
            st.write(analysis.get('abstract', 'No abstract available'))
            
            # Key concepts
            st.subheader("🔑 Key Concepts")
            key_concepts = analysis.get('key_concepts', [])
            if key_concepts:
                for i, concept in enumerate(key_concepts, 1):
                    st.write(f"{i}. {concept}")
            
            # Technical requirements
            st.subheader("⚙️ Technical Requirements")
            tech_requirements = analysis.get('technical_requirements', {})
            if tech_requirements:
                for category, items in tech_requirements.items():
                    st.write(f"**{category.title()}:**")
                    for item in items:
                        st.write(f"- {item}")
    
    def render_project_roadmap(self):
        """Render project roadmap"""
        if 'project_plan' in st.session_state:
            plan = st.session_state.project_plan
            
            st.subheader("🗺️ Project Implementation Roadmap")
            
            # Timeline overview
            phases = plan.get('phases', [])
            
            # Create timeline visualization
            timeline_data = []
            for i, phase in enumerate(phases):
                timeline_data.append({
                    'Phase': f"Phase {i+1}",
                    'Name': phase.get('name', ''),
                    'Duration': phase.get('duration', ''),
                    'Start Month': phase.get('start_month', 0),
                    'End Month': phase.get('end_month', 0)
                })
            
            if timeline_data:
                df = pd.DataFrame(timeline_data)
                st.dataframe(df, use_container_width=True)
            
            # Detailed phases
            st.subheader("📋 Phase Details")
            
            for i, phase in enumerate(phases, 1):
                with st.expander(f"Phase {i}: {phase.get('name', 'Unnamed Phase')}"):
                    st.write(f"**Duration:** {phase.get('duration', 'N/A')}")
                    st.write(f"**Objectives:** {phase.get('objectives', 'N/A')}")
                    
                    # Key tasks
                    st.write("**Key Tasks:**")
                    tasks = phase.get('tasks', [])
                    for task in tasks:
                        st.write(f"- {task}")
                    
                    # Deliverables
                    st.write("**Deliverables:**")
                    deliverables = phase.get('deliverables', [])
                    for deliverable in deliverables:
                        st.write(f"- {deliverable}")
                    
                    # Success criteria
                    st.write("**Success Criteria:**")
                    criteria = phase.get('success_criteria', [])
                    for criterion in criteria:
                        st.write(f"- {criterion}")
    
    def render_implementation_plan(self):
        """Render detailed implementation plan"""
        if 'project_plan' in st.session_state:
            plan = st.session_state.project_plan
            
            st.subheader("📋 Technical Implementation Details")
            
            # Technical stack
            tech_stack = plan.get('technical_stack', {})
            if tech_stack:
                st.write("**Programming Stack:**")
                for category, items in tech_stack.items():
                    st.write(f"- **{category.title()}:** {', '.join(items) if isinstance(items, list) else items}")
            
            # Architecture
            architecture = plan.get('architecture', {})
            if architecture:
                st.subheader("🏗️ System Architecture")
                for component, description in architecture.items():
                    st.write(f"**{component.title()}:** {description}")
            
            # Resource requirements
            resources = plan.get('resources', {})
            if resources:
                st.subheader("💻 Resource Requirements")
                for resource_type, details in resources.items():
                    st.write(f"**{resource_type.title()}:** {details}")
            
            # Risk mitigation
            risks = plan.get('risks', [])
            if risks:
                st.subheader("⚠️ Risk Mitigation")
                for risk in risks:
                    st.write(f"- **Risk:** {risk.get('risk', '')}")
                    st.write(f"  **Mitigation:** {risk.get('mitigation', '')}")
    
    def render_workflow_diagrams(self):
        """Render workflow diagrams"""
        if 'diagrams' in st.session_state:
            diagrams = st.session_state.diagrams
            
            st.subheader("📊 Project Workflow Diagrams")
            
            # Display each diagram
            for diagram_name, diagram_content in diagrams.items():
                st.write(f"**{diagram_name.replace('_', ' ').title()}**")
                
                if diagram_name.endswith('.md'):
                    # Mermaid diagram
                    st.code(diagram_content, language='mermaid')
                else:
                    # Other diagram types
                    st.text_area(
                        f"{diagram_name} content",
                        diagram_content,
                        height=200
                    )
    
    def render_downloads(self):
        """Render download options"""
        st.subheader("📥 Download Generated Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Download Project Plan (PDF)", use_container_width=True):
                self.generate_pdf_report()
        
        with col2:
            if st.button("📊 Download Diagrams (ZIP)", use_container_width=True):
                self.generate_diagrams_zip()
        
        with col3:
            if st.button("📋 Download Implementation Guide (MD)", use_container_width=True):
                self.generate_markdown_report()
    
    def generate_pdf_report(self):
        """Generate PDF report"""
        st.info("📄 PDF generation feature coming soon!")
    
    def generate_diagrams_zip(self):
        """Generate ZIP file with all diagrams"""
        st.info("📊 Diagram ZIP generation feature coming soon!")
    
    def generate_markdown_report(self):
        """Generate Markdown report"""
        if 'project_plan' in st.session_state:
            report_content = self.project_planner.generate_markdown_report(
                st.session_state.project_plan,
                st.session_state.paper_analysis
            )
            
            # Create download button
            st.download_button(
                label="📋 Download Implementation Guide",
                data=report_content,
                file_name=f"implementation_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )


def main():
    """Main application entry point"""
    app = ResearchAnalyzerApp()
    app.run()


if __name__ == "__main__":
    main()
