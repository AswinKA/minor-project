import 'dart:typed_data';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';
import 'package:google_mlkit_language_id/google_mlkit_language_id.dart';
import 'package:google_mlkit_commons/google_mlkit_commons.dart';
import '../models/ocr_result.dart';

class OnDeviceOCRService {
  final _textRecognizer = TextRecognizer();
  final _languageIdentifier = LanguageIdentifier(confidenceThreshold: 0.5);

  /// Perform OCR on image bytes and return extracted text
  Future<String> extractText(Uint8List imageBytes) async {
    final inputImage = InputImage.fromBytes(
      bytes: imageBytes,
      metadata: InputImageMetadata(
        size: const Size(0, 0),
        rotation: InputImageRotation.rotation0deg,
        format: InputImageFormat.bgra8888,
        bytesPerRow: 0,
      ),
    );
    final recognizedText = await _textRecognizer.processImage(inputImage);
    
    StringBuffer fullText = StringBuffer();
    for (var block in recognizedText.blocks) {
      for (var line in block.lines) {
        fullText.writeln(line.text);
      }
    }
    
    return fullText.toString().trim();
  }

  /// Detect the language of the extracted text
  Future<String> detectLanguage(String text) async {
    if (text.isEmpty) return 'unknown';
    try {
      final identifiedLang = await _languageIdentifier.identifyLanguage(text);
      return identifiedLang ?? 'unknown';
    } catch (e) {
      return 'unknown';
    }
  }

  /// Simple on-device translation using a basic dictionary approach
  /// For production, you'd want to use a proper translation library or API
  Future<String> translateText(String text, String targetLanguage) async {
    // Basic placeholder - in real app you could use offline translation models
    // or a free API like MyMemory Translation API
    if (text.isEmpty) return '';
    
    // For now, return the original text with a note
    // This is where you'd integrate an offline translation solution
    return text; // Placeholder - no translation without backend
  }

  /// Full OCR pipeline: extract text, detect language, translate
  Future<OCRResult> processImage({
    required Uint8List imageBytes,
    required String targetLanguage,
    String? imagePath,
  }) async {
    final stopwatch = Stopwatch()..start();
    
    // Extract text
    final extractedText = await extractText(imageBytes);
    
    if (extractedText.isEmpty) {
      throw Exception('No text found in image');
    }
    
    // Detect language
    final detectedLang = await detectLanguage(extractedText);
    
    // Translate (placeholder - returns original text)
    final translatedText = await translateText(extractedText, targetLanguage);
    
    stopwatch.stop();
    
    return OCRResult(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: extractedText,
      detectedLanguage: detectedLang,
      translation: translatedText,
      targetLanguage: targetLanguage,
      imagePath: imagePath,
      processingTime: stopwatch.elapsedMilliseconds / 1000,
    );
  }

  void dispose() {
    _textRecognizer.close();
    _languageIdentifier.close();
  }
}
