import streamlit as st
from agent_llm import agent_executor
from agent_core import audit_log

st.set_page_config(page_title="Agentic Commerce Engine", layout="wide")
st.title("🛒 Agentic Commerce & Revenue Growth")

# Layout: Split into Chat and Audit Trail Side Panel
col_chat, col_audit = st.columns([3, 2])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- RIGHT COLUMN: Real-Time Audit Trail ---
with col_audit:
    st.subheader("🛡️ Real-Time Audit Trail")
    st.caption("Gated actions, spending checks & Razorpay API logs")
    audit_container = st.empty()

def render_audit_trail():
    with audit_container.container():
        for log in reversed(audit_log):
            color = "🟢" if log['status'] in ['SUCCESS', 'PASSED'] else ("🔴" if log['status'] in ['BLOCKED', 'FAILED'] else "🟡")
            st.markdown(f"**{color} {log['action']}** (`{log['status']}`)")
            st.caption(f"_{log['timestamp']}_ | {log['reasoning']}")
            st.divider()

render_audit_trail()

# --- LEFT COLUMN: Chat Interface ---
with col_chat:
    st.subheader("💬 AI Buyer / Assistant")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("What are you looking to buy? (e.g. 'I need a mechanical keyboard under ₹3000')"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            # Format chat history for agent execution
            history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
            response = agent_executor.invoke({"input": user_input, "chat_history": history})
            output_text = response["output"]
            st.markdown(output_text)
            
        st.session_state.messages.append({"role": "assistant", "content": output_text})
        render_audit_trail()