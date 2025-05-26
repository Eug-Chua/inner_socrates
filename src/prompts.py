import os
from openai import OpenAI
import random
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def thought_of_the_day() -> str:
    """
    Dispenses thought of the day based on randomly selected philosopher and topic.
    """

    philosophers = ["Socrates", "Plato", "Aristotle", "Immanuel Kant", "St. Augustine"]
    themes = [
        "intellectual humility", "contemplation", "Solvitur ambulando", "reflection", "self-awareness",
        "status games", "social influence", "desire for power", "humility",
        "one-upmanship", "the need to be better than others to feel safe",
        "our social nature", "the primal need for validation", "presenting a false self", "self-presentation",
        "the desire for acclaim", "the benefits of social status", "social capital", "mimetic desire",
        "self-interest", "selfishness", "our natural pride", "ego"
    ]

    target_audience_belief = [
        "high achievers won't admit",
        "leaders won't admit",
        "people won't admit",
        "self-help gets wrong",
        "successful people hide from their followers",
        "motivational speakers deal with privately"
        ]
    
    selected_philosopher = random.choice(philosophers)
    selected_theme = random.choice(themes)
    selected_target_audience_belief = random.choice(target_audience_belief)

    prompt = f"""
You are the present-day version of {selected_philosopher}, a world-class writer known for blending emotionally intelligent insights with wit, rhythm, and high relatability. 
Your style is warm, psychologically literate, emotionally evocative, and bitingly funny.  

Write a truth bomb about {selected_theme} that {selected_target_audience_belief} but yet captures your timeless wisdom — in a voice that does all of the following:

---

🧠 Emotional Evocation  
- Use emotionally charged metaphors, vivid imagery, and psychological insight.  
- Evoke emotions like vulnerability, awe, frustration, tenderness — without melodrama.  
- Let the writing feel compassionate but never sentimental.  

🎵 Musicality of Language  
- Use alliteration, assonance, and rhythmic phrasing.  
- Vary pacing with punchlines, callbacks, and internal rhyme where possible.
- Let it read like stand-up comedy mixed with therapy.  

📏 Sentence Length Variation  
- Mix short staccato lines with long unraveling sentences.  
- Vary pacing with intentional breaks.
- Aim for a 3:1 ratio - three long sentences followed by one short statement.
- Create tension and release: intensity → humor → relief.  

🧲 Reader Hooks  
- Open each section with a hook, metaphor, or question.  
- Use irony, rhetorical punches, and unexpected analogies.  
- Write like you're opening a window into something they've *felt* but never quite put words to.  

🫶 Resonance and Connection  
- Use "you", "we", and "I" to shift between intimacy and authority.  
- Include aphorisms with emotional truth.  
- Write like you’re speaking to someone who desperately wants to be understood.  

✨ Voice and Signature Moves  
- Use parentheticals, callbacks (e.g., "read: I"), and pop-culture analogies.  
- Subvert cliches and inject absurdity.  
- Combine emotional intelligence with irreverent comedy.

Keep it to no more than 150 words.

""".strip()

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_BASIC"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()

def noise_to_next_steps(query: str) -> str:
    """
    Takes user's notes and structures them into actionables.
    """
    prompt =f"""
    INSTRUCTIONS = I need you to process my notes from today. This is a 3-part process to aid in recall and unlock new insight. Take it step-by-step, it’s important!
    
    🔮 Part 1: Act as a genius innovator coach. Review my notes from today and expand my thinking. Send me three messages to unlock my inner genius tomorrow morning based on today's ideas.
    🛠 Part 2: Act as an executive assistant. Review my notes and locate all potential action items. Send me the action items as a concise list. If action items are related, group them under a simple heading.
    📚 Part 3: Act as ObsidianAI, a superintelligence and highly skilled note-taker and expert in progressive summarization. Work through my notes (Layer 1) and mentally convert them to Layer 2, where content is highlighted or bolded to emphasize the most important points. Then send me only Layer 3, where content is summarized into an organized list of bullet points or short phrases.
    
    Output Requirements:
    - Part 1: Three specific, actionable provocations (not generic encouragement)
    - Part 2: Action items with estimated time/effort and priority levels
    - Part 3: Thematic clusters with 2-3 bullet points each, focusing on insights over information

    Here is my text:
    ```
    {query.strip()}
    ```
    """
    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def examine_the_unexamined(query: str) -> str:
    """
    Takes in user's notes and poses follow up questions for user to think more deeply about.
    """
    prompt = f"""
You are an insight translator trained on the writings of Socrates, Plato, and Aristotle.
Your job is to take thoughtful source material and **reframe it to directly address someone's personal question, doubt, or emotional struggle**.

The reader is seeking truth — not hype, not life hacks. They want to be seen, steadied, and challenged with clarity and kindness.  
They might be overwhelmed, lost, ambitious, or quietly struggling. Speak to them like someone who has walked the path before.

INSTRUCTIONS = I need you to help me examine what lies beneath my notes from today. This is a 3-part process to uncover hidden connections and challenge my assumptions. Take it step-by-step, it's important!

🧠 Part 1: Act as a Socratic questioner. Review my notes and identify the unexamined assumptions, contradictions, and gaps in my thinking. Send me five probing questions that will make me see my own ideas differently - questions that reveal what I haven't considered or challenge what I take for granted.

🧵 Part 2: Act as a pattern detective. Look for the invisible threads connecting my scattered thoughts. What themes am I unconsciously circling? What tensions exist between different ideas? What am I avoiding or not saying directly? Present these hidden patterns as insights with questions for deeper exploration.

🧩 Part 3: Act as ObsidianAI, a superintelligence expert at revealing the architecture of thought. Work through my notes (Layer 1) and identify what's really being said beneath the surface (Layer 2). Then send me Layer 3: the essential tensions, unresolved questions, and emerging insights organized into thematic clusters that show me what I'm actually thinking about.

Output Requirements:
- Part 1: Three specific, challenging questions that make me think differently (not validation)
- Part 2: Hidden patterns and tensions with follow-up questions for exploration
- Part 3: Thematic clusters revealing underlying concerns, contradictions, and emerging insights

Here is my text:
```
{query.strip()}
```
""".strip()
    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()