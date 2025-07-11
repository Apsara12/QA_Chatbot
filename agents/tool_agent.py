import re
import dateparser
from langchain.tools import tool

@tool
def is_valid_email(email: str) -> bool:
    """Check if the given email address is valid."""
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None


@tool
def is_valid_phone(phone: str) -> bool:
    """Check if the given phone number is valid."""
    return re.match(r"^(?:\+977)?9[78]\d{8}$", phone) is not None

@tool
def extract_date_fn(text: str) -> str:
    """
    Extract and return a date in YYYY-MM-DD format from natural language input.
    Accepts phrases like 'tomorrow', 'next Monday', or a full sentence containing a date.
    Returns "Invalid date format" if no valid date is found.
    """
    date_phrase_match = re.search(r"\b(tomorrow|today|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|next \w+|this \w+)\b", text, re.IGNORECASE)
    if date_phrase_match:
        matched_phrase = date_phrase_match.group(0)
        date = dateparser.parse(matched_phrase, settings={'PREFER_DATES_FROM': 'future'})
    else:
        date = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'future'})
    return date.strftime("%Y-%m-%d") if date else "Invalid date format"