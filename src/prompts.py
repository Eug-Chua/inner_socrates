import os
from openai import OpenAI
import random
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

philosophers = ["Socrates", "Plato", "Aristotle", "Immanuel Kant", "St. Augustine"]

themes = [
    "intellectual humility", "contemplation", "Solvitur ambulando", "reflection", "self-awareness",
    "status games", "social influence", "desire for power", "humility",
    "one-upmanship", "the need to be better than others to feel safe",
    "our social nature", "the primal need for validation", "presenting a false self", "self-presentation",
    "the desire for acclaim", "the benefits of social status", "social capital", "mimetic desire",
    "self-interest", "selfishness", "our natural pride", "ego", "status anxiety",
    "feeling less than others", "feeling better than others"
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
    "self-help gets wrong",
    "successful people hide from their followers",
    "motivational speakers deal with privately"
    ]

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

def coach_insight(query: str) -> str:
    prompt = f"""
You are a genius innovator coach. Review my notes from today and expand my thinking. Send me three messages to unlock my inner genius based on my notes.

Generate three specific, actionable provocations that:
1. **Amplify** the most promising idea from their notes
2. **Connect** their ideas to unexpected domains or applications
3. **Accelerate** by suggesting the next concrete step they haven't considered

Each provocation should:
- Build directly on something specific they wrote
- Include an immediate "what if you..." or "try this..." element
- Push their existing thinking further, not sideways
- Be energizing and forward-momentum focused

Avoid: generic encouragement, broad motivation, challenging their premises
Focus on: idea expansion, tactical next moves, creative combinations

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
**[CATEGORY]** (if multiple related items)
- Action item (Time: X min/hrs | Priority: High/Med/Low)

Requirements:
- Group related items under simple category headings
- Estimate realistic time/effort for each item
- Assign priority based on urgency + impact
- Include both explicit tasks and implied next steps
- Keep language action-oriented (start with verbs)

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

🔄 **Meta-Patterns** 
- [What patterns exist within the patterns? What are you noticing about how you think/operate?]

🌊 **Second-Order Effects**
- [If this insight is true, what else becomes true? What ripple effects emerge?]

🔮 **Third-Order Implications** 
- [What does this mean for your broader systems, identity, or trajectory? What becomes possible/impossible?]

Guidelines:
- Skip obvious takeaways - go deeper to recursive insights
- Ask "what does this reveal about..." rather than "what happened"
- Look for systemic implications, not just tactical ones
- Each bullet should be a realization about realizations
- Focus on emergent properties and cascade effects

Here is the note:
```
{query.strip()}
```

Limit the output to 300 words or less.
""".strip()
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADV"),
        messages=[{"role":"user", "content":prompt}]
    )
    return response.choices[0].message.content.strip()

role = "insight translator trained on the writings of Socrates, Plato, and Aristotle"
job = "take thoughtful source material and help examine what lies beneath the surface."
what_the_reader_wants = "seeks truth — not validation or life hacks. They want to be seen, steadied, and challenged with clarity and kindness. Speak to them like someone who has walked the path before."
tone = "Wise, direct, compassionate - like a thoughtful mentor"

def socratic_questioner(query: str) -> str:
    prompt = f"""
    You are an {role}.
    
    Your job is to {job}.
    
    The reader {what_the_reader_wants}.

Act as a Socratic questioner. Review my notes and identify unexamined assumptions, contradictions, and gaps in my thinking. 

Send me three probing questions that will make me see my own ideas differently - questions that reveal what I haven't considered or challenge what I take for granted.

Requirements:
- Three specific, challenging questions (not validation)
- Tone: {tone}

Here is my text:
```
{query.strip()}
```  
Limit the output to 200 words or less.
""".strip()
    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL_ADV"),
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
        model=os.getenv("OPENAI_GPT_MODEL_ADV"),
        messages=[{"role":"user", "content":prompt}]
    )
    return response.choices[0].message.content.strip()

###
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

🧠 Part 1: Act as a Socratic questioner. Review my notes and identify the unexamined assumptions, contradictions, and gaps in my thinking. Send me three probing questions that will make me see my own ideas differently - questions that reveal what I haven't considered or challenge what I take for granted.

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