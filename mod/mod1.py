from mod.screen import cap
from mod.click import tap
from PIL import Image
import json
import cv2
import numpy as np
import time  # ← 記得加上這行

def find(img, tpl):
    # 讀成灰階
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    tpl = cv2.imread(tpl, cv2.IMREAD_GRAYSCALE)

    # 檢查圖片是否成功讀取
    if img is None:
        print(f"[錯誤] 找不到圖片檔案: {img}")
        return None
    if tpl is None:
        print(f"[錯誤] 找不到模板檔案: {tpl}")
        return None

    res = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
    _, val, _, loc = cv2.minMaxLoc(res)
    if val > 0.9:
        x, y = loc
        h, w = tpl.shape[:2]  # 安全取得高寬
        return (x + w // 2, y + h // 2)
    return None


def run(eid, log_func):
    with open("photo.json", "r", encoding="utf-8") as f:
        d = json.load(f)

    # === hub1 判斷 ===
    path = cap(eid)
    hub1 = d.get("hub1", "")
    hub2 = d.get("hub2", "")
    if hub1 and hub2:
        pos1 = find(path, hub2)
        if pos1:
            tap(eid, *pos1)
            log_func("出城")

    time.sleep(1)  # 延遲 1 秒
    path = cap(eid)
    time.sleep(1)
    if hub1:
        pos2 = find(path, hub1)
        if pos2:
            tap(eid, *pos2)
            print("矯正一次")
    time.sleep(1)  # 延遲 1 秒
    path = cap(eid)
    time.sleep(1)
    if hub2:
        pos3 = find(path, hub2)
        if pos3:
            tap(eid, *pos3)
            print("矯正完成")


