
# 🔤 Local English-Chinese Translator

A lightweight **offline** translator for English to Chinese.  
Features include:

- 🌐 **Offline Translation** using [Argos Translate](https://www.argosopentech.com/argospm/index/)
- 🔊 **Text-to-Speech** playback (English)
- 🔡 **IPA Phonetic Transcription**
- 📋 Translate selected text via **Ctrl + Alt + T**
- 📌 Neat popup near the cursor for quick translation
- 🧊 Runs silently in system tray after startup

> ⚠️ Currently supports **English ➜ Chinese** only.


---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/local-translator.git
cd local-translator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install argostranslate pyttsx3 pyperclip pynput pyautogui pystray eng_to_ipa
```

### 3. Download the Translation Model

Go to [Argos Translate model repository](https://www.argosopentech.com/argospm/index/)  
Download the **English to Chinese** model (`translate-en_zh-1_9.argosmodel`) and place it in the same folder as the script.

### 4. Run the Translator

```bash
python translator.py
```

---

## 🧠 How It Works

- On startup, the app shows a sample translation.
- It minimizes to the tray.
- Whenever you press `Ctrl + Alt + T`, the app:
  - Copies your selected text
  - Translates it from English to Chinese
  - Converts it to IPA
  - Shows a popup with all results
  - Optionally reads the English text aloud

---

## ⌨️ Hotkey

- **Translate selection**: `Ctrl + Alt + T`  
Make sure to first select some English text in any app or browser.

---

## 📦 Dependencies

- [Argos Translate](https://github.com/argosopentech/argos-translate)
- `pyttsx3` (for TTS)
- `pyautogui` (get mouse position + copy)
- `pyperclip` (clipboard handling)
- `pynput` (hotkey listener)
- `pystray` (system tray)
- `eng_to_ipa` (IPA conversion)
- `tkinter` (built-in GUI)

---

## 📌 Notes

- Only supports English ➜ Chinese for now
- IPA may not cover complex phrases accurately
- Some TTS voices may vary depending on OS

---

## 🧊 Tray Mode

After showing the first translation, the app minimizes and runs silently in the tray. Right-click the tray icon to exit.

---

## 🛠️ Todo

- [ ] Add Chinese ➜ English support
- [ ] User-configurable hotkey
- [ ] More elegant popup window
- [ ] Support for more languages

---

## 📃 License

MIT License
