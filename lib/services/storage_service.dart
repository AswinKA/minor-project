import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class StorageService {
  static const String _serverUrlKey = 'backend_server_url';
  static const String _defaultTargetLangKey = 'default_target_language';
  static const String _scanHistoryKey = 'scan_history';

  /// Save backend server URL
  static Future<void> saveServerUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_serverUrlKey, url);
  }

  /// Get saved backend server URL
  static Future<String> getServerUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_serverUrlKey) ?? 'http://10.0.2.2:8000';
  }

  /// Save default target language
  static Future<void> saveDefaultTargetLang(String langCode) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_defaultTargetLangKey, langCode);
  }

  /// Get default target language
  static Future<String> getDefaultTargetLang() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_defaultTargetLangKey) ?? 'en';
  }

  /// Save scan result to history
  static Future<void> saveResult(Map<String, dynamic> result) async {
    final prefs = await SharedPreferences.getInstance();
    final history = await getHistory();
    
    // Add timestamp
    result['timestamp'] = DateTime.now().toIso8601String();
    
    // Add to beginning of list
    history.insert(0, result);
    
    // Keep only last 50 results
    if (history.length > 50) {
      history.removeRange(50, history.length);
    }
    
    final jsonString = json.encode(history);
    await prefs.setString(_scanHistoryKey, jsonString);
  }

  /// Get scan history
  static Future<List<Map<String, dynamic>>> getHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonString = prefs.getString(_scanHistoryKey);
    
    if (jsonString == null || jsonString.isEmpty) {
      return [];
    }
    
    try {
      final List<dynamic> decoded = json.decode(jsonString);
      return decoded.map((item) => Map<String, dynamic>.from(item)).toList();
    } catch (e) {
      return [];
    }
  }

  /// Clear scan history
  static Future<void> clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_scanHistoryKey);
  }

  /// Delete specific result from history
  static Future<void> deleteResult(int index) async {
    final history = await getHistory();
    if (index >= 0 && index < history.length) {
      history.removeAt(index);
      final prefs = await SharedPreferences.getInstance();
      final jsonString = json.encode(history);
      await prefs.setString(_scanHistoryKey, jsonString);
    }
  }
}
