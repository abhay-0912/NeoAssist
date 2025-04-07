from serpapi import GoogleSearch
from .config import SERPAPI_API_KEY
from .voice import speak

def search_google(query):
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": SERPAPI_API_KEY
        })
        results = search.get_dict()
        answer = results.get("answer_box", {}).get("answer") or \
                 results.get("answer_box", {}).get("snippet") or \
                 results.get("organic_results", [{}])[0].get("snippet", "Sorry, I couldn't find anything.")
        speak(answer)
        print(f"🔍 {answer}")
    except Exception as e:
        speak("There was an error searching Google.")
        print(f"⚠️ SerpApi error: {e}")
        logger.error(f"Google search error: {e}")
