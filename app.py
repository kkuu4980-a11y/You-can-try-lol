import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np

# 裝置選擇邏輯
def select_device():
    devices = sd.query_devices()
    input_devices = {i: dev['name'] for i, dev in enumerate(devices) if dev['max_input_channels'] > 0}
    
    selected_id = [None]
    win = tk.Tk()
    win.title("選擇裝置")
    
    tk.Label(win, text="請選擇音訊輸入裝置:").pack(pady=10)
    combo = ttk.Combobox(win, values=[f"{i}: {name}" for i, name in input_devices.items()], width=50)
    combo.pack(pady=10)
    
    def confirm():
        val = combo.get()
        if val:
            selected_id[0] = int(val.split(":")[0])
            win.destroy()
            
    tk.Button(win, text="確認", command=confirm).pack(pady=10)
    win.mainloop()
    return selected_id[0]

# 主邏輯
DEVICE_ID = select_device()
if DEVICE_ID is None: exit()

root = tk.Tk()
root.title("Sound Reactive")
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

shared_data = {"brightness": 0}
SENSITIVITY = 20000 

def audio_callback(indata, frames, time, status):
    if not status:
        shared_data["brightness"] = min(255, int(np.abs(indata).mean() * SENSITIVITY))

def update_ui():
    val = shared_data["brightness"]
    canvas.configure(bg=f"#{val:02x}{val:02x}{val:02x}")
    root.after(10, update_ui)

stream = sd.InputStream(device=DEVICE_ID, channels=1, callback=audio_callback)
stream.start()
update_ui()
root.mainloop()
