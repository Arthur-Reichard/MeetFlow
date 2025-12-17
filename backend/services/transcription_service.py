"""
Transcription service using faster-whisper
Handles audio file transcription with local Whisper model
"""

import os
import tempfile
from faster_whisper import WhisperModel
from typing import Tuple, Optional


class TranscriptionService:
    """Service for transcribing audio files using faster-whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the transcription service with a Whisper model.
        
        Args:
            model_size: Size of the Whisper model ("tiny", "base", "small")
        """
        self.model_size = model_size
        self.model = None
    
    def load_model(self) -> WhisperModel:
        """
        Load the Whisper model (with caching support).
        
        Returns:
            WhisperModel: The loaded Whisper model
            
        Raises:
            Exception: If model loading fails
        """
        if self.model is None:
            try:
                # Load faster-whisper model
                # The model will be automatically downloaded on first use
                self.model = WhisperModel(
                    self.model_size, 
                    device="cpu", 
                    compute_type="int8"
                )
            except Exception as e:
                raise Exception(f"Error loading Whisper model: {str(e)}")
        
        return self.model
    
    def transcribe_audio_file(
        self, 
        audio_file_path: str, 
        language: Optional[str] = None,
        beam_size: int = 5
    ) -> Tuple[str, dict]:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_file_path: Path to the audio file
            language: Language code (None for auto-detection)
            beam_size: Beam size for transcription (default: 5)
            
        Returns:
            Tuple[str, dict]: Transcription text and metadata (language, probability, etc.)
            
        Raises:
            Exception: If transcription fails
        """
        if self.model is None:
            self.load_model()
        
        try:
            # Transcribe audio
            segments, info = self.model.transcribe(
                audio_file_path,
                language=language,  # None = automatic language detection
                beam_size=beam_size
            )
            
            # Combine all segments into full text
            transcription_text = ""
            for segment in segments:
                transcription_text += segment.text + " "
            
            transcription_text = transcription_text.strip()
            
            # Prepare metadata
            metadata = {
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": getattr(info, "duration", None)
            }
            
            return transcription_text, metadata
            
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")
    
    def transcribe_uploaded_file(
        self, 
        uploaded_file, 
        language: Optional[str] = None,
        beam_size: int = 5
    ) -> Tuple[str, dict]:
        """
        Transcribe an uploaded file (Streamlit UploadedFile object).
        Creates a temporary file for faster-whisper processing.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            language: Language code (None for auto-detection)
            beam_size: Beam size for transcription (default: 5)
            
        Returns:
            Tuple[str, dict]: Transcription text and metadata
            
        Raises:
            Exception: If transcription fails
        """
        temp_file = None
        temp_file_path = None
        
        try:
            # Create temporary file with appropriate extension
            file_extension = os.path.splitext(uploaded_file.name)[1] or ".mp3"
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name
            temp_file.close()
            
            # Transcribe the temporary file
            transcription_text, metadata = self.transcribe_audio_file(
                temp_file_path,
                language=language,
                beam_size=beam_size
            )
            
            return transcription_text, metadata
            
        except Exception as e:
            # Clean up temporary file on error
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
            raise e
            
        finally:
            # Clean up temporary file after transcription
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    # Log warning but don't fail
                    print(f"Warning: Unable to delete temporary file: {str(e)}")

