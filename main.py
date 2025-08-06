import tkinter as tk
from tkinter import messagebox
import json
import sys
import os
import requests
import random
import string
import winreg
import time
import locale
import pycountry

from mod.screen import cap
from mod.mod1 import run as run1
from mod.mod2 import run as run2
from mod.Farm_food import run as food #食材耕種
from mod.Farm_wood import run as wood #木材耕種
from mod.Farm_stone import run as stone #石頭耕種
from mod.Farm_gold import run as gold #金幣耕種
from mod.city_farm import run as city #金幣耕種
from mod.gem import toggle_gem


def load_cfg():
    try:
        # 如果是打包后的程序
        if getattr(sys, 'frozen', False):
            # 获取与 exe 相同的路径
            base_path = os.path.dirname(sys.executable)  # 获取当前 exe 的路径
        else:
            # 如果是开发环境，使用当前目录
            base_path = os.path.abspath(".")
        
        config_path = os.path.join(base_path, "config.json")  # 获取 config.json 路径
        with open(config_path, "r", encoding="utf-8") as f:
            j = json.load(f)
            return [e["id"] for e in j.get("emulators", [])]
    except Exception as err:
        messagebox.showerror("錯誤", f"載入 config.json 失敗: {err}")
        return []

def do_job():
    ids = load_cfg()
    for eid in ids:
        run1(eid,update_msg)

def do_job2():
    ids = load_cfg()
    for eid in ids:
        run2(eid)

def do_job3():
    ids = load_cfg()
    for eid in ids:
        cap(eid)
#================耕種模組===================
def farm_food():
    ids = load_cfg()
    for eid in ids:
        food(eid,update_msg)
def farm_wood():
    ids = load_cfg()
    for eid in ids:
        wood(eid,update_msg)
def farm_stone():
    ids = load_cfg()
    for eid in ids:
        stone(eid,update_msg)
def farm_gold():
    ids = load_cfg()
    for eid in ids:
        gold(eid,update_msg)
#================你媽分隔線===================
def auto_gem():
    ids = load_cfg()
    if ids:
        toggle_gem(ids[0], update_msg)  # 只取第一個模擬器


def city_farm():
    ids = load_cfg()
    for eid in ids:
        city(eid,update_msg)

#使用者介面數計
def open_input_window():
    win2 = tk.Toplevel()
    win2.title("設定數值")
    win2.geometry("300x220")
    win2.resizable(False, False)
    default_count = 3
    default_troop = 2
    if os.path.exists("set.json"):
        try:
            with open("set.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                default_count = data.get("count", 3)
                default_troop = data.get("troop", 5)
        except Exception as e:
            print("讀取 set.json 失敗：", e)


    # 第一組：通用數值
    tk.Label(win2, text="田地等級：").grid(row=0, column=0, padx=10, pady=10)
    scale1 = tk.Scale(win2, from_=1, to=6, orient=tk.HORIZONTAL, length=150)
    scale1.set(default_count)
    scale1.grid(row=0, column=1, padx=10, pady=10)

    # 第二組：部隊數量
    tk.Label(win2, text="部隊數量：").grid(row=1, column=0, padx=10, pady=10)
    scale2 = tk.Scale(win2, from_=1, to=5, orient=tk.HORIZONTAL, length=150)
    scale2.set(default_troop)
    scale2.grid(row=1, column=1, padx=10, pady=10)

    def save_value():
        val1 = scale1.get()
        val2 = scale2.get()
        with open("set.json", "w", encoding="utf-8") as f:
            json.dump({"count": val1, "troop": val2}, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("成功", f"已儲存：count={val1}, troop={val2}")
        win2.destroy()

    tk.Button(win2, text="確定", command=save_value, width=10).grid(row=2, column=0, columnspan=2, pady=10)

def update_msg(text):
    msg.set(text)  # 更新顯示框內容

#死人驗證

win = tk.Tk()
win.title("ROK助手BETA")
win.geometry("500x500")            # 設定視窗大小
win.resizable(False, False)        # 禁止拉伸
# 在 btn1...btn6 前加這段，放在最上面
msg = tk.StringVar()
msg.set("ROK助手已啟動，請選擇操作")  # 設定初始訊息

# 创建标签并设置字体、背景框和对齐方式
msg_lbl = tk.Label(win, textvariable=msg, font=("標楷體", 12), fg="blue", 
                   bg="white", borderwidth=2, relief="solid", width=25, height=2,
                   anchor="center")  # anchor="center" 可确保文本居中
msg_lbl.grid(row=0, column=0, columnspan=3, pady=5)


btn1 = tk.Button(win, text="hub矯正", command=do_job, width=15, height=2)
btn1.grid(row=1, column=0, padx=5, pady=10)

btn2 = tk.Button(win, text="hub進出", command=do_job2, width=15, height=2)
btn2.grid(row=1, column=1, padx=5, pady=10)

btn3 = tk.Button(win, text="螢幕截圖", command=do_job3, width=15, height=2)
btn3.grid(row=1, column=2, padx=5, pady=10)
#採集
btn4 = tk.Button(win, text="採集食物", command=farm_food, width=15, height=2)
btn4.grid(row=2, column=0, padx=5, pady=10)

btn5 = tk.Button(win, text="採集木頭", command=farm_wood, width=15, height=2)
btn5.grid(row=2, column=1, padx=5, pady=10)

btn6 = tk.Button(win, text="採集石頭", command=farm_stone, width=15, height=2)
btn6.grid(row=2, column=2, padx=5, pady=10)

btn7 = tk.Button(win, text="採集金幣", command=farm_gold, width=15, height=2)
btn7.grid(row=2, column=3, padx=5, pady=10)
#城市農場收集 and 自動幫助 and 自動捐獻 
btn8 = tk.Button(win, text="城市農場", command=city_farm, width=15, height=2)
btn8.grid(row=3, column=0, padx=5, pady=10)

#城市農場收集 and 自動幫助 and 自動捐獻 
gem1 = tk.Button(win, text="自動寶石", command=auto_gem, width=15, height=2)
gem1.grid(row=3, column=1, padx=5, pady=10)

#城市農場收集 and 自動幫助 and 自動捐獻 

#數計設置
btn9 = tk.Button(win, text="設定數值", command=open_input_window, width=15, height=2)
btn9.grid(row=5, column=0, padx=5, pady=10)


win.mainloop()

