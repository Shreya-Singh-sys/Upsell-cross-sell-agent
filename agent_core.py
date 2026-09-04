import json
import datetime
from razorpay_client import create_razorpay_order

# Audit Trail Ledger
audit_log = []

def log_action(action: str, reasoning: str, status: str):
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "reasoning": reasoning,
        "status": status
    }
    audit_log.append(entry)
    print(f"[AUDIT LOG] {json.dumps(entry, indent=2)}")

def evaluate_and_checkout(cart_items: list, max_budget: float):
    total_amount = sum(item['price'] for item in cart_items)
    
    # 1. Bounded & Gated Check
    log_action("CHECK_BUDGET", f"Checking if total ₹{total_amount} <= budget ₹{max_budget}", "PENDING")
    
    if total_amount > max_budget:
        log_action("CHECK_BUDGET", f"Amount ₹{total_amount} exceeds budget ₹{max_budget}", "BLOCKED")
        return {
            "status": "BLOCKED",
            "message": f"Cart total (₹{total_amount}) exceeds user budget cap (₹{max_budget}). Transaction stopped."
        }
    
    log_action("CHECK_BUDGET", "Budget criteria satisfied.", "PASSED")
    
    # 2. Execute Payment Action
    log_action("CREATE_RAZORPAY_ORDER", f"Initiating order creation for ₹{total_amount}", "EXECUTING")
    response = create_razorpay_order(total_amount)
    
    if response["status"] == "SUCCESS":
        log_action("CREATE_RAZORPAY_ORDER", f"Order created successfully: {response['order_id']}", "SUCCESS")
    else:
        log_action("CREATE_RAZORPAY_ORDER", f"Razorpay API Error: {response['error']}", "FAILED")
        
    return response

if __name__ == "__main__":
    with open("catalog.json") as f:
        catalog = json.load(f)

    print("\n--- Test 1: Within Budget (Success Flow) ---")
    cart = [catalog[0]] # ₹2500 item
    res1 = evaluate_and_checkout(cart, max_budget=3000)
    
    print("\n--- Test 2: Over Budget (Gated Block Flow) ---")
    cart = [catalog[0], catalog[2]] # ₹2500 + ₹1800 = ₹4300
    res2 = evaluate_and_checkout(cart, max_budget=3000)