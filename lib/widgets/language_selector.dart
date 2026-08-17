import 'package:flutter/material.dart';
import '../models/language.dart';

class LanguageSelector extends StatelessWidget {
  final String selectedLangCode;
  final ValueChanged<String> onLanguageSelected;
  final List<Language> languages;
  final String? label;

  const LanguageSelector({
    super.key,
    required this.selectedLangCode,
    required this.onLanguageSelected,
    required this.languages,
    this.label,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (label != null) ...[
          Text(
            label!,
            style: const TextStyle(
              fontSize: 14,
              color: Colors.white70,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
        ],
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
            color: const Color(0xFF1E2022),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: const Color(0xFF6C5CE7)),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: selectedLangCode,
              isExpanded: true,
              dropdownColor: const Color(0xFF1E2022),
              icon: const Icon(Icons.arrow_drop_down, color: Color(0xFF6C5CE7)),
              style: const TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.w500,
              ),
              items: languages.map((lang) {
                return DropdownMenuItem<String>(
                  value: lang.code,
                  child: Row(
                    children: [
                      _getFlagIcon(lang.code),
                      const SizedBox(width: 8),
                      Text(lang.name),
                    ],
                  ),
                );
              }).toList(),
              onChanged: (value) {
                if (value != null) {
                  onLanguageSelected(value);
                }
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _getFlagIcon(String langCode) {
    // Simple emoji flags for languages
    switch (langCode.toLowerCase()) {
      case 'en':
        return const Text('🇺🇸', style: TextStyle(fontSize: 20));
      case 'ne':
        return const Text('🇳🇵', style: TextStyle(fontSize: 20));
      case 'hi':
        return const Text('🇮🇳', style: TextStyle(fontSize: 20));
      case 'es':
        return const Text('🇪🇸', style: TextStyle(fontSize: 20));
      case 'fr':
        return const Text('🇫🇷', style: TextStyle(fontSize: 20));
      case 'de':
        return const Text('🇩🇪', style: TextStyle(fontSize: 20));
      case 'ja':
        return const Text('🇯🇵', style: TextStyle(fontSize: 20));
      case 'zh-cn':
      case 'zh':
        return const Text('🇨🇳', style: TextStyle(fontSize: 20));
      case 'ar':
        return const Text('🇸🇦', style: TextStyle(fontSize: 20));
      case 'ko':
        return const Text('🇰🇷', style: TextStyle(fontSize: 20));
      default:
        return const Text('🌐', style: TextStyle(fontSize: 20));
    }
  }
}
