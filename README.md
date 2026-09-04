# ⚡ Razorpay Agentic Commerce & Revenue Growth Engine

An autonomous AI Agentic Commerce Engine powered by **Gemini 2.5 Flash**, **Razorpay Test Mode APIs**, and a real-time **Audit Trail Ledger**. The agent dynamically searches product catalogs, negotiates dynamic upsells/cross-sells, enforces strict spending guardrails, and triggers seamless Razorpay modal checkouts.

---

## 🌟 Key Architectural Features

- **Autonomous Tool Calling**: Gemini native function calling dynamically queries merchant inventories (`search_catalog`) and executes Razorpay payment orders (`process_checkout`).
- **Revenue Growth & Upsell Engine**: Maximizes merchant Average Order Value (AOV) by intelligently recommending cross-sell items within the user's explicit budget constraints.
- **Bounded Spending Guardrails**: Enforces explicit spending limits before payment generation. Every financial action is evaluated, gated, and approved/blocked autonomously.
- **Real-Time Explainability Audit Ledger**: A transparent, side-by-side audit trail logging every agent thought, tool execution, status code (`PASSED`, `BLOCKED`, `EXECUTING`), and API response in real time.
- **Graceful Failure Recovery**: Built-in simulation toggle to handle Razorpay API timeouts or payment declines without breaking chat continuity or state.
- **Interactive Fintech UI**: Enterprise dark-mode Streamlit dashboard with embedded Razorpay JS Checkout modal support.

---

## 🏗️ System Architecture & Workflow
```
[ User Prompt ]
│
▼
[ Gemini 2.5 Flash Agent ]
│
├─► [ Tool: search_catalog ] ──► Real-Time Product & Cross-Sell Search
│
├─► [ Safety Gate: Budget Check ] ──► Gated Spending Rules (PASSED / BLOCKED)
│
└─► [ Tool: process_checkout ] ──► Razorpay Order Creation API (order_...)
│
▼
[ Real-Time Audit Trail ] ◄───────────────── [ Streamlit Fintech UI ]
(Action Logs & Timestamps)                    (Embedded Razorpay Checkout)
```
## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10 or higher
- Razorpay Test Account Credentials (`Key ID` & `Key Secret`)
- Google AI Studio API Key (`GEMINI_API_KEY`)

### 2. Environment Setup

Clone the repository and install dependencies:

```bash
# Clone repository
git clone [https://github.com/YOUR_USERNAME/razorpay-agentic-commerce.git](https://github.com/YOUR_USERNAME/razorpay-agentic-commerce.git)
cd razorpay-agentic-commerce

# Create & activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```
### 3. Environment Variables Configuration

Create a .env file in the root directory:
```bash
RAZORPAY_KEY_ID="rzp_test_YOUR_KEY_ID"
RAZORPAY_KEY_SECRET="YOUR_KEY_SECRET"
GEMINI_API_KEY="AIzaSy_YOUR_GEMINI_API_KEY"
```
### 4. Run the Application

Launch the Streamlit dashboard:
```bash
streamlit run app.py
```
