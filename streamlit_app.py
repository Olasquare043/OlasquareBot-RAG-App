import streamlit as st
import requests
import time
from datetime import datetime
import os
from helper import DocumentProcessing, VectorManager, RagBuilder

# Page configuration
st.set_page_config(
    page_title="Olasquare Bot - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional, clean styling - NO RED COLORS
st.markdown("""
<style>
    /* Main header styling */
            
    *{
        box-sizing: border-box;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3B82F6;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Status indicator - FIXED: Proper status display */
    .status-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .status-healthy {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #10B981;
    }
    
    .status-unhealthy {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #F59E0B;
    }
    
    /* Chat message styling  */
    .chat-row {
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .user-row {
        display: flex;
        justify-content: flex-end;
    }
    
    .bot-row {
        display: flex;
        justify-content: flex-start;
    }
    
    .message-wrapper {
        display: flex;
        flex-direction: column;
        max-width: 70%;
    }
    
    .message-label {
        font-weight: 600;
        font-size: 0.85rem;
        color: #6B7280;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .message-content {
        padding: 0.5rem 0.5rem;
        border-radius: 1rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border-radius: 1rem 1rem 0.25rem 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .bot-message {
        background-color: #F9FAFB;
        color: #111827;
        border: 1px solid #E5E7EB;
        border-radius: 1rem 1rem 1rem 0.25rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .timestamp {
        font-size: 0.75rem;
        color: #9CA3AF;
        margin-top: 0.25rem;
        text-align: right;
        font-style: italic;
    }
    
    /* Typewriter effect */
    .typing-animation {
        overflow: hidden;
        white-space: pre-wrap;
        animation: typing 1.5s ease-in-out;
    }
    
    @keyframes typing {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
       
   
    /* Target secondary buttons in sidebar */
    .stButton button[kind="secondary"] {
        width: 100%;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #0082F6 01%, #1D4ED8 100%);
        border: 1px solid #D1D5DB;
        border-radius: 0.5rem;
        text-align: left;
        font-size: 0.9rem;
        color: #fff;
        transition: all 0.2s;
    }
    
    .stButton button[kind="secondary"]:hover {
        background-color: #E5E7EB;
        border-color: #9CA3AF;
    }
            

    .footer{
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        bottom: 0;
        z-index: 99;
        width: 65%;
        border-radius: 5px;
        background: linear-gradient(135deg, #0082F6 01%, #1D4ED8 100%);
        
    }
</style>
""", unsafe_allow_html=True)


class OlasquareBotClient:
    """Integrated RAG system - no API calls needed"""
    
    def __init__(self):
        self.vector_manager = None
        self.rag_builder = None
        self.is_initialized = False
        
    def _initialize_rag(self):
        """Initialize the RAG system"""
        try:
            self.vector_manager = VectorManager()
            self.rag_builder = RagBuilder(self.vector_manager)
            self.is_initialized = True
            return True
        except Exception as e:
            st.error(f"Failed to initialize RAG: {str(e)}")
            return False
    
    def health_check(self) -> bool:
        """Check if RAG system is ready"""
        try:
            if not self.is_initialized:
                return self._initialize_rag()
            return True
        except:
            return False
    
    def ask_question(self, question: str) -> dict:
        """Send a question directly to the RAG system"""
        if not self.is_initialized:
            if not self._initialize_rag():
                return {"answer": "RAG system not initialized"}
        
        try:
            # Call the RAG system directly
            response = self.rag_builder.query(question)
            return response
        except Exception as e:
            return {"answer": f"RAG error: {str(e)}"}

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'api_status' not in st.session_state:
        st.session_state.api_status = "unknown"
    if 'current_query' not in st.session_state:
        st.session_state.current_query = ""
    if 'auto_send' not in st.session_state:
        st.session_state.auto_send = False


def display_sidebar(client):
    """Display the sidebar with quick questions and controls"""
    with st.sidebar:
        # Header
        st.markdown('<div class="sidebar-header">🤖 Olasquare Bot</div>', unsafe_allow_html=True)
        
        # Status indicator 
        if st.session_state.api_status == "healthy":
            st.markdown(
                '<div class="status-box status-healthy">'
                '<span style="font-size: 1.2em;">✅</span> '
                '<span>API Connected</span>'
                '</div>',
                unsafe_allow_html=True
            )
        elif st.session_state.api_status == "unhealthy":
            st.markdown(
                '<div class="status-box status-unhealthy">'
                '<span style="font-size: 1.2em;">⚠️</span> '
                '<span>API Unavailable</span>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            with st.container():
                st.info("🔃 Checking connection...")
        
        # Refresh button
        if st.button("🔄 Refresh Connection", use_container_width=True, type="secondary"):
            with st.spinner("Checking..."):
                if client.health_check():
                    st.session_state.api_status = "healthy"
                    st.success("✅ Connected!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.api_status = "unhealthy"
                    st.error("❌ Connection failed")
                    time.sleep(1)
                    st.rerun()
        
        st.divider()
        
        # Quick Questions section
        st.markdown("**Quick Questions**")
        
        # Define quick questions with unique identifiers
        quick_questions = [
            ("Who is Olasquare?", "q_who_is"),
            ("What are Olasquare's core skills?", "q_skills"),
            ("Tell me about Olasquare's projects", "q_projects"),
            ("What teaching experience does Olasquare have?", "q_teaching"),
            ("Describe Olasquare's background", "q_background"),
            ("What is Olasquare's professional expertise?", "q_expertise"),
            ("Tell me about Olasquare's community involvement", "q_community"),
            ("What are Olasquare's career achievements?", "q_achievements")
        ]
        
        # Display quick questions as clickable buttons
        for question, key in quick_questions:
            if st.button(question, key=key, use_container_width=True, type="secondary"):
                st.session_state.current_query = question
                st.session_state.auto_send = True
                st.rerun()
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="primary"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            time.sleep(0.5)
            st.rerun()
        
        # Simple stats
        if st.session_state.chat_history:
            user_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "user"])
            st.caption(f"📊 {user_messages} questions asked")

def display_chat_messages():
    """Display chat messages in reverse order (newest at top)"""
    if not st.session_state.chat_history:
        # Show welcome message when no chat history
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #6B7280; margin: 2rem 0;">
            <h3 style="color: #1E3A8A; margin-bottom: 1rem;">👋 Welcome to Olasquare Bot</h3>
            <p>Ask me anything about Olasquare's professional background, skills, and experience!</p>
            <p>Try a quick question from the sidebar or type your own below.</p>
        </div>
        """, unsafe_allow_html=True)
        return 

    # Display messages in reverse order (newest first at top)
    for chat in reversed(st.session_state.chat_history):
        if chat["role"] == "user":
            # User message
            st.markdown('<div class="chat-row user-row">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 3])
            with col2:
                # User label with icon
                st.markdown(
                    f'<div class="message-label">'
                    f'<span style="background-color: #3B82F6; color: white; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem;">👤</span>'
                    f'<span>You</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Message content 
                st.markdown(f'<div class="message-content user-message">{chat["content"]}</div>', unsafe_allow_html=True)
                
                # Timestamp -
                if "timestamp" in chat:
                    st.markdown(f'<div class="timestamp">🕒 {chat["timestamp"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            # Bot message
            st.markdown('<div class="chat-row bot-row">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                # Bot label with icon
                st.markdown(
                    f'<div class="message-label">'
                    f'<span style="background-color: #6B7280; color: white; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem;">🤖</span>'
                    f'<span>Bot</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Message content with typing effect
                message_class = "message-content bot-message typing-animation" if chat.get("typing_effect", True) else "message-content bot-message"
                st.markdown(f'<div class="{message_class}">{chat["content"]}</div>', unsafe_allow_html=True)
                
                # Timestamp
                if "timestamp" in chat:
                    st.markdown(f'<div class="timestamp">🕒 {chat["timestamp"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider between messages
        st.markdown('<div style="margin: 1rem 0; border-bottom: 1px solid #E5E7EB;"></div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Create client
    client = OlasquareBotClient()
    
    # Check API status on startup
    if st.session_state.api_status == "unknown":
        with st.spinner("Connecting to API..."):
            st.session_state.api_status = "healthy" if client.health_check() else "unhealthy"
    
    # Display sidebar
    with st.sidebar:
        display_sidebar(client)
    
    # Main content area
    st.markdown('<div class="main-header">💬 Chat with Olasquare Bot</div>', unsafe_allow_html=True)
    
    # Display chat history (newest messages at the top)
    display_chat_messages()
        
    # Check for auto-send from quick questions
    if st.session_state.auto_send and st.session_state.current_query:
        query = st.session_state.current_query
        st.session_state.current_query = ""
        
        # Add user message to history
        st.session_state.chat_history.insert(0, {
            "role": "user",
            "content": query,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Get bot response
        with st.spinner("🤖 Thinking..."):
            try:
                result = client.ask_question(query)
                
                if result:
                    # Add bot response to history
                    st.session_state.chat_history.insert(0, {
                        "role": "bot",
                        "content": result.get("answer", "I couldn't generate a response."),
                        "timestamp": datetime.now().strftime("%H:%M"),
                        "typing_effect": True
                    })
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.session_state.auto_send = False
        st.rerun()
    
    # Input area at the bottom (sticky)
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Create a form for Enter key support
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            # Text input for questions - value="" clears after submit
            query = st.text_input(
                "Type your question here...",
                value="",
                key="chat_input",
                label_visibility="collapsed",
                placeholder="Ask about Olasquare's skills, projects, or experience..."
            )
        
        with col2:
            submit_button = st.form_submit_button("**Send**", use_container_width=True, type="primary")
        
        # Process form submission (Enter key or Send button)
        if submit_button and query:
            # Add user message to history
            st.session_state.chat_history.insert(0, {
                "role": "user",
                "content": query,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # Get bot response
            with st.spinner("🤖 Thinking..."):
                try:
                    result = client.ask_question(query)
                    
                    if result:
                        # Add bot response to history
                        st.session_state.chat_history.insert(0, {
                            "role": "bot",
                            "content": result.get("answer", "I couldn't generate a response."),
                            "timestamp": datetime.now().strftime("%H:%M"),
                            "typing_effect": True
                        })
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            # Clear form and rerun
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    
    
    st.markdown('<div class="footer">Olasquare Bot v1.0 • Powered by OpenAI GPT-3.5</div>', unsafe_allow_html=True)


    # st.markdown("---")
    # col1, col2, col3 = st.columns(3)
    # with col2:
    #     st.caption("Olasquare Bot v1.0 • Powered by OpenAI GPT-3.5")

if __name__ == "__main__":
    main()