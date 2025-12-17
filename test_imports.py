"""
Test script to verify all imports work correctly
Used in GitHub Actions workflow
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_imports():
    """Test all required imports"""
    print("Testing external dependencies...")
    try:
        import streamlit
        import groq
        import faster_whisper
        print("✅ All external imports successful")
    except ImportError as e:
        print(f"❌ External import failed: {e}")
        sys.exit(1)
    
    print("\nTesting backend imports...")
    try:
        from backend.services.transcription_service import TranscriptionService
        print("✅ TranscriptionService import successful")
    except ImportError as e:
        print(f"❌ TranscriptionService import failed: {e}")
        sys.exit(1)
    
    try:
        from backend.services.analysis_service import AnalysisService
        print("✅ AnalysisService import successful")
    except ImportError as e:
        print(f"❌ AnalysisService import failed: {e}")
        sys.exit(1)
    
    try:
        from backend.utils.config import get_groq_api_key
        print("✅ Config utility import successful")
    except ImportError as e:
        print(f"❌ Config utility import failed: {e}")
        sys.exit(1)
    
    print("\n✅ All imports successful!")

if __name__ == "__main__":
    test_imports()

