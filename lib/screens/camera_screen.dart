import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';
import '../models/language.dart';
import '../models/ocr_result.dart';
import '../widgets/language_selector.dart';
import 'result_screen.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  final ImagePicker _picker = ImagePicker();
  Uint8List? _selectedBytes;
  String _selectedFilename = 'image.jpg';
  bool _isLoading = false;
  String _selectedTargetLang = 'en';
  List<Language> _languages = Language.defaultList;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final defaultLang = await StorageService.getDefaultTargetLang();
    final langs = await ApiService.getLanguages();
    setState(() {
      _selectedTargetLang = defaultLang;
      _languages = langs.cast<Language>();
    });
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? file = await _picker.pickImage(
        source: source,
        imageQuality: 90,
      );

      if (file != null) {
        final bytes = await file.readAsBytes();
        setState(() {
          _selectedBytes = bytes;
          _selectedFilename = file.name.isNotEmpty ? file.name : 'image.jpg';
        });
        _processImage();
      }
    } catch (e) {
      _showSnackBar('Failed to pick image: $e');
    }
  }

  Future<void> _processImage() async {
    if (_selectedBytes == null) return;

    setState(() {
      _isLoading = true;
    });

    try {
      final resultData = await ApiService.uploadImageBytes(
        imageBytes: _selectedBytes!,
        filename: _selectedFilename,
        targetLanguage: _selectedTargetLang,
      );

      final result = OCRResult.fromJson(resultData);
      await StorageService.saveResult(result);

      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(result: result),
        ),
      );
    } catch (e) {
      _showSnackBar('OCR / Translation error: $e');
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _showSnackBar(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: Colors.redAccent,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F1016),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text('Signboard OCR Scanner'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              // Target Language Picker Header
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E2022),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white10),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Translate Signboard To:',
                      style: TextStyle(
                        color: Colors.white70,
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 10),
                    LanguageSelector(
                      selectedLangCode: _selectedTargetLang,
                      languages: _languages,
                      onLanguageSelected: (val) {
                        setState(() {
                          _selectedTargetLang = val;
                        });
                      },
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 24),

              // Image Preview or Scanner Placeholder Area
              Expanded(
                child: Container(
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: const Color(0xFF161822),
                    borderRadius: BorderRadius.circular(24),
                    border: Border.all(
                      color: _selectedBytes != null
                          ? Colors.cyanAccent.withOpacity(0.5)
                          : Colors.white12,
                      width: 2,
                    ),
                  ),
                  child: _isLoading
                      ? const Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            CircularProgressIndicator(color: Colors.cyanAccent),
                            SizedBox(height: 20),
                            Text(
                              'Extracting text & translating...',
                              style: TextStyle(color: Colors.white, fontSize: 16),
                            ),
                          ],
                        )
                      : _selectedBytes != null
                          ? ClipRRect(
                              borderRadius: BorderRadius.circular(22),
                              child: Image.memory(
                                _selectedBytes!,
                                fit: BoxFit.contain,
                              ),
                            )
                          : Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(20),
                                  decoration: BoxDecoration(
                                    color: Colors.cyanAccent.withOpacity(0.1),
                                    shape: BoxShape.circle,
                                  ),
                                  child: const Icon(
                                    Icons.document_scanner_rounded,
                                    size: 64,
                                    color: Colors.cyanAccent,
                                  ),
                                ),
                                const SizedBox(height: 16),
                                const Text(
                                  'Scan any Signboard or Text Image',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 8),
                                const Padding(
                                  padding: EdgeInsets.symmetric(horizontal: 30),
                                  child: Text(
                                    'Take a photo or choose an existing photo to extract OCR text and get real-time Google Translation.',
                                    textAlign: TextAlign.center,
                                    style: TextStyle(color: Colors.white54, fontSize: 13),
                                  ),
                                ),
                              ],
                            ),
                ),
              ),

              const SizedBox(height: 24),

              // Action Buttons Row (Camera vs Gallery)
              Row(
                children: [
                  Expanded(
                    child: SizedBox(
                      height: 56,
                      child: ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF6C5CE7),
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        onPressed: _isLoading ? null : () => _pickImage(ImageSource.camera),
                        icon: const Icon(Icons.camera_alt_rounded),
                        label: const Text(
                          'Capture Photo',
                          style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: SizedBox(
                      height: 56,
                      child: OutlinedButton.icon(
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.white,
                          side: const BorderSide(color: Colors.white24),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        onPressed: _isLoading ? null : () => _pickImage(ImageSource.gallery),
                        icon: const Icon(Icons.photo_library_rounded, color: Colors.cyanAccent),
                        label: const Text(
                          'From Gallery',
                          style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
