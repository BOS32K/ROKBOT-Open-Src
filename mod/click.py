import subprocess

def tap(eid, x, y):
    subprocess.run(f"adb -s {eid} shell input tap {x} {y}", shell=True)
