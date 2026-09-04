# import streamlit as st
# import streamlit.components.v1 as components
# from agent_llm import agent_executor
# from agent_core import audit_log

# st.set_page_config(page_title="Razorpay Agentic Commerce Engine", layout="wide")

# st.markdown("""
#     <style>
#     .main-header {font-size:26px; font-weight:bold; color:#072654;}
#     .audit-card {padding:10px; border-radius:5px; background-color:#f8f9fa; margin-bottom:8px;}
#     </style>
# """, unsafe_allow_html=True)

# st.markdown("<div class='main-header'>⚡ Agentic Commerce Engine — Track 01</div>", unsafe_allow_html=True)
# st.caption("AI Growth, Dynamic Upselling, Budget Guardrails & Razorpay Payment Integration")

# col_chat, col_audit = st.columns([3, 2])

# # Sidebar Controls for Failure Simulation
# with st.sidebar:
#     st.header("⚙️ Hackathon Demo Controls")
#     simulate_fail = st.toggle("Simulate Payment Failure", value=False)
#     st.info("Toggle this ON to showcase how the agent gracefully recovers from Razorpay API errors.")

# # Right Column: Live Audit Trail
# with col_audit:
#     st.subheader("🛡️ Real-Time Audit Ledger")
#     audit_container = st.empty()

# def render_audit_trail():
#     with audit_container.container():
#         for log in reversed(audit_log):
#             color = "🟢" if log['status'] in ['SUCCESS', 'PASSED'] else ("🔴" if log['status'] in ['BLOCKED', 'FAILED'] else "🟡")
#             st.markdown(f"**{color} {log['action']}** (`{log['status']}`)")
#             st.caption(f"_{log['timestamp']}_ | {log['reasoning']}")
#             st.divider()

# render_audit_trail()

# # Left Column: Interactive Chat Interface
# with col_chat:
#     st.subheader("💬 AI Commerce Agent")
    
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if user_input := st.chat_input("Ask agent to shop... (e.g. 'Buy me a keyboard under 2000')"):
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.markdown(user_input)

#         with st.chat_message("assistant"):
#             response = agent_executor.invoke({"input": user_input})
#             output_text = response["output"]
#             st.markdown(output_text)

#             # Embed Razorpay Checkout Modal Button HTML dynamically if order ID is in response
#             if "order_" in output_text:
#                 st.success("💳 Live Razorpay Payment Modal Ready:")
#                 # Razorpay Checkout Button Script (Test Mode)
#                 razorpay_html = """
#                 <button id="rzp-button" style="background-color:#146ef5; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">
#                     Pay Now via Razorpay
#                 </button>
#                 <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
#                 <script>
#                 document.getElementById('rzp-button').onclick = function(e){
#                     var options = {
#                         "key": "rzp_test_YOUR_KEY", 
#                         "amount": "225000",
#                         "currency": "INR",
#                         "name": "Agentic Commerce Demo",
#                         "description": "AI Autonomous Purchase",
#                         "handler": function (response){
#                             alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
#                         }
#                     };
#                     var rzp1 = new Razorpay(options);
#                     rzp1.open();
#                     e.preventDefault();
#                 }
#                 </script>
#                 """
#                 components.html(razorpay_html, height=60)

#         st.session_state.messages.append({"role": "assistant", "content": output_text})
#         render_audit_trail()

import os
import re
import streamlit as st
import streamlit.components.v1 as components
from agent_llm import agent_executor
from agent_core import audit_log

