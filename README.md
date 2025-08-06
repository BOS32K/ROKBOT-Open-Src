# ROKBOT-Open-Src

## 自述
目前屬於測試版本，仍有些許邏輯錯誤。  
寶石模型下載：[gem.pt download](https://www.mediafire.com/file/2ozn9oom6ahdv2g/gem.pt/file)  
請將 `gem.pt` 放在 `main.py` 同層資料夾。

---

## 目前已有功能
1. **自動尋找田地並耕種**
2. **自動收穫城市農田**
3. **多開模擬器** — 調整 `config.json` 設置運作的模擬器
4. **客製化田地等級**

---

## 功能添加項目
1. **寶石自動檢測**

---

## 本腳本使用工具如下:
- **Python 3.15**
- **Ldplayer**


## 需要的pip項目:
本腳本需要 Ldplayer，Python 3.10.11

pip install opencv-python

pip install numpy

pip install ultralytics

pip install pillow

---

## 安裝 SDK 平台工具

1. 到 [Google 官方下載 SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
2. 加入系統環境變數 `Path`
3. 對應的模擬器修改config.json

---

### 示例命令
```bash
# 設置環境變數
set PATH=%PATH%;C:\platform-tools

# 啟用 adb 調試模式
adb devices
