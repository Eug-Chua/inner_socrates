# DM Socrates - A Telegram Bot for Deep Thinking
Have you confused the aesthetic of deep thinking with the experience of it?

This Telegram bot combines deep questioning with strategic clarity for your own life—not by downloading insights into your brain, but by nudging you to discover them yourself.

## Why I Made This Bot
This bot was inspired by [Beyond the 'Matrix' Theory of the Mind](https://www.nytimes.com/2023/05/28/opinion/artificial-intelligence-thinking-minds-concentration.html).

In that article, the author draws out the fantasy many of us have:
> *If only we had a little jack in the back of our necks like in "The Matrix", we could download the knowledge of a book into ours heads (or, to use the movie’s example, a kung fu master), and then we'd have it, instantly.*

But that misses much of what’s really happening when we spend hours reading a book and thinking about it.

The time we have to spend with information, wrestling with it, being attentive to it — that’s where we draw connections, where we come to insights, where parts of us come into relationship with parts of it and something new emerges.

Part of what is happening when we spend seven hours reading a book is we spend seven hours with our minds on this topic. LLM outputs don't impress themselves upon us. 

They don't change us.

This bot aspires to fix that. It nudges and probes us into thinking deeper—not by giving us answers, but by helping us discover better questions. Because real understanding isn't downloaded; it's earned through the slow work of grappling with ideas until they become part of who we are.

## What It Does
- Dispenses truth bombs from stylized philosophers like Socrates, Nietzsche, or Kant
- Automatically follows up with penetrating shadow-work questions

It also lets you submit your own thoughts and choose how to process them:
- **Leadership Coach**: Expands your thinking to unlock your hidden potential
- **Executive Assistant**: Turns scattered ideas into actionable next steps
- **Socratic Questioner**: Discover unexamined assumptions and gaps in your thinking
- **Pattern Detective**: Observe invisible patterns of thought that remain unspoken
- **ObsidianAI**: Surfaces meta-patterns and second-order implications

## How It Works
- Built using `python-telegram-bot` with `async` handlers
- Uses **OpenAI's GPT API** to generate insights and reflection prompts
- Hosted on [Railway](https://railway.app) using a **webhook-based deployment**

## Requirements
- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- OpenAI API key
- Railway account (for deployment)

## Usage/Commands
- `/start` - Initialize the bot and get welcome message
- `/end` - End the conversation
- Simply tap on the "Musing of the Day" button to receive thought bombs or enter in your own thoughts
- Choose from different processing lenses: `Leadership Coach`, `Executive Assistant`, `Socratic Questioner`, `Pattern Detective`, or `ObsidianAI`.

## Getting Started
### Local Development

1. Clone the repo
```bash
git clone https://github.com/eug-chua/inner-socrates.git && cd inner-socrates
```

2. Create a .env file
```bash
cp .env.example .env
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run it locally
```bash
python bot/main.py
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
├── LICENSE
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



## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.