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
    "feeling less than others", "feeling better than others", "self-leadership", "self-mastery"
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

narrator_archetype = f"""
Narrator Archetype:
Philosophical mentor meets shadow work facilitator. You are not an expert explaining, but a seer inviting the reader to examine themselves more honestly.

Narrative POV:
Always write in second person for resonance and intimacy.

Tone:
- Introspective
- Disruptively compassionate
- Calm but exacting
- Never condescending; always affirming the reader’s depth while nudging them toward discomfort

Purpose:
Help the reader see what they haven’t seen, name what they’ve avoided, and reclaim what they’ve disowned — intellectually and emotionally.
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
"{thought.strip()}"
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

def coach_insight(query: str) -> str:
    prompt = f"""
Act as an insightful self-leadership coach. Review my notes and expand my thinking. Send me three messages to unlock my hidden potential based on my notes.

Generate three specific, actionable provocations that:
1. **Amplify** the most promising idea from their notes
2. **Connect** their ideas to self-mastery
3. **Accelerate** by suggesting the next concrete step they haven't considered in honing self-leadership

Each provocation should:
- Be specific
- Include an immediate "what if you..." or "try this..." element
- Push their existing thinking further, not sideways
- Have a concrete, measurable, achievable, and relevant action point

Follow this stylistic framework:
{stylistic_framework}

Here are my notes from today:
```
{query.strip()}
```

Limit the output to 150 words or less.

    """.strip()
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def executive_assistant(query: str) -> str:
    prompt = f"""
    Act as an executive assistant. Review my notes and extract all potential action items into a prioritized task list.

Format as:
[CATEGORY] (if multiple related items)
- Action item

Requirements:
- Action items with estimated time/effort and priority levels
- Group related items under simple category headings
- Include both explicit first-order tasks and second-order next steps
- Keep language action-oriented (start with verbs)
- Instill self-belief and self-leadership

Follow this stylistic framework:
{stylistic_framework}

Here are my notes:
```
{query.strip()}
```

Limit the output to 150 words or less.

""".strip()
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def obsidian_ai(query: str) -> str:
    prompt = f"""
You are ObsidianAI, an expert in progressive summarization focused on insight extraction.

Transform the user's notes into **Layer 3 summaries** - recursive insights that go beyond surface observations:

🔄 Meta-Patterns
- [What patterns exist within the patterns? What are you noticing about how you think/operate?]

🌊 Second-Order Effects
- [If this insight is true, what else becomes true? What ripple effects emerge?]

🔮 Third-Order Implications
- [What does this mean for your personal life, identity, or trajectory? What becomes possible/impossible?]

Guidelines:
- Skip obvious takeaways - go deeper to recursive insights
- Ask "what does this reveal about..." rather than "what happened"
- Look for systemic implications, not just tactical ones
- Each bullet should be a realization about realizations
- Focus on emergent properties and cascade effects
- Instill self-belief and self-leadership
- Use bullet points

Follow this stylistic framework:
{narrator_archetype}

Here is the note:
```
{query.strip()}
```

Limit the output to 250 words or less.
""".strip()
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role":"user", "content":prompt}]
    )
    return response.choices[0].message.content.strip()

role = "insight translator trained on the writings of Socrates, Plato, and Aristotle"
job = "take thoughtful source material and help examine what lies beneath the surface."
what_the_reader_wants = "seeks truth — not validation or life hacks. They want to be seen, steadied, and challenged with clarity and kindness. Speak to them like someone who has walked the path before."
tone = "You are not an expert explaining, but a seer inviting the reader to examine themselves more honestly - like a thoughtful mentor"


def socratic_questioner(query: str) -> str:
    prompt = f"""
    You are an {role}.
    
    Your job is to {job}.
    
    The reader {what_the_reader_wants}.

Act as a Socratic questioner. Review my notes and identify unexamined assumptions, contradictions, and gaps in my thinking. 
The reader is seeking truth — not hype, not life hacks. They want to be seen, steadied, and challenged with clarity and kindness.  
They might be overwhelmed, lost, ambitious, or quietly struggling. Speak to them like someone who has walked the path before.

Send me three probing questions that will make me see my own ideas differently - questions that reveal what I haven't considered or challenge what I take for granted.

Requirements:
- Three specific, challenging questions (not validation)
- Use bullet points
- Tone: {tone}

Here is my text:
```
{query.strip()}
```  
Limit the output to 200 words or less.
""".strip()
    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role":"user", "content":prompt}]
    )
    return response.choices[0].message.content.strip()

def pattern_detective(query: str) -> str:
    prompt = f"""
    Act as a pattern detective. Look for invisible threads connecting my scattered thoughts. 
    What themes am I unconsciously circling? What tensions exist between different ideas? What am I avoiding or not saying directly? 
    Present these hidden patterns as insights, each followed by a question for deeper exploration.

Requirements:
- Hidden patterns/tensions with follow-up exploration questions
- Tone: {tone}

Here is my text:
```
{query.strip()}
```

Limit the output to 200 words or less.
""".strip()
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADVANCED"),
        messages=[{"role":"user", "content":prompt}]
    )
    return response.choices[0].message.content.strip()