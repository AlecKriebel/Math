"""Exact independently derived full period-four family, a=5,b=3,c=4."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'_python'))
import sympy as s
z,h=s.symbols('z h',real=True)
p=(5*(1-z*z)/(1+z*z),6*z/(1+z*z))
q=(-250*z/h,27*(1-z*z)/h)
poly=[p,q,(-p[0],-p[1]),(-q[0],-q[1])]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
k=det(p,q)
ap=4*k**3/((dot(p,p)+dot(q,q))**2-4*dot(p,q)**2)
relative=[(x-4,y) for x,y in poly];av=[]
for p,q in zip(relative,relative[1:]+relative[:1]):
 k=det(p,q);p2=dot(p,p);q2=dot(q,q)
 av.append(((p2*q[1]-q2*p[1])/k,(p[0]*q2-q[0]*p2)/k))
aa=sum(det(p,q) for p,q in zip(av,av[1:]+av[:1]))/2
num,den=s.fraction(s.cancel(ap*aa-s.Rational(202500,289)))
relation=h*h-(81*z**4+2338*z*z+81)
remainder=s.rem(num,relation,h)
assert remainder==0
Path('EXACT_FOUR_PHASE.json').write_text('{"a":5,"b":3,"focus":4,"phase_parameter":"z=tan(t/2)","root_relation":"h²=81z⁴+2338z²+81, h>0","constant":"202500/289","numerator_remainder":"0","scope":"exact complete four-period phase family for one noncircular ellipse; derived before proof exposure"}\n')
print('Exact full four-period phase product verified:',s.Rational(202500,289))
print('Numerator factor:',s.factor(num))
