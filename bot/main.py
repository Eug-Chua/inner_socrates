import os
import sys
import asyncio
import aiohttp
from aiohttp import web
import nest_asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from src.prompts import (
    thought_of_the_day,
    coach_insight,
    executive_assistant,
    obsidian_ai,
    socratic_questioner,
    pattern_detective,
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# State dictionaries
pending_noise_input = {}
pending_examine_input = {}

# Healthcheck route
async def healthcheck(request):
    return web.Response(text="✅ InnerSocrates bot is alive.")

async def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Healthcheck server started on port {port} (/).")

    # 👇 Force-ping the health endpoint after starting
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:{port}/") as resp:
                print(f"👋 Internal health ping: {resp.status}")
    except Exception as e:
        print(f"⚠️ Failed to self-ping: {e}")


# Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Today's Musing", callback_data="thought")],
        [InlineKeyboardButton("🔍 Turn Noise into Next Steps", callback_data="steps")],
        [InlineKeyboardButton("🧩 Examine Your Unexamined Thoughts", callback_data="examine")],
    ]
    await update.message.reply_text(
        "🌞 I'm your inner Socrates.\nTap a button below to begin your daily mental upgrade:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def handle_thought(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = thought_of_the_day()
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(message_text)

async def handle_steps_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_noise_input[user_id] = True
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("💡 Drop your thoughts here. I’ll help you turn your noise into next steps.")

async def handle_noise_lens_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = context.user_data.get("noise_text", "")
    callback = update.callback_query.data
    await update.callback_query.answer()

    if callback == "noise_coach":
        result = coach_insight(query)
    elif callback == "noise_exec":
        result = executive_assistant(query)
    elif callback == "noise_obsidian":
        result = obsidian_ai(query)
    else:
        result = "⚠️ Something went wrong. Please try again."

    await update.callback_query.edit_message_text(result, parse_mode="HTML")

async def handle_examine_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_examine_input[user_id] = True
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("🧐 Share what's on your mind. Let's deepen them.")

async def handle_examine_lens_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = context.user_data.get("examine_text", "")
    callback = update.callback_query.data
    await update.callback_query.answer()

    if callback == "examine_socratic":
        result = socratic_questioner(query)
    elif callback == "examine_pattern":
        result = pattern_detective(query)
    elif callback == "examine_obsidian":
        result = obsidian_ai(query)
    else:
        result = "⚠️ Something went wrong. Please try again."

    await update.callback_query.edit_message_text(result, parse_mode="HTML")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = update.message.text.strip()

    if pending_noise_input.pop(user_id, False):
        context.user_data["noise_text"] = query
        keyboard = [
            [InlineKeyboardButton("🧠 Genius Coach", callback_data="noise_coach")],
            [InlineKeyboardButton("🗂 Executive Assistant", callback_data="noise_exec")],
            [InlineKeyboardButton("📓 ObsidianAI", callback_data="noise_obsidian")],
        ]
        await update.message.reply_text("Choose how to process your thoughts:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if pending_examine_input.pop(user_id, False):
        context.user_data["examine_text"] = query
        keyboard = [
            [InlineKeyboardButton("❓ Socratic Questioner", callback_data="examine_socratic")],
            [InlineKeyboardButton("🧠 Pattern Detective", callback_data="examine_pattern")],
            [InlineKeyboardButton("📓 ObsidianAI", callback_data="examine_obsidian")],
        ]
        await update.message.reply_text("Choose your lens of inquiry:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text("🧭 Try /start and choose a reflection path.")

# Combined startup
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_thought, pattern="^thought$"))
    app.add_handler(CallbackQueryHandler(handle_steps_button, pattern="^steps$"))
    app.add_handler(CallbackQueryHandler(handle_examine_button, pattern="^examine$"))
    app.add_handler(CallbackQueryHandler(handle_noise_lens_choice, pattern="^noise_.*$"))
    app.add_handler(CallbackQueryHandler(handle_examine_lens_choice, pattern="^examine_.*$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    await app.bot.set_webhook(url=WEBHOOK_URL)

    print("✅ Webhook registered.")
    print("🚀 Starting healthcheck server AND Telegram webhook...")

    await start_health_server()  # this binds to Railway's PORT

    await app.start()
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=8443,  # Telegram webhook listener
        webhook_url=WEBHOOK_URL,
    )
    
    print("✅ Both servers started — waiting forever to keep Railway alive.")
    await asyncio.Event().wait()  # Keeps container alive


if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
