import sys
import os
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
    noise_to_next_steps,
    examine_the_unexamined,
)


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")


# 🧠 Thought for the Day (button handler)
async def handle_thought(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = thought_of_the_day()
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(message_text)

# 🔍 Noise to Next Steps — waits for user to send input
pending_steps = {}

async def handle_steps_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_steps[user_id] = True
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "💡 Drop your thoughts here. I’ll help you turn your noise into next steps."
    )

# 🧩 Examine the Unexamined — waits for user to send input
pending_examine = {}

async def handle_examine_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_examine[user_id] = True
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("🧐 Share what's on your mind. Let's deepen them.")

# Handles all incoming text based on previous button context

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = update.message.text.strip()

    if pending_steps.pop(user_id, False):
        message_text = noise_to_next_steps(query)
        await update.message.reply_text(message_text, parse_mode="HTML")

        return

    if pending_examine.pop(user_id, False):
        message_text = examine_the_unexamined(query)
        await update.message.reply_text(message_text, parse_mode="HTML")

        return

    # Catch-all
    await update.message.reply_text("🧭 Pick a button below to guide the kind of reflection you're looking for. Try /start.")


# /start command with button UI
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Thought for the Day", callback_data="thought")],
        [InlineKeyboardButton("🔍 Turn Noise into Next Steps", callback_data="steps")],
        [InlineKeyboardButton("🧩 Examine Your Unexamined Thoughts", callback_data="examine")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🌞 I'm Socrates... if he were on Twitter.\nTap a button below to begin your daily mental upgrade:",
        reply_markup=reply_markup,
    )

# App entrypoint
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_thought, pattern="^thought$"))
    app.add_handler(CallbackQueryHandler(handle_steps_button, pattern="^steps$"))
    app.add_handler(CallbackQueryHandler(handle_examine_button, pattern="^examine$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("📡 Twitter Socrates is thinking...")
    app.run_polling()

if __name__ == "__main__":
    main()

