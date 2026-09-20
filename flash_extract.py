# -*- coding: utf-8 -*-
import json, subprocess, sys

video = r"C:\Users\林绎客\Downloads\澜_雾影狼魂（闪光海报）_动态闪光海报.mp4"
root = r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills\doubao-video-extract"
outdir = r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\shots\flash-frames"

windows = [{"window_id": "full", "start_ms": 0, "end_ms": 15600}]
with open(r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\flash-windows.json", "w", encoding="utf-8") as f:
    json.dump({"windows": windows}, f)

cmd = [sys.executable, root + r"\scripts\video_extract\video_frame_extract.py",
       "--video", video,
       "--windows", r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\flash-windows.json",
       "--output-dir", outdir,
       "--sample-every", "1.3",
       "--max-frames-per-window", "12",
       "--format", "jpg",
       "--manifest", outdir + r"\manifest.json"]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[-2500:])
print("ERR", r.stderr[-800:])
