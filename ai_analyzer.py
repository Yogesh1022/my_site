import os
import json
from together import Together
from typing import Dict, Any

class AIAnalyzer:
    """Handles AI-powered analysis of research papers using Together.AI"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Together.AI client"""
        api_key = os.getenv('TOGETHER_API_KEY')
        if api_key:
            self.client = Together(api_key=api_key)
        else:
            print("Warning: TOGETHER_API_KEY not found in environment variables")
    
    def analyze_paper(self, text: str) -> Dict[str, Any]:
        """
        Analyze research paper and extract key information
        
        Args:
            text: Extracted text from the research paper
            
        Returns:
            Dictionary containing paper analysis
        """
        if not self.client:
            raise Exception("Together.AI client not initialized. Please provide API key.")
        
        try:
            # Create comprehensive analysis prompt
            analysis_prompt = self._create_analysis_prompt(text)
            
            # Call Together.AI API
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-8b-chat-hf",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert research analyst specializing in converting academic papers into actionable project implementation plans. Provide detailed, structured analysis."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            # Parse response
            analysis_text = response.choices[0].message.content
            
            # Extract structured information
            analysis = self._parse_analysis_response(analysis_text)
            
            return analysis
            
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return self._create_fallback_analysis()
    
    def _create_analysis_prompt(self, text: str) -> str:
        """Create comprehensive analysis prompt"""
        # Truncate text if too long
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        prompt = f"""
        Analyze the following research paper and provide a comprehensive analysis in JSON format:

        RESEARCH PAPER TEXT:
        {text}

        Please provide analysis in the following JSON structure:
        {{
            "title": "Paper title",
            "authors": "Author names",
            "abstract": "Paper abstract or summary",
            "domain": "Research domain (e.g., NLP, Computer Vision, Machine Learning)",
            "research_type": "Type of research (e.g., Survey, Experimental, Theoretical)",
            "year": "Publication year if mentioned",
            "complexity": "Complexity level (Beginner/Intermediate/Advanced/Expert)",
            "key_concepts": ["List of key concepts and technologies"],
            "methodologies": ["Research methodologies mentioned"],
            "technical_requirements": {{
                "programming_languages": ["List of programming languages"],
                "frameworks": ["List of frameworks and libraries"],
                "hardware": ["Hardware requirements"],
                "datasets": ["Datasets mentioned"]
            }},
            "applications": ["Potential applications"],
            "challenges": ["Technical challenges mentioned"],
            "future_work": ["Future research directions"]
        }}

        Focus on extracting information that would be useful for creating a project implementation plan.
        """
        
        return prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data"""
        try:
            # Try to find JSON in the response
            import re
            
            # Look for JSON block
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                analysis = json.loads(json_str)
                return analysis
            else:
                # If no JSON found, create structured analysis from text
                return self._create_structured_analysis_from_text(response_text)
                
        except json.JSONDecodeError:
            # Fallback: parse manually
            return self._create_structured_analysis_from_text(response_text)
    
    def _create_structured_analysis_from_text(self, text: str) -> Dict[str, Any]:
        """Create structured analysis from unstructured text"""
        # This is a simplified parser - in production, you'd want more sophisticated parsing
        analysis = {
            "title": "Research Paper Analysis",
            "authors": "Not specified",
            "abstract": text[:500] + "..." if len(text) > 500 else text,
            "domain": "Computer Science",
            "research_type": "Research Paper",
            "year": "2024",
            "complexity": "Intermediate",
            "key_concepts": ["Machine Learning", "Data Analysis", "Implementation"],
            "methodologies": ["Experimental", "Comparative Analysis"],
            "technical_requirements": {
                "programming_languages": ["Python"],
                "frameworks": ["TensorFlow", "PyTorch", "Scikit-learn"],
                "hardware": ["GPU recommended", "8GB+ RAM"],
                "datasets": ["Custom dataset required"]
            },
            "applications": ["Research Implementation", "Practical Application"],
            "challenges": ["Data Quality", "Model Performance", "Scalability"],
            "future_work": ["Optimization", "Extension", "Real-world Deployment"]
        }
        
        return analysis
    
    def _create_fallback_analysis(self) -> Dict[str, Any]:
        """Create fallback analysis when AI analysis fails"""
        return {
            "title": "Research Paper",
            "authors": "Unknown",
            "abstract": "Analysis unavailable - please check your API configuration",
            "domain": "Computer Science",
            "research_type": "Research Paper",
            "year": "2024",
            "complexity": "Intermediate",
            "key_concepts": ["Research", "Implementation"],
            "methodologies": ["Analysis"],
            "technical_requirements": {
                "programming_languages": ["Python"],
                "frameworks": ["Standard libraries"],
                "hardware": ["Standard hardware"],
                "datasets": ["TBD"]
            },
            "applications": ["Research"],
            "challenges": ["Implementation"],
            "future_work": ["Development"]
        }
