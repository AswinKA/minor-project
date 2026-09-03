import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'services/tts_service.dart';
import 'services/storage_service.dart';
import 'services/api_service.dart';
import 'screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await TTSService.init();

  // Load saved backend server URL preference
  final savedServerUrl = await StorageService.getServerUrl();
  ApiService.setBaseUrl(savedServerUrl);

  runApp(const SignboardTranslatorApp());
}

class SignboardTranslatorApp extends StatelessWidget {
  const SignboardTranslatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Signboard Reader & Translator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0F1016),
        primaryColor: const Color(0xFF6C5CE7),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF6C5CE7),
          secondary: Colors.cyanAccent,
          surface: Color(0xFF1E2022),
        ),
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          centerTitle: true,
          titleTextStyle: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
