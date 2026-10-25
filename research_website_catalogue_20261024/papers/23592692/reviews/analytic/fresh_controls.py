#!/usr/bin/env python3
"""Fresh manuscript-derived exact checks; no submitted helper imported."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from datetime import datetime,timezone
import json
import sympy as s
checks=[]
def ck(name, condition):
 assert condition,name
 checks.append(name)
a,alpha,q,r,B,z=s.symbols('a alpha q r B z',positive=True)
y=s.symbols('y',positive=True)
ck('Hessian diagonal from -y^(1/alpha)',s.simplify(alpha**2*s.diff(-y**(1/alpha),y,2)-(alpha-1)*y**(1/alpha-2))==0)
A0,A1,b=s.symbols('A0 A1 b',positive=True)
ck('weighted incidence inequality exact square',s.factor(b*s.Rational(1,4)*(1/A0+1/A1)-b/(A0+A1))==b*(A0-A1)**2/(4*A0*A1*(A0+A1)))
S=s.symbols('S',positive=True)
f=a-2*S+2*S*S/a
Sp=s.symbols('Sp')
ck('whisker f derivative identity',s.expand(s.diff(f,a)+s.diff(f,S)*Sp-(1-2*(S/a)**2+2*(2*S/a-1)*Sp))==0)
ck('lower z bound factor',s.expand(a*a*(2-a)-1-(a-1)*(1+a-a*a))==0)
R=2*a**7-3*a**6+2
ck('upper z derivative',s.expand(s.diff(R,a)-2*a**5*(7*a-9))==0)
ck('upper z exact minimum',R.subs(a,s.Rational(9,7))==s.Rational(52763,823543))
rows=[(Q(17,4),Q(13,3),Q(29,5),Q(1325,1734),Q(1,1734)),(Q(13,3),Q(9,2),Q(25,4),Q(3869,5046),Q(163,65598)),(Q(9,2),Q(5),Q(243,32),Q(117039,151250),Q(5399,1361250)),(Q(5),Q(6),Q(729,64),Q(991335,1257698),Q(74117,6288490)),(Q(6),Q(7),Q(2187,128),Q(8580639,10718450),Q(527104,16077675))]
for i,(lo,hi,T,expected,margin) in enumerate(rows):
 cap=T**hi.denominator-Q(3,2)**hi.numerator
 ck('power cap '+str(i),cap>=0)
 S0=T/(1+T); actual=(S0*S0+(Q(3,2)-S0)**2)/Q(3,2)
 ck('exact table value '+str(i),actual==expected)
 ck('positive stability margin '+str(i),1-1/lo-actual==margin and margin>0)
 ck('cap lies in f monotonic domain '+str(i),S0>=Q(3,4))
 if i:ck('closed intervals join '+str(i),rows[i-1][1]==lo)
ck('first irrational cap excess',rows[0][2]**3-Q(3,2)**13==Q(504313,1024000))
ck('second irrational cap excess',rows[1][2]**2-Q(3,2)**9==Q(317,512))
C=3-s.sqrt(2);h=lambda t:alpha*t*t-(alpha-1)*t+1
ck('tail C identity',s.simplify(C*C+C-7*(C-1))==0)
ck('tail h evaluation',s.simplify(h(C/alpha)+(C-1)*(1-7/alpha))==0)
ck('tail endpoint sign formula',s.expand(h(s.Rational(1,2))-(6-alpha)/4)==0)
partial=sum(Q(8,5)**k/s.factorial(k) for k in range(5));tail=Q(8,5)**5/s.factorial(5)/(1-Q(4,15))
ck('exponential degree4 sum',partial==s.Rational(9067,1875))
ck('exponential tail cap',tail==s.Rational(4096,34375))
ck('strict exponential upper bound',partial+tail==s.Rational(510973,103125) and partial+tail<6)
J=s.ones(3)*(-alpha/4)+s.eye(3)*(3*alpha/4-1)
ck('triangle characteristic polynomial',(J-s.symbols('x')*s.eye(3)).det().factor()==-((4*s.symbols('x')-3*alpha+4)**2*(s.symbols('x')+1))/16)
for k in range(2,7):
 # Any positive vertex b gives an exact equilibrium at alpha=1+1/k.
 # These examples include a weighted odd cycle with chords and a pendant.
 av=Q(k+1,k); edges=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,2),(1,5)]
 bs=[Q(4+i,9+i) for i in range(6)];weights=[(bs[u]+bs[v])**(-k) for u,v in edges]
 powers=[(bs[u]+bs[v])**(-(k+1)) for u,v in edges]
 sv=[sum(A for e,A in zip(edges,powers) if v in e) for v in range(6)]
 rates=[bs[v]*sv[v] for v in range(6)]
 for j,(u,v) in enumerate(edges):ck(f'exact weighted equilibrium k{k} edge{j}',rates[u]*powers[j]/sv[u]+rates[v]*powers[j]/sv[v]==weights[j])
 ds=[(bs[u]+bs[v])**(k+2) for u,v in edges];cs=[bs[v]/sv[v] for v in range(6)]
 ck('cycle aggregate inequality with chord/attachment k'+str(k),sum(ds[:5])>=4*sum(cs[:5]))
 # Exact odd frequency trace at m=5, sin^2(pi/10)=(3-sqrt(5))/8.
 trace=(s.Rational(av.numerator,av.denominator)-1)*sum(ds[:5])-s.Rational(av.numerator,av.denominator)*(3-s.sqrt(5))/2*sum(cs[:5])
 ck('positive five-cycle Hessian trace k'+str(k),bool(trace>0))
# Equal-rate unweighted triangle checks distinguish the excluded endpoint.
for av,positive in [(s.Rational(5,4),False),(s.Rational(4,3),False),(s.Rational(3,2),True)]:
 ck('triangle transverse sign at '+str(av),bool(3*av/4-1>0)==positive)
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','count':len(checks),'checks':checks,'scope':'Fresh exact algebra, all closed exponent-interval margins, unbounded-tail constants, triangle endpoint controls, and five explicitly constructed weighted equilibrium examples with a chord/attachment. Universal arguments are reviewed separately; finite cases do not prove the theorem.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','count':len(checks)}))
