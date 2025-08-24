#!/usr/bin/env python3
"""
Simple launcher for the Circuit Solving Agent
"""
import subprocess
import sys
import time
import os

def main():
    print("🚀 Launching Circuit Solving Agent...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found in current directory")
        print("Please run this script from the project root directory")
        return
    
    # Launch the app
    try:
        print("Starting Streamlit app on port 8501...")
        print("Local URL: http://localhost:8501")
        print("Press Ctrl+C to stop the app")
        print("-" * 50)
        
        # Launch the app
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.fileWatcherType", "none"
        ], capture_output=False)
        
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main()
