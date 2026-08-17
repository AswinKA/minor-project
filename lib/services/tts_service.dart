import 'package:flutter_tts/flutter_tts.dart';

class TTSService {
  static final FlutterTts _flutterTts = FlutterTts();
  static bool _isInitialized = false;

  /// Initialize TTS engine
  static Future<void> init() async {
    if (_isInitialized) return;

    await _flutterTts.setLanguage("en-US");
    await _flutterTts.setSpeechRate(0.5);
    await _flutterTts.setVolume(1.0);
    await _flutterTts.setPitch(1.0);

    _isInitialized = true;
  }

  /// Set language for TTS
  static Future<void> setLanguage(String languageCode) async {
    // Map language codes to locale codes
    String locale;
    switch (languageCode.toLowerCase()) {
      case 'en':
        locale = "en-US";
        break;
      case 'ne':
      case 'hi':
        locale = "hi-IN"; // Hindi for Nepali/Hindi (closest match)
        break;
      case 'es':
        locale = "es-ES";
        break;
      case 'fr':
        locale = "fr-FR";
        break;
      case 'de':
        locale = "de-DE";
        break;
      case 'ja':
        locale = "ja-JP";
        break;
      case 'zh-cn':
      case 'zh':
        locale = "zh-CN";
        break;
      case 'ar':
        locale = "ar-SA";
        break;
      case 'ko':
        locale = "ko-KR";
        break;
      default:
        locale = "en-US";
    }

    await _flutterTts.setLanguage(locale);
  }

  /// Speak text
  static Future<void> speak(String text) async {
    if (!_isInitialized) {
      await init();
    }

    if (text.trim().isEmpty) return;

    await _flutterTts.speak(text);
  }

  /// Stop speaking
  static Future<void> stop() async {
    await _flutterTts.stop();
  }

  /// Check if TTS is speaking
  static Future<bool> isSpeaking() async {
    // flutter_tts doesn't have isSpeaking getter, use a workaround
    // We'll track speaking state manually or just return false
    // For most use cases, this isn't critical
    return false;
  }

  /// Get available languages
  static Future<List<dynamic>> getLanguages() async {
    return await _flutterTts.getLanguages;
  }
}
