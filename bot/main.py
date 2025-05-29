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
    obsidian_ai, socratic_questioner, pattern_detective, reflection_questions
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
    ctx.user_data["stage"] = "main"
    await show_menu(update, ctx)

async def handle_thought(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    # ── 1) Generate content ──────────────────────────
    thought   = thought_of_the_day()
    questions = reflection_questions(thought)

    # ── 2) Edit the original message to show the thought
    await update.callback_query.edit_message_text(
        thought,
        parse_mode="HTML"
    )

    # ── 3) Push a NEW message with the Back button
    await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"<b>Shadow-Work Reflections</b>\n\n{questions}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("↩️ Back", callback_data="back_to_menu")]]
        )
    )

    # track where we are for Back navigation
    ctx.user_data["stage"] = "thought_reflection"


async def handle_steps_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_noise_input[user_id] = True
    ctx.user_data['stage'] = 'noise_prompt'
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "💡 Drop your thoughts below. I’ll help you turn your noise into next steps.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("↩️ Back", callback_data="back_to_menu")]]
        ),
    )

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
    
    ctx.user_data["stage"] = "noise_lenses"

async def handle_examine_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pending_examine_input[user_id] = True
    ctx.user_data['stage'] = 'examine_prompt'
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🧘‍♂️ Share what's on your mind. Let's deepen it.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("↩️ Back", callback_data="back_to_menu")]]
        ),
    )

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
    
    ctx.user_data["stage"] = "examine_lenses"

async def back_to_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    stage = ctx.user_data.get("stage")

    if stage == "noise_prompt":
        await show_menu(update, ctx, edit=True)

    elif stage == "noise_lenses":
        # rebuild the same kb used earlier
        kb_noise = InlineKeyboardMarkup([
            [InlineKeyboardButton("🖋️ Leadership Coach",       callback_data="noise_coach")],
            [InlineKeyboardButton("🗂 Executive Assistant", callback_data="noise_exec")],
            [InlineKeyboardButton("🤖 ObsidianAI",          callback_data="noise_obsidian")],
            [InlineKeyboardButton("↩️ Back",               callback_data="back_to_menu")],
        ])
        await update.callback_query.edit_message_text(
            "Choose how to process your thoughts:", reply_markup=kb_noise
        )
        # move back one step
        ctx.user_data["stage"] = "noise_prompt"

    elif stage == "examine_prompt":
        await show_menu(update, ctx, edit=True)

    elif stage == "examine_lenses":
        kb_ex = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡️ Socratic Questioner", callback_data="examine_socratic")],
            [InlineKeyboardButton("🫆 Pattern Detective",   callback_data="examine_pattern")],
            [InlineKeyboardButton("🤖 ObsidianAI",          callback_data="examine_obsidian")],
            [InlineKeyboardButton("↩️ Back",               callback_data="back_to_menu")],
        ])
        await update.callback_query.edit_message_text(
            "Choose your lens of inquiry:", reply_markup=kb_ex
        )
        ctx.user_data["stage"] = "examine_prompt"

    elif stage == "thought_reflection":
        await show_menu(update, ctx, edit=True)
        ctx.user_data["stage"] = "main"

    else:
        # default: main menu
        await show_menu(update, ctx, edit=True)
        ctx.user_data["stage"] = "main"


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text    = update.message.text.strip()

    if pending_noise_input.pop(user_id, False):
        ctx.user_data["noise_text"] = text
        ctx.user_data['stage'] = 'noise_lenses'
        kb_noise = InlineKeyboardMarkup([
            [InlineKeyboardButton("🖋️ Leadership Coach",       callback_data="noise_coach")],
            [InlineKeyboardButton("🗂 Executive Assistant", callback_data="noise_exec")],
            [InlineKeyboardButton("🤖 ObsidianAI",          callback_data="noise_obsidian")],
            [InlineKeyboardButton("↩️ Back",               callback_data="back_to_menu")],
        ])
        await update.message.reply_text("🧠 Choose how to process your thoughts:", reply_markup=kb_noise)
        return

    if pending_examine_input.pop(user_id, False):
        ctx.user_data["examine_text"] = text
        ctx.user_data['stage'] = 'examine_lenses'
        kb_ex = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡️ Socratic Questioner", callback_data="examine_socratic")],
            [InlineKeyboardButton("🫆 Pattern Detective",   callback_data="examine_pattern")],
            [InlineKeyboardButton("🤖 ObsidianAI",          callback_data="examine_obsidian")],
            [InlineKeyboardButton("↩️ Back",               callback_data="back_to_menu")],
        ])
        await update.message.reply_text("Choose your lens of inquiry:", reply_markup=kb_ex)
        return

    await update.message.reply_text("🧭 Try /start and choose a reflection path.")

async def end_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # clear any pending multi-step states
    pending_noise_input.pop(user_id, None)
    pending_examine_input.pop(user_id, None)
    ctx.user_data.clear()
    await update.message.reply_text(
        "✅ Convo ended. Type /start whenever you’d like another cognitive boost."
    )

# ── BUILD APPLICATION ──────────────────────────────
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("end", end_cmd))
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
        drop_pending_updates= True,
        stop_signals        = None,
        close_loop          = False,
    )
