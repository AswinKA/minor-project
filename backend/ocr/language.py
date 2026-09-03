from langdetect import detect

def detect_language(text):
    """
    Detects language of input text using langdetect with 'en' fallback.
    """
    if not text or len(text.strip()) < 3:
        return "en"
    try:
        lang = detect(text)
        return lang
    except Exception:
        return "en"