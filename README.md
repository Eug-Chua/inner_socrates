# DM Socrates - A Telegram Bot for Deep Thinking
A Telegram-based insight generator that combines philosophical depth, shadow work, and strategic clarity — in under 1 minute.

## What It Does
- Dispenses daily “thought bombs” from stylized philosophers like Socrates, Nietzsche, or Kant
- Automatically follows up with penetrating shadow-work questions

It also lets you submit your own thoughts and choose how to process them:
- **Leadership Coach**: Expands your thinking to unlock your hidden potential
- **Executive Assistant**: Turns scattered ideas into prioritized task lists 
- **Socratic Questioner**: identify unexamined assumptions and gaps in your thinking
- **Pattern Detective**: Reveals invisible patterns of thought you’re not saying directly
- **ObsidianAI**: Surfaces meta-patterns and second-order implications

## How It Works
- Built using `python-telegram-bot` with `async` handlers
- Uses **OpenAI's GPT API** to generate insights and reflection prompts
- Hosted on [Railway](https://railway.app) using a **webhook-based deployment**
- Keeps track of user states (stages like "input", "lens", etc.) for smooth UX

## Getting Started
### Local Development
```
# 1. Clone the repo
git clone https://github.com/yourusername/inner-socrates.git && cd inner-socrates

# 2. Create a .env file
cp .env.example .env
# Fill in: TELEGRAM_TOKEN, OPENAI_API_KEY, OPENAI_GPT_MODEL_BASIC, OPENAI_GPT_MODEL_ADVANCED

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run it locally
python main.py
```

### Deploying to Railway
1. Go to https://railway.app and create a new project
2. Connect your GitHub repo
3. Set the following environment variables under Settings > Variables:
    - `TELEGRAM_TOKEN`
    - `OPENAI_API_KEY`
    - `OPENAI_GPT_MODEL_BASIC`
    - `OPENAI_GPT_MODEL_ADVANCED`
4. Railway will auto-deploy on push
5. Your webhook is auto-registered when the app boots on Railway (uses `start_webhook()` binding to Railway’s `$PORT`)

## Folder Structure
```
.
├── bot
│   └── main.py
├── src
│   ├── examine_prompts.py
│   ├── noise_prompts.py
│   └── thought.py
├── README.md
├── requirements.txt
└── .env
```

## Configuration
| Key                         | Description                     |
| --------------------------- | ------------------------------- |
| `TELEGRAM_TOKEN`            | Your bot’s token from BotFather |
| `TELEGRAM_CHAT_ID`          | Your Telegram chat ID           |
| `OPENAI_API_KEY`            | Your OpenAI secret key          |
| `OPENAI_GPT_MODEL_BASIC`    | For quick creative completions  |
| `OPENAI_GPT_MODEL_ADVANCED` | For longer, structured prompts  |
| `WEBHOOK_URL`               | Your Railway webhook            |


## Licence
MIT License.