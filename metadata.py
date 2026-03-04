from datetime import datetime
from langdetect import detect


def detect_language(text):

    try:
        return detect(text)
    except:
        return None


def detect_country(text):

    if text is None:
        return None

    countries = [
        "india","pakistan","uae","uk","usa","russia",
        "china","iran","afghanistan"
    ]

    for c in countries:

        if c in text.lower():
            return c

    return None


def extract_metadata(channel, full, keyword):

    desc = full.full_chat.about

    language = detect_language(desc) if desc else None
    country = detect_country(desc)

    data = {

        "channel_id": channel.id,
        "name": channel.title,
        "username": channel.username,
        "url": f"https://t.me/{channel.username}",
        "description": desc,
        "subscribers": full.full_chat.participants_count,
        "verified": channel.verified,
        "language": language,
        "country_hint": country,
        "keyword_found": keyword,
        "discovered_at": datetime.now()
    }

    return data