import os
import subprocess
from PIL import Image

def cap(eid):
    path = f"screen/{eid}.png"
    subprocess.run(f"adb -s {eid} exec-out screencap -p > {path}", shell=True)

    img = Image.open(path).convert("L").point(lambda x: 0 if x < 128 else 255, '1')
    img.save(path)
    return path
