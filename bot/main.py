import os
import asyncio
from aiohttp import web
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# ────────────────────────────────────────────────────────────
load_dotenv()
BOT_TOKEN   = os.getenv("TELEGRAM_TOKEN")
PUBLIC_URL  = os.getenv("WEBHOOK_URL")         # e.g. https://xxx.up.railway.app
PORT        = int(os.getenv("PORT", "8080"))   # Railway injects the right value
WEBHOOK_PATH = "/telegram"                     # one route for Telegram
WEBHOOK_URL  = f"{PUBLIC_URL}{WEBHOOK_PATH}"
# ────────────────────────────────────────────────────────────

# ─── tiny “OK” route for Railway ────────────────────────────
async def health(request):                      #  GET /
    return web.Response(text="✅ OK")

# ─── Telegram handlers (minimal demo) ───────────────────────
async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("Ping", callback_data="ping")]]
    await update.message.reply_text("Hi!", reply_markup=InlineKeyboardMarkup(kb))

async def on_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("pong⚡")

# ─── build PTB app ──────────────────────────────────────────
tg_app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)
tg_app.add_handler(CommandHandler("start", start_cmd))
tg_app.add_handler(CallbackQueryHandler(on_button, pattern="ping"))
tg_runner = tg_app.as_webhook_server(
    path        = WEBHOOK_PATH,
    listen      = None,          # we’ll attach it to the *same* aiohttp app
)

# ─── create ONE aiohttp application ─────────────────────────
aio_app = web.Application()
aio_app.router.add_get("/", health)             # GET /
aio_app.add_routes(tg_runner.web_app.router)    # mount Telegram routes

async def on_startup(app):
    # Initialise PTB and set webhook
    await tg_app.initialize()
    await tg_app.bot.set_webhook(url=WEBHOOK_URL)
    await tg_app.start()                        # start dispatcher

async def on_cleanup(app):
    await tg_app.stop()
    await tg_app.shutdown()

aio_app.on_startup.append(on_startup)
aio_app.on_cleanup.append(on_cleanup)

# ─── run the single aiohttp server ──────────────────────────
if __name__ == "__main__":
    web.run_app(aio_app, host="0.0.0.0", port=PORT)
