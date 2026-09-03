class OCRResult {
  final String id;
  final String text;
  final String detectedLanguage;
  final String translation;
  final String targetLanguage;
  final String? imagePath;
  final double? processingTime;
  final DateTime timestamp;
  bool isFavorite;

  OCRResult({
    required this.id,
    required this.text,
    required this.detectedLanguage,
    required this.translation,
    required this.targetLanguage,
    this.imagePath,
    this.processingTime,
    DateTime? timestamp,
    this.isFavorite = false,
  }) : timestamp = timestamp ?? DateTime.now();

  factory OCRResult.fromJson(Map<String, dynamic> json, {String? imagePath}) {
    return OCRResult(
      id: json['id'] ?? DateTime.now().millisecondsSinceEpoch.toString(),
      text: json['text'] ?? json['original_text'] ?? '',
      detectedLanguage: json['detected_language'] ?? json['source_language'] ?? 'auto',
      translation: json['translation'] ?? '',
      targetLanguage: json['target_language'] ?? 'en',
      imagePath: imagePath ?? json['image_path'],
      processingTime: (json['processing_time_seconds'] as num?)?.toDouble(),
      timestamp: json['timestamp'] != null ? DateTime.parse(json['timestamp']) : DateTime.now(),
      isFavorite: json['isFavorite'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'text': text,
      'detected_language': detectedLanguage,
      'translation': translation,
      'target_language': targetLanguage,
      'image_path': imagePath,
      'processing_time_seconds': processingTime,
      'timestamp': timestamp.toIso8601String(),
      'isFavorite': isFavorite,
    };
  }
}
