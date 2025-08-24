"""
Data models for circuit analysis.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class CircuitComponent(BaseModel):
    """Represents a circuit component."""
    name: str = Field(..., description="Component name/type")
    value: str = Field(..., description="Component value/rating")
    position: Optional[str] = Field(None, description="Position in circuit")
    properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional properties")

class CircuitAnalysis(BaseModel):
    """Complete circuit analysis result."""
    circuit_type: str = Field(..., description="Type of circuit identified")
    components: List[CircuitComponent] = Field(..., description="List of circuit components")
    analysis_summary: str = Field(..., description="Summary of circuit analysis")
    calculations: List[str] = Field(..., description="Step-by-step calculations")
    solution: str = Field(..., description="Final solution or answer")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Confidence in analysis (0-1)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AnalysisRequest(BaseModel):
    """Request for circuit analysis."""
    image_data: bytes = Field(..., description="Circuit image data")
    additional_context: Optional[str] = Field(None, description="Additional context or specific question")
    analysis_depth: str = Field(default="comprehensive", description="Depth of analysis required")

class AnalysisResponse(BaseModel):
    """Response from circuit analysis."""
    success: bool = Field(..., description="Whether analysis was successful")
    analysis: Optional[CircuitAnalysis] = Field(None, description="Circuit analysis result")
    error_message: Optional[str] = Field(None, description="Error message if analysis failed")
    processing_time: float = Field(..., description="Time taken for analysis in seconds")
    enhancement_info: Optional[Dict[str, Any]] = Field(None, description="Image enhancement information")
    validation_results: Optional[Dict[str, Any]] = Field(None, description="Validation results and confidence adjustments")
