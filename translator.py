import argostranslate.package
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import pyperclip
import pyautogui
import pyttsx3
import tkinter as tk
from pynput import keyboard
import argostranslate.translate
import time
import threading
import eng_to_ipa as ipa
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# 获取程序所在目录（支持 .exe 和 .py 运行）
if getattr(sys, 'frozen', False):
    # 如果是打包后的 .exe 文件，获取 .exe 所在目录
    base_path = os.path.dirname(sys.executable)
else:
    # 如果是 .py 文件，获取脚本所在目录
    base_path = os.path.dirname(os.path.abspath(__file__))
# Load offline translation model
# model_path = "E:\\my_translator\\translate-en_zh-1_9.argosmodel"
model_path = os.path.join(base_path, "translate-en_zh-1_9.argosmodel")
argostranslate.package.install_from_path(model_path)

# Check if the model has been loaded properly
langs = argostranslate.translate.get_installed_languages()
print("Loaded languages:", langs)  # Debugging line

print("Language codes:")
for l in langs:
    print(f"- {l.name} ({l.code})")
# More robust matching logic
from_lang = next((l for l in langs if l.code.startswith("en")), None)
to_lang = next((l for l in langs if l.code.startswith("zh")), None)

if from_lang and to_lang:
    translate_fn = from_lang.get_translation(to_lang)
else:
    print("Error: Translation languages not loaded properly.")
    translate_fn = None


# Try to fetch the 'en' to 'zh' translation function
from_lang = next((l for l in langs if l.code == "en"), None)
to_lang = next((l for l in langs if l.code == "zh"), None)

if from_lang and to_lang:
    translate_fn = from_lang.get_translation(to_lang)
else:
    print("Error: Translation languages not loaded properly.")
    translate_fn = None

# Check if the translation function is loaded
if translate_fn is None:
    print("Error: translate_fn is None, translation model could not be loaded.")

# TTS setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def show_popup(original, ipa_text, translated):
    # Get cursor position
    x, y = pyautogui.position()

    # Create a popup window
    popup = tk.Tk()
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.geometry(f"+{x + 20}+{y + 20}")

    frame = tk.Frame(popup, bg="lightyellow", padx=10, pady=5)
    frame.pack()

    # Display original text
    tk.Label(frame, text=f"English: {original}", bg="lightyellow", anchor='w', font=("Arial", 11)).pack(anchor='w')
    tk.Label(frame, text=f"IPA: {ipa_text}", bg="lightyellow", anchor='w', font=("Arial", 10, "italic")).pack(anchor='w')
    tk.Label(frame, text=f"中文: {translated}", bg="lightyellow", anchor='w', font=("Arial", 12)).pack(anchor='w', pady=(5, 5))

    # Add 'Read' button
    def on_read():
        threading.Thread(target=speak, args=(original,), daemon=True).start()

    tk.Button(frame, text="🔊 Read", command=on_read).pack()

    # Auto-close after 6 seconds
    popup.after(6000, popup.destroy)
    popup.mainloop()

def translate_clipboard():
    time.sleep(0.2)  # Clipboard delay
    text = pyperclip.paste().strip()
    if not text:
        return

    # Perform translation if translate_fn is valid
    if translate_fn:
        translation = translate_fn.translate(text)
    else:
        print("Error: Translation function not available.")
        return

    # Convert to IPA
    ipa_text = ipa.convert(text)

    # Show the popup
    show_popup(text, ipa_text, translation)

def on_activate():
    pyautogui.hotkey('ctrl', 'c')  # Simulate Ctrl+C to copy text to clipboard
    threading.Thread(target=translate_clipboard, daemon=True).start()

# Listen for Ctrl+Alt+T
def listen_shortcut():
    # COMBO = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('t')}
    current_keys = set()

    def on_press(key):
        current_keys.add(key)
        print(f"[KEY DOWN] {key}, currently pressed: {current_keys}")  # <-- 调试输出

        if (any(k in current_keys for k in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]) and
                any(k in current_keys for k in [keyboard.Key.alt_l, keyboard.Key.alt_r]) and
                any(isinstance(k, keyboard.KeyCode) and (
                        hasattr(k, 'char') and k.char and k.char.lower() == 't' or k.vk == 84) for k in current_keys)):
            print("✅ HOTKEY triggered")
            on_activate()

    def on_release(key):
        current_keys.discard(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Function to create the system tray icon
def create_tray_icon():
    # Create an image for the tray icon
    icon_image = Image.new("RGB", (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.rectangle([16, 16, 48, 48], fill="blue")

    # Define tray icon menu
    def on_quit(icon, item):
        icon.stop()

    tray_icon = pystray.Icon("Translator", icon_image, menu=(
        item("Quit", on_quit),
    ))

    tray_icon.run()

# Function to handle the initial popup window when the program starts
def show_initial_popup():
    # Initial popup
    original_text = "Hello"  # Default text to show initially
    ipa_text = ipa.convert(original_text)

    # Ensure translate_fn is valid before using it
    if translate_fn:
        translated_text = translate_fn.translate(original_text)
        show_popup(original_text, ipa_text, translated_text)
    else:
        print("Error: Translation function not available.")
        return

    # Minimize the app to tray when the user closes the window
    def on_close():
        root.withdraw()
        threading.Thread(target=create_tray_icon, daemon=True).start()

    root = tk.Tk()
    root.title("Translator")
    root.geometry("300x150")
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Show initial translation in popup
    tk.Button(root, text="Show Translation", command=lambda: show_popup(original_text, ipa_text, translated_text)).pack(pady=20)
    root.mainloop()

# Start listener in background for keyboard shortcut
threading.Thread(target=listen_shortcut, daemon=True).start()

# Show the initial translation popup when the program starts
show_initial_popup()

print("🔧 Translator is running... Press Ctrl+Alt+T to translate selected text.")
while True:
    time.sleep(1)
