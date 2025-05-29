import os
from openai import OpenAI
import random
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

main_stylistic_framework = f"""
- Embrace rhythmic cadence and internal rhyme where appropriate.
- Mix short sentences for impact with reflective ones to unravel complexity.
- Vary rhythm for tension and release. Build, pause, then release insight.
- Avoid: generic encouragement, broad motivation, challenging their premises
- Focus on: idea expansion and tactical next moves
"""

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
{main_stylistic_framework}

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
{main_stylistic_framework}

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