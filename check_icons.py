# -*- coding: utf-8 -*-
import re
t = open(r'C:\Users\林绎客\Doubao\skills\RuiC-card-skill-main\assets\web-template\index.html', encoding='utf-8').read()
vals = sorted(set(re.findall(r'data-lucide="([^"]+)"', t)))
print('template data-lucide values:', vals)
a = open(r'C:\Users\林绎客\Doubao\skills\RuiC-card-skill-main\assets\web-template\app.js', encoding='utf-8').read()
i = a.find('const tree = icons')
print('--- template app.js refreshIcons ---')
print(a[max(0, i - 250):i + 250])
# ICON_TREES keys
d = open(r'C:\Users\林绎客\Doubao\skills\RuiC-card-skill-main\assets\web-template\icons.data.js', encoding='utf-8').read()
keys = re.findall(r'^\s{2}"([A-Za-z0-9]+)":', d, re.M)
print('ICON_TREES keys:', sorted(set(keys)))
