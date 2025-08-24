"""
Gemini API service for circuit analysis.
"""
import time
import base64
from typing import Optional, Tuple
import google.generativeai as genai
from PIL import Image
import io

from config.settings import settings
from models.circuit_analysis import AnalysisRequest, AnalysisResponse, CircuitAnalysis

class GeminiService:
    """Service for interacting with Gemini API for circuit analysis."""
    
    def __init__(self):
        """Initialize Gemini service."""
        if not settings.validate_config():
            raise ValueError("Gemini API key not configured")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use the correct model name format
        model_name = settings.GEMINI_MODEL
        if not model_name.startswith('models/'):
            model_name = f'models/{model_name}'
        self.model = genai.GenerativeModel(model_name)
        
    def _prepare_image(self, image_data: bytes) -> Image.Image:
        """Prepare image for Gemini API."""
        try:
            image = Image.open(io.BytesIO(image_data))
            return image
        except Exception as e:
            raise ValueError(f"Invalid image format: {str(e)}")
    
    def _extract_analysis_from_response(self, response: str) -> CircuitAnalysis:
        """Extract structured analysis from Gemini response."""
        # This is a simplified parser - in production, you might want more sophisticated parsing
        # or use Gemini's structured output capabilities
        
        # Default values
        circuit_type = "Unknown Circuit"
        components = []
        analysis_summary = response
        calculations = []
        solution = "Analysis completed"
        confidence_level = 0.8
        
        # Try to extract structured information
        lines = response.split('\n')
        current_section = ""
        solution_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if "circuit" in line.lower() and ("type" in line.lower() or "identification" in line.lower()):
                current_section = "circuit_type"
            elif "component" in line.lower():
                current_section = "components"
            elif "calculation" in line.lower():
                current_section = "calculations"
            elif any(keyword in line.lower() for keyword in ["solution", "answer", "final", "result"]):
                current_section = "solution"
            elif "confidence" in line.lower():
                current_section = "confidence"
            
            # Extract information based on current section
            if current_section == "circuit_type" and ":" in line:
                circuit_type = line.split(":", 1)[1].strip()
            elif current_section == "calculations" and line and not line.startswith('#'):
                calculations.append(line)
            elif current_section == "solution":
                # Collect all solution lines
                if line and not line.startswith('#'):
                    # Clean up markdown formatting
                    clean_line = line.replace('**', '').replace('*', '').replace('`', '')
                    if clean_line.strip():
                        solution_lines.append(clean_line)
        
        # Combine solution lines and clean up
        if solution_lines:
            solution = ' '.join(solution_lines)
            # Remove common prefixes like "Final Answer:", "Solution:", etc.
            for prefix in ["final answer:", "solution:", "answer:", "result:"]:
                if solution.lower().startswith(prefix):
                    solution = solution[len(prefix):].strip()
                    break
        
        return CircuitAnalysis(
            circuit_type=circuit_type,
            components=components,
            analysis_summary=analysis_summary,
            calculations=calculations,
            solution=solution,
            confidence_level=confidence_level
        )
    
    async def analyze_circuit(self, request: AnalysisRequest) -> AnalysisResponse:
        """Analyze circuit image using Gemini API."""
        start_time = time.time()
        
        try:
            # Prepare image
            image = self._prepare_image(request.image_data)
            
            # Prepare prompt
            prompt = settings.ANALYSIS_PROMPT_TEMPLATE
            if request.additional_context:
                prompt += f"\n\nAdditional Context: {request.additional_context}"
            
            # Generate response from Gemini
            try:
                response = self.model.generate_content([prompt, image])
            except Exception as e:
                print(f"Image analysis error: {e}")
                # Try with a different model if the first one fails
                try:
                    fallback_model = genai.GenerativeModel("models/gemini-1.5-flash")
                    response = fallback_model.generate_content([prompt, image])
                except Exception as e2:
                    print(f"Fallback model also failed: {e2}")
                    raise e
            
            if not response.text:
                return AnalysisResponse(
                    success=False,
                    error_message="No response generated from Gemini API",
                    processing_time=time.time() - start_time
                )
            
            # Extract structured analysis
            analysis = self._extract_analysis_from_response(response.text)
            
            return AnalysisResponse(
                success=True,
                analysis=analysis,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            return AnalysisResponse(
                success=False,
                error_message=f"Analysis failed: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    def test_connection(self) -> bool:
        """Test Gemini API connection."""
        try:
            # Simple test with text generation
            test_model = genai.GenerativeModel("models/gemini-1.5-pro")
            response = test_model.generate_content("Hello")
            return response.text is not None
        except Exception as e:
            print(f"Connection test error: {e}")
            return False
