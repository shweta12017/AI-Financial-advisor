"""
Chatbot page for conversational AI financial assistance.

Relies on the current FinancialProfile stored in `st.session_state`
so the assistant can answer in context.
"""

from __future__ import annotations

import streamlit as st

from models.financial_profile import FinancialProfile
from services.chatbot import ChatMessage, chat_reply
from services.fallback_chatbot import chat_reply_fallback


def _get_profile() -> FinancialProfile | None:
    return st.session_state.get("profile")


def render() -> None:
    """Render the chatbot page."""
    # Custom CSS for chat styling with blue, red, green, and golden theme
    st.markdown("""
    <style>
        .chat-header {
            background: linear-gradient(90deg, #fbbf24 0%, #1e40af 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .error-message {
            background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
            border: 2px solid #dc2626;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .info-message {
            background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
            border: 2px solid #1e40af;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .stButton > button {
            background: linear-gradient(90deg, #16a34a 0%, #fbbf24 100%);
            border: none;
            color: white;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chat-header"><h2>🟡 Smart Financial Assistant</h2><p>Ask questions about your finances and get AI-powered advice</p></div>', unsafe_allow_html=True)

    profile = _get_profile()
    if profile is None:
        st.markdown("""
        <div class="info-message">
            <h4>📊 No Financial Profile Found</h4>
            <p>To get personalized advice, please:</p>
            <ol>
                <li>Go to the <strong>Dashboard</strong> page</li>
                <li>Enter your financial details</li>
                <li>Run an analysis</li>
            </ol>
            <p><em>The chatbot can still answer generic questions, but will be more helpful with your data.</em></p>
        </div>
        """, unsafe_allow_html=True)
        # Use a blank profile-like object if needed; for now we just proceed.

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []  # type: ignore[assignment]
    
    # Add offline mode flag - start in offline mode by default to avoid API issues
    if "force_offline_mode" not in st.session_state:
        st.session_state["force_offline_mode"] = True
    
    # Add option to force offline mode
    with st.sidebar:
        if st.button("🔄 Switch to Offline Mode"):
            st.session_state["force_offline_mode"] = not st.session_state["force_offline_mode"]
            st.rerun()
        
        if st.session_state["force_offline_mode"]:
            st.success("🤖 Offline Mode Active")
        else:
            st.info("🌐 Trying API First")

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("💬 Ask a question about your finances...")
    if user_input:
        st.session_state["chat_history"].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(f"**You:** {user_input}")
            
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Check if offline mode is forced
                    if st.session_state.get("force_offline_mode", False):
                        # Use fallback directly
                        history: list[ChatMessage] = st.session_state["chat_history"]  # type: ignore[assignment]
                        active_profile = profile or FinancialProfile(
                            monthly_income=0.0,
                            monthly_expenses=0.0,
                            monthly_savings=0.0,
                            monthly_debt_payments=0.0,
                        )
                        reply = chat_reply_fallback(active_profile, history)
                        st.markdown(f"**🤖 AI Assistant (Offline Mode):** {reply}")
                        st.info("💡 Offline mode is active. Toggle in sidebar to try API.")
                    else:
                        # Try API first
                        history: list[ChatMessage] = st.session_state["chat_history"]  # type: ignore[assignment]
                        active_profile = profile or FinancialProfile(
                            monthly_income=0.0,
                            monthly_expenses=0.0,
                            monthly_savings=0.0,
                            monthly_debt_payments=0.0,
                        )
                        reply = chat_reply(active_profile, history)
                        st.markdown(f"**🤖 AI Assistant:** {reply}")
                except Exception as e:
                    # Handle API errors gracefully with fallback
                    error_str = str(e).lower()
                    if any(keyword in error_str for keyword in ["429", "quota", "api_key_invalid", "limit", "exceeded"]):
                        # Use fallback chatbot service
                        reply = chat_reply_fallback(active_profile, history)
                        st.markdown(f"**🤖 AI Assistant (Offline Mode):** {reply}")
                        st.info("💡 Using offline financial advice mode. For AI-powered responses, please update your API key or enable billing.")
                    else:
                        # Other errors
                        error_msg = f"""
                        <div class="error-message">
                            <h4>🚫 Service Unavailable</h4>
                            <p>Unable to contact the AI advisor right now.</p>
                            <p><strong>Error:</strong> {str(e)}</p>
                            <p><em>Please try again later or use the other features of the app.</em></p>
                        </div>
                        """
                        st.markdown(error_msg, unsafe_allow_html=True)
                        reply = "I'm experiencing technical difficulties right now. Please try again later."
        
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": reply}
        )


__all__ = ["render"]

