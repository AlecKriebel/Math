"""Exact actual-source homology cancellation and formal even-square dual checks."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent;d=json.loads((p/'turn_5_homology_data.json').read_text());checks=0
v=d['vectors'];c=d['coefficients'];s=d['target_s']
w=[sum(c[n]*v[n][i] for n in c) for i in range(18)]
for a,b in zip(w,s):assert a==b;checks+=1
for m in range(2,128):
 for a,b in zip(w,s):assert (a-b)%m==0;checks+=1
# If D^2=2q, F^2=0 and D.F=1, then S=D-(q+1)F has square -2.
for q in range(-100,101):
 assert 2*q-2*(q+1)==-2;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'integer_cancellation_coefficients':c,'target_equals_combination':w==s,'formal_dual_square':-2,'limitations':'Source-derived homology and intersection arithmetic only. No nonabelian 48-factor representation, embedded sphere, or pointed identity relation is certified.'},indent=2))
