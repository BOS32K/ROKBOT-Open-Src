# mod/gem.py
import random
import threading
import time
import subprocess
import cv2
import numpy as np
from ultralytics import YOLO
from mod.click import tap
import tkinter as tk
from PIL import Image, ImageTk

import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "gem.pt")
MODEL_PATH = os.path.abspath(MODEL_PATH)  # 轉成絕對路徑
model = YOLO(MODEL_PATH)

gem_running = False
gem_window = None
gem_thread = None
current_frame = None


def adb_screencap(eid):
    """直接用 ADB 截圖回傳 OpenCV 圖片"""
    result = subprocess.run(
        ["adb", "-s", eid, "exec-out", "screencap", "-p"],
        stdout=subprocess.PIPE
    )
    img_array = np.frombuffer(result.stdout, np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)


def detection_loop(eid):
    """背景執行 YOLO 偵測並更新畫面"""
    global gem_running, current_frame

    while gem_running:
        frame = adb_screencap(eid)
        if frame is None:
            continue

        # YOLO 偵測
        results = model.predict(frame, classes=[15, 16], conf=0.3, verbose=False)
        annotated = results[0].plot()

        # 保存最新畫面
        current_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        time.sleep(0.03)  # 約 30fps


def update_frame(label):
    """更新 Tkinter 畫面，並根據視窗大小自動縮放"""
    global current_frame, gem_running

    if current_frame is not None:
        # 取得當前 Label 大小
        target_width = label.winfo_width()
        target_height = label.winfo_height()

        # 如果還沒顯示過圖片，Label 大小可能是 1x1，要用原圖大小
        if target_width <= 1 or target_height <= 1:
            h, w = current_frame.shape[:2]
            target_width, target_height = w, h

        # 依視窗大小等比例縮放
        img_resized = cv2.resize(current_frame, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

        # 轉換成 Tkinter 圖片格式
        img = Image.fromarray(img_resized)
        imgtk = ImageTk.PhotoImage(image=img)

        # 更新 Label 圖片
        label.imgtk = imgtk
        label.config(image=imgtk)

    if gem_running:
        label.after(33, update_frame, label)  # 33ms ≈ 30fps



def toggle_gem(eid, log_func):
    """按鈕切換啟動 / 停止"""
    global gem_running, gem_window, gem_thread

    if not gem_running:
        # 開啟
        gem_running = True
        log_func("🚀 寶石自動偵測啟動")

        # 建立新視窗
        gem_window = tk.Toplevel()
        gem_window.title("寶石偵測")
        gem_window.geometry("640x360")  # 預設大小
        gem_window.minsize(320, 180)    # 最小大小
        gem_window.resizable(True, True) # 允許自由縮放

        gem_window.title("寶石偵測")
        gem_window.protocol("WM_DELETE_WINDOW", lambda: toggle_gem(eid, log_func))
        lbl = tk.Label(gem_window)
        lbl.pack()

        # 啟動 YOLO 執行緒
        gem_thread = threading.Thread(target=detection_loop, args=(eid,), daemon=True)
        gem_thread.start()

        # 開始更新畫面
        update_frame(lbl)

    else:
        # 關閉
        gem_running = False
        log_func("🛑 寶石自動偵測已停止")
        if gem_window:
            gem_window.destroy()
            gem_window = None
