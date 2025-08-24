"""
Configuration settings for the Circuit Solving Agent.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to get API key from Streamlit secrets first, then environment variables
try:
    import streamlit as st
    if hasattr(st, 'secrets') and st.secrets.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    elif not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "AIzaSyD8CIHYtHlL6z6yeoiOoo0pOx9Asn_7FFc"
except ImportError:
    # If not running in Streamlit, use environment variables
    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "AIzaSyD8CIHYtHlL6z6yeoiOoo0pOx9Asn_7FFc"

class Settings:
    """Application settings and configuration."""
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    
    # Application Configuration
    APP_TITLE: str = "Circuit Solving Agent"
    APP_DESCRIPTION: str = "AI-powered circuit analysis and problem solving"
    
    # Image Processing
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FORMATS: list = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    
    # Analysis Configuration
    ANALYSIS_PROMPT_TEMPLATE: str = """
    You are an expert electrical engineer and circuit analyst with extensive experience in analyzing various types of circuit images, including blurry photos and handwritten diagrams.
    
    Analyze the uploaded circuit image and provide a comprehensive solution. Pay special attention to:
    
    **For Blurry Images:**
    - Use pattern recognition to identify circuit elements even when details are unclear
    - Look for characteristic shapes and arrangements of components
    - Infer component values from context and typical circuit configurations
    - Consider multiple interpretations and provide confidence levels
    
    **For Handwritten Circuits:**
    - Recognize hand-drawn symbols and their electrical meanings
    - Interpret handwritten text and component labels
    - Understand informal circuit notation and abbreviations
    - Look for common circuit patterns in educational or prototyping contexts
    
    **IMPORTANT: Answer Format**
    - Provide a CLEAR, DIRECT ANSWER at the end of your analysis
    - The answer should be a single, concise sentence or paragraph
    - Do NOT use phrases like "Final Answer:" or "Solution:" - just give the answer directly
    - Make the answer easy to understand for students
    
    **Standard Analysis Steps:**
    1. **Circuit Identification**: Identify the type of circuit and its components
    2. **Component Analysis**: List all components with their values/ratings (estimate if unclear)
    3. **Circuit Analysis**: Perform necessary calculations (voltage, current, resistance, etc.)
    4. **Problem Solving**: If there's a specific problem, solve it step by step
    5. **Verification**: Verify your solution and provide confidence level
    6. **Quality Assessment**: Note any uncertainties due to image quality and suggest improvements
    7. **ANSWER**: Provide a clear, direct answer to the problem
    
    Present your analysis in a clear, structured format suitable for engineering students.
    Use proper electrical engineering terminology and show all calculations.
    If any part is unclear due to image quality, clearly state your assumptions and confidence level.
    """
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            return False
        return True

# Global settings instance
settings = Settings()
