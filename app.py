"""
MeetFlow AI - Meeting transcription and analysis application (Open Source & Free Version)
University project - AAA Application

This application uses:
1. faster-whisper (local, free) for audio transcription
2. Groq API (free) for text analysis via open source LLM
"""

import streamlit as st
from groq import Groq
from faster_whisper import WhisperModel
import os
import tempfile
from dotenv import load_dotenv
import json

# Streamlit page configuration
st.set_page_config(
    page_title="MeetFlow AI - Open Source",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables (optional)
load_dotenv()

# ==================== API KEY CONFIGURATION ====================
# Import API key from config.py (not committed to Git)
try:
    from config import GROQ_API_KEY
    api_key_input = GROQ_API_KEY
except ImportError:
    # Fallback if config.py doesn't exist
    st.error("❌ config.py file not found. Please create it with your GROQ_API_KEY.")
    st.stop()

# Main title with emoji
st.title("🎙️ MeetFlow AI")
st.markdown("### Intelligent meeting transcription and analysis (100% Free & Open Source)")
st.markdown("---")

# ==================== SIDEBAR - Configuration ====================
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    st.markdown("### 🎤 Whisper Model")
    whisper_model_size = st.selectbox(
        "Model size (smaller = faster)",
        ["tiny", "base", "small"],
        index=1,
        help="tiny = very fast, base = balanced, small = more accurate"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Supported Formats")
    st.markdown("- MP3")
    st.markdown("- WAV")
    st.markdown("- M4A")
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **MeetFlow AI** uses :
    - 🤖 **faster-whisper** (local, free)
    - 🧠 **Groq** (free API, open source LLM)
    """)

# ==================== FUNCTION TO LOAD WHISPER MODEL ====================
@st.cache_resource
def load_whisper_model(model_size="base"):
    """
    Load Whisper model with cache to avoid reloading it every time.
    This is where the local transcription AI is initialized.
    """
    try:
        # Load faster-whisper model
        # The model will be automatically downloaded on first use
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        return model
    except Exception as e:
        st.error(f"❌ Error loading Whisper model: {str(e)}")
        st.error("💡 **Help:** Make sure faster-whisper is correctly installed.")
        st.error("Try: `pip install faster-whisper`")
        return None

# Initialize Groq client
try:
    groq_client = Groq(api_key=api_key_input)
except Exception as e:
    st.error(f"❌ Error initializing Groq client: {str(e)}")
    st.stop()

# ==================== FILE UPLOAD ====================
st.header("📤 Upload Recording")
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["mp3", "wav", "m4a"],
    help="Supported formats: MP3, WAV, M4A"
)

# ==================== TRAITEMENT ====================
if uploaded_file is not None:
    # Display file information
    file_details = {
        "File name": uploaded_file.name,
        "File type": uploaded_file.type,
        "Size": f"{uploaded_file.size / (1024*1024):.2f} MB"
    }
    
    with st.expander("📄 File Details"):
        for key, value in file_details.items():
            st.text(f"{key}: {value}")
    
    st.markdown("---")
    
    # Button to start analysis
    if st.button("🚀 Analyze Meeting", type="primary", use_container_width=True):
        
        # Use st.status to display processing steps
        with st.status("🔄 Processing...", expanded=True) as status:
            
            # ==================== STEP 1: LOAD MODEL ====================
            status.update(label="📦 Loading Whisper model...", state="running")
            whisper_model = load_whisper_model(whisper_model_size)
            
            if whisper_model is None:
                st.error("❌ Unable to load Whisper model. Please check the installation.")
                st.stop()
            
            # ==================== STEP 2: TEMPORARY FILE SAVE ====================
            status.update(label="💾 Preparing audio file...", state="running")
            
            # Create temporary file for faster-whisper
            # faster-whisper requires a physical file, not a memory buffer
            temp_file = None
            try:
                # Create temporary file with appropriate extension
                file_extension = os.path.splitext(uploaded_file.name)[1] or ".mp3"
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
                temp_file.write(uploaded_file.getbuffer())
                temp_file_path = temp_file.name
                temp_file.close()
                
            except Exception as e:
                st.error(f"❌ Error creating temporary file: {str(e)}")
                st.stop()
            
            # ==================== STEP 3: TRANSCRIPTION (local faster-whisper) ====================
            status.update(label="🎤 Transcribing audio (local faster-whisper)...", state="running")
            
            try:
                # This is where local Whisper AI converts audio to text
                # Let Whisper automatically detect the language (language=None)
                segments, info = whisper_model.transcribe(
                    temp_file_path,
                    language=None,  # Automatic language detection
                    beam_size=5
                )
                
                # Get complete transcription text
                transcription_text = ""
                for segment in segments:
                    transcription_text += segment.text + " "
                
                transcription_text = transcription_text.strip()
                
                # Display transcription information
                st.success(f"✅ Transcription complete! (Detected language: {info.language}, Probability: {info.language_probability:.2%})")
                
            except Exception as e:
                # Clean up temporary file on error
                if temp_file_path and os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                
                error_msg = str(e)
                st.error(f"❌ Error during transcription: {error_msg}")
                
                # Specific help messages for common errors
                if "No such file" in error_msg or "path" in error_msg.lower():
                    st.error("💡 **Help:** File path issue.")
                    st.error("Make sure faster-whisper can access the temporary file.")
                elif "CUDA" in error_msg or "cuda" in error_msg.lower():
                    st.info("💡 The model uses CPU by default. This is normal if you don't have a GPU.")
                
                st.stop()
            
            finally:
                # Clean up temporary file after transcription
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except Exception as e:
                        st.warning(f"⚠️ Unable to delete temporary file: {str(e)}")
            
            # ==================== STEP 4: GROQ ANALYSIS ====================
            status.update(label="🧠 Analyzing content with Groq (open source LLM)...", state="running")
            
            try:
                # Prompt système pour structurer l'analyse (multilingue)
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
                
                # Call Groq API for analysis
                # This is where Groq AI (open source LLM) analyzes and structures the content
                # Currently available models on Groq (updated 2025)
                models_to_try = [
                    "llama-3.1-8b-instant",      # Fast and efficient model
                    "llama-3.3-70b-versatile",  # More powerful model
                    "mixtral-8x7b-32768"        # Alternative model
                ]
                analysis_data = None
                last_error = None
                response = None
                
                for model_name in models_to_try:
                    try:
                        response = groq_client.chat.completions.create(
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
                
                status.update(label="✅ Analysis complete!", state="complete")
            except Exception as e:
                st.error(f"❌ Error during Groq analysis: {str(e)}")
                # On error, still display the transcription
                analysis_data = {
                    "resume_executif": "Error during analysis. Please check your Groq API key.",
                    "action_items": []
                }
        
        st.markdown("---")
        
        # ==================== DISPLAY RESULTS IN TABS ====================
        st.header("📊 Analysis Results")
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs([
            "📝 Transcription",
            "📋 Executive Summary",
            "✅ Action Items"
        ])
        
        # Tab 1: Complete transcription
        with tab1:
            st.subheader("🎤 Complete Transcription")
            st.markdown("**Raw meeting text:**")
            st.text_area(
                "Transcription",
                value=transcription_text,
                height=400,
                label_visibility="collapsed"
            )
            # Download button
            st.download_button(
                label="💾 Download Transcription",
                data=transcription_text,
                file_name=f"transcription_{uploaded_file.name}.txt",
                mime="text/plain"
            )
        
        # Tab 2: Executive Summary
        with tab2:
            st.subheader("📋 Executive Summary")
            st.markdown("**Meeting summary:**")
            resume = analysis_data.get("resume_executif", "No summary available")
            st.info(resume)
        
        # Tab 3: Action Items
        with tab3:
            st.subheader("✅ Action Items")
            st.markdown("**Identified tasks and responsible persons:**")
            
            action_items = analysis_data.get("action_items", [])
            if action_items:
                for idx, item in enumerate(action_items, 1):
                    tache = item.get("tache", "Task not specified")
                    responsable = item.get("responsable", "Not assigned")
                    
                    st.markdown(f"""
                    **{idx}. {tache}**
                    - 👤 Responsible: *{responsable}*
                    """)
                    st.markdown("---")
            else:
                st.info("No action items detected in this meeting.")
        
        # Completion message
        st.markdown("---")
        st.success("🎉 Analysis completed successfully!")
        
else:
    # Welcome message if no file is uploaded
    st.info("👆 Please upload an audio file above to start the analysis.")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>MeetFlow AI - Open Source & Free Version | Powered by faster-whisper & Groq</p>
        <p><small>100% free - No data is sent to paid services</small></p>
    </div>
    """,
    unsafe_allow_html=True
)

