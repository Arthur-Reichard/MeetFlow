"""
Analysis service using Groq API
Handles meeting transcription analysis with open source LLM
"""

import json
import os
import sys
from groq import Groq
from typing import Dict, Optional

# Add project root to path for imports
# This ensures backend.* imports work from anywhere
_current_file = os.path.abspath(__file__)
# Current: backend/services/analysis_service.py
# Go up 2 levels: backend/services -> backend -> project root
_backend_dir = os.path.dirname(os.path.dirname(_current_file))  # backend/
_project_root = os.path.dirname(_backend_dir)  # project root

# Ensure project root is in path (check and add if needed)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Import using absolute import (now that path is set)
# Use a try-except to handle import errors gracefully
try:
    from backend.utils.config import get_groq_api_key
except ImportError:
    # Fallback: try importing directly from the file
    import importlib.util
    config_file_path = os.path.join(_backend_dir, 'utils', 'config.py')
    if os.path.exists(config_file_path):
        spec = importlib.util.spec_from_file_location("backend.utils.config", config_file_path)
        if spec and spec.loader:
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            get_groq_api_key = config_module.get_groq_api_key
        else:
            raise ImportError(f"Could not load config module from {config_file_path}")
    else:
        raise ImportError(f"Config file not found at {config_file_path}")


class AnalysisService:
    """Service for analyzing meeting transcriptions using Groq API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the analysis service with Groq client.
        
        Args:
            api_key: Groq API key (if None, will try to load from environment/config)
            
        Raises:
            ValueError: If API key cannot be found
            Exception: If Groq client initialization fails
        """
        if api_key is None:
            api_key = get_groq_api_key()
        
        try:
            self.client = Groq(api_key=api_key)
        except Exception as e:
            raise Exception(f"Error initializing Groq client: {str(e)}")
    
    def analyze_meeting(
        self, 
        transcription_text: str,
        models_to_try: Optional[list] = None
    ) -> Dict:
        """
        Analyze a meeting transcription and extract summary and action items.
        
        Args:
            transcription_text: The transcribed meeting text
            models_to_try: List of Groq models to try (default: predefined list)
            
        Returns:
            Dict: Analysis results with "resume_executif" and "action_items"
            
        Raises:
            Exception: If analysis fails for all models
        """
        if models_to_try is None:
            models_to_try = [
                "llama-3.1-8b-instant",      # Fast and efficient model
                "llama-3.3-70b-versatile",  # More powerful model
                "mixtral-8x7b-32768"        # Alternative model
            ]
        
        system_prompt = """You are an expert assistant for analyzing professional meetings.
        Analyze a meeting transcription and provide:
        1. A concise executive summary (3-4 sentences)
        2. A list of action items with identified responsible persons
        
        Respond ONLY in JSON format with this exact structure:
        {
            "resume_executif": "Concise summary in 3-4 sentences (use the same language as the transcription)",
            "action_items": [
                {"tache": "Task description", "responsable": "Person's name or 'To be determined'"},
                ...
            ]
        }
        
        Use the same language as the transcription (English or French)."""
        
        analysis_data = None
        last_error = None
        response = None
        
        for model_name in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Analyze this meeting transcription:\n\n{transcription_text}"}
                    ],
                    temperature=0.7,
                    response_format={"type": "json_object"}
                )
                
                # Parse JSON response
                analysis_data = json.loads(response.choices[0].message.content)
                break  # Success, exit loop
                
            except json.JSONDecodeError as e:
                # If it's a JSON error, keep the response for fallback
                last_error = e
                if response:
                    # Fallback: use raw content
                    raw_content = response.choices[0].message.content
                    analysis_data = {
                        "resume_executif": raw_content[:500] if len(raw_content) > 500 else raw_content,
                        "action_items": []
                    }
                    break
                continue  # Try next model
                
            except Exception as e:
                last_error = e
                continue  # Try next model
        
        if analysis_data is None:
            raise Exception(f"All models failed. Last error: {str(last_error)}")
        
        return analysis_data