# Page Configuration
st.set_page_config(
    page_title="Razorpay Agentic Commerce Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Theme
st.markdown("""
    <style>
    /* Dark Theme Base & Typography */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Header Container */
    .header-box {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .main-title {
        font-size: 28px;
        font-weight: 800;
        color: #58a6ff;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sub-title {
        font-size: 14px;
        color: #8b949e;
        margin-top: 4px;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 20px;
        font-weight: bold;
        color: #f0f6fc;
    }
    .metric-label {
        font-size: 11px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Audit Log Styling */
    .audit-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        max-height: 520px;
        overflow-y: auto;
    }
    .audit-item {
        background-color: #0d1117;
        border-left: 4px solid #30363d;
        padding: 10px 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .audit-item.SUCCESS { border-left-color: #2ea043; }
    .audit-item.PASSED { border-left-color: #2ea043; }
    .audit-item.BLOCKED { border-left-color: #da3633; }
    .audit-item.FAILED { border-left-color: #da3633; }
    .audit-item.EXECUTING { border-left-color: #d29922; }

    .badge {
        font-size: 10px;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    .badge-success { background-color: rgba(46, 160, 67, 0.15); color: #3fb950; }
    .badge-danger { background-color: rgba(218, 54, 51, 0.15); color: #f85149; }
    .badge-warning { background-color: rgba(210, 153, 34, 0.15); color: #d29922; }

    /* Hide default Streamlit padding */
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# Top Header
st.markdown("""
    <div class="header-box">
        <div class="main-title">⚡ Agentic Commerce Engine <span style="font-size: 12px; background: #1f6feb; color: white; padding: 2px 8px; border-radius: 12px;">Track 01</span></div>
        <div class="sub-title">Razorpay Test Gateway • Dynamic Upsell • Bounded Spending Guardrail • Real-time Audit Trail</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Controls & Key Configs
with st.sidebar:
    st.image("https://razorpay.com/assets/razorpay-glyph.svg", width=40)
    st.title("Control Panel")
    st.divider()
    
    st.subheader("⚙️ Simulation Settings")
    simulate_fail = st.toggle("Simulate API Failure", value=False)
    st.caption("Triggers simulated payment gateway timeouts to demonstrate graceful failure recovery.")
    
    st.divider()
    
    # Live Key Status
    rzp_key = os.getenv("RAZORPAY_KEY_ID", "rzp_test_YOUR_KEY")
    st.markdown("**API Status:**")
    st.markdown("🟢 `Razorpay Test Mode`")
    st.markdown(f"🔑 Key: `{rzp_key[:12]}...`")

# Layout: Split into Chat and Audit Trail Side Panel
col_chat, col_audit = st.columns([3, 2], gap="medium")

# --- RIGHT COLUMN: Real-Time Audit Ledger ---
with col_audit:
    st.markdown("### 🛡️ Real-Time Audit Ledger")
    
    # Top Quick Metrics
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">Bounded</div>
                <div class="metric-label">Spending Guardrail</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">Active</div>
                <div class="metric-label">Agent Safety Gating</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    audit_container = st.empty()

def render_audit_trail():
    with audit_container.container():
        if not audit_log:
            st.info("No agent actions recorded yet. Start a interaction in the chat!")
            return
            
        st.markdown('<div class="audit-container">', unsafe_allow_html=True)
        for log in reversed(audit_log):
            status = log.get('status', 'PENDING')
            badge_class = "badge-success" if status in ['SUCCESS', 'PASSED'] else ("badge-danger" if status in ['BLOCKED', 'FAILED'] else "badge-warning")
            
            st.markdown(f"""
                <div class="audit-item {status}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <strong style="color:#f0f6fc; font-size:13px;">{log.get('action')}</strong>
                        <span class="badge {badge_class}">{status}</span>
                    </div>
                    <div style="font-size:11px; color:#8b949e; margin-top:4px;">{log.get('reasoning')}</div>
                    <div style="font-size:9px; color:#484f58; margin-top:4px;">⏰ {log.get('timestamp')}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

render_audit_trail()

# --- LEFT COLUMN: Chat Interface ---
with col_chat:
    st.markdown("### 💬 AI Agent Interface")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if user_input := st.chat_input("Ask agent to shop... (e.g., 'I want a keyboard under ₹3000')"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Agent evaluating catalog & guardrails..."):
                response = agent_executor.invoke({"input": user_input})
                output_text = response.get("output", "")
                st.markdown(output_text)

            # Dynamic Razorpay Payment Button Embedding
            if "order_" in output_text:
                st.divider()
                st.markdown("#### 💳 Instant Razorpay Checkout")
    
                rzp_key_id = os.getenv("RAZORPAY_KEY_ID", "rzp_test_YOUR_KEY")
    
                # 1. Dynamically extract Order ID from agent response
                order_id_match = re.search(r'order_[A-Za-z0-9]+', output_text)
                order_id_val = order_id_match.group(0) if order_id_match else ""
    
                # 2. Dynamically extract Total Amount from agent response (e.g., ₹4,300 -> 4300)
                amount_match = re.search(r' Total Amount:?\s*₹?([0-9,]+)', output_text, re.IGNORECASE) or \
                    re.search(r'₹([0-9,]+)', output_text)
                   
                if amount_match:
                    # Remove commas if present and convert to paise (x 100)
                    clean_amount = int(amount_match.group(1).replace(',', ''))
                    amount_in_paise = clean_amount * 100
                else:
                    amount_in_paise = 250000 # Fallback default
        
                # 3. Pass dynamic order_id and dynamic amount to Razorpay JS Checkout Options
                razorpay_html = f"""
               <div style="text-align:center; padding: 10px;">
               <button id="rzp-button" style="background: linear-gradient(135deg, #146ef5 0%, #084bbb 100%); color:white; padding:12px 28px; border:none; border-radius:8px; font-weight:bold; font-size:15px; cursor:pointer; box-shadow:0 4px 14px rgba(20,110,245,0.4);">
            ⚡ Pay ₹{amount_in_paise // 100:,} via Razorpay
               </button>
              </div>
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <script>
    document.getElementById('rzp-button').onclick = function(e){{
        var options = {{
            "key": "{rzp_key_id}", 
            "amount": "{amount_in_paise}",
            "currency": "INR",
            "name": "Agentic Commerce Order",
            "description": "AI Autonomous Purchase",
            "order_id": "{order_id_val}",
            "handler": function (response){{
                alert("Payment Successful! Razorpay Payment ID: " + response.razorpay_payment_id);
            }}
        }};
        var rzp1 = new Razorpay(options);
        rzp1.open();
        e.preventDefault();
    }}
    </script>
    """
        components.html(razorpay_html, height=650)
            # if "order_" in output_text:
            #     st.divider()
            #     st.markdown("#### 💳 Instant Razorpay Checkout")
                
            #     rzp_key_id = os.getenv("RAZORPAY_KEY_ID", "rzp_test_YOUR_KEY")
            #     razorpay_html = f"""
            #     <div style="text-align:center; padding: 10px;">
            #         <button id="rzp-button" style="background: linear-gradient(135deg, #146ef5 0%, #084bbb 100%); color:white; padding:12px 28px; border:none; border-radius:8px; font-weight:bold; font-size:15px; cursor:pointer; box-shadow:0 4px 14px rgba(20,110,245,0.4);">
            #             ⚡ Pay Now via Razorpay
            #         </button>
            #     </div>
            #     <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
            #     <script>
            #     document.getElementById('rzp-button').onclick = function(e){{
            #         var options = {{
            #             "key": "{rzp_key_id}", 
            #             "amount": "250000",
            #             "currency": "INR",
            #             "name": "Agentic Commerce Order",
            #             "description": "AI Autonomous Purchase",
            #             "handler": function (response){{
            #                 alert("Payment Successful! Razorpay Payment ID: " + response.razorpay_payment_id);
            #             }}
            #         }};
            #         var rzp1 = new Razorpay(options);
            #         rzp1.open();
            #         e.preventDefault();
            #     }}
            #     </script>
            #     """
            #     components.html(razorpay_html, height=550)

        st.session_state.messages.append({"role": "assistant", "content": output_text})
        render_audit_trail()