import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;

class ApiService {
  static String _baseUrl = 'http://192.168.1.66:8000';

  static void setBaseUrl(String url) {
    _baseUrl = url;
  }

  static String get baseUrl => _baseUrl;

  /// Test API connection
  static Future<Map<String, dynamic>> testConnection() async {
    final response = await http.get(Uri.parse('$_baseUrl/api/test/'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to connect to server');
    }
  }

  /// Upload image bytes for OCR and translation
  static Future<Map<String, dynamic>> uploadImageBytes({
    required Uint8List imageBytes,
    required String filename,
    String targetLanguage = 'en',
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$_baseUrl/api/upload/'),
    );

    request.files.add(http.MultipartFile.fromBytes(
      'image',
      imageBytes,
      filename: filename,
    ));

    request.fields['target_language'] = targetLanguage;

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('OCR processing failed: ${response.reasonPhrase}');
    }
  }

  /// Translate text
  static Future<Map<String, dynamic>> translateText({
    required String text,
    String sourceLanguage = 'auto',
    String targetLanguage = 'en',
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/api/translate/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'text': text,
        'source_language': sourceLanguage,
        'target_language': targetLanguage,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Translation failed: ${response.reasonPhrase}');
    }
  }

  /// Get supported languages
  static Future<List<Map<String, String>>> getLanguages() async {
    final response = await http.get(Uri.parse('$_baseUrl/api/languages/'));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      List<dynamic> languages = data['languages'];
      return languages.map((lang) => {
        'code': lang['code'].toString(),
        'name': lang['name'].toString(),
      }).cast<Map<String, String>>().toList();
    } else {
      // Return default languages if API fails
      return [
        {'code': 'en', 'name': 'English'},
        {'code': 'ne', 'name': 'Nepali'},
        {'code': 'hi', 'name': 'Hindi'},
        {'code': 'es', 'name': 'Spanish'},
        {'code': 'fr', 'name': 'French'},
        {'code': 'de', 'name': 'German'},
        {'code': 'ja', 'name': 'Japanese'},
        {'code': 'zh-CN', 'name': 'Chinese'},
        {'code': 'ar', 'name': 'Arabic'},
        {'code': 'ko', 'name': 'Korean'},
      ];
    }
  }
}
