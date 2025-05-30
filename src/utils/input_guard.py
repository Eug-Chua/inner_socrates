import os
import re
import tiktoken

# Load models and their token caps
MODEL_BASIC    = os.getenv("OPENAI_GPT_MODEL_BASIC", "gpt-3.5-turbo")
MODEL_ADVANCED = os.getenv("OPENAI_GPT_MODEL_ADVANCED", "gpt-4")

MAX_TOKEN_LIMITS = {
    MODEL_BASIC: int(os.getenv("MAX_TOKEN_LIMIT", 500)),
    MODEL_ADVANCED: int(os.getenv("MAX_TOKEN_LIMIT", 800)),
}

# Load patterns
def load_suspicious_patterns():
    return [
        os.getenv(key)
        for key in sorted(os.environ)
        if key.startswith("SUS_PATTERN_") and os.getenv(key)
    ]

SUSPICIOUS_PATTERNS = load_suspicious_patterns()

# Token counting
def count_tokens(text: str, model: str = MODEL_ADVANCED) -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def exceeds_token_limit(text: str, model: str = MODEL_ADVANCED) -> bool:
    max_tokens = MAX_TOKEN_LIMITS.get(model, 500)
    return count_tokens(text, model) > max_tokens

# Suspicious input detection
def contains_suspicious_patterns(text: str) -> bool:
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            print(f"[⚠️] Suspicious pattern matched: {pattern}")
            return True
    return False
