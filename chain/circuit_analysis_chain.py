"""
Circuit analysis chain that orchestrates the analysis workflow.
"""
import asyncio
from typing import Optional
from models.circuit_analysis import AnalysisRequest, AnalysisResponse
from services.gemini_service import GeminiService
from config.settings import settings
from utils.image_enhancement import auto_enhance_circuit_image
from utils.validation_engine import CircuitValidationEngine

class CircuitAnalysisChain:
    """Main chain for circuit analysis workflow."""
    
    def __init__(self):
        """Initialize the analysis chain."""
        self.gemini_service = GeminiService()
        self.validation_engine = CircuitValidationEngine()
    
    async def execute_analysis(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Execute the complete circuit analysis workflow.
        
        This follows a simplified chain approach:
        1. Image validation and preprocessing
        2. Circuit analysis via Gemini
        3. Result validation and formatting
        """
        try:
            # Step 1: Validate request
            if not self._validate_request(request):
                return AnalysisResponse(
                    success=False,
                    error_message="Invalid request: Image data is required",
                    processing_time=0.0
                )
            
            # Step 2: Auto-enhance image if needed
            enhanced_image, enhancement_info = auto_enhance_circuit_image(request.image_data)
            
            # Step 3: Execute analysis with enhanced image
            enhanced_request = AnalysisRequest(
                image_data=enhanced_image,
                additional_context=request.additional_context,
                analysis_depth=request.analysis_depth
            )
            
            response = await self.gemini_service.analyze_circuit(enhanced_request)
            
            # Step 4: Post-process results if successful
            if response.success and response.analysis:
                response.analysis = self._enhance_analysis(response.analysis)
                
                # Step 5: Validate results for accuracy
                validation_results = self.validation_engine.validate_analysis(response.analysis)
                response.validation_results = validation_results
                
                # Adjust confidence based on validation
                if validation_results['confidence_adjustment'] != 0:
                    response.analysis.confidence_level = max(0.0, min(1.0, 
                        response.analysis.confidence_level + validation_results['confidence_adjustment']))
                
                # Add enhancement information to response
                response.enhancement_info = enhancement_info
            
            return response
            
        except Exception as e:
            return AnalysisResponse(
                success=False,
                error_message=f"Chain execution failed: {str(e)}",
                processing_time=0.0
            )
    
    def _validate_request(self, request: AnalysisRequest) -> bool:
        """Validate the analysis request."""
        if not request.image_data:
            return False
        
        # Check image size
        if len(request.image_data) > settings.MAX_IMAGE_SIZE:
            return False
        
        return True
    
    def _enhance_analysis(self, analysis) -> 'CircuitAnalysis':
        """Enhance the analysis results with additional processing."""
        # Note: We can't add new fields to the Pydantic model
        # The confidence_level is already available as a float (0.0-1.0)
        # The timestamp is already available as a datetime object
        
        return analysis
    
    def test_chain(self) -> bool:
        """Test the analysis chain."""
        try:
            return self.gemini_service.test_connection()
        except Exception:
            return False



