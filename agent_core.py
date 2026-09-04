# import json
# import datetime
# from razorpay_client import create_razorpay_order

# # Audit Trail Ledger
# audit_log = []

# def log_action(action: str, reasoning: str, status: str):
#     entry = {
#         "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "action": action,
#         "reasoning": reasoning,
#         "status": status
#     }
#     audit_log.append(entry)
#     print(f"[AUDIT LOG] {json.dumps(entry, indent=2)}")

# def evaluate_and_checkout(cart_items: list, max_budget: float):
#     total_amount = sum(item['price'] for item in cart_items)
    
#     # 1. Bounded & Gated Check
#     log_action("CHECK_BUDGET", f"Checking if total ₹{total_amount} <= budget ₹{max_budget}", "PENDING")
    
#     if total_amount > max_budget:
#         log_action("CHECK_BUDGET", f"Amount ₹{total_amount} exceeds budget ₹{max_budget}", "BLOCKED")
#         return {
#             "status": "BLOCKED",
#             "message": f"Cart total (₹{total_amount}) exceeds user budget cap (₹{max_budget}). Transaction stopped."
#         }
    
#     log_action("CHECK_BUDGET", "Budget criteria satisfied.", "PASSED")
    
#     # 2. Execute Payment Action
#     log_action("CREATE_RAZORPAY_ORDER", f"Initiating order creation for ₹{total_amount}", "EXECUTING")
#     response = create_razorpay_order(total_amount)
    
#     if response["status"] == "SUCCESS":
#         log_action("CREATE_RAZORPAY_ORDER", f"Order created successfully: {response['order_id']}", "SUCCESS")
#     else:
#         log_action("CREATE_RAZORPAY_ORDER", f"Razorpay API Error: {response['error']}", "FAILED")
        
#     return response
import json
import datetime
from razorpay_client import create_razorpay_order

audit_log = []

def log_action(action: str, reasoning: str, status: str):
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "reasoning": reasoning,
        "status": status
    }
    audit_log.append(entry)

def evaluate_and_checkout(cart_items: list, max_budget: float, apply_discount: bool = False, simulate_failure: bool = False):
    total_amount = sum(item['price'] for item in cart_items)
    
    # Feature 1: AI Negotiation / Discount Logic
    discount_applied = 0
    if total_amount > max_budget and apply_discount:
        log_action("AI_NEGOTIATION", f"Total ₹{total_amount} exceeds budget ₹{max_budget}. Evaluating dynamic 10% coupon.", "EVALUATING")
        discount_applied = total_amount * 0.10
        total_amount = total_amount - discount_applied
        log_action("AI_NEGOTIATION", f"Applied AI_SPECIAL_10 coupon. New Total: ₹{total_amount}", "SUCCESS")

    # Feature 2: Safety & Spending Gate
    log_action("CHECK_BUDGET", f"Validating total ₹{total_amount} against budget ₹{max_budget}", "PENDING")
    if total_amount > max_budget:
        log_action("CHECK_BUDGET", f"Amount ₹{total_amount} exceeds budget cap ₹{max_budget}", "BLOCKED")
        return {
            "status": "BLOCKED",
            "message": f"Cart total (₹{total_amount}) exceeds budget (₹{max_budget}). Discount limit reached.",
            "can_negotiate": True
        }
    
    log_action("CHECK_BUDGET", "Spending criteria satisfied.", "PASSED")

    # Feature 3: Simulated Failure Handling
    if simulate_failure:
        log_action("PAYMENT_GATEWAY", "Simulating Razorpay Payment Timeout/Failure scenario.", "FAILED")
        return {
            "status": "FAILED",
            "reason": "Payment Gateway Timeout (Simulated). Agent recovery active.",
            "recovery_action": "Generated Razorpay Payment Link via SMS/Email as fallback."
        }

    # Execute Razorpay API Order Creation
    log_action("CREATE_RAZORPAY_ORDER", f"Creating Order for ₹{total_amount}", "EXECUTING")
    response = create_razorpay_order(total_amount)
    
    if response["status"] == "SUCCESS":
        response["discount_applied"] = discount_applied
        log_action("CREATE_RAZORPAY_ORDER", f"Razorpay Order Created: {response['order_id']}", "SUCCESS")
    else:
        log_action("CREATE_RAZORPAY_ORDER", f"Razorpay API Error: {response['error']}", "FAILED")
        
    return response
