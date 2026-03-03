import streamlit as st

from ui import dashboard, goal_planner, risk_analysis, chatbot


# Custom CSS for better overall styling
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global styles with blue, red, green, and golden theme
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e40af 0%, #dc2626 50%, #16a34a 100%);
    }
    .stSelectbox > div > div > select {
        background-color: white;
        border: 2px solid #fbbf24;
    }
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #dc2626 33%, #16a34a 66%, #fbbf24 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .metric-card {
        background: linear-gradient(135deg, #fef3c7 0%, #ffffff 100%);
        border-left: 4px solid #fbbf24;
        box-shadow: 0 4px 6px rgba(251, 191, 36, 0.2);
    }
    .form-section {
        background: linear-gradient(135deg, #dbeafe 0%, #ffffff 100%);
        border: 2px solid #1e40af;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #dc2626 0%, #16a34a 100%);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #1e40af 0%, #dc2626 100%);
        border: none;
        color: white;
        font-weight: bold;
    }
    .stButton > button[kind="secondary"] {
        background: linear-gradient(90deg, #16a34a 0%, #fbbf24 100%);
        border: none;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


PAGES = {
    "� Dashboard": dashboard.render,
    "🔴 Risk analysis": risk_analysis.render,
    "🟢 Goal planner": goal_planner.render,
    "🟡 Chatbot": chatbot.render,
}


def main() -> None:
    """Navigation and routing between modular UI pages."""
    with st.sidebar:
        st.markdown('<h1 style="color: white; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">💰 AI Financial Advisor</h1>', unsafe_allow_html=True)
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        page_name = st.selectbox(
            "📍 Navigate to:", 
            list(PAGES.keys()),
            index=0,
            key="page_selector"
        )
        
        st.markdown("---")
        st.markdown("""
        <div style="color: white; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 8px; border: 2px solid #fbbf24;">
        <h4 style="color: #fbbf24;">📋 Quick Start Guide</h4>
        <p><strong style="color: #1e40af;">1️⃣ Dashboard:</strong> Enter your financial data</p>
        <p><strong style="color: #dc2626;">2️⃣ Risk Analysis:</strong> Understand your risk profile</p>
        <p><strong style="color: #16a34a;">3️⃣ Goal Planner:</strong> Plan your financial goals</p>
        <p><strong style="color: #fbbf24;">4️⃣ Chatbot:</strong> Get AI-powered advice</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add footer
        st.markdown("""
        <div style="color: white; text-align: center; margin-top: 20px; font-size: 12px; border-top: 2px solid #fbbf24; padding-top: 10px;">
        <p style="color: #fbbf24;">💡 <em>For educational purposes only</em></p>
        <p>Not professional financial advice</p>
        </div>
        """, unsafe_allow_html=True)

    render_page = PAGES[page_name]
    render_page()


if __name__ == "__main__":
    main()

