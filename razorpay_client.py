import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

client = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

def create_razorpay_order(amount_in_inr: float):
    try:
        # Razorpay expects amount in paise (₹1 = 100 paise)
        amount_in_paise = int(amount_in_inr * 100)
        
        # Test intentional failure scenario
        if amount_in_inr <= 0:
            raise ValueError("Amount must be greater than 0")

        order_data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1
        }
        order = client.order.create(data=order_data)
        return {"status": "SUCCESS", "order_id": order["id"], "amount": amount_in_inr}
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}

# Quick test run
if __name__ == "__main__":
    print(create_razorpay_order(2500))