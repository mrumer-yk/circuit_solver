"""
Circuit Solving Agent - Streamlit Application
"""
import streamlit as st
import asyncio
import time
from PIL import Image
import io

# Import our modules
from config.settings import settings
from models.circuit_analysis import AnalysisRequest
from chain.circuit_analysis_chain import CircuitAnalysisChain
from utils.image_utils import validate_image_format, optimize_image_for_analysis, get_image_info
from utils.image_enhancement import auto_enhance_circuit_image, create_enhancement_comparison

# Page configuration
st.set_page_config(
    page_title=settings.APP_TITLE,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">⚡ Circuit Solving Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered circuit analysis and problem solving</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Gemini API key here"
        )
        
        if api_key:
            # Update settings
            settings.GEMINI_API_KEY = api_key
            
            # Test connection
            if st.button("Test Connection"):
                try:
                    chain = CircuitAnalysisChain()
                    if chain.test_chain():
                        st.success("✅ Connection successful!")
                    else:
                        st.error("❌ Connection failed!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Upload a clear image of your circuit
        2. Add any specific context or questions
        3. Click 'Analyze Circuit' to get results
        4. Review the comprehensive analysis
        """)
        
        st.markdown("### 📁 Supported Formats")
        st.markdown(f"**Image formats:** {', '.join(settings.SUPPORTED_FORMATS)}")
        st.markdown(f"**Max size:** {settings.MAX_IMAGE_SIZE // (1024*1024)} MB")
        
        st.markdown("---")
        st.markdown("### 🚀 Smart Features")
        st.markdown("""
        **Auto-Enhancement:**
        - Blurry photo correction
        - Handwritten circuit recognition
        - Quality improvement
        - Before/after comparison
        
        **AI Analysis:**
        - Pattern recognition
        - Component identification
        - Circuit calculations
        - Confidence scoring
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Circuit Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a circuit image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="Upload a clear image of your circuit for analysis"
        )
        
        if uploaded_file is not None:
            # Display image info
            image_data = uploaded_file.read()
            image_info = get_image_info(image_data)
            
            if 'error' not in image_info:
                st.success(f"✅ Image uploaded successfully!")
                st.info(f"""
                **Format:** {image_info['format']}  
                **Size:** {image_info['width']} × {image_info['height']} pixels  
                **File size:** {image_info['file_size_mb']:.2f} MB
                """)
                
                # Display original image
                image = Image.open(io.BytesIO(image_data))
                st.image(image, caption="Original Circuit Image", use_column_width=True)
                
                # Auto-enhance and show comparison
                with st.spinner("🔧 Enhancing image quality..."):
                    enhanced_image, enhancement_info = auto_enhance_circuit_image(image_data)
                    
                    if enhancement_info.get('enhancements_applied'):
                        st.success("✨ Image enhanced automatically!")
                        
                        # Create and show comparison
                        comparison_image = create_enhancement_comparison(image_data, enhanced_image)
                        st.image(comparison_image, caption="Original vs Enhanced", use_column_width=True)
                        
                        # Show enhancement details
                        st.info(f"""
                        **Enhancements Applied:** {', '.join(enhancement_info['enhancements_applied'])}
                        **Quality Score:** {enhancement_info.get('quality_score', 0):.2f}/1.0
                        """)
                        
                        # Store enhanced image for analysis
                        st.session_state.enhanced_image = enhanced_image
                    else:
                        st.info("✅ Image quality is good - no enhancements needed")
                        st.session_state.enhanced_image = image_data
                
                # Validate image
                is_valid, validation_msg = validate_image_format(image_data)
                if is_valid:
                    st.success(validation_msg)
                else:
                    st.error(validation_msg)
            else:
                st.error(f"❌ Error reading image: {image_info['error']}")
    
    with col2:
        st.header("🔍 Analysis Options")
        
        # Additional context
        additional_context = st.text_area(
            "Additional Context (Optional)",
            placeholder="Describe any specific problems, questions, or context about this circuit...",
            height=100,
            help="Provide additional information to help with analysis"
        )
        
        # Analysis depth
        analysis_depth = st.selectbox(
            "Analysis Depth",
            ["comprehensive", "basic", "detailed"],
            help="Choose the level of detail for the analysis"
        )
        
        # Analyze button
        if st.button("🚀 Analyze Circuit", type="primary", disabled=not uploaded_file):
            if not settings.validate_config():
                st.error("❌ Please configure your Gemini API key in the sidebar!")
                return
            
            # Show progress
            with st.spinner("🔍 Analyzing circuit..."):
                try:
                    # Use enhanced image if available, otherwise use original
                    analysis_image = st.session_state.get('enhanced_image', image_data)
                    
                    # Create analysis request
                    request = AnalysisRequest(
                        image_data=analysis_image,
                        additional_context=additional_context,
                        analysis_depth=analysis_depth
                    )
                    
                    # Execute analysis
                    chain = CircuitAnalysisChain()
                    response = asyncio.run(chain.execute_analysis(request))
                    
                    # Display results
                    if response.success:
                        display_analysis_results(response)
                    else:
                        st.error(f"❌ Analysis failed: {response.error_message}")
                        
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Built with Streamlit and Gemini AI</p>",
        unsafe_allow_html=True
    )

