import tkinter as tk
import sounddevice as sd
import numpy as np

def select_device():
    # 獲取所有裝置列表
    devices = sd.query_devices()
    print("--- 可用的音訊輸入裝置 ---")
    # 只列出有輸入通道的裝置 (max_input_channels > 0)
    input_devices = []
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"編號 {i}: {dev['name']}")
            input_devices.append(i)
    
    while True:
        try:
            choice = int(input("\n請輸入你要使用的裝置編號: "))
            if choice in input_devices:
                return choice
            else:
                print("無效的編號，請重新輸入。")
        except ValueError:
            print("請輸入數字。")

# --- 初始化設定 ---
DEVICE_ID = select_device() # 啟動時詢問
SENSITIVITY = 20000 

root = tk.Tk()
root.title("Sound Reactive App")
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

shared_data = {"brightness": 0}

def audio_callback(indata, frames, time, status):
    if status: return
    volume = np.abs(indata).mean() * SENSITIVITY
    shared_data["brightness"] = min(255, int(volume))

def update_ui():
    val = shared_data["brightness"]
    hex_color = f"#{val:02x}{val:02x}{val:02x}"
    canvas.configure(bg=hex_color)
    root.after(10, update_ui)

# --- 啟動 ---
try:
    stream = sd.InputStream(device=DEVICE_ID, channels=1, callback=audio_callback)
    stream.start()
    print(f"已成功連接裝置 {DEVICE_ID}，視窗啟動中...")
except Exception as e:
    print(f"錯誤: {e}")

update_ui()
root.mainloop()
