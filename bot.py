import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

# টোকেন ও চ্যানেল আইডি এখানে বসাতে হবে
TOKEN = "8637183628:AAGgp96gEmGpJ6tnZiTA_4e6xNTTgo1t0hA"
DB_CHANNEL_ID = "-1003995039828"      # ডাটাবেজ চ্যানেলের নেগেটিভ আইডি
WITHDRAW_CHANNEL_ID = "-1004474241535" # পেমেন্ট উইথড্র রিকোয়েস্ট চ্যানেলের আইডি

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

USER_MESSAGES = {}

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    if user_id not in USER_MESSAGES:
        initial_text = f"User ID: {user_id}\nName: {user_name}\nPoints: 0"
        try:
            sent_msg = await bot.send_message(chat_id=DB_CHANNEL_ID, text=initial_text)
            USER_MESSAGES[user_id] = sent_msg.message_id
            await message.answer(f"স্বাগতম {user_name}! SohojAaybot-এ আপনার অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে।")
        except Exception as e:
            await message.answer("টেকনিক্যাল সমস্যার কারণে অ্যাকাউন্ট তৈরি করা যায়নি। পরে চেষ্টা করুন।")
    else:
        await message.answer("আপনি ইতিমধ্যে রেজিস্টার্ড আছেন!")

# উইথড্র রিকোয়েস্ট হ্যান্ডেল করার ফাংশন
async def handle_withdraw_request(user_id: int, name: str, method: str, account: str, points: int, taka: str):
    withdraw_message = (
        f"🚨 **নতুন উইথড্র রিকোয়েস্ট!** 🚨\n\n"
        f"👤 **ইউজার নাম:** {name}\n"
        f"🆔 **ইউজার আইডি:** `{user_id}`\n"
        f"💳 **মেথড:** {method}\n"
        f"📱 **নম্বর/ওয়ালেট:** `{account}`\n"
        f"💰 **কাটা হবে:** {points} পয়েন্ট\n"
        f"💵 **পেমেন্ট পরিমাণ:** ৳{taka}\n\n"
        f"*(টাকা পাঠিয়ে চ্যানেল থেকে মেসেজটি পিন বা ডিলিট করে দিন)*"
    )

    try:
        await bot.send_message(chat_id=WITHDRAW_CHANNEL_ID, text=withdraw_message, parse_mode="Markdown")
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

dp.include_router(router)

async def main():
    print("SohojAaybot স্টার্ট হচ্ছে...")
    run_duration = 21300 # ৫ ঘণ্টা ৫৫ মিনিট
    start_time = time.time()

    polling_task = asyncio.create_task(dp.start_polling(bot))

    while time.time() - start_time < run_duration:
        await asyncio.sleep(60)

    print("সার্ভার আপডেট হচ্ছে, দয়া করে ৫ থেকে ৬ মিনিট পর আবার চেষ্টা করুন।")
    await dp.stop_polling()
    bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
