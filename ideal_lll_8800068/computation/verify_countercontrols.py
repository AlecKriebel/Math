from pathlib import Path
#!/usr/bin/env python3
import json
import sympy as S
from cyclic_search import audit
out=[]
B=S.Matrix([[2,0,0],[1,1,1],[-1,1,-1]])
out.append({'n':3,'m':2,'basis':B.tolist(),'first_squared':4,'lambda_squared':3,'audit':audit(B,2)})
for m in range(3,7):
 n=(3*m*m+3)//4
 B=S.zeros(n,n);B[0,0]=m;B[1,:]=S.ones(1,n)
 for i in range(2,n):B[i,i-1]=m
 r={'n':n,'m':m,'basis':B.tolist(),'first_squared':m*m,'lambda_squared':n,'audit':audit(B,m)}
 assert r['audit']['reduced'] and r['audit']['membership']
 assert int(r['audit']['determinant_abs'])==m**(n-1)
 out.append(r)
 print(n,m,str(S.Rational(m*m,n)),flush=True)
# The exceptional mixed-sign shortest set for m=2 is deliberately separate.
assert out[0]['audit']['reduced'] and out[0]['audit']['membership']
with open(Path(__file__).with_name('countercontrol_results.json'),'w') as f:json.dump(out,f,indent=2,default=int)
