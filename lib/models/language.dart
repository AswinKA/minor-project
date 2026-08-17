class Language {
  final String code;
  final String name;

  const Language({required this.code, required this.name});

  factory Language.fromJson(Map<String, dynamic> json) {
    return Language(
      code: json['code'] ?? 'en',
      name: json['name'] ?? 'English',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'code': code,
      'name': name,
    };
  }

  static const List<Language> defaultList = [
    Language(code: 'en', name: 'English'),
    Language(code: 'ne', name: 'Nepali'),
    Language(code: 'hi', name: 'Hindi'),
    Language(code: 'es', name: 'Spanish'),
    Language(code: 'fr', name: 'French'),
    Language(code: 'de', name: 'German'),
    Language(code: 'ja', name: 'Japanese'),
    Language(code: 'zh-CN', name: 'Chinese (Simplified)'),
    Language(code: 'ar', name: 'Arabic'),
    Language(code: 'ko', name: 'Korean'),
  ];
}
