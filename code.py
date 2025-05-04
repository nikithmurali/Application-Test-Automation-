import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk, ImageOps
import threading
import time
import os
import sys
import pyautogui
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
import datetime

pyautogui.PAUSE = 0  # Disable default pyautogui pause

# ------------------------ License Checking Module ------------------------ #
VALID_LICENSES = {
    "ABC123-XYZ789": "2025-12-31",   # expires Dec 31, 2025
    "MYAPP-9999-2025": "2025-06-30", # expires June 30, 2025
}

def check_license_gui():
    root = tk.Tk()
    root.withdraw()  # Hide main root window

    license_key = simpledialog.askstring("License Verification", "Enter your license key:")

    if license_key and license_key.strip() in VALID_LICENSES:
        expiration_str = VALID_LICENSES[license_key.strip()]
        expiration_date = datetime.datetime.strptime(expiration_str, "%Y-%m-%d").date()
        today = datetime.date.today()

        if today <= expiration_date:
            messagebox.showinfo("License Status", f"✅ License validated.\nExpires on: {expiration_date}")
            root.destroy()
            return True
        else:
            messagebox.showerror("License Status", "❌ License expired. Please renew.")
            root.destroy()
            return False
    else:
        messagebox.showerror("License Status", "❌ Invalid license key. Exiting application.")
        root.destroy()
        return False

# ------------------------ Resource Path ------------------------ #
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Use user's documents folder for log file
LOG_FILE = os.path.join(os.path.expanduser("~/Documents"), "automation_log.txt")
recording = False

# ------------------------ Recorder ------------------------ #
def stop_recording():
    global recording
    recording = False
    print("Recording stopped")

def record_actions():
    global recording
    recording = True

    def write_log(data):
        nonlocal last_time
        current_time = time.time()
        delay = current_time - last_time
        last_time = current_time
        with open(LOG_FILE, "a") as f:
            f.write(f"{data} {delay:.4f}\n")

    def on_mouse_move(x, y):
        if not recording:
            return False
        write_log(f"MOVE {x} {y}")

    def on_mouse_click(x, y, button, pressed):
        if not recording:
            return False
        action = "PRESS" if pressed else "RELEASE"
        write_log(f"CLICK {x} {y} {button} {action}")

    def on_key_press(key):
        if not recording:
            return False
        try:
            key_str = key.char if hasattr(key, 'char') else str(key)
        except AttributeError:
            key_str = str(key)
        if key == Key.space:
            key_str = "SPACE"
        elif key == Key.enter:
            key_str = "ENTER"
        write_log(f"KEY {key_str} PRESS")

    def on_key_release(key):
        if not recording:
            return False
        if key == Key.esc:
            return False
        write_log(f"KEY {key} RELEASE")

    with open(LOG_FILE, "w") as f:
        f.write("")

    os.system("start chrome")
    time.sleep(3)

    last_time = time.time()
    with MouseListener(on_move=on_mouse_move, on_click=on_mouse_click) as mouse_listener, \
            KeyboardListener(on_press=on_key_press, on_release=on_key_release) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()

# ------------------------ Player ------------------------ #
def play_actions():
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        messagebox.showinfo("Info", "Log file is empty or doesn't exist.")
        return

    messagebox.showinfo("Info", "Opening Chrome and starting playback...")
    os.system("start chrome")
    time.sleep(3)

    print("Starting playback...")
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        action = parts[0]
        delay = float(parts[-1])
        time.sleep(delay)

        if action == "MOVE":
            x, y = int(parts[1]), int(parts[2])
            pyautogui.moveTo(x, y, duration=0)
        elif action == "CLICK":
            x, y = int(parts[1]), int(parts[2])
            button = parts[3].split(".")[-1].lower()
            click_type = parts[4]
            if click_type == "PRESS":
                pyautogui.mouseDown(x=x, y=y, button=button)
            else:
                pyautogui.mouseUp(x=x, y=y, button=button)
        elif action == "KEY":
            key = parts[1]
            key_action = parts[2]
            if key_action == "PRESS":
                if key == "ENTER":
                    pyautogui.press('enter')
                elif key == "SPACE":
                    pyautogui.press('space')
                elif len(key) == 1:
                    pyautogui.press(key)

    messagebox.showinfo("Info", "Playback finished.")

# ------------------------ GUI ------------------------ #
def build_gui():
    window = tk.Tk()
    window.title("MacroMind")
    window.geometry("420x380")
    window.configure(bg="#f4f1e1")
    window.resizable(False, False)

    try:
        window.iconphoto(True, tk.PhotoImage(file=resource_path("record.png")))
    except:
        pass

    title_label = tk.Label(window, text="MacroMind", font=("Segoe UI", 20, "bold"),
                           fg="#000000", bg="#f4f1e1")
    title_label.pack(pady=30)

    try:
        record_img = Image.open(resource_path("record.png")).resize((60, 60))
        play_img = Image.open(resource_path("play.png")).resize((60, 60))
        record_img = ImageOps.contain(record_img, (60, 60))
        play_img = ImageOps.contain(play_img, (60, 60))

        record_icon = ImageTk.PhotoImage(record_img)
        play_icon = ImageTk.PhotoImage(play_img)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load images: {e}")
        record_icon = None
        play_icon = None

    style = {"font": ("Segoe UI", 12, "bold"), "fg": "#000000", "bg": "#f4f1e1",
             "activebackground": "#00FFD1", "activeforeground": "#000", "borderwidth": 0, "width": 140, "height": 60}

    if record_icon:
        record_btn = tk.Button(window, image=record_icon, text="  Record", compound="left", command=start_recorder, **style)
        record_btn.image = record_icon
    else:
        record_btn = tk.Button(window, text="Record", command=start_recorder, **style)
    record_btn.pack(pady=10)

    if play_icon:
        play_btn = tk.Button(window, image=play_icon, text="  Play", compound="left", command=start_player, **style)
        play_btn.image = play_icon
    else:
        play_btn = tk.Button(window, text="Play", command=start_player, **style)
    play_btn.pack(pady=10)

    footer = tk.Label(window, text="Made by Nikith Murali, Shilpa Nagaraj", font=("Segoe UI", 9),
                      fg="#000000", bg="#f4f1e1")
    footer.pack(side="bottom", pady=10)

    window.protocol("WM_DELETE_WINDOW", lambda: (stop_recording(), window.destroy()))
    window.mainloop()

# ------------------------ Start Threads ------------------------ #
def start_recorder():
    stop_recording()
    recorder_thread = threading.Thread(target=record_actions)
    recorder_thread.start()

def start_player():
    player_thread = threading.Thread(target=play_actions)
    player_thread.start()

# ------------------------ Run ------------------------ #
if __name__ == "_main_":
    if check_license_gui():
        build_gui()
    else:
        sys.exit(1)