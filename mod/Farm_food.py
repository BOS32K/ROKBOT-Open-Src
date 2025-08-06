from mod.screen import cap
from mod.click import tap
from PIL import Image
import json
import cv2
import numpy as np
import time  # ← 記得加上這行

import cv2

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


def run(eid,log_func):
    with open("photo.json", "r", encoding="utf-8") as f:
        d = json.load(f)
        # === hub1 判斷 ===
    with open("set.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

# 直接用裡面的值
    nigger = cfg["count"]       # 使用 count 值當作點擊次數
    
    path = cap(eid)
    hub1 = d.get("hub2", "")
    hub2 = d.get("hub1", "")
    if hub1 and hub2:
        pos1 = find(path, hub2)
        if pos1:
            tap(eid, *pos1)
            print("出城")

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
    time.sleep(1)  # 延遲 1 秒

    #以下是放大鏡判斷
    path = cap(eid)
    a1 = d.get("search", "")
    if a1:
        A1 = find(path, a1)
        if A1:
            log_func(f"{eid} 尋找放大鏡")
            tap(eid, *A1)
            time.sleep(1)                   #尋找放大鏡
#====================================================================================
            log_func(f"{eid} 食物搜索")

            path = cap(eid)
            time.sleep(0.5)
            food = d.get("food", "")
            if food:
                FOOD=find(path,food)
                if FOOD:
                    tap(eid,*FOOD)
                    time.sleep(1)           #食物搜索
#====================================================================================
                    log_func(f"{eid} 計算等級中...")
                    path = cap(eid)
                    time.sleep(0.5)
                    delete=d.get("delete", "")
                    if delete:
                        D1=find(path,delete)
                        if D1:
                            for _ in range(6):
                                tap(eid, *D1)
                                time.sleep(0.5)
                    time.sleep(1)           #減少
#====================================================================================
                    log_func(f"{eid} 計算等級中...")
                    path = cap(eid)
                    time.sleep(0.5)
                    add=d.get("add", "")
                    if add:
                        ADD=find(path,add)
                        if ADD:
                            for _ in range(nigger-1):
                                tap(eid, *ADD)
                                time.sleep(0.5)
                    time.sleep(1)           #增加
#====================================================================================
                    log_func(f"{eid} 定位田地")
                    path = cap(eid)
                    time.sleep(0.5)
                    search1=d.get("search1", "")
                    if search1:
                        Search1=find(path,search1)
                        if Search1:
                            tap(eid, *Search1)
                    time.sleep(3)           #定位田地
#====================================================================================
                    log_func(f"{eid} 按下採集鍵")
                    path = cap(eid)
                    time.sleep(0.5)
                    get=d.get("get", "")
                    if get:
                        Get=find(path,get)
                        if Get:
                            tap(eid, *Get)
                    time.sleep(2)           #按下採集
#====================================================================================
                    log_func(f"{eid} 建立部隊")
                    path = cap(eid)
                    time.sleep(0.5)
                    make_troop=d.get("make_troop", "")
                    if make_troop:
                        Make_troop=find(path,make_troop)
                        if Make_troop:
                            tap(eid, *Make_troop)
                    time.sleep(2)           #建立部隊
#====================================================================================
                    log_func(f"{eid} 發送部隊!")
                    path = cap(eid)
                    time.sleep(0.5)
                    send_troop=d.get("send_troop", "")
                    if send_troop:
                        Send_troop=find(path,send_troop)
                        if Send_troop:
                            tap(eid, *Send_troop)
                    time.sleep(2)           #發送部隊


        else:
            log_func(f"{eid} 未成功種田")



    time.sleep(1)  # 延遲 1 秒
