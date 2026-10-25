#!/usr/bin/env python3
"""Independent symbolic controls from the printed two-active cut argument."""
import sympy as s
import json
from pathlib import Path
from datetime import datetime, timezone
a,b,c,t,A,B,C,T,z=s.symbols('a b c t A B C T z', positive=True)
checks=[]
def ck(label, value):
    assert value, label
    checks.append(label)
def endpoint(g, pair):
    x,y,w,v=pair
    if g==(0,0,0): return s.Integer(1)
    if g[0]==g[1] and g[2]==0:return x
    if g[0]==g[2] and g[1]==0:return y
    if g[1]==g[2] and g[0]==0:return w
    assert len(set(g))==3 and 0 not in g
    return v
def entry(row,col):
    g1,g3=row;g2,g4=col;h=g1^g2
    assert h==g3^g4
    return endpoint((g1,g2,h),(a,b,c,t))*endpoint((g3,g4,h),(A,B,C,T))*z**int(h!=0)
f=[a*A-z*z*b*c*B*C,z*T*t-z*z*b*c*B*C,z*C*(A*t-z*T*b*c),z*c*(z*B*C*t-T*a)]
rows=[[(0,0),(1,1)],[(0,0),(1,1)],[(0,1),(1,0)],[(0,1),(1,0)]]
cols=[[(0,0),(1,1)],[(0,0),(2,2)],[(0,1),(2,3)],[(1,0),(2,3)]]
for i,(r,k) in enumerate(zip(rows,cols)):
    determinant=s.det(s.Matrix([[entry(x,y) for y in k] for x in r]))
    ck(f'printed cut minor {i+1} equals independent convolution',s.expand(determinant-f[i])==0)
identities=[a*A-z*T*t-(f[0]-f[1]),z*z*C*T*(a*b*c-t*t)-(z*C*t*(f[0]-f[1])-a*f[2]),z*z*c*t*(A*B*C-T*T)-(A*f[3]+z*c*T*(f[0]-f[1]))]
for i,expr in enumerate(identities):ck(f'cut elimination identity {i+1}',s.expand(expr)==0)
for d in range(3,21):
    pairs=[(0,1),(0,2),(1,2)]+[(0,j) for j in range(3,d)]
    anchor=s.Matrix([[int(j in pair) for j in range(d)] for pair in pairs])
    ck(f'incidence anchor determinant degree {d}',anchor.det()==-2)
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','method':'fresh exact SymPy identities, independently constructed endpoint convolution; no supplied helpers','checks':checks,'count':len(checks),'universal_argument':'Each of the four cut sectors has a positive entry. Rank <=4 forces all four displayed minors to vanish. The three identities then force both Delta to vanish; the endpoint dichotomy and 0<z<1 imply f1>0, contradiction. Endpoint dichotomy itself remains a separate finite exact dependency.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'count':len(checks)}))
