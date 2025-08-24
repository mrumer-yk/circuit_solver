#!/usr/bin/env python3
"""
Streamlit Deployment Script for Circuit Solving Agent
Handles both local deployment and Streamlit Cloud preparation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed."""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'streamlit',
        'google-generativeai',
        'pillow',
        'opencv-python',
        'pydantic',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n🚨 Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements satisfied!")
    return True

def check_api_key():
    """Check if Gemini API key is configured."""
    print("\n🔑 Checking API key configuration...")
    
    # Check environment variable
    if os.getenv("GEMINI_API_KEY"):
        print("✅ API key found in environment variables")
        return True
    
    # Check Streamlit secrets
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and st.secrets.get("GEMINI_API_KEY"):
            print("✅ API key found in Streamlit secrets")
            return True
    except ImportError:
        pass
    
    # Check .streamlit/secrets.toml
    secrets_file = Path(".streamlit/secrets.toml")
    if secrets_file.exists():
        print("✅ API key found in .streamlit/secrets.toml")
        return True
    
    print("❌ No API key found!")
    print("Please set GEMINI_API_KEY environment variable or add it to .streamlit/secrets.toml")
    return False

def test_app_import():
    """Test if the app can be imported successfully."""
    print("\n🧪 Testing app import...")
    
    try:
        import app
        print("✅ App imports successfully!")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def run_local():
    """Run the app locally."""
    print("\n🚀 Starting local deployment...")
    
    # Use local config
    config_file = Path(".streamlit/config_local.toml")
    if config_file.exists():
        print("📁 Using local configuration")
        os.environ["STREAMLIT_CONFIG_FILE"] = str(config_file)
    
    try:
        print("🌐 Starting Streamlit app...")
        print("📍 Local URL: http://localhost:8501")
        print("📍 Network URL: http://YOUR_IP:8501")
        print("\nPress Ctrl+C to stop the app")
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")
    except Exception as e:
        print(f"❌ Failed to start app: {e}")

def prepare_deployment():
    """Prepare for Streamlit Cloud deployment."""
    print("\n☁️ Preparing for Streamlit Cloud deployment...")
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a git repository!")
        print("Please run: git init && git add . && git commit -m 'Initial commit'")
        return False
    
    # Check if remote origin is set
    try:
        result = subprocess.run(
            ["git", "remote", "-v"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        if "origin" in result.stdout:
            print("✅ Git remote origin configured")
        else:
            print("❌ Git remote origin not configured")
            return False
    except subprocess.CalledProcessError:
        print("❌ Git not available")
        return False
    
    print("✅ Repository ready for deployment!")
    print("\n📋 Next steps:")
    print("1. Push your code: git push origin main")
    print("2. Go to: https://share.streamlit.io")
    print("3. Connect your GitHub account")
    print("4. Select your repository")
    print("5. Set main file to: app.py")
    print("6. Add your API key in secrets")
    print("7. Deploy!")
    
    return True

def main():
    """Main deployment function."""
    print("🚀 Circuit Solving Agent - Deployment Script")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python deploy_streamlit.py local     - Run locally")
        print("  python deploy_streamlit.py deploy   - Prepare for Streamlit Cloud")
        print("  python deploy_streamlit.py check    - Check system status")
        return
    
    command = sys.argv[1].lower()
    
    if command == "check":
        check_requirements()
        check_api_key()
        test_app_import()
        
    elif command == "local":
        if not check_requirements():
            return
        if not check_api_key():
            return
        if not test_app_import():
            return
        run_local()
        
    elif command == "deploy":
        if not check_requirements():
            return
        if not check_api_key():
            return
        if not test_app_import():
            return
        prepare_deployment()
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: local, deploy, or check")

if __name__ == "__main__":
    main()
