# 🎮 MacroMind - Intelligent Action Recorder & Player

**MacroMind** is a GUI-based automation tool that allows you to **record** your mouse movements, clicks, and keyboard presses (including timing delays), and then **replay** those actions exactly. This is useful for automating repetitive tasks such as browsing, form filling, or testing workflows.

## 🚀 Features

- Record all user actions (mouse move, click, key press)
- Play back recorded actions with exact timing
- Simple and clean GUI with intuitive buttons
- License key protection for controlled access
- Saves log to `Documents/automation_log.txt`
- Opens Google Chrome automatically during recording and playback

---

## 🖥️ How to Use

1. **Start the App**  
   Launch the `.exe` file (after installation instructions below).

2. **Enter License Key**  
   A popup will prompt you for a license key. Valid sample keys include:
   ABC123-XYZ789 (Valid till: 2025-12-31)
   MYAPP-9999-2025 (Valid till: 2025-06-30)
   
4. **Record Your Actions**
- Click the **Record** button.
- Chrome will open.
- Perform your actions (clicks, typing, etc.).
- Press **Esc** key to stop recording.

4. **Replay the Actions**
- Click the **Play** button.
- Chrome will reopen and your recorded actions will be played back exactly.

---

## 📦 Files Included

| File Name           | Description                        |
|---------------------|------------------------------------|
| `main_gui.py`       | Main launcher script               |
| `record.png`        | Image icon for Record button       |
| `play.png`          | Image icon for Play button         |
| `automation_log.txt`| Log file storing recorded actions  |

---

## 🔐 License Key Validation

- Before using the tool, you must enter a valid license key.
- Keys are hardcoded for now (can be extended for database/API use).
- Invalid or expired keys will terminate the program.

---

## 🛠️ How to Install the Executable (Windows Users)

> 🛑 If you downloaded a `.zip` containing the `.exe`, follow these steps to avoid Windows blocking it.

### ✅ STEP 1: Exclude the Folder from Windows Security

1. Open **Windows Security**.
2. Go to **Virus & Threat Protection** → **Manage Settings**.
3. Scroll to **Exclusions** and click **Add or remove exclusions**.
4. Click **Add an exclusion** → **Folder**.
5. Select the folder where you'll extract or install the `.exe` file.

### ✅ STEP 2: Install the App

- Extract the ZIP file (if zipped).
- Place all files (`.exe`, `.png`, `.jpg`, etc.) into the **excluded folder**.
- Double-click the `.exe` to launch **MacroMind**.

> 📌 *If you get a SmartScreen warning, click "More Info" → "Run Anyway".*

---

## 🧰 Dependencies

These are already bundled with the `.exe`, but if you're running from source:

```bash
pip install pyautogui pynput pillow
```
🧾 License
This project is under a custom license mechanism. Please use only with valid keys provided.
"""

csharp
Copy
Edit

If you want to save it as a file directly, you can add this:

```python
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
