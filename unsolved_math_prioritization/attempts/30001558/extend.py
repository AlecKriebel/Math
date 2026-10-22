from pathlib import Path
exec(Path(__file__).with_name('frozen32.py').read_text().split('words=')[0])
words=['0']
for L in range(2,33):words=[s+a for s in words for a in '012' if app(s,a)]
# must compare all alphabet permutations, including prefixes whose first symbol differs
import itertools
full=set()
for w in words:
 for p in itertools.permutations('012'):full.add(w.translate(str.maketrans('012',''.join(p))))
b={}
for s in full:b.setdefault(s[6:],[]).append(s)
candidates=[v[0] for v in b.values() if len(v)==1]
print('candidates',sorted(candidates))
for s in sorted(candidates)[:1]:
 def extend(s,N):
  if len(s)==N:return s
  for a in '012':
   if app(s,a):
    r=extend(s+a,N)
    if r:return r
  return None
 print('extension128',extend(s,128))

s=sorted(candidates)[0]
states=[s]
while states:
 print('extension level',len(states[0]),'count',len(states))
 states=[w+a for w in states for a in '012' if app(w,a)]
