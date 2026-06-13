import tkinter as tk
import sounddevice as sd
import numpy as np

# --- 設定 ---
DEVICE_ID = 4
SENSITIVITY = 20000 

root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

# 用來存取最新亮度的共享變數
shared_data = {"brightness": 0}

def audio_callback(indata, frames, time, status):
    """當有音訊進入時，這段程式會立即被觸發"""
    if status:
        return
    # 計算該區塊的平均振幅
    volume = np.abs(indata).mean() * SENSITIVITY
    shared_data["brightness"] = min(255, int(volume))

def update_ui():
    """負責更新畫面"""
    val = shared_data["brightness"]
    hex_color = f"#{val:02x}{val:02x}{val:02x}"
    canvas.configure(bg=hex_color)
    # 這裡設為 10ms，這是畫面的極限速度
    root.after(10, update_ui)

# --- 啟動音訊流 (Callback) ---
try:
    stream = sd.InputStream(device=DEVICE_ID, channels=1, callback=audio_callback)
    stream.start()
    print("音訊流已啟動，正在聆聽...")
except Exception as e:
    print(f"無法啟動音訊裝置: {e}")

update_ui()
root.mainloop()