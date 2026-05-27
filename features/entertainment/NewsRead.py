"""
features/entertainment/NewsRead.py
────────────────────────────────────
Reads latest news headlines by category.
API key loaded from .env — never hardcoded.
"""

import os
import requests
import json
from dotenv import load_dotenv
from core.voice import Speak, TakeCommand

load_dotenv()

CATEGORIES = ["business", "entertainment", "health", "science", "sports", "technology"]


def latestnews() -> None:
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        Speak("News API key not configured.")
        return

    Speak(f"Which category? {', '.join(CATEGORIES)}")
    field = TakeCommand().lower()

    category = next((c for c in CATEGORIES if c in field), None)
    if not category:
        Speak("Category not recognised.")
        return

    url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    if not articles:
        Speak("No news found right now.")
        return

    Speak(f"Here are the top {category} headlines.")

    for article in articles:
        title = article.get("title", "")
        print(title)
        Speak(title)

        Speak("Say 'next' to continue or 'stop' to exit.")
        user = TakeCommand().lower()
        if "stop" in user:
            break

    Speak("That's all the news.")