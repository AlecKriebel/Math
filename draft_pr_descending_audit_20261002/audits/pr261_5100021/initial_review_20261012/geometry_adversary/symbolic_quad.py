import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'_python'))
import sympy as s
x,y,u,v,c=s.symbols('x y u v c',real=True)
P=[(x-c,y),(u-c,v),(-x-c,-y),(-u-c,-v)]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
anti=[]
for p,q in zip(P,P[1:]+P[:1]):
 k=det(p,q);p2=dot(p,p);q2=dot(q,q)
 anti.append(((p2*q[1]-q2*p[1])/k,(p[0]*q2-q[0]*p2)/k))
A=sum(det(p,q) for p,q in zip(anti,anti[1:]+anti[:1]))/2
print('antipedal area factored:',s.factor(A))
Path('SYMBOLIC_QUAD_AREA.txt').write_text(str(s.factor(A))+'\n')
