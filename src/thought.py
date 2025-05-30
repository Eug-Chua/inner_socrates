import os
from openai import OpenAI
import random
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

philosophers = ["Socrates", "Plato", "Aristotle", "Immanuel Kant", "St. Augustine", "Friedrich Nietzsche"]

themes = [
    "intellectual humility", "contemplation", "reflection", "self-awareness",
    "status games", "social influence", "desire for power", "humility",
    "one-upmanship", "the need to be better than others to feel safe",
    "our social nature", "the primal need for validation", "presenting a false self", "self-presentation",
    "the desire for acclaim", "the benefits of social status", "social capital", "mimetic desire", 
    "self-interest", "selfishness", "our natural pride", "ego", "status anxiety",
    "feeling less than others", "feeling better than others", "self-leadership", "self-mastery",
    "fear of insignificance", "fear of irrelevance", "emotional safety through status", "our search for psychological shelter",
    "toxic resilience", "performative authenticity", "ego disguised as enlightenment", "pseudo-growth",
    "the loneliness of leadership", "hidden envy among peers", "power without intimacy", "leadership as armor",
    "social mirroring", "emotional contagion", "subtle dominance rituals", "unconscious imitation",
    "identity as performance", "burnout from persona maintenance", "success without self", "validation addiction"
    ]

target_audience_belief = [
    "high achievers won't admit",
    "leaders won't admit",
    "leaders avoid talking about",
    "people won't admit",
    "nobody will admit",
    "nobody likes to talk about",
    "society won't admit",
    "society avoids talking about",
    "society finds difficult to talk about",
    "self-help gets wrong",
    "successful people hide from their followers",
    "motivational speakers deal with privately"
    ]

stylistic_framework = f"""
- Embrace rhythmic cadence and internal rhyme where appropriate.
- Mix short sentences for impact with reflective ones to unravel complexity.
- Vary rhythm for tension and release. Build, pause, then release insight.
- Avoid: generic encouragement, broad motivation, challenging their premises
- Focus on: idea expansion and tactical next moves
"""

def thought_of_the_day() -> str:
    """
    Dispenses thought of the day based on randomly selected philosopher and topic.
    """
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

def reflection_questions(thought: str) -> str:
    """
    Given a truth-bomb, ask three shadow-work questions.
    """
    prompt = f"""
The following is a stylized philosophical insight designed to emotionally resonate:

```
{thought.strip()}
```

Now, as a depth-oriented shadow work facilitator, generate 3 reflection questions that:
- Illuminate what this insight reveals about rejected or hidden aspects of the self
- Surface unconscious patterns, defenses, coping strategies or projections at play
- Invite confrontation with uncomfortable truths and disowned parts - and discover the gold in that shadow 

Focus on the shadow elements: what's being avoided, repressed, or projected onto others. Make each question penetrating enough to breach psychological defenses and reveal the gold hidden in darkness.
""".strip()
    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        )
    return response.choices[0].message.content.strip()