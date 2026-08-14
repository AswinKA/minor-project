from deep_translator import GoogleTranslator

# Map common language codes for Google Translator
LANG_MAP = {
    "nep": "ne",
    "eng": "en",
    "hin": "hi",
    "spa": "es",
    "fre": "fr",
    "ger": "de",
    "jpn": "ja",
    "chi": "zh-CN",
}

def translate_text(text, source="auto", target="en"):
    """
    Translates text using Google Translator API via deep-translator.
    """
    if not text or not text.strip():
        return ""

    # Normalize source/target codes
    src_lang = LANG_MAP.get(source, source) if source else "auto"
    tgt_lang = LANG_MAP.get(target, target) if target else "en"

    # If source and target are the same, return text directly
    if src_lang == tgt_lang and src_lang != "auto":
        return text

    try:
        translated = GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
        return translated if translated else text
    except Exception as e:
        # Fallback to auto source detection if specific source fails
        try:
            translated = GoogleTranslator(source="auto", target=tgt_lang).translate(text)
            return translated if translated else text
        except Exception:
            return text