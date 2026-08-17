import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/ocr_result.dart';
import '../services/tts_service.dart';

class ResultScreen extends StatefulWidget {
  final OCRResult result;

  const ResultScreen({super.key, required this.result});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  bool _isSpeaking = false;

  @override
  void dispose() {
    TTSService.stop();
    super.dispose();
  }

  Future<void> _speakText(String text) async {
    if (_isSpeaking) {
      await TTSService.stop();
      setState(() => _isSpeaking = false);
      return;
    }

    setState(() => _isSpeaking = true);
    await TTSService.speak(text);
    setState(() => _isSpeaking = false);
  }

  void _copyToClipboard(String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Copied to clipboard'),
        backgroundColor: Color(0xFF6C5CE7),
        duration: Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final originalText = widget.result.text;
    final translatedText = widget.result.translation;
    final detectedLang = widget.result.detectedLanguage;
    final targetLang = widget.result.targetLanguage;
    final processingTime = widget.result.processingTime;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan Result'),
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              // Share functionality can be added here
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Share feature coming soon')),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Original Text Card
            _buildSectionCard(
              title: 'Original Text',
              subtitle: 'Detected: $detectedLang',
              text: originalText,
              onCopy: () => _copyToClipboard(originalText),
              onSpeak: () => _speakText(originalText),
              isSpeaking: _isSpeaking && originalText.isNotEmpty,
            ),
            
            const SizedBox(height: 16),
            
            // Translation Card
            _buildSectionCard(
              title: 'Translation',
              subtitle: 'Target: $targetLang',
              text: translatedText,
              onCopy: () => _copyToClipboard(translatedText),
              onSpeak: () => _speakText(translatedText),
              isSpeaking: _isSpeaking && translatedText.isNotEmpty,
              highlight: true,
            ),
            
            const SizedBox(height: 24),
            
            // Processing Info
            if (processingTime != null)
              Center(
                child: Text(
                  'Processed in ${processingTime.toStringAsFixed(2)}s',
                  style: TextStyle(
                    color: Colors.white54,
                    fontSize: 12,
                    fontStyle: FontStyle.italic,
                  ),
                ),
              ),
            
            const SizedBox(height: 32),
            
            // Action Buttons
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF6C5CE7),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    onPressed: () => _copyToClipboard(translatedText),
                    icon: const Icon(Icons.copy_all_rounded),
                    label: const Text('Copy Translation'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.cyanAccent,
                      side: const BorderSide(color: Colors.cyanAccent),
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    onPressed: () => _speakText(translatedText),
                    icon: Icon(_isSpeaking ? Icons.stop : Icons.volume_up_rounded),
                    label: Text(_isSpeaking ? 'Stop' : 'Listen'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionCard({
    required String title,
    required String subtitle,
    required String text,
    required VoidCallback onCopy,
    required VoidCallback onSpeak,
    bool isSpeaking = false,
    bool highlight = false,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: highlight 
            ? const Color(0xFF6C5CE7).withOpacity(0.15)
            : const Color(0xFF1E2022),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: highlight ? const Color(0xFF6C5CE7) : Colors.white12,
          width: highlight ? 1.5 : 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Card Header
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 8, 8),
            child: Row(
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: highlight ? const Color(0xFF6C5CE7) : Colors.white,
                  ),
                ),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.copy, size: 20),
                  color: Colors.white70,
                  onPressed: text.isEmpty ? null : onCopy,
                  tooltip: 'Copy',
                ),
                IconButton(
                  icon: Icon(isSpeaking ? Icons.stop : Icons.volume_up, size: 20),
                  color: isSpeaking ? Colors.redAccent : Colors.cyanAccent,
                  onPressed: text.isEmpty ? null : onSpeak,
                  tooltip: isSpeaking ? 'Stop' : 'Listen',
                ),
              ],
            ),
          ),
          
          // Subtitle
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              subtitle,
              style: TextStyle(
                fontSize: 12,
                color: Colors.white54,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
          
          const SizedBox(height: 8),
          
          // Text Content
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.2),
              borderRadius: const BorderRadius.only(
                bottomLeft: Radius.circular(16),
                bottomRight: Radius.circular(16),
              ),
            ),
            child: Text(
              text.isEmpty ? 'No text detected' : text,
              style: TextStyle(
                fontSize: 16,
                color: text.isEmpty ? Colors.white38 : Colors.white,
                height: 1.5,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
