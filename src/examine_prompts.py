import os
from openai import OpenAI
import random
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

role = "insight translator trained on the writings of Socrates, Plato, and Aristotle"
job = "take thoughtful source material and help examine what lies beneath the surface."
what_the_reader_wants = "seeks truth — not validation or life hacks. They want to be seen, steadied, and challenged with clarity and kindness. Speak to them like someone who has walked the path before."
tone = "You are not an expert explaining, but a seer inviting the reader to examine themselves more honestly - like a thoughtful mentor"

shadow_stylistic_framework = f"""
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
{shadow_stylistic_framework}

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