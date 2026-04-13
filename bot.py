from flask import Flask, request, Response
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ---------------------------
# 🔐 USER SESSION STORAGE
# ---------------------------
user_data = {}

# ---------------------------
# 📧 EMAIL SETTINGS (EDIT THESE)
# ---------------------------
EMAIL_ADDRESS = "iamkariuki7@gmail.com"
EMAIL_PASSWORD = "fysh gjiz quhu upay"
RECEIVER_EMAIL = "iamkariuki7@gmail.com"


# ---------------------------
# 📧 SAFE EMAIL FUNCTION
# ---------------------------
def send_email(name, phone, email, items):
    try:
        body = f"""
📦 NEW BOOKING - FreshClean

👤 Name: {name}
📞 Phone: {phone}
📧 Email: {email}
🧺 Items: {items}
"""

        msg = MIMEText(body)
        msg["Subject"] = "New FreshClean Booking"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ EMAIL ERROR:", e)


# ---------------------------
# 🤖 MAIN BOT LOGIC
# ---------------------------
@app.route("/message", methods=["POST"])
def reply():
    print("🔥 REQUEST RECEIVED")

    incoming = request.form.get("Body")
    sender = request.form.get("From")

    if not incoming:
        incoming = ""
    incoming = incoming.strip().lower()

    # INIT USER
    if sender not in user_data:
        user_data[sender] = {"step": "start"}

    step = user_data[sender]["step"]

    # ---------------------------
    # 🟢 START
    # ---------------------------
    if incoming in ["hi", "hello", "hey"]:
        user_data[sender]["step"] = "menu"

        message = """✨ Welcome to FreshClean Dry Cleaners 👕✨

We keep your clothes fresh, clean, and perfectly styled!

🧺 Services:
1️⃣ Dresses 👗
2️⃣ Jackets 🧥
3️⃣ Laundry
4️⃣ Place Order
5️⃣ Location

Reply with a number 😊"""

    # ---------------------------
    # 📋 MENU
    # ---------------------------
    elif step == "menu":

        if incoming == "1":
            message = """👗 Dresses Cleaning:

• Light: 200 KES  
• Heavy: 300 KES  
• Delicate: 400 KES  

Reply *menu* or *order*"""

        elif incoming == "2":
            message = """🧥 Jackets Cleaning:

• Light: 250 KES  
• Heavy: 350 KES  
• Designer: 500 KES  

Reply *menu* or *order*"""

        elif incoming == "3":
            message = """🧺 Laundry:

• Wash & Fold: 150 KES/kg  
• Wash & Iron: 200 KES/kg  

Reply *menu* or *order*"""

        elif incoming in ["4", "order"]:
            user_data[sender]["step"] = "name"
            message = "😊 Please enter your *full name*:"

        elif incoming == "5":
            message = """📍 Location: Spur Mall

🕒 Hours:
Mon–Sat: 8AM–7PM  
Sun: 10AM–4PM"""

        elif incoming == "menu":
            message = "Reply 1-5 to continue 😊"

        else:
            message = "❗ Please choose 1–5"

    # ---------------------------
    # 🧍 NAME
    # ---------------------------
    elif step == "name":
        user_data[sender]["name"] = incoming
        user_data[sender]["step"] = "phone"
        message = "📞 Enter your phone number:"

    # ---------------------------
    # 📞 PHONE
    # ---------------------------
    elif step == "phone":
        user_data[sender]["phone"] = incoming
        user_data[sender]["step"] = "email"
        message = "📧 Enter your email address:"

    # ---------------------------
    # 📧 EMAIL
    # ---------------------------
    elif step == "email":
        user_data[sender]["email"] = incoming
        user_data[sender]["step"] = "items"
        message = "🧺 What items? (e.g. 2 dresses, 1 jacket)"

    # ---------------------------
    # 🧺 ITEMS + FINAL
    # ---------------------------
    elif step == "items":

        user_data[sender]["items"] = incoming

        # SEND EMAIL (SAFE)
        send_email(
            user_data[sender]["name"],
            user_data[sender]["phone"],
            user_data[sender]["email"],
            user_data[sender]["items"]
        )

        message = f"""✅ Order Confirmed!

Thank you {user_data[sender]['name']} 😊

🧺 Items: {user_data[sender]['items']}

📅 Pickup: Tomorrow after 2PM  
📍 Spur Mall

We’ll notify you when ready!

✨ FreshClean"""

        user_data[sender]["step"] = "done"

    # ---------------------------
    # 🔁 RESET
    # ---------------------------
    else:
        message = "👋 Type *hi* to start again"

    # ---------------------------
    # 📤 XML RESPONSE (IMPORTANT)
    # ---------------------------
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{message}</Message>
</Response>"""

    return Response(xml, status=200, headers={"Content-Type": "text/xml"})


# ---------------------------
# 🚀 RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
