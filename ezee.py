import requests
import json
import time
import os

# =========================
# CONFIG
# =========================

BOT_TOKEN = "8629429297:AAGB-GLWLLIsT70kHJLjR9fEOiAffiymuSQ"

EXTERNAL_API_URL = "https://exploitsindia.site/lookup/number.php?exploits="

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

OWNER_USERNAME = "@wooninjae"

# =========================
# CREDIT SYSTEM
# =========================

USER_FILE = "users.json"

def load_users():

    if not os.path.exists(USER_FILE):

        with open(USER_FILE, "w") as f:
            json.dump({}, f)

    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):

    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def get_credit(user_id):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:

        users[user_id] = {
            "credits": 3
        }

        save_users(users)

    return users[user_id]["credits"]

def remove_credit(user_id):

    users = load_users()

    user_id = str(user_id)

    if users[user_id]["credits"] > 0:

        users[user_id]["credits"] -= 1

    save_users(users)

# =========================
# TELEGRAM FUNCTIONS
# =========================

def send_message(chat_id, text, reply_markup=None, parse_mode=None):

    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:

        response = requests.post(url, data=payload)

        return response.json()

    except Exception as e:

        print("Send Message Error:", e)

def get_updates(offset=None):

    url = f"{BASE_URL}/getUpdates"

    params = {
        "timeout": 30
    }

    if offset:
        params["offset"] = offset

    try:

        response = requests.get(url, params=params)

        return response.json()

    except Exception as e:

        print("Get Updates Error:", e)

        return {}

# =========================
# KEYBOARD
# =========================

reply_keyboard = {
    "keyboard": [
        [
            {
                "text": "📱 Phone Lookup"
            }
        ],
        [
            {
                "text": "💳 My Credits"
            }
        ]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}

# =========================
# API LOOKUP
# =========================

def phone_lookup(number):

    try:

        final_url = f"{EXTERNAL_API_URL}{number}"

        response = requests.get(final_url)

        cleaned_text = response.text

        cleaned_text = cleaned_text.replace(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💳 BUY API : @wooninjae",
            ""
        )

        return cleaned_text

    except Exception as e:

        return f"Error: {str(e)}"

# =========================
# BUY MESSAGE
# =========================

def buy_message():

    return (
        "💎 BUY CREDITS\n\n"

        "💰 PRICING:\n"
        "• ₹100 = 15 Credits\n"
        "• ₹200 = 30 Credits\n"
        "• ₹500 = 100 Credits\n\n"

        "📩 Purchase Credits Here:\n"
        f"{OWNER_USERNAME}"
    )

# =========================
# MAIN BOT
# =========================

def main():

    print("Bot Started...")

    offset = None

    while True:

        updates = get_updates(offset)

        if updates.get("ok"):

            for update in updates["result"]:

                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                message = update["message"]

                chat_id = message["chat"]["id"]

                text = message.get("text", "").strip()

                # =========================
                # START
                # =========================

                if text == "/start":

                    credits = get_credit(chat_id)

                    welcome_text = (
                        "👋 Welcome To Premium Phone Lookup Bot\n\n"

                        "🎁 You received 3 free credits.\n\n"

                        f"💳 Your Credits: {credits}\n\n"

                        "Use button below to start lookup."
                    )

                    send_message(
                        chat_id,
                        welcome_text,
                        reply_markup=reply_keyboard
                    )

                # =========================
                # PHONE LOOKUP BUTTON
                # =========================

                elif text == "📱 Phone Lookup":

                    send_message(
                        chat_id,
                        "📞 Send 10 digit mobile number:"
                    )

                # =========================
                # MY CREDITS
                # =========================

                elif text == "💳 My Credits":

                    credits = get_credit(chat_id)

                    send_message(
                        chat_id,
                        (
                            f"💳 Your Remaining Credits: {credits}\n\n"
                            f"{buy_message()}"
                        )
                    )

                # =========================
                # NUMBER CHECK
                # =========================

                elif text.isdigit() and len(text) == 10:

                    credits = get_credit(chat_id)

                    if credits <= 0:

                        send_message(
                            chat_id,
                            (
                                "❌ Your credits are finished.\n\n"
                                f"{buy_message()}"
                            )
                        )

                    else:

                        send_message(
                            chat_id,
                            "🔍 Checking number..."
                        )

                        api_response = phone_lookup(text)

                        remove_credit(chat_id)

                        left_credit = get_credit(chat_id)

                        final_response = (
                            f"{api_response}\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"💳 You have left {left_credit} credit(s)\n\n"
                            f"{buy_message()}"
                        )

                        send_message(
                            chat_id,
                            f"<pre>{final_response}</pre>",
                            parse_mode="HTML"
                        )

                # =========================
                # INVALID INPUT
                # =========================

                else:

                    send_message(
                        chat_id,
                        (
                            "❌ Invalid Input\n\n"

                            "Please use:\n"
                            "• /start\n"
                            "• 📱 Phone Lookup\n"
                            "• 💳 My Credits\n"
                            "• Send 10 digit number"
                        )
                    )

        time.sleep(1)

# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
    main()
