"""
MeetFlow AI - Frontend Application (Streamlit)
Meeting transcription and analysis application (Open Source & Free Version)
University project - AAA Application

This frontend uses:
1. Backend services for transcription (faster-whisper)
2. Backend services for analysis (Groq API)
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.transcription_service import TranscriptionService
from backend.services.analysis_service import AnalysisService
from backend.utils.config import get_groq_api_key

# Streamlit page configuration
st.set_page_config(
    page_title="MeetFlow AI - Open Source",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== INITIALIZE SERVICES ====================
# Initialize services with error handling
try:
    api_key = get_groq_api_key()
    analysis_service = AnalysisService(api_key=api_key)
except ValueError as e:
    st.error("❌ GROQ_API_KEY not found. Please set it as:")
    st.error("1. Environment variable: `GROQ_API_KEY`")
    st.error("2. GitHub Secret (for deployment)")
    st.error("3. .env file: `GROQ_API_KEY=your_key_here`")
    st.error("4. config.py (local dev only): `GROQ_API_KEY = 'your_key_here'`")
    st.stop()
except Exception as e:
    st.error(f"❌ Error initializing services: {str(e)}")
    st.stop()

# ==================== UI COMPONENTS ====================
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
def get_transcription_service(model_size="base"):
    """
    Get transcription service with cache to avoid reloading model every time.
    """
    return TranscriptionService(model_size=model_size)

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
            try:
                transcription_service = get_transcription_service(whisper_model_size)
                transcription_service.load_model()
            except Exception as e:
                st.error(f"❌ Unable to load Whisper model: {str(e)}")
                st.error("💡 **Help:** Make sure faster-whisper is correctly installed.")
                st.error("Try: `pip install faster-whisper`")
                st.stop()
            
            # ==================== STEP 2: TRANSCRIPTION ====================
            status.update(label="🎤 Transcribing audio (local faster-whisper)...", state="running")
            
            try:
                transcription_text, metadata = transcription_service.transcribe_uploaded_file(
                    uploaded_file,
                    language=None,  # Automatic language detection
                    beam_size=5
                )
                
                # Display transcription information
                st.success(
                    f"✅ Transcription complete! "
                    f"(Detected language: {metadata['language']}, "
                    f"Probability: {metadata['language_probability']:.2%})"
                )
                
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Error during transcription: {error_msg}")
                
                # Specific help messages for common errors
                if "No such file" in error_msg or "path" in error_msg.lower():
                    st.error("💡 **Help:** File path issue.")
                    st.error("Make sure faster-whisper can access the temporary file.")
                elif "CUDA" in error_msg or "cuda" in error_msg.lower():
                    st.info("💡 The model uses CPU by default. This is normal if you don't have a GPU.")
                
                st.stop()
            
            # ==================== STEP 3: GROQ ANALYSIS ====================
            status.update(label="🧠 Analyzing content with Groq (open source LLM)...", state="running")
            
            try:
                analysis_data = analysis_service.analyze_meeting(transcription_text)
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

