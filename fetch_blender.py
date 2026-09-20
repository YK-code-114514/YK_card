# -*- coding: utf-8 -*-
"""断点续传下载 Blender zip（Range 续传），校验 SHA-256 并解压到项目 tools/。"""
import urllib.request, hashlib, zipfile, os, sys, time

BASE = 'https://download.blender.org/release/Blender4.5/'
VER = '4.5.12'
NAME = 'blender-%s-windows-x64.zip' % VER
TOOLS = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\tools'
os.makedirs(TOOLS, exist_ok=True)
pkg = os.path.join(TOOLS, NAME)

def resume_fetch(url, target):
    """Range 续传直到完整下载。"""
    have = os.path.getsize(target) if os.path.exists(target) else 0
    tries = 0
    while True:
        tries += 1
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        if have:
            req.add_header('Range', 'bytes=%d-' % have)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                total = int(r.headers.get('Content-Length') or 0) + have
                mode = 'ab' if have else 'wb'
                with open(target, mode) as f:
                    while True:
                        chunk = r.read(1024 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        have += len(chunk)
                        print('  %d / %d MB' % (have // 1048576, total // 1048576), flush=True)
                if total and have >= total:
                    return True
                # 服务器未给 Content-Length 时按连接结束判断
                if total == 0:
                    return True
        except Exception as e:
            print('retry %d: %s (have %d MB)' % (tries, e, have // 1048576), flush=True)
            time.sleep(2)
            if tries > 12:
                return False
            continue

sha_file = os.path.join(TOOLS, 'blender-%s.sha256' % VER)
if not os.path.exists(sha_file) or os.path.getsize(sha_file) < 50:
    for i in range(5):
        try:
            req = urllib.request.Request(BASE + 'blender-%s.sha256' % VER, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r, open(sha_file, 'wb') as f:
                f.write(r.read())
            break
        except Exception as e:
            print('sha retry', i, e); time.sleep(2)
expected = None
for line in open(sha_file, encoding='utf-8'):
    parts = line.split()
    if len(parts) > 1 and parts[-1].lstrip('*') == NAME:
        expected = parts[0].lower(); break
if not expected:
    print('sha entry missing'); sys.exit(1)

if not os.path.exists(pkg) or os.path.getsize(pkg) < 200 * 1024 * 1024:
    print('downloading with resume:', NAME, flush=True)
    if not resume_fetch(BASE + NAME, pkg):
        print('download failed'); sys.exit(2)

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()

got = digest(pkg)
print('expected:', expected, flush=True)
print('got     :', got, flush=True)
if got != expected:
    print('MISMATCH'); sys.exit(3)
print('SHA-256 OK; extracting...', flush=True)
with zipfile.ZipFile(pkg) as z:
    z.extractall(TOOLS)
exe = os.path.join(TOOLS, 'blender-%s-windows-x64' % VER, 'blender.exe')
print('blender exists:', os.path.exists(exe))
print('DONE')
