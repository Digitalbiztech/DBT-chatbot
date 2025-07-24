#!/usr/bin/env python3
"""
Setup script for local Python virtual environment
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        return None

def create_virtual_environment():
    """Create a Python virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("Virtual environment already exists at 'venv'")
        return True
    
    print("Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def get_activate_script():
    """Get the appropriate activation script based on OS"""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\activate"
    else:  # Unix/Linux/Mac
        return "venv/bin/activate"

def install_requirements():
    """Install requirements in the virtual environment"""
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    print("Installing requirements...")
    result = run_command(f"{pip_cmd} install -r requirements.txt")
    
    if result and result.returncode == 0:
        print("✅ Requirements installed successfully!")
        return True
    else:
        print("❌ Error installing requirements")
        return False

def main():
    """Main setup function"""
    print("🐍 Setting up Python Virtual Environment")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Create virtual environment
    if not create_virtual_environment():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Get activation script
    activate_script = get_activate_script()
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo activate the virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("  venv\\Scripts\\activate")
        print("\nOr in PowerShell:")
        print("  venv\\Scripts\\Activate.ps1")
    else:  # Unix/Linux/Mac
        print("  source venv/bin/activate")
    
    print("\nTo run the application:")
    print("  python main.py")
    
    print("\nTo deactivate:")
    print("  deactivate")

if __name__ == "__main__":
    main() 