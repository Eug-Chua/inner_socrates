import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters,
)
from dotenv import load_dotenv
from src.prompts import (
    thought_of_the_day, coach_insight, executive_assistant,
    obsidian_ai, socratic_questioner, pattern_detective
)

# ── ENV ─────────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]

# ── STATE ───────────────────────────────────────────
pending_noise_input, pending_examine_input = {}, {}

# ── MAIN MENU KEYBOARD & HELPER ────────────────────
MAIN_KB = InlineKeyboardMarkup([
    [InlineKeyboardButton("🧠 Today's Musing",               callback_data="thought")],
    [InlineKeyboardButton("🔍 Turn Noise into Next Steps",    callback_data="steps")],
    [InlineKeyboardButton("🧩 Examine Your Unexamined Thoughts", callback_data="examine")],
])

async def show_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE, *, edit=False):
    text = "🌞 I'm your inner Socrates.\nTap a button to begin your mental upgrade:"
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=MAIN_KB)
    else:
        await update.message.reply_text(text, reply_markup=MAIN_KB)

# ── HANDLERS ───────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await show_menu(update, ctx)          # initial menu

async def handle_thought(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(thought_of_the_day(),
                                                  reply_markup=InlineKeyboardMarkup(
                                                      [[InlineKeyboardButton("↩️ Back", callback_data="back_to_menu")]]
                                                  ))

async def handle_steps_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_noise_input[user_id] = True
    await update.callback_query.answer()
    kb_noise = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 Genius Coach",       callback_data="noise_coach")],
        [InlineKeyboardButton("🗂 Executive Assistant", callback_data="noise_exec")],
        [InlineKeyboardButton("📓 ObsidianAI",          callback_data="noise_obsidian")],
        [InlineKeyboardButton("↩️ Back",               callback_data="back_to_menu")],
    ])
    await update.callback_query.edit_message_text(
        "💡 Drop your thoughts here. I’ll help you turn your noise into next steps.",
        reply_markup=kb_noise)

async def handle_noise_lens_choice(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query   = ctx.user_data.get("noise_text", "")
    cb      = update.callback_query.data
    await update.callback_query.answer()
    result = (
        coach_insight(query)        if cb == "noise_coach"   else
        executive_assistant(query)  if cb == "noise_exec"    else
        obsidian_ai(query)          if cb == "noise_obsidian" else
        "⚠️ Something went wrong."
    )
    await update.callback_query.edit_message_text(result, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Back", callback_data="back_to_menu")]]))

async def handle_examine_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_examine_input[user_id] = True
    await update.callback_query.answer()
    kb_ex = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Socratic Questioner", callback_data="examine_socratic")],
        [InlineKeyboardButton("🧠 Pattern Detective",   callback_data="examine_pattern")],
        [InlineKeyboardButton("📓 ObsidianAI",          callback_data="examine_obsidian")],
        [InlineKeyboardButton("↩️ Back",               callback_data="back_to_menu")],
    ])
    await update.callback_query.edit_message_text("🧐 Share what's on your mind. Let's deepen them.",
                                                  reply_markup=kb_ex)

async def handle_examine_lens_choice(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query   = ctx.user_data.get("examine_text", "")
    cb      = update.callback_query.data
    await update.callback_query.answer()
    result = (
        socratic_questioner(query)  if cb == "examine_socratic" else
        pattern_detective(query)    if cb == "examine_pattern"  else
        obsidian_ai(query)          if cb == "examine_obsidian" else
        "⚠️ Something went wrong."
    )
    await update.callback_query.edit_message_text(result, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ Back", callback_data="back_to_menu")]]))

async def back_to_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await show_menu(update, ctx, edit=True)

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # unchanged logic; your message handler stays the same
    ...

# ── BUILD APPLICATION ──────────────────────────────
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_thought,           pattern="^thought$"))
app.add_handler(CallbackQueryHandler(handle_steps_button,      pattern="^steps$"))
app.add_handler(CallbackQueryHandler(handle_examine_button,    pattern="^examine$"))
app.add_handler(CallbackQueryHandler(handle_noise_lens_choice,    pattern="^noise_.*$"))
app.add_handler(CallbackQueryHandler(handle_examine_lens_choice,  pattern="^examine_.*$"))
app.add_handler(CallbackQueryHandler(back_to_menu,             pattern="^back_to_menu$"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ── ENTRYPOINT (polling) ───────────────────────────
if __name__ == "__main__":
    print("📡 running in long-polling mode …")
    app.run_polling(
        allowed_updates     = Update.ALL_TYPES,
        reset_webhook       = True,   # nuke old pollers & webhooks
        drop_pending_updates= True,
        stop_signals        = None,
        close_loop          = False,
    )
