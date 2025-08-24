#!/usr/bin/env python3
"""
Deployment helper script for Circuit Solving Agent
"""
import os
import subprocess
import sys

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        'app.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'config/settings.py',
        'models/circuit_analysis.py',
        'services/gemini_service.py',
        'chain/circuit_analysis_chain.py',
        'utils/image_utils.py',
        'utils/image_enhancement.py',
        'utils/validation_engine.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present")
    return True

def check_dependencies():
    """Check if all dependencies are installed."""
    try:
        import streamlit
        import google.generativeai
        import PIL
        import cv2
        import numpy
        import pydantic
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_connection():
    """Test Gemini API connection."""
    try:
        from services.gemini_service import GeminiService
        service = GeminiService()
        if service.test_connection():
            print("✅ Gemini API connection successful")
            return True
        else:
            print("❌ Gemini API connection failed")
            return False
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        return False

def run_local():
    """Run the application locally."""
    print("\n🚀 Starting local Streamlit app...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

def main():
    """Main deployment function."""
    print("⚡ Circuit Solving Agent - Deployment Helper")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix missing files before deployment")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        return
    
    # Test connection
    if not test_connection():
        print("\n❌ Please check your Gemini API key configuration")
        return
    
    print("\n🎉 All checks passed! Your app is ready for deployment.")
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Run locally")
    print("2. Deploy to Streamlit Cloud")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        run_local()
    elif choice == "2":
        print("\n🚀 To deploy to Streamlit Cloud:")
        print("1. Push your code to GitHub")
        print("2. Go to https://share.streamlit.io")
        print("3. Sign in with GitHub")
        print("4. Click 'New app' and select your repository")
        print("5. Set main file to: app.py")
        print("6. Add your Gemini API key in the app settings")
        print("7. Click 'Deploy!'")
        print("\n📖 See DEPLOYMENT.md for detailed instructions")
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
