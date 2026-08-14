# AI Signboard Reader & Translator

An AI-powered mobile application built with **Flutter** and **Django REST Framework** that uses **Tesseract OCR** and **Google Translate API** to scan signboard text, detect languages (English, Nepali, Hindi, etc.), translate text in real-time, read aloud with Text-to-Speech (TTS), and save scan history.

---

## 📁 Project Structure

```text
Minor project/
├── backend/                  # Django REST API Backend
│   ├── api/                  # API endpoints (/upload/, /translate/, /languages/, /test/)
│   ├── config/               # Settings & CORS configuration
│   ├── ocr/                  # OCR Extraction & Google Translate engine
│   ├── uploads/              # Media uploads storage
│   ├── db.sqlite3            # SQLite database
│   └── manage.py
├── mobile_app/               # Flutter Mobile Application
│   ├── lib/                  # Dart source code (screens, widgets, services, models)
│   └── pubspec.yaml          # Flutter dependencies
├── requirements.txt          # Python dependencies
└── README.md                 # Project Setup Guide
```

---

## 🛠️ System Requirements

1. **Python 3.10+** installed.
2. **Flutter SDK (3.20+)** installed.
3. **Tesseract OCR Engine** installed on Windows:
   - Default install path: `C:\Users\<user>\AppData\Local\Programs\Tesseract-OCR\tesseract.exe` or `C:\Program Files\Tesseract-OCR\tesseract.exe`.
   - Download Tesseract Windows installer: [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).

---

## 🚀 Step-by-Step Setup Guide

### 1. Setting up the Backend (Django REST API)

1. Open PowerShell / Terminal in the project root:
   ```powershell
   cd "Minor project"
   ```

2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install required Python packages:
   ```powershell
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```powershell
   cd backend
   python manage.py migrate
   ```

5. Start the Django backend server:
   ```powershell
   python manage.py runserver 0.0.0.0:8000
   ```
   *(The server will run on `http://0.0.0.0:8000` to allow mobile devices to connect).*

---

### 2. Setting up the Mobile App (Flutter)

1. Open a new terminal in the `mobile_app` directory:
   ```powershell
   cd "Minor project\mobile_app"
   ```

2. Get Flutter dependencies:
   ```powershell
   flutter pub get
   ```

3. Launch the app:
   - **On Desktop / Chrome**:
     ```powershell
     flutter run -d windows
     ```
     or
     ```powershell
     flutter run -d chrome
     ```
   - **On Android Emulator / Physical Phone**:
     ```powershell
     flutter run
     ```

---

### 📱 Connecting Mobile App to Backend Server

- **Android Emulator**: Uses `http://10.0.2.2:8000` by default.
- **Physical Phone**: 
  1. Ensure phone and PC are connected to the same Wi-Fi network.
  2. Find your PC's IP address by running `ipconfig` in PowerShell (e.g. `192.168.1.50`).
  3. Open the **Settings** tab inside the mobile app and set the URL to `http://192.168.1.50:8000`.

---

### 📦 How to Build Android APK for Friends

To generate an `.apk` file to send to a friend's Android phone:

```powershell
cd mobile_app
flutter build apk --release
```

The APK file will be generated at:
`mobile_app/build/app/outputs/flutter/apk/release/app-release.apk`
