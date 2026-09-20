# -*- coding: utf-8 -*-
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\editor.js'
s = open(p, encoding='utf-8').read()
s = s.replace('keyOut(states.subjectOriginal, keyColor, tol, 40)', 'keyOut(states.subjectOriginal, keyColor, tol, 35)')
s = s.replace('states.subject = keyOut(canvas, states.keyColor, tol, 40)', 'states.subject = keyOut(canvas, states.keyColor, tol, 35)')
s = s.replace('var tol = parseInt($("key-tol").value, 10) || 80;', 'var tol = parseInt($("key-tol").value, 10) || 55;')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('feather35:', s.count('tol, 35)'), 'default55:', s.count('|| 55;'))