def display_analysis_results(response):
    """Display the analysis results in a structured format."""
    
    st.success("🎉 Circuit analysis completed successfully!")
    
    # Results header
    st.header("📊 Analysis Results")
    
    # Processing time
    st.info(f"⏱️ Processing time: {response.processing_time:.2f} seconds")
    
    analysis = response.analysis
    
    # 🎯 QUICK ANSWER AT THE VERY TOP
    st.markdown("---")
    st.markdown('<h2 style="color: #1f77b4; text-align: center;">🎯 QUICK ANSWER</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Quick answer in a prominent box
    st.markdown("""
    <div style="background-color: #e8f4fd; border: 2px solid #1f77b4; padding: 25px; margin: 20px 0; border-radius: 8px; text-align: center;">
        <h3 style="color: #1f77b4; margin-top: 0; font-size: 24px;">💡 Answer:</h3>
        <p style="font-size: 20px; line-height: 1.6; margin-bottom: 0; font-weight: 500;">{}</p>
    </div>
    """.format(analysis.solution), unsafe_allow_html=True)
    
    # Quick summary boxes
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🔌 **Circuit Type:** {analysis.circuit_type}")
    with col2:
        confidence_color = "green" if analysis.confidence_level > 0.8 else "orange" if analysis.confidence_level > 0.6 else "red"
        st.info(f"📊 **Confidence:** :{confidence_color}[{analysis.confidence_level:.1%}]")
    
    st.markdown("---")
    st.markdown('<h3 style="color: #666;">📋 Detailed Analysis</h3>', unsafe_allow_html=True)
    
    # Enhancement information
    if hasattr(response, 'enhancement_info') and response.enhancement_info:
        enhancement_info = response.enhancement_info
        if 'enhancements_applied' in enhancement_info and enhancement_info['enhancements_applied']:
            st.info(f"🔧 Image Enhancements Applied: {', '.join(enhancement_info['enhancements_applied'])}")
            if 'quality_score' in enhancement_info:
                st.info(f"📊 Image Quality Score: {enhancement_info['quality_score']:.2f}/1.0")
    
    # Validation results
    if hasattr(response, 'validation_results') and response.validation_results:
        validation_results = response.validation_results
        
        if validation_results.get('errors'):
            st.error("❌ Validation Errors Found!")
        elif validation_results.get('warnings'):
            st.warning("⚠️ Validation Warnings")
        else:
            st.success("✅ Validation Passed")
        
        # Show validation summary
        if validation_results.get('confidence_adjustment') != 0:
            adjustment = validation_results['confidence_adjustment']
            if adjustment > 0:
                st.info(f"📈 Confidence Boosted: +{adjustment:.2f}")
            else:
                st.warning(f"📉 Confidence Reduced: {adjustment:.2f}")
    
    # Components (if available)
    if analysis.components:
        st.subheader("🧩 Components")
        for i, component in enumerate(analysis.components, 1):
            st.write(f"{i}. **{component.name}**: {component.value}")
    
    # Analysis summary
    st.subheader("📝 Analysis Summary")
    st.write(analysis.analysis_summary)
    
    # Calculations (if available)
    if analysis.calculations:
        st.subheader("🧮 Calculations")
        for i, calc in enumerate(analysis.calculations, 1):
            st.code(calc, language="text")
    
    # Timestamp
    st.caption(f"Analysis performed at: {analysis.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Detailed validation report
    if hasattr(response, 'validation_results') and response.validation_results:
        validation_results = response.validation_results
        
        with st.expander("🔍 View Detailed Validation Report"):
            from utils.validation_engine import CircuitValidationEngine
            validation_engine = CircuitValidationEngine()
            validation_report = validation_engine.generate_validation_report(validation_results)
            st.markdown(validation_report)
            
            # Show specific errors and warnings
            if validation_results.get('errors'):
                st.error("### Critical Issues:")
                for error in validation_results['errors']:
                    st.error(f"• {error}")
            
            if validation_results.get('warnings'):
                st.warning("### Areas of Concern:")
                for warning in validation_results['warnings']:
                    st.warning(f"• {warning}")
    
    # Download results option
    if st.button("📥 Download Analysis Report"):
        # Create a comprehensive text report
        report = f"""
Circuit Analysis Report
======================

🎯 SOLUTION (ANSWER)
===================
{analysis.solution}

📊 QUICK SUMMARY
================
Circuit Type: {analysis.circuit_type}
Confidence Level: {analysis.confidence_level:.1%}
Timestamp: {analysis.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

📋 DETAILED ANALYSIS
====================
ANALYSIS SUMMARY:
{analysis.analysis_summary}

CALCULATIONS:
{chr(10).join(analysis.calculations) if analysis.calculations else 'No calculations provided'}

COMPONENTS:
{chr(10).join([f"- {c.name}: {c.value}" for c in analysis.components]) if analysis.components else 'No components listed'}

VALIDATION RESULTS:
"""
        
        # Add validation information to report
        if hasattr(response, 'validation_results') and response.validation_results:
            validation_results = response.validation_results
            if validation_results.get('errors'):
                report += f"❌ ERRORS: {len(validation_results['errors'])} found\n"
                for error in validation_results['errors']:
                    report += f"  - {error}\n"
            
            if validation_results.get('warnings'):
                report += f"⚠️ WARNINGS: {len(validation_results['warnings'])} found\n"
                for warning in validation_results['warnings']:
                    report += f"  - {warning}\n"
            
            if validation_results.get('confidence_adjustment') != 0:
                report += f"📊 Confidence Adjustment: {validation_results['confidence_adjustment']:+.2f}\n"
        
        report += "\n" + "=" * 50 + "\n"
        report += "Report generated by Circuit Solving Agent with AI validation"
        
        st.download_button(
            label="📄 Download Report",
            data=report,
            file_name=f"circuit_analysis_{int(time.time())}.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
